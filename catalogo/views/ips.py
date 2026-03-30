from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.views.generic import TemplateView

from catalogo.forms.ips import FormIps
from catalogo.models import Ips
from core.history import GenericHistoryListView
from core.mixin import DataTableMixin
from core.utils import IncludeUserFormCreate, IncludeUserFormUpdate

MODULE_NAME = 'Ips'


class IpsListView(DataTableMixin, TemplateView):
    template_name = 'ips/list.html'
    model = Ips
    datatable_columns = ['ID', 'Ip', 'Asignado']
    datatable_order_fields = ['id', None, 'ip', 'asignado']
    datatable_search_fields = ['ip__icontains', 'asignado__icontains']

    url_detail = 'detail_ips'
    url_update = 'update_ips'

    def render_row(self, obj):
        return {
            'ID': obj.id,
            'Ip': obj.ip.upper(),
            'Asignado': (
                '<span class="badge bg-danger p-2">Asignada</span>'
                if obj.asignado
                else '<span class="badge bg-success p-2">Libre</span>'
            ),
        }

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.GET.get('datatable'):
            return self.get_datatable_response(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Listado de Ips',
            'list_url': reverse_lazy('list_ips'),
            'create_url': reverse_lazy('create_ips'),
            'datatable_enabled': True,
            'datatable_order': [[0, 'asc']],
            'datatable_page_length': 100,
            'columns': self.datatable_columns,
        })
        return context


class IpsDetailView(DetailView):
    model = Ips
    template_name = 'ips/detail.html'

    def render_to_response(self, context, **response_kwargs):
        # Si es una solicitud AJAX, devolvemos solo el fragmento HTML
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.template.loader import render_to_string
            html = render_to_string(self.template_name, context=context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)


class IpsCreateView(IncludeUserFormCreate, CreateView):
    template_name = 'ips/form.html'
    model = Ips
    form_class = FormIps
    success_url = reverse_lazy('list_ips')

    def form_valid(self, form):
        messages.success(self.request, 'Ips creada correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hay errores en el formulario')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Ips'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        return context


class IpsUpdateView(IncludeUserFormUpdate, UpdateView):
    template_name = 'ips/form.html'
    model = Ips
    form_class = FormIps
    success_url = reverse_lazy('list_ips')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Ips creada correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hay errores en el formulario')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Ips'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME
        return context


class IpsHistoryListView(GenericHistoryListView):
    base_model = Ips
    template_name = 'history/list.html'
