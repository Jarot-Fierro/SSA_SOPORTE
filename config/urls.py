from django.contrib import admin
from django.urls import path, include

from core.views import DashboardView

# from core.views import dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('core.urls')),
    path('', DashboardView.as_view(), name='home'),
    path('', include('establecimiento.urls')),
    path('', include('catalogo.urls')),
    path('', include('equipo.urls')),
    path('', include('tickets.urls')),
    path('', include('inventario.urls')),
    path('', include('reports.urls')),
]
