from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from simple_history.admin import SimpleHistoryAdmin

from .models import Ticket


# --- Resources ---

class TicketResource(resources.ModelResource):
    asignado_a_nombre = Field(attribute='asignado_a__username', column_name='Asignado A')
    funcionario_nombre = Field(attribute='funcionario__nombres', column_name='Funcionario')

    class Meta:
        model = Ticket
        import_id_fields = ['id']
        skip_unchanged = True
        report_skipped = True


# --- Admins ---

@admin.register(Ticket)
class TicketAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = TicketResource
    list_display = ("id", "numero_ticket", "titulo", "estado", "asignado_a", "funcionario")
    search_fields = ("numero_ticket", "titulo", "descripcion", "asignado_a__username", "funcionario__nombres")
    list_filter = ("estado", "asignado_a", "created_at")
    ordering = ("-id",)
