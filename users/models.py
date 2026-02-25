from django.contrib.auth.models import AbstractUser
from django.db import models
from simple_history.models import HistoricalRecords


class Role(models.Model):
    PERMISSION_CHOICES = [
        (0, 'Sin acceso'),
        (1, 'Solo lectura'),
        (2, 'Lectura y escritura'),
    ]

    role_name = models.CharField(max_length=50, unique=True)
    mantenedores = models.IntegerField(choices=PERMISSION_CHOICES, default=0)
    organizacion = models.IntegerField(choices=PERMISSION_CHOICES, default=0)

    equipos = models.IntegerField(choices=PERMISSION_CHOICES, default=0)

    usuarios = models.IntegerField(choices=PERMISSION_CHOICES, default=0)

    soporte = models.IntegerField(choices=PERMISSION_CHOICES, default=0)

    history = HistoricalRecords()

    class Meta:
        db_table = 'roles'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.role_name


class User(AbstractUser):
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=128)
    establecimiento = models.ForeignKey('establecimiento.Establecimiento', on_delete=models.PROTECT, null=True,
                                        blank=True,
                                        verbose_name='Establecimiento'
                                        )

    rol = models.ForeignKey(Role, on_delete=models.PROTECT, null=True,
                            blank=True,
                            verbose_name='Establecimiento'
                            )

    history = HistoricalRecords()

    USERNAME_FIELD = 'username'

    def save(self, *args, **kwargs):
        if self.username:
            self.username = self.username.upper()

        if self.first_name:
            self.first_name = self.first_name.upper()

        if self.last_name:
            self.last_name = self.last_name.upper()

        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'users'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.username
