from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.views.generic import TemplateView

from core.history import GenericHistoryListView
from core.mixin import DataTableMixin
from core.utils import IncludeUserFormCreate, IncludeUserFormUpdate
from equipo.forms.celular import FormCelular
from equipo.models.celular import Celular

MODULE_NAME = 'Celulares'


class CelularListView(DataTableMixin, TemplateView):
    template_name = 'celular/list.html'
    model = Celular

    datatable_columns = [
        'ID',
        'Tipo',
        'Propietario',
        'Marca',
        'Modelo',
        'Número Teléfono',
        'Plan MINSAL',
        'PIN',
        'PUK',
        'IMEI',
        'N° Chip',
        'Minutos',
        'Responsable',
        'Jefe Entrega'
    ]

    datatable_order_fields = [
        'id',
        'tipo__nombre',
        'propietario__nombre',
        'marca__nombre',
        'modelo__nombre',
        'numero_telefono',
        'minsal',
        'pin',
        'puk',
        'imei',
        'numero_chip',
        'minutos',
        'responsable__nombres',
        'jefe_entrega__nombre',
    ]

    datatable_search_fields = [
        'tipo__nombre__icontains',
        'propietario__nombre__icontains',
        'marca__nombre__icontains',
        'modelo__nombre__icontains',
        'numero_telefono__icontains',
        'pin__icontains',
        'puk__icontains',
        'imei__icontains',
        'numero_chip__icontains',
        'minutos__icontains',
        'responsable__nombres__icontains',
        'jefe_entrega__nombre__icontains',
    ]

    url_detail = 'detail_celular'
    url_update = 'update_celular'

    def render_row(self, obj):
        return {
            'ID': obj.id,
            'Tipo': obj.tipo.nombre.upper() if obj.tipo else '-',
            'Propietario': obj.propietario.nombre.upper() if obj.propietario else '-',
            'Marca': obj.marca.nombre.upper() if obj.marca else '-',
            'Modelo': obj.modelo.nombre.upper() if obj.modelo else '-',
            'Número Teléfono': obj.numero_telefono,
            'Plan MINSAL': 'Sí' if obj.minsal else 'No',
            'PIN': obj.pin if obj.pin else '-',
            'PUK': obj.puk if obj.puk else '-',
            'IMEI': obj.imei,
            'N° Chip': obj.numero_chip if obj.numero_chip else '-',
            'Minutos': obj.minutos if obj.minutos else '-',
            'Responsable': obj.responsable.nombres.upper() if obj.responsable else '-',
            'Jefe Entrega': obj.jefe_entrega.nombre.upper() if obj.jefe_entrega else '-',
        }

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.GET.get('datatable'):
            return self.get_datatable_response(request)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        # 🔥 Optimización importante para evitar N+1 queries
        return Celular.objects.filter(status=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Listado de Celulares',
            'list_url': reverse_lazy('list_celular'),
            'create_url': reverse_lazy('create_celular'),
            'datatable_enabled': True,
            'datatable_order': [[0, 'asc']],
            'datatable_page_length': 100,
            'columns': self.datatable_columns,
        })
        return context


class CelularDetailView(DetailView):
    model = Celular
    template_name = 'celular/detail.html'

    def render_to_response(self, context, **response_kwargs):
        # Si es una solicitud AJAX, devolvemos solo el fragmento HTML
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.template.loader import render_to_string
            html = render_to_string(self.template_name, context=context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)


class CelularCreateView(IncludeUserFormCreate, CreateView):
    template_name = 'celular/form.html'
    model = Celular
    form_class = FormCelular
    success_url = reverse_lazy('list_celular')

    def form_valid(self, form):
        messages.success(self.request, 'Celular creado correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hay errores en el formulario')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Celular'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        return context


class CelularUpdateView(IncludeUserFormUpdate, UpdateView):
    template_name = 'celular/form.html'
    model = Celular
    form_class = FormCelular
    success_url = reverse_lazy('list_celular')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Celular creada correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hay errores en el formulario')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Celular'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME
        return context


class CelularHistoryListView(GenericHistoryListView):
    base_model = Celular
    template_name = 'history/list.html'
