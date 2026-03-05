from django.contrib import admin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import path, include
from weasyprint import HTML

from core.views import dashboard_view
from equipo.models.computador import Computador


def generar_pdf(request):
    # Datos a pasar a la plantilla
    equipo = Computador.objects.filter(status=True).get(id=1)
    contexto = {
        'nombre': 'Usuario',
        'fecha': '10/10/2023',
        'equipo': equipo
    }
    html_string = render_to_string('pdfs/computer_acta.html', contexto, request=request)

    # Crear respuesta PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte.pdf"'  # 'attachment' para descargar

    # Generar PDF
    HTML(string=html_string).write_pdf(response)
    return response


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('core.urls')),
    path('', dashboard_view, name='home'),
    path('', include('establecimiento.urls')),
    path('', include('catalogo.urls')),
    path('', include('equipo.urls')),
    path('pdf/', generar_pdf, name='generar_pdf'),
]
