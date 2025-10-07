from django.db import models


class Sale(models.Model):
    """
    Venta/Orden sincronizada desde Etsy.
    Representa un recibo (receipt) de Etsy.
    """
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('processing', 'Procesando'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada'),
    ]
    
    store = models.ForeignKey(
        'stores.Store',
        on_delete=models.CASCADE,
        related_name='sales',
        verbose_name='Tienda',
        help_text='Tienda donde se realizó la venta'
    )
    etsy_receipt_id = models.CharField(
        max_length=100,
        verbose_name='ID de Recibo Etsy',
        help_text='ID único del recibo en Etsy'
    )
    
    # Información de la venta
    buyer_name = models.CharField(
        max_length=255,
        verbose_name='Nombre del Comprador',
        help_text='Nombre del comprador'
    )
    buyer_email = models.EmailField(
        verbose_name='Email del Comprador',
        help_text='Email del comprador'
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Monto Total',
        help_text='Monto total de la venta'
    )
    currency = models.CharField(
        max_length=3,
        default='USD',
        verbose_name='Moneda',
        help_text='Código de moneda (USD, EUR, etc.)'
    )
    
    # Estado
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Estado',
        help_text='Estado actual de la orden'
    )
    sale_date = models.DateTimeField(
        verbose_name='Fecha de Venta',
        help_text='Fecha y hora en que se realizó la venta'
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
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['-sale_date']
        unique_together = ['store', 'etsy_receipt_id']

    def __str__(self):
        return f"Venta #{self.etsy_receipt_id} - {self.buyer_name}"


class SaleItem(models.Model):
    """
    Ítem individual dentro de una venta.
    Representa los productos específicos vendidos en una orden.
    """
    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Venta',
        help_text='Venta a la que pertenece este ítem'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Producto',
        help_text='Producto vendido (puede ser null si se eliminó)'
    )
    
    quantity = models.IntegerField(
        verbose_name='Cantidad',
        help_text='Cantidad de unidades vendidas'
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Precio Unitario',
        help_text='Precio por unidad'
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Precio Total',
        help_text='Precio total del ítem (cantidad * precio unitario)'
    )

    class Meta:
        verbose_name = 'Ítem de Venta'
        verbose_name_plural = 'Ítems de Venta'

    def __str__(self):
        product_name = self.product.title if self.product else "Producto eliminado"
        return f"{self.quantity}x {product_name}"