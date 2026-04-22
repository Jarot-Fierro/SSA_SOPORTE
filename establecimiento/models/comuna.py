from django.db import models
from simple_history.models import HistoricalRecords

from core.models import StandardModel


class Comuna(StandardModel):
    nombre = models.CharField(max_length=100, unique=True, null=False, verbose_name='Nombre')
    history = HistoricalRecords()

    def __str__(self):
        return self.nombre

    UPPERCASE_FIELDS = ['nombre', ]

    class Meta:
        verbose_name = 'Comuna'
        verbose_name_plural = 'Comunas'
