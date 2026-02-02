from django.db import models
from simple_history.models import HistoricalRecords

from catalogo.models import Marca, Modelo, LicenceOs, MicrosoftOffice, TipoComputador, \
    TipoCelular, TipoImpresora
from core.models import StandardModel


class Plan(StandardModel):
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Plan')

    gigabytes = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name='Gigas')
    minutos = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name='Minutos')
    mensajes = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name='Mensajes')

    gigabytes_ilimitados = models.BooleanField(default=False, verbose_name='Gigas Ilimitados')
    minutos_ilimitados = models.BooleanField(default=False, verbose_name='Minutos Ilimitados')
    mensajes_ilimitados = models.BooleanField(default=False, verbose_name='Mensajes Ilimitados')

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Plan'
        verbose_name_plural = 'Planes'

    def __str__(self):
        return self.nombre


class Chip(StandardModel):
    numero_telefono = models.CharField(max_length=9, verbose_name='Número de Teléfono')
    sim = models.CharField(max_length=100, null=True, blank=True, verbose_name='Código SIM')
    pin = models.CharField(max_length=50, null=True, blank=True, verbose_name='PIN')
    puk = models.CharField(max_length=50, null=True, blank=True, verbose_name='PUK')

    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Plan Asociado')
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name='Marca')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Chip'
        verbose_name_plural = 'Chips'

    def __str__(self):
        return f"{self.numero_telefono}"


class Celular(StandardModel):
    imei = models.CharField(max_length=30, verbose_name='IMEI')

    asignado = models.BooleanField(default=0, verbose_name='¿Asignado?')

    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, verbose_name='Marca')
    chip = models.ForeignKey(Chip, on_delete=models.SET_NULL, null=True, blank=True, related_name='phones_assigned',
                             verbose_name='Chip Asignado')
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE, verbose_name='Modelo')
    tipo = models.ForeignKey(TipoCelular, on_delete=models.CASCADE, null=True, blank=True,
                             verbose_name='Tipo Equipo')

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Teléfono'
        verbose_name_plural = 'Teléfonos'

    def __str__(self):
        return self.imei


class Computador(StandardModel):
    serie = models.CharField(max_length=100, verbose_name='Número de Serie')
    mac = models.CharField(max_length=30, verbose_name='MAC Address')
    ip = models.CharField(max_length=30, verbose_name='Dirección IP')
    asignado = models.BooleanField(default=0, verbose_name='¿Asignado?')

    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, verbose_name='Marca')
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE, verbose_name='Modelo')
    licencia_os = models.ForeignKey(LicenceOs, on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name='Licencia del SO')
    microsoft_office = models.ForeignKey(MicrosoftOffice, on_delete=models.CASCADE, null=True, blank=True,
                                         verbose_name='Microsoft Office')
    tipo = models.ForeignKey(TipoComputador, on_delete=models.CASCADE, null=True, blank=True,
                             verbose_name='Tipo Equipo')
    history = HistoricalRecords()

    @property
    def universal_id(self):
        return self.id_computer

    class Meta:
        verbose_name = 'Computador'
        verbose_name_plural = 'Computadores'

    def __str__(self):
        return self.number_serie


class Toner(StandardModel):
    name = models.CharField(max_length=100, verbose_name='Nombre del Toner')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Tinta'
        verbose_name_plural = 'Tintas'

    def __str__(self):
        return self.name


class Impresora(StandardModel):
    serie = models.CharField(max_length=100, verbose_name='Número de Serie')
    hh = models.CharField(max_length=30, verbose_name='Hostname / Identificador')
    ip = models.CharField(max_length=30, verbose_name='Dirección IP')

    asignado = models.BooleanField(default=0, verbose_name='¿Asignado?')

    tipo = models.ForeignKey(TipoImpresora, on_delete=models.CASCADE, null=True, blank=True,
                             verbose_name='Tipo Equipo')

    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, verbose_name='Marca')
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE, verbose_name='Modelo')
    toner = models.ForeignKey(Toner, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Tinta Asociada')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Impresora'
        verbose_name_plural = 'Impresoras'

    def __str__(self):
        return self.serie
