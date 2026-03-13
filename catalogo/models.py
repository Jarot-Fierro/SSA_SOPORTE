from django.db import models
from simple_history.models import HistoricalRecords

from core.models import StandardModel
from establecimiento.models.departamento import Departamento
from establecimiento.models.establecimiento import Establecimiento


class Marca(StandardModel):
    nombre = models.CharField(max_length=100, verbose_name='Nombre de la Marca')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        super().save(*args, **kwargs)


class Categoria(StandardModel):
    nombre = models.CharField(max_length=100, verbose_name='Nombre de la Categoría')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        super().save(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        super().save(*args, **kwargs)


class Modelo(StandardModel):
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Modelo')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Modelo'
        verbose_name_plural = 'Modelos'

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        super().save(*args, **kwargs)


class Propietario(StandardModel):
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Propietario')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Propietario de Dispositivo'
        verbose_name_plural = 'Propietarios de Dispositivo'

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        super().save(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        super().save(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        super().save(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        super().save(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        super().save(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        super().save(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        super().save(*args, **kwargs)


class Toner(StandardModel):
    nombre = models.CharField(max_length=100)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Tinta'
        verbose_name_plural = 'Tintas'

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        super().save(*args, **kwargs)


class JefeTic(StandardModel):
    nombre = models.CharField(max_length=100)
    posicion = models.CharField(max_length=100, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'JefeTic'
        verbose_name_plural = 'JefesTic'

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()

        if self.posicion:
            self.posicion = self.posicion.upper()
        super().save(*args, **kwargs)


class Contrato(StandardModel):
    nombre = models.CharField(max_length=100)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        super().save(*args, **kwargs)


class TipoSoporte(StandardModel):
    nombre = models.CharField(max_length=100)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Tipo de Soporte'
        verbose_name_plural = 'Tipos de Soportes'

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        super().save(*args, **kwargs)


class PuestoTrabajo(StandardModel):
    nombre = models.CharField(max_length=100)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Puesto de Trabajo'
        verbose_name_plural = 'Puesto de Trabajo'

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        super().save(*args, **kwargs)


class Ips(StandardModel):
    ip = models.GenericIPAddressField(
        unique=True,
        protocol='IPv4',
        verbose_name='Dirección IP'
    )
    asignado = models.BooleanField(default=False)
    establecimiento = models.ForeignKey(
        Establecimiento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ips',
        verbose_name='Establecimiento'
    )
    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ips',
        verbose_name='Departamento'
    )
    observacion = models.TextField(
        null=True,
        blank=True,
        verbose_name='Observación'
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Dirección IP'
        verbose_name_plural = 'Direcciones IP'
        ordering = ['ip']

    def __str__(self):
        return f'{self.ip} ({self.asignado})'
