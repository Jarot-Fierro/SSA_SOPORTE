from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView, DetailView

from core.history import GenericHistoryListView
from core.mixin import DataTableMixin
from core.utils import IncludeUserFormCreate, IncludeUserFormUpdate
from equipo.forms.impresora import FormImpresora
from equipo.models.equipos import Equipo

MODULE_NAME = 'Impresoras'

from django.urls import reverse_lazy
from django.views.generic import TemplateView


class ImpresoraListView(DataTableMixin, TemplateView):
    template_name = 'impresora/list.html'
    model = Equipo

    datatable_columns = [
        'ID',
        'Tipo',
        'Propietario',
        'Marca',
        'Modelo',
        'Departamento',
        'HH',
        'IP',
        'Serial',
        'Toner',
        'Descripcion'
    ]

    datatable_order_fields = [
        'id',
        'tipo__nombre',
        'propietario__nombre',
        'marca__nombre',
        'modelo__nombre',
        'departamento__nombre',
        'hh',
        'ip__ip',
        'serie',
        'toner__nombre',
        'descripcion',
    ]

    datatable_search_fields = [
        'tipo__nombre__icontains',
        'propietario__nombre__icontains',
        'marca__nombre__icontains',
        'modelo__nombre__icontains',
        'departamento__nombre__icontains',
        'hh__icontains',
        'ip__ip__icontains',
        'serie__icontains',
        'toner__nombre__icontains',
        'descripcion__icontains',
    ]

    url_update = 'update_impresora'

    def render_row(self, obj):
        return {
            'ID': obj.id,
            'Tipo': obj.tipo_impresora.nombre.upper() if obj.tipo_impresora else '-',
            'Propietario': obj.propietario.nombre.upper() if obj.propietario else '-',
            'Marca': obj.marca.nombre.upper() if obj.marca else '-',
            'Modelo': obj.modelo.nombre.upper() if obj.modelo else '-',
            'Departamento': obj.departamento.nombre.upper() if obj.departamento else '-',
            'HH': obj.hh if obj.hh else '-',
            'IP': (
                f'<span class="badge bg-success p-2">{obj.ip.ip}</span>'
                if obj.ip
                else '-'
            ),
            'Serial': obj.serie if obj.serie else '-',
            'Toner': obj.toner.nombre.upper() if obj.toner else '-',
            'Descripcion': obj.observaciones if obj.observaciones else '-',
        }

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.GET.get('datatable'):
            return self.get_datatable_response(request)
        return super().get(request, *args, **kwargs)

    def get_base_queryset(self):
        # Optimización para evitar N+1 queries y filtro por tipo IMP
        return Equipo.objects.filter(tipo_equipo='IMP').select_related(
            'tipo_impresora',
            'marca',
            'modelo',
            'toner',
            'propietario',
            'departamento',
            'ip'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Listado de Impresoras',
            'list_url': reverse_lazy('list_impresora'),
            'create_url': reverse_lazy('create_impresora'),
            'datatable_enabled': True,
            'datatable_order': [[0, 'asc']],
            'datatable_page_length': 100,
            'columns': self.datatable_columns,
        })
        return context

    def get_actions(self, obj):
        """
        Agrega botones personalizados a la columna de acciones.
        """
        actions = super().get_actions(obj)
        # Botón para generar acta PDF del impresora
        # if obj.responsable:
        #
        #     pdf_button = f"""
        #         <a href="{reverse_lazy('acta_impresora', kwargs={'pk': obj.id})}"
        #            target="_blank"
        #            class="btn p-1 btn-sm btn-danger" title="Ver Acta PDF">
        #            <i class="fas fa-file-pdf"></i></a>
        #     """
        #     return actions + pdf_button
        # else:
        #     return actions

        return actions


class ImpresoraDetailView(DetailView):
    model = Equipo
    template_name = 'impresora/detail.html'

    def render_to_response(self, context, **response_kwargs):
        # Si es una solicitud AJAX, devolvemos solo el fragmento HTML
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.template.loader import render_to_string
            html = render_to_string(self.template_name, context=context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)


class ImpresoraCreateView(IncludeUserFormCreate, CreateView):
    template_name = 'impresora/form.html'
    model = Equipo
    form_class = FormImpresora
    success_url = reverse_lazy('list_impresora')

    def form_valid(self, form):
        impresora = form.save(commit=False)

        # Asignación automática del tipo de equipo
        impresora.tipo_equipo = 'IMP'

        # asignar establecimiento del usuario
        impresora.establecimiento = self.request.user.establecimiento

        impresora.save()

        # Marcar la IP como asignada si se proporcionó una
        if impresora.ip:
            impresora.ip.asignado = True
            impresora.ip.save()

            # Crear registro en AsignacionIP
            from equipo.models.equipos import AsignacionIP
            AsignacionIP.objects.create(
                ip=impresora.ip,
                equipo=impresora,
                activa=True
            )

        messages.success(self.request, 'Impresora creado correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hay errores en el formulario')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Impresora'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        return context


class ImpresoraUpdateView(IncludeUserFormUpdate, UpdateView):
    template_name = 'impresora/form.html'
    model = Equipo
    form_class = FormImpresora
    success_url = reverse_lazy('list_impresora')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Obtenemos el objeto anterior para saber si cambió la IP
        old_equipo = self.get_object()
        old_ip = old_equipo.ip

        impresora = form.save()
        new_ip = impresora.ip

        from equipo.models.equipos import AsignacionIP

        # Si la IP cambió o fue removida
        if old_ip and old_ip != new_ip:
            old_ip.asignado = False
            old_ip.save()
            # Desactivar asignación previa
            AsignacionIP.objects.filter(equipo=impresora, ip=old_ip, activa=True).update(activa=False)

        # Si se asignó una nueva IP o se mantiene la misma
        if new_ip:
            new_ip.asignado = True
            new_ip.save()

            # Buscar si ya existe una asignación activa para este equipo
            asignacion = AsignacionIP.objects.filter(equipo=impresora, activa=True).first()

            if asignacion:
                # Si la IP es diferente, actualizamos el registro existente
                if asignacion.ip != new_ip:
                    asignacion.ip = new_ip
                    asignacion.save()
            else:
                # Si no existe asignación previa activa, creamos una nueva
                AsignacionIP.objects.create(
                    ip=new_ip,
                    equipo=impresora,
                    activa=True
                )

        messages.success(self.request, 'Impresora actualizada correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hay errores en el formulario')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Impresora'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME
        return context


class ImpresoraHistoryListView(GenericHistoryListView):
    base_model = Equipo
    template_name = 'history/list.html'
