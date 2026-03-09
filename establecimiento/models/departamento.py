from django.db import models
from simple_history.models import HistoricalRecords

from core.models import StandardModel
from establecimiento.models.establecimiento import Establecimiento


class Departamento(StandardModel):
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Departamento')
    alias = models.CharField(max_length=100, verbose_name='Alias del Departamento')
    direccion = models.CharField(max_length=100, null=True, blank=True, verbose_name='Dirección')

    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE,
                                        verbose_name='Establecimiento')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

        constraints = [
            models.UniqueConstraint(
                fields=['nombre', 'establecimiento'],
                name='unique_departamento_por_establecimiento'
            )
        ]

    def __str__(self):
        return f"{self.alias}"

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()

        if self.alias:
            self.alias = self.alias.upper()
        super().save(*args, **kwargs)
