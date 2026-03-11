from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from core.models import StandardModel
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
    numero_ticket = models.CharField(max_length=20, unique=True)

    departamento = models.CharField(max_length=20, default='NO INFORMADO')

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
    solucion = models.TextField(null=True, blank=True)

    fecha_cierre = models.DateTimeField(null=True, blank=True)

    funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='funcionario'
    )

    history = HistoricalRecords()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"Ticket #{self.id}"

    def create_number_ticket(self):
        year = timezone.now().year

        ultimo_ticket = Ticket.objects.filter(
            numero_ticket__startswith=f"TCK-{year}"
        ).order_by('-numero_ticket').first()

        if ultimo_ticket:
            ultimo_num = int(ultimo_ticket.numero_ticket.split('-')[-1])
            nuevo_num = ultimo_num + 1
        else:
            nuevo_num = 1

        return f"TCK-{year}-{str(nuevo_num).zfill(5)}"

    def save(self, *args, **kwargs):

        if not self.numero_ticket:
            self.numero_ticket = self.create_number_ticket()

        super().save(*args, **kwargs)
