# from django.db import models
# from simple_history.models import HistoricalRecords
#
# from catalogo.models import (
#     Marca,
#     Modelo,
#     TipoComputador,
#     TipoImpresora,
#     SistemaOperativo,
#     MicrosoftOffice,
#     Toner,
#     Propietario,
#     JefeTic,
#     Contrato,
#     Ips
# )
# from core.models import StandardModel
# from establecimiento.models.departamento import Departamento
# from establecimiento.models.establecimiento import Establecimiento
# from establecimiento.models.funcionario import Funcionario
#
#
# class Equipo(StandardModel):
#     """
#     Modelo único para todos los activos TI.
#     Escalable para futuros dispositivos.
#     """
#
#     TIPO_EQUIPO = (
#         ('PC', 'Computador'),
#         ('IMP', 'Impresora'),
#         ('NB', 'Notebook'),
#         ('ROU', 'Router'),
#         ('SW', 'Switch'),
#         ('SCAN', 'Scanner'),
#         ('OTRO', 'Otro'),
#     )
#
#     # =========================
#     # IDENTIFICACIÓN GENERAL
#     # =========================
#     tipo_equipo = models.CharField(
#         max_length=10,
#         choices=TIPO_EQUIPO
#     )
#
#     serie = models.CharField(
#         max_length=100,
#         unique=True
#     )
#
#     ip = models.OneToOneField(
#         Ips,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name='equipo'
#     )
#
#     marca = models.ForeignKey(
#         Marca,
#         on_delete=models.CASCADE
#     )
#
#     modelo = models.ForeignKey(
#         Modelo,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )
#
#     # =========================
#     # UBICACIÓN / RESPONSABLE
#     # =========================
#     propietario = models.ForeignKey(
#         Propietario,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )
#
#     departamento = models.ForeignKey(
#         Departamento,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )
#
#     establecimiento = models.ForeignKey(
#         Establecimiento,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )
#
#     responsable = models.ForeignKey(
#         Funcionario,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )
#
#     jefe_entrega = models.ForeignKey(
#         JefeTic,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )
#
#     contrato = models.ForeignKey(
#         Contrato,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )
#
#     # =========================
#     # CAMPOS PC / NOTEBOOK
#     # =========================
#     tipo_pc = models.ForeignKey(
#         TipoComputador,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )
#
#     mac = models.CharField(
#         max_length=30,
#         null=True,
#         blank=True
#     )
#
#     sistema_operativo = models.ForeignKey(
#         SistemaOperativo,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )
#
#     microsoft_office = models.ForeignKey(
#         MicrosoftOffice,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )
#     # PC ARMADO
#     es_armado = models.BooleanField(default=False)
#
#     ram_gb = models.IntegerField(null=True, blank=True)
#     wifi = models.BooleanField(default=False)
#     procesador = models.BooleanField(default=False)
#     tarjeta_video = models.BooleanField(default=False)
#     red_lan = models.BooleanField(default=True)
#
#     tipo_disco = models.CharField(
#         max_length=20,
#         choices=[
#             ('SSD', 'SSD'),
#             ('HDD', 'Mecánico'),
#             ('NVME', 'NVMe')
#         ],
#         null=True,
#         blank=True
#     )
#
#     capacidad_disco_gb = models.IntegerField(null=True, blank=True)
#
#     # =========================
#     # CAMPOS IMPRESORA
#     # =========================
#     tipo_impresora = models.ForeignKey(
#         TipoImpresora,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )
#
#     hh = models.CharField(
#         max_length=30,
#         null=True,
#         blank=True
#     )
#
#     toner = models.ForeignKey(
#         Toner,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )
#
#     # =========================
#     # ESTADO GENERAL
#     # =========================
#     de_baja = models.BooleanField(default=False)
#
#     motivo_baja = models.TextField(
#         null=True,
#         blank=True
#     )
#
#     observaciones = models.TextField(
#         null=True,
#         blank=True
#     )
#
#     history = HistoricalRecords()
#
#     UPPERCASE_FIELDS = [
#         'serie',
#         'mac',
#         'hh',
#         'motivo_baja',
#         'observaciones'
#     ]
#
#     # =========================
#     # PROPIEDADES
#     # =========================
#     @property
#     def asignado_ticket(self):
#         return self.activos_relacionados.exists()
#
#     @property
#     def tiene_ip(self):
#         return self.ip is not None
#
#     @property
#     def es_computador(self):
#         return self.tipo_equipo == 'PC'
#
#     @property
#     def es_impresora(self):
#         return self.tipo_equipo == 'IMP'
#
#     # =========================
#     # VALIDACIONES
#     # =========================
#     def clean(self):
#         from django.core.exceptions import ValidationError
#
#         # Computador requiere campos PC
#         if self.tipo_equipo == 'PC':
#             if not self.tipo_pc:
#                 raise ValidationError("Debe seleccionar tipo computador.")
#
#         # Impresora requiere campos impresora
#         if self.tipo_equipo == 'IMP':
#             if not self.tipo_impresora:
#                 raise ValidationError("Debe seleccionar tipo impresora.")
#
#     # =========================
#     # META
#     # =========================
#     class Meta:
#         verbose_name = 'Equipo'
#         verbose_name_plural = 'Equipos'
#         ordering = ['serie']
#
#     def __str__(self):
#         return f'{self.get_tipo_equipo_display()} - {self.serie}'
#
#
# from django.db import models
# from simple_history.models import HistoricalRecords
#
# from catalogo.models import Ips
# from core.models import StandardModel
# from inventario.models import Equipo
#
#
# class AsignacionIP(StandardModel):
#     """
#     Tabla intermedia entre IP y Equipo.
#
#     Reglas:
#     - Una IP solo puede estar asignada a un equipo.
#     - Un equipo solo puede tener una IP.
#     - Historial de asignación posible.
#     """
#
#     ip = models.OneToOneField(
#         Ips,
#         on_delete=models.CASCADE,
#         related_name='asignacion_ip',
#         verbose_name='Dirección IP'
#     )
#
#     equipo = models.OneToOneField(
#         Equipo,
#         on_delete=models.CASCADE,
#         related_name='asignacion_ip',
#         verbose_name='Equipo'
#     )
#
#     activa = models.BooleanField(
#         default=True,
#         verbose_name='Asignación activa'
#     )
#
#     fecha_asignacion = models.DateTimeField(
#         auto_now_add=True
#     )
#
#     fecha_liberacion = models.DateTimeField(
#         null=True,
#         blank=True
#     )
#
#     observacion = models.TextField(
#         null=True,
#         blank=True
#     )
#
#     history = HistoricalRecords()
#
#     UPPERCASE_FIELDS = ['observacion']
#
#     class Meta:
#         verbose_name = 'Asignación IP'
#         verbose_name_plural = 'Asignaciones IP'
#         ordering = ['-fecha_asignacion']
#
#     def __str__(self):
#         estado = "ACTIVA" if self.activa else "LIBERADA"
#         return f'{self.ip.ip} → {self.equipo} ({estado})'
#
#
# class TicketActivo(StandardModel):
#     ticket = models.ForeignKey(
#         Ticket,
#         on_delete=models.CASCADE,
#         related_name='equipos'
#     )
#
#     equipo = models.ForeignKey(
#         Equipo,
#         on_delete=models.CASCADE,
#         related_name='tickets'
#     )
#
#     observacion = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True
#     )
#
#     class Meta:
#         unique_together = ('ticket', 'equipo')
