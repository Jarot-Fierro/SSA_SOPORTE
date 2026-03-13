from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from equipo.models.celular import Celular
from equipo.models.computador import Computador
from equipo.models.impresora import Impresora


def generar_pdf_computador(request):
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


def generar_pdf_celular(request):
    # Datos a pasar a la plantilla
    equipo = Celular.objects.filter(status=True).get(id=1)
    contexto = {
        'nombre': 'Usuario',
        'fecha': '10/10/2023',
        'equipo': equipo
    }
    html_string = render_to_string('pdfs/phone_acta.html', contexto, request=request)

    # Crear respuesta PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte.pdf"'  # 'attachment' para descargar

    # Generar PDF
    HTML(string=html_string).write_pdf(response)
    return response


def generar_pdf_impresora(request):
    # Datos a pasar a la plantilla
    equipo = Impresora.objects.filter(status=True).get(id=1)
    contexto = {
        'nombre': 'Usuario',
        'fecha': '10/10/2023',
        'equipo': equipo
    }
    html_string = render_to_string('pdfs/printer_acta.html', contexto, request=request)

    # Crear respuesta PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte.pdf"'  # 'attachment' para descargar

    # Generar PDF
    HTML(string=html_string).write_pdf(response)
    return response
