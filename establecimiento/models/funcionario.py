from django.db import models
from simple_history.models import HistoricalRecords

from catalogo.models import PuestoTrabajo
from core.models import StandardModel
from establecimiento.models.departamento import Departamento


class Funcionario(StandardModel):
    nombres = models.CharField(max_length=200, verbose_name='Nombres')
    rut = models.CharField(max_length=12, verbose_name='RUT')
    correo = models.CharField(max_length=200, null=True, blank=True, verbose_name='Correo Electrónico')
    jefatura = models.BooleanField(default=0, verbose_name='¿Es Jefatura?')

    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True, blank=True,
                                     verbose_name='Departamento')
    puesto_trabajo = models.ForeignKey(PuestoTrabajo, on_delete=models.CASCADE, null=True, blank=True,
                                       verbose_name='Puesto de Trabajo')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Funcionario'
        verbose_name_plural = 'Funcionarios'

    def __str__(self):
        return self.nombres

    def save(self, *args, **kwargs):
        if self.nombres:
            self.nombres = self.nombres.upper()

        if self.rut:
            self.rut = self.rut.upper()

        if self.correo:
            self.correo = self.correo.lower()
        super().save(*args, **kwargs)
