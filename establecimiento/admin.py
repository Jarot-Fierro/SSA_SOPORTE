from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from simple_history.admin import SimpleHistoryAdmin

from .models.comuna import Comuna
from .models.departamento import Departamento
from .models.establecimiento import Establecimiento
from .models.funcionario import Funcionario


# --- Resources ---

class ComunaResource(resources.ModelResource):
    class Meta:
        model = Comuna
        import_id_fields = ['id']
        fields = ('id', 'nombre', 'status')
        skip_unchanged = True
        report_skipped = True


class EstablecimientoResource(resources.ModelResource):
    comuna_nombre = Field(attribute='comuna__nombre', column_name='Comuna')

    class Meta:
        model = Establecimiento
        import_id_fields = ['id']
        fields = ('id', 'nombre', 'alias', 'direccion', 'telefono', 'comuna', 'comuna_nombre', 'status')
        skip_unchanged = True
        report_skipped = True


class DepartamentoResource(resources.ModelResource):
    establecimiento_nombre = Field(attribute='establecimiento__nombre', column_name='Establecimiento')

    class Meta:
        model = Departamento
        import_id_fields = ['id']
        fields = ('id', 'nombre', 'alias', 'direccion', 'establecimiento', 'establecimiento_nombre', 'status')
        skip_unchanged = True
        report_skipped = True


class FuncionarioResource(resources.ModelResource):
    departamento_nombre = Field(attribute='departamento__nombre', column_name='Departamento')
    puesto_trabajo_nombre = Field(attribute='puesto_trabajo__nombre', column_name='Puesto Trabajo')

    class Meta:
        model = Funcionario
        import_id_fields = ['id']
        fields = ('id', 'nombres', 'rut', 'correo', 'jefatura', 'departamento', 'departamento_nombre', 'puesto_trabajo',
                  'puesto_trabajo_nombre', 'status')
        skip_unchanged = True
        report_skipped = True


# --- Admins ---

@admin.register(Comuna)
class ComunaAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = ComunaResource
    list_display = ("id", "nombre", "status")
    search_fields = ("nombre",)
    ordering = ("-id",)


@admin.register(Establecimiento)
class EstablecimientoAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = EstablecimientoResource
    list_display = ("id", "nombre", "alias", "comuna", "status")
    search_fields = ("nombre", "comuna__nombre")
    list_filter = ("comuna", "status")
    ordering = ("-id",)


@admin.register(Departamento)
class DepartamentoAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = DepartamentoResource
    list_display = ("id", "alias", "nombre", "establecimiento", "status")
    search_fields = ("nombre", "alias", "establecimiento__nombre")
    list_filter = ("establecimiento", "status")
    ordering = ("-id",)


@admin.register(Funcionario)
class FuncionarioAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = FuncionarioResource
    list_display = ("id", "nombres", "rut", "departamento", "status")
    search_fields = ("nombres", "rut", "correo", "departamento__nombre")
    list_filter = ("departamento", "status", "jefatura")
    ordering = ("-id",)
