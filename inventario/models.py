from django.db import models
from simple_history.models import HistoricalRecords

from core.models import StandardModel


class CategoriaInventario(models.Model):
    nombre = models.CharField(max_length=50)

    UPPERCASE_FIELDS = ['nombre', ]

    def __str__(self):
        return self.nombre


class InventarioMantencion(StandardModel):
    producto = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=250, blank=True)
    unidad = models.CharField(max_length=50)
    tipo_material = models.CharField(max_length=50)
    tipo_compra = models.CharField(max_length=50)

    codigo = models.CharField(max_length=50, unique=True)
    stock_actual = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=0)
    stock_maximo = models.PositiveIntegerField(null=True, blank=True)

    ubicacion = models.CharField(max_length=100, blank=True)

    lote = models.CharField(max_length=50, blank=True, null=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)

    categoria = models.ForeignKey('catalogo.SubCategoria', on_delete=models.PROTECT)

    history = HistoricalRecords()

    UPPERCASE_FIELDS = ['producto', 'descripcion', 'unidad', 'tipo_material', 'tipo_compra', 'codigo', 'ubicacion',
                        'lote']

    class Meta:
        verbose_name = 'Producto Mantencion'
        verbose_name_plural = 'Productos Mantecion'

    def __str__(self):
        return self.producto


class InventarioInformatica(StandardModel):
    producto = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=250, blank=True)
    unidad = models.CharField(max_length=50)
    tipo_material = models.CharField(max_length=50)
    tipo_compra = models.CharField(max_length=50)

    codigo = models.CharField(max_length=50, unique=True)
    stock_actual = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=0)
    stock_maximo = models.PositiveIntegerField(null=True, blank=True)

    ubicacion = models.CharField(max_length=100, blank=True)

    lote = models.CharField(max_length=50, blank=True, null=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)

    categoria = models.ForeignKey('catalogo.SubCategoria', on_delete=models.PROTECT)

    history = HistoricalRecords()

    UPPERCASE_FIELDS = ['producto', 'descripcion', 'unidad', 'tipo_material', 'tipo_compra', 'codigo', 'ubicacion',
                        'lote']

    class Meta:
        verbose_name = 'Producto TIC'
        verbose_name_plural = 'Productos TIC'

    def __str__(self):
        return self.producto
