from django.contrib import admin
from .models import Store


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    """
    Configuración del modelo Store en el admin.
    """
    list_display = [
        'shop_name', 
        'owner', 
        'etsy_shop_id', 
        'is_active', 
        'sync_enabled',
        'last_sync',
        'created_at'
    ]
    list_filter = ['is_active', 'sync_enabled', 'created_at']
    search_fields = ['shop_name', 'etsy_shop_id', 'owner__username', 'owner__email']
    readonly_fields = ['created_at', 'updated_at', 'last_sync']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('owner', 'shop_name', 'etsy_shop_id')
        }),
        ('Tokens OAuth', {
            'fields': ('access_token', 'refresh_token', 'token_expires_at'),
            'classes': ('collapse',),
            'description': '⚠️ Tokens sensibles - manejar con cuidado'
        }),
        ('Configuración de Sincronización', {
            'fields': ('is_active', 'sync_enabled', 'sync_interval', 'last_sync')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimizar queries incluyendo owner"""
        qs = super().get_queryset(request)
        return qs.select_related('owner')