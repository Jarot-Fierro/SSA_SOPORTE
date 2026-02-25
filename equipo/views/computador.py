from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView, DetailView

from core.history import GenericHistoryListView
from core.mixin import DataTableMixin
from core.utils import IncludeUserFormCreate, IncludeUserFormUpdate
from equipo.forms.computador import FormComputador

MODULE_NAME = 'Computadores'

from django.urls import reverse_lazy
from django.views.generic import TemplateView

from equipo.models.computador import Computador


class ComputadorListView(DataTableMixin, TemplateView):
    template_name = 'computador/list.html'
    model = Computador

    datatable_columns = [
        'ID',
        'Tipo Equipo',
        'Propietario',
        'Marca',
        'Modelo',
        'Sistema Operativo',
        'MAC',
        'IP',
        'Serial',
        'Responsable',
        'Contrato',
        'Descripción',
        'Jefe Entrega',
    ]

    datatable_order_fields = [
        'id',
        'tipo__nombre',
        'propietario__nombre',
        'marca__nombre',
        'modelo__nombre',
        'sistema_operativo__nombre',
        'mac',
        'ip',
        'serie',
        'responsable__first_name',
        'contrato__numero',
        'descripcion',
        'jefe_tic__nombre',
    ]

    datatable_search_fields = [
        'tipo__nombre__icontains',
        'propietario__nombre__icontains',
        'marca__nombre__icontains',
        'modelo__nombre__icontains',
        'sistema_operativo__nombre__icontains',
        'mac__icontains',
        'ip__icontains',
        'serie__icontains',
        'responsable__first_name__icontains',
        'responsable__last_name__icontains',
        'contrato__numero__icontains',
        'descripcion__icontains',
        'jefe_tic__nombre__icontains',
    ]

    url_detail = 'detail_computador'
    url_update = 'update_computador'
    computadores = Computador.objects.all()
    for i in computadores:
        print(i)

    def render_row(self, obj):
        return {
            'ID': obj.id,
            'Tipo Equipo': obj.tipo.nombre.upper() if obj.tipo else '-',
            'Propietario': obj.propietario.nombre.upper() if obj.propietario else '-',
            'Marca': obj.marca.nombre.upper() if obj.marca else '-',
            'Modelo': obj.modelo.nombre.upper() if obj.modelo else '-',
            'Sistema Operativo': obj.sistema_operativo.nombre.upper() if obj.sistema_operativo else '-',
            'MAC': obj.mac if obj.mac else '-',
            'IP': obj.ip if obj.ip else '-',
            'Serial': obj.serie if obj.serie else '-',
            'Responsable': obj.responsable.nombres.upper() if obj.responsable else '-',
            'Contrato': obj.contrato.nombre if obj.contrato else '-',
            'Descripción': obj.observaciones if obj.observaciones else '-',
            'Jefe Entrega': obj.jefe_entrega.nombre.upper() if obj.jefe_entrega else '-',
        }

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.GET.get('datatable'):
            return self.get_datatable_response(request)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        # 🔥 Optimización importante
        return Computador.objects.select_related(
            'marca',
            'modelo',
            'tipo',
            'sistema_operativo',
            'microsoft_office'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Listado de Computadores',
            'list_url': reverse_lazy('list_computador'),
            'create_url': reverse_lazy('create_computador'),
            'datatable_enabled': True,
            'datatable_order': [[0, 'asc']],
            'datatable_page_length': 100,
            'columns': self.datatable_columns,
        })
        return context


class ComputadorDetailView(DetailView):
    model = Computador
    template_name = 'computador/detail.html'

    def render_to_response(self, context, **response_kwargs):
        # Si es una solicitud AJAX, devolvemos solo el fragmento HTML
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.template.loader import render_to_string
            html = render_to_string(self.template_name, context=context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)


class ComputadorCreateView(IncludeUserFormCreate, CreateView):
    template_name = 'computador/form.html'
    model = Computador
    form_class = FormComputador
    success_url = reverse_lazy('list_computador')

    def form_valid(self, form):
        messages.success(self.request, 'Computador creado correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hay errores en el formulario')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Computador'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        return context


class ComputadorUpdateView(IncludeUserFormUpdate, UpdateView):
    template_name = 'computador/form.html'
    model = Computador
    form_class = FormComputador
    success_url = reverse_lazy('list_computador')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Computador creada correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hay errores en el formulario')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Computador'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME
        return context


class ComputadorHistoryListView(GenericHistoryListView):
    base_model = Computador
    template_name = 'history/list.html'
