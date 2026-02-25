from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView, DetailView

from core.history import GenericHistoryListView
from core.mixin import DataTableMixin
from core.utils import IncludeUserFormCreate, IncludeUserFormUpdate
from equipo.forms.impresora import FormImpresora
from equipo.models.impresora import Impresora

MODULE_NAME = 'Impresoras'

from django.urls import reverse_lazy
from django.views.generic import TemplateView


class ImpresoraListView(DataTableMixin, TemplateView):
    template_name = 'impresora/list.html'
    model = Impresora

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
        'ip',
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
        'ip__icontains',
        'serie__icontains',
        'toner__nombre__icontains',
        'descripcion__icontains',
    ]

    url_detail = 'detail_impresora'
    url_update = 'update_impresora'

    def render_row(self, obj):
        return {
            'ID': obj.id,
            'Tipo': obj.tipo.nombre.upper() if obj.tipo else '-',
            'Propietario': obj.propietario.nombre.upper() if obj.propietario else '-',
            'Marca': obj.marca.nombre.upper() if obj.marca else '-',
            'Modelo': obj.modelo.nombre.upper() if obj.modelo else '-',
            'Departamento': obj.departamento.nombre.upper() if obj.departamento else '-',
            'HH': obj.hh if obj.hh else '-',
            'IP': obj.ip if obj.ip else '-',
            'Serial': obj.serie if obj.serie else '-',
            'Toner': obj.toner.nombre.upper() if obj.toner else '-',
            'Descripcion': obj.observaciones if obj.observaciones else '-',
        }

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.GET.get('datatable'):
            return self.get_datatable_response(request)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        # 🔥 Optimización para evitar N+1 queries
        return Impresora.objects.select_related(
            'tipo',
            'marca',
            'modelo',
            'toner'
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


class ImpresoraDetailView(DetailView):
    model = Impresora
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
    model = Impresora
    form_class = FormImpresora
    success_url = reverse_lazy('list_impresora')

    def form_valid(self, form):
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
    model = Impresora
    form_class = FormImpresora
    success_url = reverse_lazy('list_impresora')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Impresora creada correctamente')
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
    base_model = Impresora
    template_name = 'history/list.html'
