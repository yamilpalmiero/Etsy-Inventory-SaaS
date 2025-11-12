from .base import *
import os
import dj_database_url

DEBUG = False

# Render proporciona RENDER_EXTERNAL_HOSTNAME
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
if 'RENDER' in os.environ:
    ALLOWED_HOSTS.append(os.environ.get('RENDER_EXTERNAL_HOSTNAME'))

# Database - Render proporciona DATABASE_URL
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600
        )
    }

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True

# CSRF
CSRF_TRUSTED_ORIGINS = []
if 'RENDER_EXTERNAL_HOSTNAME' in os.environ:
    CSRF_TRUSTED_ORIGINS.append(
        f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}"
    )