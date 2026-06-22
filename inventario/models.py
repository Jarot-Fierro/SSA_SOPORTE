from django.db import models
from simple_history.models import HistoricalRecords

from core.models import StandardModel


class CategoriaInventario(models.Model):
    nombre = models.CharField(max_length=50)

    UPPERCASE_FIELDS = ['nombre', ]

    def __str__(self):
        return self.nombre


class InventarioMantencion(StandardModel):
    UNIDAD_CHOICES = [
        ('UNIDAD', 'UNIDAD'),
        ('METRO', 'METRO'),
        ('CAJA', 'CAJA'),
        ('BOLSA', 'BOLSA'),
        ('LITRO', 'LITRO'),
        ('GALÓN', 'GALÓN'),
        ('PAR', 'PAR'),
        ('ROLLO', 'ROLLO'),
        ('PAQUETE', 'PAQUETE'),
    ]

    STATUS_CHOICES = [
        ('OK', 'OK'),
        ('REPOSICIÓN', 'REPOSICIÓN'),
        ('SOBRESTOCK', 'SOBRESTOCK')
    ]
    RESPONSABLE_CHOICES = [
        ('MANTENCIÓN', 'MANTENCIÓN'),
        ('AUXILIAR MANTENCIÓN', 'AUXILIAR MANTENCIÓN'),
        ('JEFE SERVICIOS GENERALES', 'JEFE SERVICIOS GENERALES'),
        ('OTRO', 'OTRO'),
    ]

    producto = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=250, blank=True)
    unidad = models.CharField(max_length=50, choices=UNIDAD_CHOICES, default='UNIDAD')
    tipo_material = models.CharField(max_length=50, null=True, blank=True)
    tipo_compra = models.CharField(max_length=50, null=True, blank=True)

    codigo = models.CharField(max_length=50, blank=True, null=True)
    stock_actual = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=0)
    stock_maximo = models.PositiveIntegerField(null=True, blank=True)

    ubicacion = models.CharField(max_length=100, blank=True, default='Bodega Mantención')

    lote = models.CharField(max_length=50, blank=True, null=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    status_stock = models.CharField(max_length=50, choices=STATUS_CHOICES, default='ACTIVO', null=True, blank=True)

    categoria = models.ForeignKey('catalogo.SubCategoria', on_delete=models.PROTECT)
    responsable = models.CharField(max_length=100, choices=RESPONSABLE_CHOICES, default='OTRO')

    fecha_ingreso = models.DateField(null=True, blank=True)
    ultima_salida = models.DateField(null=True, blank=True)

    history = HistoricalRecords()

    UPPERCASE_FIELDS = ['producto', 'descripcion', 'unidad', 'tipo_material', 'tipo_compra', 'codigo', 'ubicacion',
                        'lote', 'status_stock', 'responsable']

    class Meta:
        verbose_name = 'Producto Mantencion'
        verbose_name_plural = 'Productos Mantecion'

    def __str__(self):
        return self.producto


class InventarioInformatica(StandardModel):
    UNIDAD_CHOICES = [
        ('UNIDAD', 'UNIDAD'),
        ('METRO', 'METRO'),
        ('CAJA', 'CAJA'),
        ('BOLSA', 'BOLSA'),
        ('LITRO', 'LITRO'),
        ('GALÓN', 'GALÓN'),
        ('PAR', 'PAR'),
        ('ROLLO', 'ROLLO'),
        ('PAQUETE', 'PAQUETE'),
    ]

    STATUS_CHOICES = [
        ('OK', 'OK'),
        ('REPOSICIÓN', 'REPOSICIÓN'),
        ('SOBRESTOCK', 'SOBRESTOCK')
    ]
    RESPONSABLE_CHOICES = [
        ('MANTENCIÓN', 'MANTENCIÓN'),
        ('AUXILIAR MANTENCIÓN', 'AUXILIAR MANTENCIÓN'),
        ('JEFE SERVICIOS GENERALES', 'JEFE SERVICIOS GENERALES'),
        ('OTRO', 'OTRO'),
    ]

    producto = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=250, blank=True)
    unidad = models.CharField(max_length=50, choices=UNIDAD_CHOICES, default='UNIDAD')
    tipo_material = models.CharField(max_length=50, null=True, blank=True)
    tipo_compra = models.CharField(max_length=50, null=True, blank=True)

    codigo = models.CharField(max_length=50, blank=True, null=True)
    stock_actual = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=0)
    stock_maximo = models.PositiveIntegerField(null=True, blank=True)

    ubicacion = models.CharField(max_length=100, blank=True, default='Bodega Informática')

    lote = models.CharField(max_length=50, blank=True, null=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    status_stock = models.CharField(max_length=50, choices=STATUS_CHOICES, default='ACTIVO', null=True, blank=True)

    categoria = models.ForeignKey('catalogo.SubCategoria', on_delete=models.PROTECT)
    responsable = models.CharField(max_length=100, choices=RESPONSABLE_CHOICES, default='OTRO')

    fecha_ingreso = models.DateField(null=True, blank=True)
    ultima_salida = models.DateField(null=True, blank=True)

    history = HistoricalRecords()

    UPPERCASE_FIELDS = ['producto', 'descripcion', 'unidad', 'tipo_material', 'tipo_compra', 'codigo', 'ubicacion',
                        'lote', 'status_stock', 'responsable']

    class Meta:
        verbose_name = 'Producto TIC'
        verbose_name_plural = 'Productos TIC'

    def __str__(self):
        return self.producto
