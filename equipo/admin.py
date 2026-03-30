from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from simple_history.admin import SimpleHistoryAdmin

from .models.celular import Celular
from .models.computador import Computador
from .models.impresora import Impresora


# --- Resources ---

class ComputadorResource(resources.ModelResource):
    marca_nombre = Field(attribute='marca__nombre', column_name='Marca')
    modelo_nombre = Field(attribute='modelo__nombre', column_name='Modelo')
    tipo_nombre = Field(attribute='tipo__nombre', column_name='Tipo')
    so_nombre = Field(attribute='sistema_operativo__nombre', column_name='SO')
    establecimiento_nombre = Field(attribute='establecimiento__nombre', column_name='Establecimiento')
    funcionario_nombre = Field(attribute='responsable__nombres', column_name='Responsable')

    class Meta:
        model = Computador
        import_id_fields = ['id']
        skip_unchanged = True
        report_skipped = True


class ImpresoraResource(resources.ModelResource):
    marca_nombre = Field(attribute='marca__nombre', column_name='Marca')
    modelo_nombre = Field(attribute='modelo__nombre', column_name='Modelo')
    tipo_nombre = Field(attribute='tipo__nombre', column_name='Tipo')
    toner_nombre = Field(attribute='toner__nombre', column_name='Tóner/Tinta')
    establecimiento_nombre = Field(attribute='establecimiento__nombre', column_name='Establecimiento')
    funcionario_nombre = Field(attribute='responsable__nombres', column_name='Responsable')

    class Meta:
        model = Impresora
        import_id_fields = ['id']
        skip_unchanged = True
        report_skipped = True


class CelularResource(resources.ModelResource):
    marca_nombre = Field(attribute='marca__nombre', column_name='Marca')
    modelo_nombre = Field(attribute='modelo__nombre', column_name='Modelo')
    tipo_nombre = Field(attribute='tipo__nombre', column_name='Tipo')
    establecimiento_nombre = Field(attribute='establecimiento__nombre', column_name='Establecimiento')
    funcionario_nombre = Field(attribute='responsable__nombres', column_name='Responsable')

    class Meta:
        model = Celular
        import_id_fields = ['id']
        skip_unchanged = True
        report_skipped = True


# --- Admins ---

@admin.register(Computador)
class ComputadorAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = ComputadorResource
    list_display = ("id", "asignado", "serie", "marca", "modelo", "tipo", "establecimiento", "status")
    search_fields = ("serie", "marca__nombre", "modelo__nombre", "ip", "mac")
    list_filter = ("marca", "tipo", "establecimiento", "status", "de_baja")
    ordering = ("-id",)


@admin.register(Impresora)
class ImpresoraAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = ImpresoraResource
    list_display = ("id", "serie", "marca", "modelo", "tipo", "establecimiento", "status")
    search_fields = ("serie", "marca__nombre", "modelo__nombre", "ip")
    list_filter = ("marca", "tipo", "establecimiento", "status", "de_baja")
    ordering = ("-id",)


@admin.register(Celular)
class CelularAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = CelularResource
    list_display = ("id", "numero_telefono", "imei", "marca", "modelo", "establecimiento", "status")
    search_fields = ("numero_telefono", "imei", "marca__nombre", "modelo__nombre")
    list_filter = ("marca", "tipo", "establecimiento", "status", "de_baja")
    ordering = ("-id",)
