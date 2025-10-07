from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Configuración del modelo Product en el admin.
    """
    list_display = [
        'title',
        'store',
        'sku',
        'price',
        'currency',
        'quantity',
        'low_stock_threshold',
        'is_active',
        'last_synced'
    ]
    list_filter = ['is_active', 'currency', 'store', 'created_at']
    search_fields = ['title', 'sku', 'etsy_listing_id', 'store__shop_name']
    readonly_fields = ['etsy_listing_id', 'last_synced', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('store', 'etsy_listing_id', 'title', 'description')
        }),
        ('Precios', {
            'fields': ('price', 'currency', 'sku')
        }),
        ('Inventario', {
            'fields': ('quantity', 'low_stock_threshold')
        }),
        ('Estado', {
            'fields': ('is_active', 'last_synced')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimizar queries incluyendo store"""
        qs = super().get_queryset(request)
        return qs.select_related('store', 'store__owner')