from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import TemplateView


@login_required
def dashboard_view(request):
    permissions = {
        'comunas': 0,
        'establecimientos': 0,
        'fichas': 0,
        'genero': 0,
        'movimiento_ficha': 0,
        'paciente': 0,
        'pais': 0,
        'prevision': 0,
        'colores_sector': 0,
        'profesion': 0,
        'profesionales': 0,
        'sectores': 0,
        'servicio_clinico': 0,
        'soporte': 0,
    }

    return render(request, 'core/dashboard.html')


@login_required
def no_establecimiento(request):
    return render(request, 'core/no_establecimiento.html')


class ContactoView(LoginRequiredMixin, TemplateView):
    template_name = 'contacto/contacto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Contacto',
        })
        return context
