from django.db import models


class Product(models.Model):
    """
    Producto sincronizado desde Etsy.
    Incluye información de inventario y precios.
    """
    store = models.ForeignKey(
        'stores.Store',
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Tienda',
        help_text='Tienda a la que pertenece este producto'
    )
    etsy_listing_id = models.CharField(
        max_length=100,
        verbose_name='ID de Listing Etsy',
        help_text='ID único del listing en Etsy'
    )
    
    # Información del producto
    sku = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='SKU',
        help_text='Código SKU del producto'
    )
    title = models.CharField(
        max_length=500,
        verbose_name='Título',
        help_text='Título del producto'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Descripción',
        help_text='Descripción del producto'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Precio',
        help_text='Precio del producto'
    )
    currency = models.CharField(
        max_length=3,
        default='USD',
        verbose_name='Moneda',
        help_text='Código de moneda (USD, EUR, etc.)'
    )
    
    # Inventario
    quantity = models.IntegerField(
        default=0,
        verbose_name='Cantidad',
        help_text='Cantidad disponible en inventario'
    )
    low_stock_threshold = models.IntegerField(
        default=5,
        verbose_name='Umbral de Stock Bajo',
        help_text='Cantidad mínima antes de alertar stock bajo'
    )
    
    # Estado
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Si el producto está activo en Etsy'
    )
    last_synced = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Sincronización',
        help_text='Fecha y hora de última sincronización'
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
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-created_at']
        unique_together = ['store', 'etsy_listing_id']

    def __str__(self):
        return f"{self.title} ({self.store.shop_name})"