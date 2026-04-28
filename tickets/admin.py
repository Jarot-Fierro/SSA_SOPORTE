# from django.contrib import admin
# from import_export import resources, fields
# from import_export.admin import ImportExportModelAdmin
# from simple_history.admin import SimpleHistoryAdmin
#
# from .models import Ticket, TicketActivo
#
#
# # =========================================================
# # RESOURCE: TICKET
# # =========================================================
# class TicketResource(resources.ModelResource):
#     asignado_a_nombre = fields.Field(attribute='asignado_a__username', column_name='Asignado A')
#     funcionario_nombre = fields.Field(attribute='funcionario__nombres', column_name='Funcionario')
#
#     class Meta:
#         model = Ticket
#         import_id_fields = ['id']
#         skip_unchanged = True
#         report_skipped = True
#
#
# # =========================================================
# # RESOURCE: TICKET ACTIVO
# # =========================================================
# class TicketActivoResource(resources.ModelResource):
#     ticket_numero = fields.Field(attribute='ticket__numero_ticket', column_name='N° Ticket')
#     ticket_titulo = fields.Field(attribute='ticket__titulo', column_name='Título Ticket')
#     tipo_activo = fields.Field(column_name='Tipo Activo')
#     activo_str = fields.Field(column_name='Activo')
#     establecimiento_ticket = fields.Field(column_name='Establecimiento')
#     departamento_ticket = fields.Field(column_name='Departamento')
#
#     class Meta:
#         model = TicketActivo
#         import_id_fields = ['id']
#         skip_unchanged = True
#         report_skipped = True
#
#     def dehydrate_tipo_activo(self, obj):
#         if obj.content_type:
#             return obj.content_type.model_class()._meta.verbose_name.title()
#         return '-'
#
#     def dehydrate_activo_str(self, obj):
#         return str(obj.activo) if obj.activo else '-'
#
#     def dehydrate_establecimiento_ticket(self, obj):
#         return obj.ticket.establecimiento.nombre if obj.ticket and obj.ticket.establecimiento else '-'
#
#     def dehydrate_departamento_ticket(self, obj):
#         return obj.ticket.departamento.nombre if obj.ticket and obj.ticket.departamento else '-'
#
#
# # =========================================================
# # ADMIN: TICKET
# # =========================================================
# @admin.register(Ticket)
# class TicketAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
#     resource_class = TicketResource
#
#     list_display = (
#         "id",
#         "numero_ticket",
#         "titulo",
#         "departamento",
#         "establecimiento",
#         "estado",
#         "asignado_a",
#         "funcionario",
#         "cantidad_activos",
#         "status_icon",
#     )
#
#     search_fields = (
#         "numero_ticket",
#         "titulo",
#         "departamento__nombre",
#         "departamento__alias",
#         "descripcion",
#         "asignado_a__username",
#         "funcionario__nombres",
#     )
#
#     list_filter = (
#         "estado",
#         "departamento",
#         "asignado_a",
#         "created_at",
#     )
#
#     ordering = ("-id",)
#
#     inlines = [TicketActivoInline]
#
#     autocomplete_fields = (
#         'departamento',
#         'establecimiento',
#         'asignado_a',
#         'funcionario',
#         'tipo_soporte',
#     )
#
#     def cantidad_activos(self, obj):
#         return obj.activos_relacionados.count()
#
#     cantidad_activos.short_description = "Activos/Equipos"
#
#     def status_icon(self, obj):
#         return obj.status
#
#     status_icon.boolean = True
#     status_icon.short_description = "Estado"
#
#
# # =========================================================
# # ADMIN: TICKET ACTIVO
# # =========================================================
# @admin.register(TicketActivo)
# class TicketActivoAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
#     resource_class = TicketActivoResource
#
#     list_display = (
#         'id',
#         'ticket',
#         'tipo_activo',
#         'activo_relacionado',
#         'establecimiento_ticket',
#         'departamento_ticket',
#         'observacion',
#     )
#
#     search_fields = (
#         'ticket__numero_ticket',
#         'ticket__titulo',
#         'ticket__establecimiento__nombre',
#         'ticket__departamento__nombre',
#         'observacion',
#     )
#
#     list_filter = (
#         'content_type',
#         'ticket__estado',
#         'ticket__establecimiento',
#         'ticket__departamento',
#         'created_at',
#     )
#
#     ordering = ('-id',)
#
#     autocomplete_fields = ('ticket', 'content_type')
#
#     def tipo_activo(self, obj):
#         if obj.content_type:
#             model = obj.content_type.model_class()
#             return model._meta.verbose_name.title()
#         return '-'
#
#     tipo_activo.short_description = 'Tipo Activo'
#
#     def activo_relacionado(self, obj):
#         if obj.activo:
#             return str(obj.activo)
#         return '-'
#
#     activo_relacionado.short_description = 'Activo'
#
#     def establecimiento_ticket(self, obj):
#         return obj.ticket.establecimiento if obj.ticket and obj.ticket.establecimiento else '-'
#
#     establecimiento_ticket.short_description = 'Establecimiento'
#
#     def departamento_ticket(self, obj):
#         return obj.ticket.departamento if obj.ticket and obj.ticket.departamento else '-'
#
#     departamento_ticket.short_description = 'Departamento'
