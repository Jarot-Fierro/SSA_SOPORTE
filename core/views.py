from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView

from catalogo.models import Ips
from core.mixin import DataTableMixinAuto
from equipo.models.celular import Celular
from equipo.models.equipos import Equipo
from establecimiento.models.departamento import Departamento
from establecimiento.models.funcionario import Funcionario
from inventario.models import InventarioInformatica, InventarioMantencion
from tickets.models import Ticket


class DashboardView(DataTableMixinAuto, LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'
    model = Ticket

    datatable_columns = [
        'ID',
        'Ticket',
        'Solicitante',
        'Título',
        'Estado',
        'Área',
        'Fecha'
    ]

    datatable_order_fields = [
        'id',
        'numero_ticket',
        'funcionario__nombres',
        'titulo',
        'estado',
        'area_soporte',
        'created_at'
    ]

    datatable_search_fields = [
        'numero_ticket__icontains',
        'titulo__icontains',
        'funcionario__nombres__icontains',
    ]

    url_update = 'ticket_panel_update'

    def get_base_queryset(self):
        return Ticket.objects.filter(establecimiento=self.request.user.establecimiento).select_related(
            'funcionario',
            'asignado_a',
            'departamento',
            'establecimiento'
        )

    def render_row(self, obj):
        solicitante = str(obj.funcionario) if obj.funcionario else '—'
        badge_colors = {
            'ABIERTO': 'primary',
            'EN_PROCESO': 'info',
            'ESPERA': 'warning',
            'CERRADO': 'success',
            'RECHAZADO': 'danger',
        }
        color = badge_colors.get(obj.estado, 'secondary')
        estado_badge = f'<span class="badge bg-{color}">{obj.get_estado_display()}</span>'

        area_badge = ''
        if obj.area_soporte == 'INFORMATICA':
            area_badge = '<span class="badge badge-info">Informática</span>'
        elif obj.area_soporte == 'MANTENCION':
            area_badge = '<span class="badge badge-danger">Mantención</span>'
        else:
            area_badge = f'<span>{obj.area_soporte or "—"}</span>'

        return {
            'ID': obj.id,
            'Ticket': obj.numero_ticket,
            'Solicitante': solicitante,
            'Título': obj.titulo,
            'Estado': estado_badge,
            'Área': area_badge,
            'Fecha': obj.created_at.strftime('%d-%m-%Y %H:%M') if obj.created_at else '—',
        }

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.GET.get('datatable'):
            return self.get_datatable_response(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Dashboard',
            'datatable_enabled': True,
            'datatable_order': [[0, 'desc']],
            'columns': self.datatable_columns,
        })
        return context


@login_required
def dashboard_data_api(request):
    # Tickets
    tickets_stats = Ticket.objects.aggregate(
        total=Count('id'),
        abiertos=Count('id', filter=Q(estado='ABIERTO')),
        cerrados=Count('id', filter=Q(estado='CERRADO')),
        en_proceso=Count('id', filter=Q(estado='EN_PROCESO')),
        informatica=Count('id', filter=Q(area_soporte='INFORMATICA')),
        mantencion=Count('id', filter=Q(area_soporte='MANTENCION')),
    )

    # Tickets por persona (asignado_a)
    tickets_por_persona = list(Ticket.objects.filter(asignado_a__isnull=False)
                               .values('asignado_a__first_name', 'asignado_a__last_name')
                               .annotate(
        abiertos=Count('id', filter=Q(estado='ABIERTO')),
        cerrados=Count('id', filter=Q(estado='CERRADO'))
    ).order_by('-abiertos')[:10])

    # Equipos
    equipos_stats = Equipo.objects.aggregate(
        total=Count('id'),
        pcs=Count('id', filter=Q(tipo_equipo='PC')),
        imps=Count('id', filter=Q(tipo_equipo='IMP')),
        otros=Count('id', filter=~Q(tipo_equipo__in=['PC', 'IMP'])),
        asignados=Count('id', filter=Q(responsable__isnull=False)),
        disponibles=Count('id', filter=Q(responsable__isnull=True, de_baja=False))
    )

    # IPs
    total_ips = Ips.objects.count()
    ips_usadas = Ips.objects.filter(asignado=True).count()

    ips_stats = {
        "total": total_ips,
        "usadas": ips_usadas,
        "disponibles": total_ips - ips_usadas
    }

    # Otros conteos
    otros_stats = {
        'funcionarios': Funcionario.objects.filter(status=True).count(),
        'departamentos': Departamento.objects.filter(status=True).count(),
        'celulares': Celular.objects.filter(status=True).count(),
    }

    # Inventario
    inv_tic_stats = InventarioInformatica.objects.aggregate(
        total_productos=Count('id'),
        stock_total=models.Sum('stock_actual')
    )
    inv_mant_stats = InventarioMantencion.objects.aggregate(
        total_productos=Count('id'),
        stock_total=models.Sum('stock_actual')
    )

    # Mini listado (últimos 5 de cada uno)
    recent_tic = list(
        InventarioInformatica.objects.order_by('-updated_at')[:5].values('producto', 'stock_actual', 'codigo'))
    recent_mant = list(
        InventarioMantencion.objects.order_by('-updated_at')[:5].values('producto', 'stock_actual', 'codigo'))

    data = {
        'tickets': tickets_stats,
        'tickets_por_persona': tickets_por_persona,
        'equipos': equipos_stats,
        'ips': ips_stats,
        'otros': otros_stats,
        'inventario': {
            'tic': inv_tic_stats,
            'mantencion': inv_mant_stats,
            'recent_tic': recent_tic,
            'recent_mant': recent_mant,
        }
    }

    return JsonResponse(data)


@login_required
def no_establecimiento(request):
    return render(request, 'core/no_establecimiento.html')


class ContactoView(LoginRequiredMixin, TemplateView):
    template_name = 'contacto/contacto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Contacto',
        })
        return context
