from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Usuario personalizado extendiendo AbstractUser de Django.
    Agrega campos adicionales para el perfil del vendedor.
    """
    email = models.EmailField(
        unique=True,
        verbose_name='Email',
        help_text='Email único del usuario'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Teléfono',
        help_text='Número de teléfono del usuario'
    )
    timezone = models.CharField(
        max_length=50,
        default='UTC',
        verbose_name='Zona Horaria',
        help_text='Zona horaria del usuario para mostrar fechas correctamente'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Actualización'
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-created_at']

    def __str__(self):
        return self.username
