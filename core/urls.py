from django.urls import path

from core import views
from core.views import ContactoView

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/data/', views.dashboard_data_api, name='dashboard_data'),
    path('no-posee-establecimiento/', views.no_establecimiento, name='no_establecimiento'),
    path('contacto/', ContactoView.as_view(), name='contacto'),
]
