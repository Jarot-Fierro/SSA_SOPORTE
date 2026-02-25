from django.db import models
from simple_history.models import HistoricalRecords

from core.models import StandardModel
from establecimiento.models.departamento import Departamento
from establecimiento.models.funcionario import Funcionario
from users.models import User


class Ticket(StandardModel):
    ESTADOS = (
        ('ABIERTO', 'Abierto'),
        ('EN_PROCESO', 'En Proceso'),
        ('ESPERA', 'En Espera'),
        ('CERRADO', 'Cerrado'),
        ('RECHAZADO', 'Rechazado'),
    )

    solicitante = models.ForeignKey(
        Funcionario,
        on_delete=models.CASCADE,
        related_name='tickets_creados'
    )

    asignado_a = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets_asignados'
    )

    estado = models.CharField(max_length=20, choices=ESTADOS, default='ABIERTO')

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()

    fecha_cierre = models.DateTimeField(null=True, blank=True)

    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='departamento'
    )
    funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='funcionario'
    )

    history = HistoricalRecords()

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Ticket #{self.id}"
