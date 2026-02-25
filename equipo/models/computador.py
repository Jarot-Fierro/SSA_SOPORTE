from django.db import models
from simple_history.models import HistoricalRecords

from catalogo.models import Marca, Modelo, TipoComputador, SistemaOperativo, MicrosoftOffice, Propietario, JefeTic, \
    Contrato
from core.models import StandardModel
from establecimiento.models.departamento import Departamento
from establecimiento.models.funcionario import Funcionario


class Computador(StandardModel):
    serie = models.CharField(max_length=100)
    mac = models.CharField(max_length=30, null=True, blank=True)
    ip = models.CharField(max_length=30, null=True, blank=True)

    marca = models.ForeignKey(
        Marca,
        on_delete=models.CASCADE
    )
    modelo = models.ForeignKey(
        Modelo,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    tipo = models.ForeignKey(
        TipoComputador,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    sistema_operativo = models.ForeignKey(
        SistemaOperativo,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    microsoft_office = models.ForeignKey(
        MicrosoftOffice,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    propietario = models.ForeignKey(
        Propietario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='computador_propietario'
    )
    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='computador_departamento'
    )
    jefe_entrega = models.ForeignKey(
        JefeTic,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='computador_jefetic'
    )

    responsable = models.ForeignKey(
        Funcionario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='computador_responsable'
    )
    contrato = models.ForeignKey(
        Contrato,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='computador_contrato'
    )
    de_baja = models.BooleanField(default=False)
    motivo_baja = models.TextField(null=True, blank=True)

    observaciones = models.TextField(null=True, blank=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Computador'
        verbose_name_plural = 'Computadores'

    def __str__(self):
        return self.serie
