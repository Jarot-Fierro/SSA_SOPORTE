from django.urls import reverse_lazy
from django.views.generic import TemplateView

from catalogo.models import Ips
from core.mixin import DataTableMixin


class EquiposIpListView(DataTableMixin, TemplateView):
    template_name = 'equipo/equipos_ip_list.html'
    model = Ips

    datatable_columns = [
        'ID',
        'IP',
        'Tipo Equipo',
        'Marca',
        'Modelo',
        'Serial',
        'Responsable',
        'Departamento',
        'Establecimiento',
        'Estado',
    ]

    datatable_order_fields = [
        'id',
        None,
        'ip',
        None,  # Tipo Equipo (calculado)
        None,  # Marca (calculado)
        None,  # Modelo (calculado)
        None,  # Serial (calculado)
        None,  # Responsable (calculado)
        'departamento__nombre',
        'establecimiento__nombre',
        'asignado',
    ]

    datatable_search_fields = [
        'ip__icontains',
        'departamento__nombre__icontains',
        'establecimiento__nombre__icontains',
    ]

    def get_queryset(self):
        # Optimizamos trayendo las relaciones de Ips y los equipos asociados
        # Aseguramos que solo mostramos IPs de computadores o impresoras
        return Ips.objects.select_related(
            'departamento',
            'establecimiento'
        ).prefetch_related(
            'computador_set',
            'impresora_set',
            'computador_set__marca',
            'computador_set__modelo',
            'computador_set__responsable',
            'impresora_set__marca',
            'impresora_set__modelo',
            'impresora_set__responsable',
        )

    def render_row(self, obj):
        # Buscamos si hay un computador o impresora asociada a esta IP
        equipo = obj.computador_set.first()
        tipo = 'COMPUTADOR'

        if not equipo:
            equipo = obj.impresora_set.first()
            if equipo:
                tipo = 'IMPRESORA'
            else:
                tipo = '-'

        if equipo:
            marca = equipo.marca.nombre.upper() if equipo.marca else '-'
            modelo = equipo.modelo.nombre.upper() if equipo.modelo else '-'
            serial = equipo.serie if equipo.serie else '-'
            responsable = (
                f'<span class="badge rounded-pill bg-primary p-2">{equipo.responsable.nombres.upper()}</span>'
                if equipo.responsable
                else '<span class="badge rounded-pill bg-secondary">SIN RESPONSABLE</span>'
            )
        else:
            marca = '-'
            modelo = '-'
            serial = '-'
            responsable = '-'

        return {
            'ID': obj.id,
            'IP': (
                f'<span class="badge bg-danger p-2">{obj.ip}</span>'
                if obj.asignado
                else f'<span class="badge bg-success p-2">{obj.ip}</span>'
            ),
            'Tipo Equipo': tipo,
            'Marca': marca,
            'Modelo': modelo,
            'Serial': serial,
            'Responsable': responsable,
            'Departamento': obj.departamento.nombre.upper() if obj.departamento else '-',
            'Establecimiento': obj.establecimiento.nombre.upper() if obj.establecimiento else '-',
            'Estado': '<span class="badge bg-danger">ASIGNADA</span>' if obj.asignado else '<span class="badge bg-success">LIBRE</span>',
        }

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.GET.get('datatable'):
            return self.get_datatable_response(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Listado de IPs y Equipos',
            'list_url': reverse_lazy('list_equipos_ip'),
            'datatable_enabled': True,
            'datatable_order': [[0, 'asc']],
            'datatable_page_length': 100,
            'columns': self.datatable_columns,
        })
        return context

    def get_actions(self, obj):
        # Por ahora sin acciones específicas
        return ''
