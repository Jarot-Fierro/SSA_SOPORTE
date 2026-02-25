from django.urls import path

from equipo.views.celular import *
from equipo.views.computador import *
from equipo.views.impresora import *

urlpatterns = [

    # CELULAR
    path('lista-celular/', CelularListView.as_view(), name='list_celular'),
    path('detalle-celular/<int:pk>/detalle/', CelularDetailView.as_view(), name='detail_celular'),
    path('crear-celular/', CelularCreateView.as_view(), name='create_celular'),
    path('actualizar-celular/<int:pk>/detalle/', CelularUpdateView.as_view(), name='update_celular'),
    path('historial-celular/', CelularHistoryListView.as_view(), name='historical_celular'),

    # COMPUTADOR
    path('lista-computador/', ComputadorListView.as_view(), name='list_computador'),
    path('detalle-computador/<int:pk>/detalle/', ComputadorDetailView.as_view(), name='detail_computador'),
    path('crear-computador/', ComputadorCreateView.as_view(), name='create_computador'),
    path('actualizar-computador/<int:pk>/detalle/', ComputadorUpdateView.as_view(), name='update_computador'),
    path('historial-computador/', ComputadorHistoryListView.as_view(), name='historical_computador'),

    # IMPRESORAS
    path('lista-impresora/', ImpresoraListView.as_view(), name='list_impresora'),
    path('detalle-impresora/<int:pk>/detalle/', ImpresoraDetailView.as_view(), name='detail_impresora'),
    path('crear-impresora/', ImpresoraCreateView.as_view(), name='create_impresora'),
    path('actualizar-impresora/<int:pk>/detalle/', ImpresoraUpdateView.as_view(), name='update_impresora'),
    path('historial-impresora/', ImpresoraHistoryListView.as_view(), name='historical_impresora'),

]
