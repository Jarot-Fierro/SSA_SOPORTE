from django.utils import timezone
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
from inventario.forms import FormInventarioTIC
from inventario.models import InventarioInformatica

MODULE_NAME = 'Inventario TIC'


class InventarioTICListView(LoginRequiredMixin, DataTableMixin, TemplateView):
    template_name = 'inventariotic/list.html'
    model = InventarioInformatica
    datatable_columns = ['ID', 'Producto', 'Código', 'Stock Actual', 'Categoría', 'Responsable', 'Estado', 'F. Ingreso',
                         'U. Salida']
    datatable_order_fields = ['id', 'producto', 'codigo', 'stock_actual', 'categoria__nombre', 'responsable',
                              'status_stock', 'fecha_ingreso', 'ultima_salida']
    datatable_search_fields = ['producto__icontains', 'codigo__icontains', 'categoria__nombre__icontains',
                               'responsable__icontains']

    url_detail = 'detail_inventarios_tic'

    # url_update = 'update_inventarios_tic'

    def get_url_update(self):
        user = self.request.user
        if getattr(user, 'rol', None) and user.rol.inventario == 2:
            return 'update_inventarios_tic'
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
            'Código': obj.codigo,
            'Stock Actual': obj.stock_actual,
            'Categoría': obj.categoria.nombre if obj.categoria else 'N/A',
            'Responsable': obj.responsable,
            'Estado': status_html,
            'F. Ingreso': obj.fecha_ingreso.strftime('%d/%m/%Y') if obj.fecha_ingreso else 'N/A',
            'U. Salida': obj.ultima_salida.strftime('%d/%m/%Y') if obj.ultima_salida else 'N/A',
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


class InventarioTICDetailView(LoginRequiredMixin, DetailView):
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


class InventarioTICCreateView(LoginRequiredMixin, IncludeUserFormCreate, CreateView):
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


class InventarioTICUpdateView(LoginRequiredMixin, IncludeUserFormUpdate, UpdateView):
    template_name = 'inventariotic/form.html'
    model = InventarioInformatica
    form_class = FormInventarioTIC
    success_url = reverse_lazy('list_inventarios_tic')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        old_obj = self.get_object()
        new_stock = form.cleaned_data.get('stock_actual')

        if new_stock is not None and old_obj.stock_actual > new_stock:
            form.instance.ultima_salida = timezone.now().date()

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


class InventarioTICHistoryListView(LoginRequiredMixin, GenericHistoryListView):
    base_model = InventarioInformatica
    template_name = 'history/list.html'


class InventarioTICUpdateStatusView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        productos = InventarioInformatica.objects.all()
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

        messages.success(request, 'Estados de stock TIC actualizados correctamente.')
        return redirect('list_inventarios_tic')
