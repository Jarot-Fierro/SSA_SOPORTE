from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView

from core.mixin import DataTableMixin
from core.utils import IncludeUserFormUpdate
from tickets.forms.forms_tickets import FormTicket
from tickets.models import Ticket

MODULE_NAME = 'Tickets'


class TicketListView(DataTableMixin, TemplateView):
    template_name = 'tickets/list.html'
    model = Ticket

    datatable_columns = [
        'ID',
        'Ticket',
        'Solicitante',
        'Departamento',
        'Título',
        'Estado',
        'Fecha'
    ]

    datatable_order_fields = [
        'id',
        'numero_ticket',
        'funcionario__nombres',
        'departamento',
        'titulo',
        'estado',
        'created_at'
    ]

    datatable_search_fields = [
        'numero_ticket__icontains',
        'titulo__icontains',
        'descripcion__icontains',
        'funcionario__nombres__icontains',
        'departamento__icontains',
    ]

    url_update = 'ticket_update'

    def get_base_queryset(self):

        user = self.request.user

        queryset = Ticket.objects.select_related(
            'funcionario',
            'asignado_a'
        )

        # si el usuario pertenece a un establecimiento
        if user.establecimiento:
            queryset = queryset.filter(departamento=user.departamento)

        return queryset

    def render_row(self, obj):

        solicitante = str(obj.funcionario) if obj.funcionario else '—'

        return {
            'ID': obj.id,
            'Ticket': obj.numero_ticket,
            'Solicitante': solicitante,
            'Departamento': obj.departamento,
            'Título': obj.titulo,
            'Estado': obj.get_estado_display(),
            'Fecha': obj.created_at.strftime('%d-%m-%Y %H:%M') if obj.created_at else '—',
        }

    def get(self, request, *args, **kwargs):

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.GET.get('datatable'):
            return self.get_datatable_response(request)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        tickets_abiertos = Ticket.objects.filter(estado='ABIERTO', created_by=self.request.user.departamento).count()
        tickets_proceso = Ticket.objects.filter(estado='EN_PROCESO', created_by=self.request.user.departamento).count()
        tickets_resueltos = Ticket.objects.filter(estado='RESUELTOS', created_by=self.request.user.departamento).count()
        total_tickets = Ticket.objects.filter(created_by=self.request.user.departamento).count()

        context.update({
            'title': f'Lista de Tickets - Departamento {self.request.user.departamento}',
            'list_url': reverse_lazy('ticket_list'),
            'create_url': reverse_lazy('ticket_create'),
            'datatable_enabled': True,
            'datatable_order': [[0, 'desc']],
            'datatable_page_length': 50,
            'columns': self.datatable_columns,
            'tickets_abiertos': tickets_abiertos,
            'tickets_proceso': tickets_proceso,
            'tickets_resuletos': tickets_resueltos,
            'total_tickets': total_tickets,
        })

        return context


class TicketCreateView(CreateView):
    template_name = 'tickets/form.html'
    model = Ticket
    form_class = FormTicket
    success_url = reverse_lazy('ticket_list')

    def form_valid(self, form):
        messages.success(self.request, 'Ticket Generado correctamente')
        form.instance.departamento = self.request.user.username
        form.instance.created_by = self.request.user

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hay errores en el formulario')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Ticket'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        return context


class TicketsUpdateView(IncludeUserFormUpdate, UpdateView):
    template_name = 'tickets/form.html'
    model = Ticket
    form_class = FormTicket
    success_url = reverse_lazy('ticket_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Tickets creado correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hay errores en el formulario')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Ticket'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME
        return context
