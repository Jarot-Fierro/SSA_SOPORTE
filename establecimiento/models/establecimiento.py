from django.db import models
from simple_history.models import HistoricalRecords

from core.models import StandardModel
from establecimiento.models.comuna import Comuna


class Establecimiento(StandardModel):
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Establecimiento')
    direccion = models.CharField(max_length=200, null=True, blank=True, verbose_name='Dirección')
    telefono = models.CharField(max_length=15, null=True, blank=True, verbose_name='Teléfono')
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE, verbose_name='Comuna')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Establecimiento'
        verbose_name_plural = 'Establecimientos'

    def __str__(self):
        return self.nombre
