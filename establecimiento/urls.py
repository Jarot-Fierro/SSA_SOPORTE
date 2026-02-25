from django.urls import path

from establecimiento.views.comuna import *
from establecimiento.views.departamento import *
from establecimiento.views.establecimiento import *
from establecimiento.views.funcionario import *

urlpatterns = [

    # COMUNAS
    path('lista-comunas/', ComunaListView.as_view(), name='list_comunas'),
    path('detalle-comunas/<int:pk>/detalle/', ComunaDetailView.as_view(), name='detail_comunas'),
    path('crear-comunas/', ComunaCreateView.as_view(), name='create_comunas'),
    path('actualizar-comunas/<int:pk>/detalle/', ComunaUpdateView.as_view(), name='update_comunas'),
    path('historial-comunas/', ComunaHistoryListView.as_view(), name='historical_comunas'),

    # ESTABLECIMIENTOS
    path('lista-establecimientos/', EstablecimientoListView.as_view(), name='list_establecimientos'),
    path('detalle-establecimientos/<int:pk>/detalle/', EstablecimientoDetailView.as_view(),
         name='detail_establecimientos'),
    path('crear-establecimientos/', EstablecimientoCreateView.as_view(), name='create_establecimientos'),
    path('actualizar-establecimientos/<int:pk>/detalle/', EstablecimientoUpdateView.as_view(),
         name='update_establecimientos'),
    path('historial-establecimientos/', EstablecimientoHistoryListView.as_view(), name='historical_establecimientos'),

    # DEPARTAMENTOS
    path('lista-departamentos/', DepartamentoListView.as_view(), name='list_departamentos'),
    path('detalle-departamentos/<int:pk>/detalle/', DepartamentoDetailView.as_view(), name='detail_departamentos'),
    path('crear-departamentos/', DepartamentoCreateView.as_view(), name='create_departamentos'),
    path('actualizar-departamentos/<int:pk>/detalle/', DepartamentoUpdateView.as_view(), name='update_departamentos'),
    path('historial-departamentos/', DepartamentoHistoryListView.as_view(), name='historical_departamentos'),

    # FUNCIONARIOS
    path('lista-funcionarios/', FuncionarioListView.as_view(), name='list_funcionarios'),
    path('detalle-funcionarios/<int:pk>/detalle/', FuncionarioDetailView.as_view(), name='detail_funcionarios'),
    path('crear-funcionarios/', FuncionarioCreateView.as_view(), name='create_funcionarios'),
    path('actualizar-funcionarios/<int:pk>/detalle/', FuncionarioUpdateView.as_view(), name='update_funcionarios'),
    path('historial-funcionarios/', FuncionarioHistoryListView.as_view(), name='historical_funcionarios'),

]
