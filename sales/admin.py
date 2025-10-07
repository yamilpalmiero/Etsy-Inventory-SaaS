from django.contrib import admin
from .models import Sale, SaleItem


class SaleItemInline(admin.TabularInline):
    """
    Inline para mostrar items dentro de una venta.
    """
    model = SaleItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'unit_price', 'total_price']
    can_delete = False


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    """
    Configuración del modelo Sale en el admin.
    """
    list_display = [
        'etsy_receipt_id',
        'store',
        'buyer_name',
        'buyer_email',
        'total_amount',
        'currency',
        'status',
        'sale_date'
    ]
    list_filter = ['status', 'currency', 'store', 'sale_date', 'created_at']
    search_fields = [
        'etsy_receipt_id', 
        'buyer_name', 
        'buyer_email',
        'store__shop_name'
    ]
    readonly_fields = [
        'etsy_receipt_id',
        'buyer_name',
        'buyer_email',
        'total_amount',
        'currency',
        'sale_date',
        'created_at',
        'updated_at'
    ]
    
    fieldsets = (
        ('Información de la Venta', {
            'fields': ('store', 'etsy_receipt_id', 'sale_date')
        }),
        ('Comprador', {
            'fields': ('buyer_name', 'buyer_email')
        }),
        ('Montos', {
            'fields': ('total_amount', 'currency')
        }),
        ('Estado', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [SaleItemInline]
    
    def get_queryset(self, request):
        """Optimizar queries incluyendo store"""
        qs = super().get_queryset(request)
        return qs.select_related('store', 'store__owner')


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    """
    Configuración del modelo SaleItem en el admin.
    """
    list_display = [
        'sale',
        'product',
        'quantity',
        'unit_price',
        'total_price'
    ]
    list_filter = ['sale__store', 'sale__sale_date']
    search_fields = [
        'sale__etsy_receipt_id',
        'product__title',
        'sale__buyer_name'
    ]
    readonly_fields = ['sale', 'product', 'quantity', 'unit_price', 'total_price']
    
    def get_queryset(self, request):
        """Optimizar queries incluyendo relaciones"""
        qs = super().get_queryset(request)
        return qs.select_related('sale', 'sale__store', 'product')