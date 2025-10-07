"""
Configuración de settings basada en variable de entorno.
Por defecto usa development si no se especifica.
"""
import os

# Determinar qué configuración usar
DJANGO_SETTINGS_MODULE = os.environ.get(
    'DJANGO_SETTINGS_MODULE', 
    'config.settings.development'
)

# Importar la configuración apropiada
if 'production' in DJANGO_SETTINGS_MODULE:
    from .production import *
else:
    from .development import *