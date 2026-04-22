from django.urls import path

from inventario.views.inventariotic import (
    InventarioTICListView,
    InventarioTICDetailView,
    InventarioTICCreateView,
    InventarioTICUpdateView,
    InventarioTICHistoryListView
)
from inventario.views.mantencion import (
    InventarioMantencionListView,
    InventarioMantencionDetailView,
    InventarioMantencionCreateView,
    InventarioMantencionUpdateView,
    InventarioMantencionHistoryListView
)

urlpatterns = [
    # INVENTARIO MANTENCION
    path('mantencion/lista/', InventarioMantencionListView.as_view(), name='list_inventarios_mantencion'),
    path('mantencion/detalle/<int:pk>/', InventarioMantencionDetailView.as_view(),
         name='detail_inventarios_mantencion'),
    path('mantencion/crear/', InventarioMantencionCreateView.as_view(), name='create_inventarios_mantencion'),
    path('mantencion/actualizar/<int:pk>/', InventarioMantencionUpdateView.as_view(),
         name='update_inventarios_mantencion'),
    path('mantencion/historial/', InventarioMantencionHistoryListView.as_view(),
         name='historical_inventarios_mantencion'),

    # INVENTARIO TIC
    path('tic/lista/', InventarioTICListView.as_view(), name='list_inventarios_tic'),
    path('tic/detalle/<int:pk>/', InventarioTICDetailView.as_view(), name='detail_inventarios_tic'),
    path('tic/crear/', InventarioTICCreateView.as_view(), name='create_inventarios_tic'),
    path('tic/actualizar/<int:pk>/', InventarioTICUpdateView.as_view(), name='update_inventarios_tic'),
    path('tic/historial/', InventarioTICHistoryListView.as_view(), name='historical_inventarios_tic'),
]
