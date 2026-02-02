from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from simple_history.models import HistoricalRecords

from core.models import StandardModel
from establecimiento.models import Funcionario, Jefatura


class Transaccion(StandardModel):
    observacion = models.TextField(
        blank=True, null=True, verbose_name='Observación'
    )

    funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.PROTECT,
        related_name='transacciones',
        verbose_name='Funcionario',
        null=True,
        blank=True
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Transacción'
        verbose_name_plural = 'Transacciones'

    def __str__(self):
        return f"Transacción #{self.id}"


class TransaccionEntrega(StandardModel):
    transaction = models.OneToOneField(
        Transaccion,
        on_delete=models.CASCADE,
        related_name='entrega',
        verbose_name='Transacción'
    )

    entrega_permanente = models.BooleanField(
        default=False,
        verbose_name='¿Entrega Permanente?'
    )

    fecha_devolucion = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de Devolución'
    )

    jefatura = models.ForeignKey(
        Jefatura,
        on_delete=models.PROTECT,
        related_name='entregas',
        verbose_name='Jefatura'
    )

    fecha_carga = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Carga'
    )

    history = HistoricalRecords()

    def clean(self):
        # Si NO es permanente, debe tener fecha de devolución
        if not self.entrega_permanente and not self.fecha_devolucion:
            raise ValidationError(
                "Debe especificar fecha de devolución cuando la entrega no es permanente."
            )

        # Si ES permanente, no debería tener fecha de devolución
        if self.entrega_permanente and self.fecha_devolucion:
            raise ValidationError(
                "Una entrega permanente no debe tener fecha de devolución."
            )

    class Meta:
        verbose_name = 'Entrega de Equipos'
        verbose_name_plural = 'Entregas de Equipos'

    def __str__(self):
        return f"Entrega - Transacción #{self.transaction_id}"


class DetalleTransaccion(StandardModel):
    transaction = models.ForeignKey(
        Transaccion,
        on_delete=models.CASCADE,
        related_name='details',
        verbose_name='Transacción'
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name='Tipo de Contenido'
    )

    object_id = models.UUIDField(
        verbose_name='ID del Objeto'
    )

    device = GenericForeignKey(
        'content_type',
        'object_id'
    )

    amount = models.PositiveIntegerField(
        default=1,
        verbose_name='Cantidad'
    )

    history = HistoricalRecords()

    def clean(self):
        """
        Equipos serializados (IMEI, serie, etc.)
        solo pueden moverse de a 1 unidad.
        """
        if not self.device:
            return

        serial_fields = ('imei', 'serie', 'number_serie')

        if any(hasattr(self.device, field) for field in serial_fields):
            if self.amount != 1:
                raise ValidationError(
                    "Los equipos serializados solo pueden tener cantidad 1."
                )

    class Meta:
        verbose_name = 'Detalle de Transacción'
        verbose_name_plural = 'Detalles de Transacciones'
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self):
        return f"{self.device} x {self.amount}"
