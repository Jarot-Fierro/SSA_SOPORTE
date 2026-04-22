from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from .models import CategoriaInventario, InventarioMantencion, InventarioInformatica


# --- Resources ---

class CategoriaInventarioResource(resources.ModelResource):
    class Meta:
        model = CategoriaInventario
        import_id_fields = ['id']
        skip_unchanged = True
        report_skipped = True


class InventarioMantencionResource(resources.ModelResource):
    class Meta:
        model = InventarioMantencion
        import_id_fields = ['id']
        skip_unchanged = True
        report_skipped = True


class InventarioInformaticaResource(resources.ModelResource):
    class Meta:
        model = InventarioInformatica
        import_id_fields = ['id']
        skip_unchanged = True
        report_skipped = True


# --- Admins ---

@admin.register(CategoriaInventario)
class CategoriaInventarioAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = CategoriaInventarioResource
    list_display = ("id", "nombre")
    search_fields = ("nombre",)


@admin.register(InventarioMantencion)
class InventarioMantencionAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = InventarioMantencionResource
    list_display = ("id", "producto", "codigo", "stock_actual", "categoria", "status")
    search_fields = ("producto", "codigo")
    list_filter = ("categoria", "status")
    ordering = ("-id",)


@admin.register(InventarioInformatica)
class InventarioInformaticaAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = InventarioInformaticaResource
    list_display = ("id", "producto", "codigo", "stock_actual", "categoria", "status")
    search_fields = ("producto", "codigo")
    list_filter = ("categoria", "status")
    ordering = ("-id",)
