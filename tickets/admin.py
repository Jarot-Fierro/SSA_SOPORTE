from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from .models import Ticket, TicketActivo


# =========================================================
# RESOURCE: TICKET
# =========================================================
class TicketResource(resources.ModelResource):
    asignado_a_nombre = fields.Field(attribute='asignado_a__username', column_name='Asignado A')
    funcionario_nombre = fields.Field(attribute='funcionario__nombres', column_name='Funcionario')

    class Meta:
        model = Ticket
        import_id_fields = ['id']
        skip_unchanged = True
        report_skipped = True


# =========================================================
# RESOURCE: TICKET ACTIVO
# =========================================================
class TicketActivoResource(resources.ModelResource):
    ticket_numero = fields.Field(attribute='ticket__numero_ticket', column_name='N° Ticket')
    ticket_titulo = fields.Field(attribute='ticket__titulo', column_name='Título Ticket')
    equipo_str = fields.Field(attribute='equipo', column_name='Equipo')
    establecimiento_ticket = fields.Field(column_name='Establecimiento')
    departamento_ticket = fields.Field(column_name='Departamento')

    class Meta:
        model = TicketActivo
        import_id_fields = ['id']
        skip_unchanged = True
        report_skipped = True

    def dehydrate_establecimiento_ticket(self, obj):
        return obj.ticket.establecimiento.nombre if obj.ticket and obj.ticket.establecimiento else '-'

    def dehydrate_departamento_ticket(self, obj):
        return obj.ticket.departamento.nombre if obj.ticket and obj.ticket.departamento else '-'


# =========================================================
# INLINES
# =========================================================
class TicketActivoInline(admin.TabularInline):
    model = TicketActivo
    extra = 1
    autocomplete_fields = ['equipo']


# =========================================================
# ADMIN: TICKET
# =========================================================
@admin.register(Ticket)
class TicketAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = TicketResource

    list_display = (
        "id",
        "numero_ticket",
        "titulo",
        "departamento",
        "establecimiento",
        "estado",
        "asignado_a",
        "funcionario",
        "cantidad_activos",
        "status",
    )

    search_fields = (
        "numero_ticket",
        "titulo",
        "departamento__nombre",
        "departamento__alias",
        "descripcion",
        "asignado_a__username",
        "funcionario__nombres",
    )

    list_filter = (
        "estado",
        "departamento",
        "asignado_a",
        "status",
        "created_at",
    )

    ordering = ("-id",)

    inlines = [TicketActivoInline]

    autocomplete_fields = (
        'departamento',
        'establecimiento',
        'asignado_a',
        'funcionario',
        'tipo_soporte',
    )

    def cantidad_activos(self, obj):
        return obj.equipos.count()

    cantidad_activos.short_description = "Activos/Equipos"


# =========================================================
# ADMIN: TICKET ACTIVO
# =========================================================
@admin.register(TicketActivo)
class TicketActivoAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = TicketActivoResource

    list_display = (
        'id',
        'ticket',
        'equipo',
        'establecimiento_ticket',
        'departamento_ticket',
        'observacion',
    )

    search_fields = (
        'ticket__numero_ticket',
        'ticket__titulo',
        'ticket__establecimiento__nombre',
        'ticket__departamento__nombre',
        'equipo__serie',
        'observacion',
    )

    list_filter = (
        'ticket__estado',
        'ticket__establecimiento',
        'ticket__departamento',
        'created_at',
    )

    ordering = ('-id',)

    autocomplete_fields = ('ticket', 'equipo')

    def establecimiento_ticket(self, obj):
        return obj.ticket.establecimiento if obj.ticket and obj.ticket.establecimiento else '-'

    establecimiento_ticket.short_description = 'Establecimiento'

    def departamento_ticket(self, obj):
        return obj.ticket.departamento if obj.ticket and obj.ticket.departamento else '-'

    departamento_ticket.short_description = 'Departamento'
