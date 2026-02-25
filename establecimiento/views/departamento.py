from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.views.generic import TemplateView

from core.history import GenericHistoryListView
from core.mixin import DataTableMixin
from core.utils import IncludeUserFormCreate, IncludeUserFormUpdate
from establecimiento.forms.departamento import FormDepartamento
from establecimiento.models.departamento import Departamento

MODULE_NAME = 'Departamentos'


class DepartamentoListView(DataTableMixin, TemplateView):
    template_name = 'departamento/list.html'
    model = Departamento
    datatable_columns = ['ID', 'Nombre', 'Dirección', 'Establecimiento']
    datatable_order_fields = ['id', None, 'nombre', 'establecimiento__nombre']
    datatable_search_fields = ['nombre__icontains', 'establecimiento__nombre__icontains']

    url_detail = 'detail_departamentos'
    url_update = 'update_departamentos'

    def render_row(self, obj):
        return {
            'ID': obj.id,
            'Nombre': obj.nombre.upper(),
            'Dirección': (obj.direccion or '').upper(),
            'Establecimiento': (obj.establecimiento.nombre or '').upper(),
        }

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.GET.get('datatable'):
            return self.get_datatable_response(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Listado de Departamentos',
            'list_url': reverse_lazy('list_departamentos'),
            'create_url': reverse_lazy('departamento_create'),
            'datatable_enabled': True,
            'datatable_order': [[0, 'asc']],
            'datatable_page_length': 100,
            'columns': self.datatable_columns,
        })
        return context


class DepartamentoDetailView(DetailView):
    model = Departamento
    template_name = 'departamento/detail.html'

    def render_to_response(self, context, **response_kwargs):
        # Si es una solicitud AJAX, devolvemos solo el fragmento HTML
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.template.loader import render_to_string
            html = render_to_string(self.template_name, context=context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)


class DepartamentoCreateView(IncludeUserFormCreate, CreateView):
    template_name = 'departamento/form.html'
    model = Departamento
    form_class = FormDepartamento
    success_url = reverse_lazy('list_departamentos')

    def form_valid(self, form):
        messages.success(self.request, 'Comuna creada correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hay errores en el formulario')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Departamento'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        return context


class DepartamentoUpdateView(IncludeUserFormUpdate, UpdateView):
    template_name = 'departamento/form.html'
    model = Departamento
    form_class = FormDepartamento
    success_url = reverse_lazy('list_departamentos')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Comuna creada correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hay errores en el formulario')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Departamento'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME
        return context


class DepartamentoHistoryListView(GenericHistoryListView):
    base_model = Departamento
    template_name = 'history/list.html'
