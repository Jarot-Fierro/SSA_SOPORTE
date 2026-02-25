from django.db import models
from simple_history.models import HistoricalRecords

from catalogo.models import TipoImpresora, Marca, Modelo, Toner, Contrato, JefeTic, Propietario
from core.models import StandardModel
from establecimiento.models.departamento import Departamento
from establecimiento.models.funcionario import Funcionario


class Impresora(StandardModel):
    serie = models.CharField(max_length=100)
    hh = models.CharField(max_length=30)
    ip = models.CharField(max_length=30)

    tipo = models.ForeignKey(
        TipoImpresora,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    marca = models.ForeignKey(
        Marca,
        on_delete=models.CASCADE
    )
    modelo = models.ForeignKey(
        Modelo,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    toner = models.ForeignKey(
        Toner,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    propietario = models.ForeignKey(
        Propietario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='impresora_propietario'
    )
    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='impresora_departamento'
    )
    jefe_entrega = models.ForeignKey(
        JefeTic,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='impresora_jefetic'
    )
    responsable = models.ForeignKey(
        Funcionario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='impresora_responsable'
    )
    contrato = models.ForeignKey(
        Contrato,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='impresora_contrato'
    )
    de_baja = models.BooleanField(default=False)
    motivo_baja = models.TextField(null=True, blank=True)

    observaciones = models.TextField(null=True, blank=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Impresora'
        verbose_name_plural = 'Impresoras'

    def __str__(self):
        return self.serie
