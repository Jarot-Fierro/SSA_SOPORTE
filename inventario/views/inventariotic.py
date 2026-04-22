from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.views.generic import TemplateView

from core.history import GenericHistoryListView
from core.mixin import DataTableMixin
from core.utils import IncludeUserFormCreate, IncludeUserFormUpdate
from inventario.forms import FormInventarioTIC
from inventario.models import InventarioInformatica

MODULE_NAME = 'Inventario TIC'


class InventarioTICListView(DataTableMixin, TemplateView):
    template_name = 'inventariotic/list.html'
    model = InventarioInformatica
    datatable_columns = ['ID', 'Producto', 'Código', 'Stock Actual', 'Categoría']
    datatable_order_fields = ['id', 'producto', 'codigo', 'stock_actual', 'categoria__nombre']
    datatable_search_fields = ['producto__icontains', 'codigo__icontains', 'categoria__nombre__icontains']

    url_detail = 'detail_inventarios_tic'
    url_update = 'update_inventarios_tic'

    def render_row(self, obj):
        return {
            'ID': obj.id,
            'Producto': obj.producto,
            'Código': obj.codigo,
            'Stock Actual': obj.stock_actual,
            'Categoría': obj.categoria.nombre if obj.categoria else 'N/A',
        }

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.GET.get('datatable'):
            return self.get_datatable_response(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Listado de Inventario TIC',
            'list_url': reverse_lazy('list_inventarios_tic'),
            'create_url': reverse_lazy('create_inventarios_tic'),
            'datatable_enabled': True,
            'datatable_order': [[0, 'asc']],
            'datatable_page_length': 100,
            'columns': self.datatable_columns,
        })
        return context


class InventarioTICDetailView(DetailView):
    model = InventarioInformatica
    template_name = 'inventariotic/detail.html'

    def render_to_response(self, context, **response_kwargs):
        # Si es una solicitud AJAX, devolvemos solo el fragmento HTML
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.template.loader import render_to_string
            html = render_to_string(self.template_name, context=context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalle de Producto TIC'
        context['module_name'] = MODULE_NAME
        return context


class InventarioTICCreateView(IncludeUserFormCreate, CreateView):
    template_name = 'inventariotic/form.html'
    model = InventarioInformatica
    form_class = FormInventarioTIC
    success_url = reverse_lazy('list_inventarios_tic')

    def form_valid(self, form):
        messages.success(self.request, 'Producto TIC creado correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hay errores en el formulario')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Producto TIC'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        return context


class InventarioTICUpdateView(IncludeUserFormUpdate, UpdateView):
    template_name = 'inventariotic/form.html'
    model = InventarioInformatica
    form_class = FormInventarioTIC
    success_url = reverse_lazy('list_inventarios_tic')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Producto TIC actualizado correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hay errores en el formulario')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Producto TIC'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME
        return context


class InventarioTICHistoryListView(GenericHistoryListView):
    base_model = InventarioInformatica
    template_name = 'history/list.html'
