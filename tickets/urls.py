from django.urls import path

from tickets.views.panel_ticket import *
from tickets.views.tickets import *

urlpatterns = [
    # TICKETS
    path('soporte-tickets/', TicketListView.as_view(), name='ticket_list'),
    path('soporte-tickets/crear/', TicketCreateView.as_view(), name='ticket_create'),
    path('soporte-tickets/editar/<int:pk>', TicketsUpdateView.as_view(), name='ticket_update'),
    path('soporte-tickets/asignar-equipo/<int:pk>/', TicketAsignarEquipoView.as_view(), name='ticket_asignar_equipo'),
    path('soporte-tickets/get-equipos-ajax/', get_equipos_ajax, name='get_equipos_ajax'),
    path('soporte-tickets/eliminar-equipo/<int:pk>/', TicketEliminarEquipoView.as_view(),
         name='ticket_eliminar_equipo'),

    # PANEL DE TICKETS
    path('soporte-tickets-panel/', PanelTicketListView.as_view(), name='ticket_panel_list'),
    path('soporte-tickets-panel/crear/', PanelTicketCreateView.as_view(), name='ticket_panel_create'),
    path('soporte-tickets-panel/editar/<int:pk>', PanelTicketsUpdateView.as_view(), name='ticket_panel_update'),
]
