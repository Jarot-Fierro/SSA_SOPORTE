from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.views.generic import TemplateView

from core.history import GenericHistoryListView
from core.mixin import DataTableMixin
from core.utils import IncludeUserFormCreate, IncludeUserFormUpdate
from establecimiento.forms.funcionario import FormFuncionario
from establecimiento.models.funcionario import Funcionario

MODULE_NAME = 'Funcionario'


class FuncionarioListView(DataTableMixin, TemplateView):
    template_name = 'funcionario/list.html'
    model = Funcionario
    datatable_columns = ['ID', 'RUT', 'Nombres', 'Correo', 'Jefatura', 'Departamento']
    datatable_order_fields = ['id', None, 'rut', 'nombres', 'correo', 'jefatura', 'departamento__nombre']
    datatable_search_fields = ['rut__icontains', 'nombres__icontains', 'correo__icontains', 'jefatura__icontains',
                               'departamento__nombre__icontains']

    url_detail = 'detail_funcionarios'
    url_update = 'update_funcionarios'

    def render_row(self, obj):
        return {
            'ID': obj.id,
            'RUT': obj.rut.upper(),
            'Nombres': obj.nombres.upper(),
            'Correo': (obj.correo or '').upper(),
            'Jefatura': 'SI' if obj.jefatura else 'NO',
            'Departamento': (obj.departamento.nombre or '').upper(),
        }

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.GET.get('datatable'):
            return self.get_datatable_response(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Listado de Funcionario',
            'list_url': reverse_lazy('list_funcionarios'),
            'create_url': reverse_lazy('funcionario_create'),
            'datatable_enabled': True,
            'datatable_order': [[0, 'asc']],
            'datatable_page_length': 100,
            'columns': self.datatable_columns,
        })
        return context


class FuncionarioDetailView(DetailView):
    model = Funcionario
    template_name = 'funcionario/detail.html'

    def render_to_response(self, context, **response_kwargs):
        # Si es una solicitud AJAX, devolvemos solo el fragmento HTML
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.template.loader import render_to_string
            html = render_to_string(self.template_name, context=context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)


class FuncionarioCreateView(IncludeUserFormCreate, CreateView):
    template_name = 'funcionario/form.html'
    model = Funcionario
    form_class = FormFuncionario
    success_url = reverse_lazy('list_funcionarios')

    def form_valid(self, form):
        messages.success(self.request, 'Comuna creada correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hay errores en el formulario')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Funcionario'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        return context


class FuncionarioUpdateView(IncludeUserFormUpdate, UpdateView):
    template_name = 'funcionario/form.html'
    model = Funcionario
    form_class = FormFuncionario
    success_url = reverse_lazy('list_funcionarios')

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
        context['title'] = 'Editar Funcionario'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME
        return context


class FuncionarioHistoryListView(GenericHistoryListView):
    base_model = Funcionario
    template_name = 'history/list.html'
