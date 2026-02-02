from django.db import models
from simple_history.models import HistoricalRecords

from core.models import StandardModel


class Establecimiento(StandardModel):
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Establecimiento')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Establecimiento'
        verbose_name_plural = 'Establecimientos'

    def __str__(self):
        return self.name


class Departamento(StandardModel):
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Departamento')
    direccion = models.CharField(max_length=100, verbose_name='Dirección')

    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE, null=True, blank=True,
                                        verbose_name='Establecimiento')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

    def __str__(self):
        return self.nombre


class Funcionario(StandardModel):
    nombres = models.CharField(max_length=200, verbose_name='Nombres')
    rut = models.CharField(max_length=12, verbose_name='RUT')
    correo = models.CharField(max_length=200, verbose_name='Correo Electrónico')

    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True, blank=True,
                                     verbose_name='Departamento')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Funcionario'
        verbose_name_plural = 'Funcionarios'

    def __str__(self):
        return self.nombres


class Jefatura(StandardModel):
    nombre = models.CharField(max_length=300, verbose_name='Nombre de la Jefatura')
    rut = models.CharField(max_length=12, verbose_name='RUT')
    emcorreo = models.EmailField(max_length=100, verbose_name='Correo Electrónico')
    departamentp = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True, blank=True,
                                     verbose_name='Departamento')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Jefatura'
        verbose_name_plural = 'Jefaturas'

    def __str__(self):
        return self.nombre
