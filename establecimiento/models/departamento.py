from django.db import models
from simple_history.models import HistoricalRecords

from core.models import StandardModel
from establecimiento.models.establecimiento import Establecimiento


class Departamento(StandardModel):
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Departamento')
    direccion = models.CharField(max_length=100, null=True, blank=True, verbose_name='Dirección')

    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE,
                                        verbose_name='Establecimiento')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

    def __str__(self):
        return f"{self.establecimiento.nombre} - {self.nombre}"
