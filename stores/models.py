from django.db import models
from django.conf import settings


class Store(models.Model):
    """
    Tienda Etsy conectada a un usuario.
    Almacena tokens OAuth y configuración de sincronización.
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='stores',
        verbose_name='Propietario',
        help_text='Usuario dueño de esta tienda'
    )
    etsy_shop_id = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='ID de Tienda Etsy',
        help_text='ID único de la tienda en Etsy'
    )
    shop_name = models.CharField(
        max_length=255,
        verbose_name='Nombre de Tienda',
        help_text='Nombre de la tienda en Etsy'
    )
    
    # OAuth tokens (se cifrarán en producción)
    access_token = models.TextField(
        verbose_name='Access Token',
        help_text='Token de acceso OAuth de Etsy'
    )
    refresh_token = models.TextField(
        verbose_name='Refresh Token',
        help_text='Token de refresco OAuth de Etsy'
    )
    token_expires_at = models.DateTimeField(
        verbose_name='Expiración del Token',
        help_text='Fecha y hora de expiración del access token'
    )
    
    # Configuración
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activa',
        help_text='Si la tienda está activa para sincronización'
    )
    sync_enabled = models.BooleanField(
        default=True,
        verbose_name='Sincronización Habilitada',
        help_text='Si la sincronización automática está habilitada'
    )
    sync_interval = models.IntegerField(
        default=15,
        verbose_name='Intervalo de Sincronización',
        help_text='Intervalo de sincronización en minutos'
    )
    last_sync = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Última Sincronización',
        help_text='Fecha y hora de la última sincronización exitosa'
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
        verbose_name = 'Tienda'
        verbose_name_plural = 'Tiendas'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.shop_name} ({self.owner.username})"