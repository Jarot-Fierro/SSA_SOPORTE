from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, View
from django.views.generic import TemplateView

from core.history import GenericHistoryListView
from core.mixin import DataTableMixin
from core.utils import IncludeUserFormCreate, IncludeUserFormUpdate
from inventario.forms import FormInventarioMantencion
from inventario.models import InventarioMantencion

MODULE_NAME = 'Inventario Mantención'


class InventarioMantencionListView(LoginRequiredMixin, DataTableMixin, TemplateView):
    template_name = 'inventariomantencion/list.html'
    model = InventarioMantencion
    datatable_columns = ['ID', 'Producto', 'Stock Actual', 'Categoría', 'Responsable', 'Estado', 'Fecha Ingreso',
                         'Fecha Salida']
    datatable_order_fields = ['id', 'producto', 'stock_actual', 'categoria__nombre', 'responsable',
                              'status_stock', 'fecha_ingreso', 'ultima_salida']
    datatable_search_fields = ['producto__icontains', 'categoria__nombre__icontains',
                               'responsable__icontains']

    url_detail = 'detail_inventarios_mantencion'

    # url_update = 'update_inventarios_mantencion'

    def get_url_update(self):
        user = self.request.user
        if getattr(user, 'rol', None) and user.rol.inventario == 2:
            return 'update_inventarios_mantencion'
        return None

    def render_row(self, obj):
        status_stock = obj.status_stock
        badge_class = 'bg-success'
        if status_stock == 'REPOSICIÓN':
            badge_class = 'bg-danger'
        elif status_stock == 'SOBRESTOCK':
            badge_class = 'bg-warning text-dark'

        status_html = f'<span class="badge {badge_class}">{status_stock}</span>'

        return {
            'ID': obj.id,
            'Producto': obj.producto,
            'Stock Actual': obj.stock_actual,
            'Categoría': obj.categoria.nombre if obj.categoria else 'N/A',
            'Responsable': obj.responsable,
            'Estado': status_html,
            'Fecha Ingreso': obj.fecha_ingreso.strftime('%d/%m/%Y') if obj.fecha_ingreso else 'N/A',
            'Fecha Salida': obj.ultima_salida.strftime('%d/%m/%Y') if obj.ultima_salida else 'N/A',
        }

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.GET.get('datatable'):
            return self.get_datatable_response(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Listado de Inventario Mantención',
            'list_url': reverse_lazy('list_inventarios_mantencion'),
            'create_url': reverse_lazy('create_inventarios_mantencion'),
            'datatable_enabled': True,
            'datatable_order': [[0, 'asc']],
            'datatable_page_length': 100,
            'columns': self.datatable_columns,
        })
        return context


class InventarioMantencionDetailView(LoginRequiredMixin, DetailView):
    model = InventarioMantencion
    template_name = 'inventariomantencion/detail.html'

    def render_to_response(self, context, **response_kwargs):
        # Si es una solicitud AJAX, devolvemos solo el fragmento HTML
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.template.loader import render_to_string
            html = render_to_string(self.template_name, context=context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalle de Producto (Mantención)'
        context['module_name'] = MODULE_NAME
        return context


class InventarioMantencionCreateView(LoginRequiredMixin, IncludeUserFormCreate, CreateView):
    template_name = 'inventariomantencion/form.html'
    model = InventarioMantencion
    form_class = FormInventarioMantencion
    success_url = reverse_lazy('list_inventarios_mantencion')

    def form_valid(self, form):
        messages.success(self.request, 'Producto de mantención creado correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hay errores en el formulario')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Producto en Inventario Mantención'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        return context


class InventarioMantencionUpdateView(LoginRequiredMixin, IncludeUserFormUpdate, UpdateView):
    template_name = 'inventariomantencion/form.html'
    model = InventarioMantencion
    form_class = FormInventarioMantencion
    success_url = reverse_lazy('list_inventarios_mantencion')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Producto de mantención actualizado correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hay errores en el formulario')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Producto de Mantención'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME
        return context


class InventarioMantencionHistoryListView(LoginRequiredMixin, GenericHistoryListView):
    base_model = InventarioMantencion
    template_name = 'history/list.html'


class InventarioMantencionUpdateStatusView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        productos = InventarioMantencion.objects.all()
        for p in productos:
            if p.stock_minimo == 0 and (p.stock_maximo == 0 or p.stock_maximo is None):
                continue

            if p.stock_actual < p.stock_minimo:
                p.status_stock = 'REPOSICIÓN'
            elif p.stock_maximo is not None and p.stock_actual > p.stock_maximo:
                p.status_stock = 'SOBRESTOCK'
            else:
                p.status_stock = 'OK'
            p.save()

        messages.success(request, 'Estados de stock actualizados correctamente.')
        return redirect('list_inventarios_mantencion')
