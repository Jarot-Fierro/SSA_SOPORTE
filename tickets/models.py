from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from catalogo.models import TipoSoporte
from core.models import StandardModel
from equipo.models.equipos import Equipo
from establecimiento.models.departamento import Departamento
from establecimiento.models.establecimiento import Establecimiento
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

    numero_ticket = models.CharField(max_length=20, unique=True, blank=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='tickets')
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='tickets')
    asignado_a = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='tickets_asignados')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='ABIERTO')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    area_soporte = models.CharField(choices=[('MANTENCION', 'Mantencion'), ('INFORMATICA', 'Informatica')], null=True,
                                    blank=True)
    tipo_soporte = models.ForeignKey(TipoSoporte, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='tipo_soporte')
    solucion = models.TextField(null=True, blank=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='funcionario')

    history = HistoricalRecords()

    UPPERCASE_FIELDS = ['numero_ticket', ]
    LOWERCASE_FIELDS = ['solucion', ]

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.numero_ticket or f"Ticket #{self.id}"

    def create_number_ticket(self):
        alias_ticket = 'TCK'
        alias = 'TCK'
        year = timezone.now().year

        if self.establecimiento and self.establecimiento.alias:
            alias = self.establecimiento.alias.upper().strip()

        return f"{alias_ticket}-{year}-{alias}-{str(self.id).zfill(5)}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new and not self.numero_ticket:
            # Primer save para obtener ID
            super().save(*args, **kwargs)

            # Generar número usando alias + ID global
            self.numero_ticket = self.create_number_ticket()

            # Segundo save solo para actualizar el número
            super().save(update_fields=['numero_ticket'])
            return

        super().save(*args, **kwargs)


class TicketActivo(StandardModel):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='equipos', null=True, blank=True)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='tickets', null=True, blank=True)
    observacion = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        unique_together = ('ticket', 'equipo')
