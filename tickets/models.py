from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from catalogo.models import TipoSoporte
from core.models import StandardModel
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

    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets'
    )
    establecimiento = models.ForeignKey(
        Establecimiento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets'
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

    area_soporte = models.CharField(
        choices=[('MANTENCION', 'Mantencion'), ('INFORMATICA', 'Informatica')],
        null=True,
        blank=True,
    )

    tipo_soporte = models.ForeignKey(
        TipoSoporte,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tipo_soporte'
    )

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
    ticket = models.ForeignKey(
        'tickets.Ticket',
        on_delete=models.CASCADE,
        related_name='activos_relacionados'
    )

    # Relación genérica al activo (Computador / Impresora / Celular)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    activo = GenericForeignKey('content_type', 'object_id')

    observacion = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Activo relacionado'
        verbose_name_plural = 'Activos relacionados'
        unique_together = ('ticket', 'content_type', 'object_id')

    def __str__(self):
        return f"{self.ticket.numero_ticket} - {self.activo}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            # Al asignar equipo al ticket, marcamos como asignado y ponemos el funcionario del ticket como responsable
            activo = self.activo
            if activo:
                activo.asignado = True
                activo.responsable = self.ticket.funcionario
                activo.save()

    def delete(self, *args, **kwargs):
        # Al quitar el equipo del ticket, marcamos como no asignado y quitamos el responsable
        activo = self.activo
        if activo:
            activo.asignado = False
            activo.responsable = None
            activo.save()
        super().delete(*args, **kwargs)
