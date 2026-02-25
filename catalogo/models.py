from django.db import models
from simple_history.models import HistoricalRecords

from core.models import StandardModel


class Marca(StandardModel):
    nombre = models.CharField(max_length=100, verbose_name='Nombre de la Marca')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'

    def __str__(self):
        return self.nombre


class Categoria(StandardModel):
    nombre = models.CharField(max_length=100, verbose_name='Nombre de la Categoría')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre


class SubCategoria(StandardModel):
    nombre = models.CharField(max_length=100, verbose_name='Nombre de la Subcategoría')
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        verbose_name='Categoría'
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Subcategoría'
        verbose_name_plural = 'Subcategorías'

    def __str__(self):
        return self.nombre


class Modelo(StandardModel):
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Modelo')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Modelo'
        verbose_name_plural = 'Modelos'

    def __str__(self):
        return self.nombre


class Propietario(StandardModel):
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Propietario')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Propietario de Dispositivo'
        verbose_name_plural = 'Propietarios de Dispositivo'

    def __str__(self):
        return self.nombre


class LicenciaOs(StandardModel):
    nombre = models.CharField(
        max_length=100, verbose_name="Nombre de la Licencia de SO"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Licencia de Sistema Operativo"
        verbose_name_plural = "Licencias de Sistema Operativo"

    def __str__(self):
        return self.nombre


class MicrosoftOffice(StandardModel):
    nombre = models.CharField(
        max_length=100, verbose_name="Nombre de la Licencia de Microsoft Office"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Licencia de Microsoft Office"
        verbose_name_plural = "Licencias de Microsoft Office"

    def __str__(self):
        return self.nombre


class SistemaOperativo(StandardModel):
    nombre = models.CharField(
        max_length=100, verbose_name="Nombre del Sistema Operativo"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Sistema Operativo"
        verbose_name_plural = "Sistemas Operativos"

    def __str__(self):
        return self.nombre


class TipoCelular(StandardModel):
    nombre = models.CharField(
        max_length=100, verbose_name="Nombre del tipo plan"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Tipo Celular"
        verbose_name_plural = "Tipos Celular"

    def __str__(self):
        return self.nombre


class TipoComputador(StandardModel):
    nombre = models.CharField(
        max_length=100, verbose_name="Nombre del tipo computador"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Tipo Computador"
        verbose_name_plural = "Tipos Computador"

    def __str__(self):
        return self.nombre


class TipoImpresora(StandardModel):
    nombre = models.CharField(
        max_length=100, verbose_name="Nombre del tipo impresora"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Tipo Impresora"
        verbose_name_plural = "Tipos Impresoras"

    def __str__(self):
        return self.nombre


class Toner(StandardModel):
    nombre = models.CharField(max_length=100)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Tinta'
        verbose_name_plural = 'Tintas'

    def __str__(self):
        return self.nombre


class JefeTic(StandardModel):
    nombre = models.CharField(max_length=100)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'JefeTic'
        verbose_name_plural = 'JefesTic'

    def __str__(self):
        return self.nombre


class Contrato(StandardModel):
    nombre = models.CharField(max_length=100)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'

    def __str__(self):
        return self.nombre


class TipoSoporte(StandardModel):
    nombre = models.CharField(max_length=100)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Tipo de Soporte'
        verbose_name_plural = 'Tipos de Soportes'

    def __str__(self):
        return self.nombre
