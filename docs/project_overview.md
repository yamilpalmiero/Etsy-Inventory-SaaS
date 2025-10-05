# Etsy Inventory SaaS - Visión General del Proyecto

## 🎯 Objetivo del Proyecto

Crear un SaaS basado en Django que sincronice inventario y ventas desde Etsy y permita edición manual por cada vendedor.

## 📚 Stack Tecnológico

### Backend
- **Framework**: Django 5.2.7
- **Lenguaje**: Python 3.11.13
- **Base de datos**: PostgreSQL 16.10
- **Servidor web**: Nginx + Gunicorn
- **Sistema operativo**: Ubuntu 22.04 LTS (WSL en desarrollo)

### Sincronización
- **Método inicial**: Comando de management Django ejecutado vía cron cada 15 minutos
- **Migración futura**: Celery + Redis para tareas asíncronas
- **API**: Etsy API v3 con OAuth 2.0

### Notificaciones
- **Fase 1**: Email (SMTP)
- **Fase 2**: Telegram/WhatsApp

### Deploy
- **Hosting**: VPS (Hetzner/DigitalOcean)
- **Servidor**: Nginx como reverse proxy + Gunicorn
- **HTTPS**: Let's Encrypt (Certbot)
- **Opcional**: Docker + Docker Compose

### Control de Versiones
- **Sistema**: Git
- **Plataforma**: GitHub
- **Branching**: main, develop, feature/*
- **Hooks**: Pre-commit (black, ruff/flake8, isort)

### CI/CD
- **Plataforma**: GitHub Actions
- **Checks**: Linters + Tests en cada PR
- **Deploy**: Automático por push a main (SSH)

### Testing
- **Framework**: pytest-django o Django TestCase
- **Cobertura**: Tests unitarios y de integración

### Gestión de Secretos
- **Desarrollo**: Archivo .env (no versionado)
- **Producción**: Variables de entorno del servidor
- **Librería**: python-decouple o django-environ

## 🏗️ Arquitectura de la Aplicación

### Aplicaciones Django Planeadas

1. **accounts** - Gestión de usuarios y autenticación
2. **stores** - Tiendas Etsy conectadas
3. **products** - Productos e inventario
4. **sales** - Ventas y órdenes
5. **sync** - Lógica de sincronización con Etsy
6. **notifications** - Sistema de notificaciones

### Modelos Principales

#### Store (Tienda)
- Usuario propietario
- Tokens OAuth de Etsy
- ID de tienda en Etsy
- Configuración de sincronización

#### Product (Producto)
- Tienda asociada
- ID de producto en Etsy
- SKU, nombre, descripción
- Stock actual
- Precio
- Última sincronización

#### Sale (Venta)
- Tienda asociada
- ID de orden en Etsy
- Productos vendidos
- Cantidad, precio
- Estado de la orden
- Fecha de venta

#### SyncLog (Log de Sincronización)
- Tienda
- Tipo de sincronización (productos/ventas)
- Timestamp
- Resultado (éxito/error)
- Detalles

## 🔐 Integración con Etsy

### Flujo OAuth 2.0
1. Usuario inicia conexión con Etsy
2. Redirección a Etsy para autorización
3. Etsy devuelve código de autorización
4. Intercambio de código por access token + refresh token
5. Almacenamiento seguro de tokens en BD (cifrados)
6. Uso de tokens para llamadas API

### Endpoints de Etsy a Usar
- `/v3/application/shops/{shop_id}/listings` - Obtener productos
- `/v3/application/shops/{shop_id}/receipts` - Obtener ventas
- `/v3/application/shops/{shop_id}/inventory` - Actualizar inventario

### Gestión de Tokens
- Refresh automático antes de expiración
- Manejo de errores de autenticación
- Re-autorización si es necesario

## 📋 Funcionalidades Core

### MVP (Minimum Viable Product)
- [ ] Registro e inicio de sesión de usuarios
- [ ] Conexión OAuth con Etsy (una tienda por usuario)
- [ ] Sincronización manual de productos
- [ ] Visualización de inventario
- [ ] Edición manual de stock
- [ ] Sincronización manual de ventas
- [ ] Notificación por email de stock bajo
- [ ] Panel básico de administración

### Beta
- [ ] Sincronización automática (cron cada 15 min)
- [ ] Múltiples tiendas por usuario
- [ ] Historial de sincronizaciones
- [ ] Filtros y búsqueda avanzada
- [ ] Exportación a CSV
- [ ] Webhooks de Etsy (si disponibles)
- [ ] Dashboard con métricas básicas

### Producción
- [ ] Migración a Celery + Redis
- [ ] Notificaciones Telegram/WhatsApp
- [ ] Sistema de alertas avanzado
- [ ] API REST para integraciones
- [ ] Roles y permisos (admin, manager, viewer)
- [ ] Auditoría de cambios
- [ ] Backup automático de BD
- [ ] Monitorización con logs centralizados
- [ ] Plan de rollback automático

## 🎓 Filosofía de Desarrollo

### Principios
- **Código limpio**: PEP 8, linters automáticos
- **Testing**: Cobertura mínima 70%
- **Documentación**: README completo, docstrings en funciones
- **Seguridad**: Secrets nunca en código, validación de inputs
- **Escalabilidad**: Pensado para crecer desde el inicio

### Buenas Prácticas
- Commits atómicos con mensajes descriptivos
- Code review (incluso si eres solo tú)
- Branches para cada feature
- Merge a develop, luego a main
- Tags para releases (v1.0.0, v1.1.0, etc.)
- CHANGELOG actualizado

## 📊 Métricas de Éxito

### Técnicas
- Tiempo de respuesta < 200ms (API)
- Uptime > 99.5%
- Sincronización exitosa > 95%
- Cero errores críticos sin resolver

### Negocio
- Usuarios activos mensuales
- Tiendas conectadas
- Productos sincronizados
- Tasa de retención de usuarios

## 🚀 Timeline Estimado (Sin fechas específicas)

### Fase 1: Setup y MVP
- Configuración de entorno ✅
- Modelos y migraciones
- Autenticación básica
- OAuth con Etsy
- Sincronización manual
- Panel básico

### Fase 2: Automatización
- Comando de sincronización
- Configuración de cron
- Tests unitarios
- CI/CD con GitHub Actions
- Deploy a VPS

### Fase 3: Beta
- Celery + Redis
- Webhooks
- Mejoras de UI/UX
- Documentación completa

### Fase 4: Producción
- Optimizaciones de rendimiento
- Monitorización avanzada
- Backups automatizados
- Plan de escalabilidad

## 📞 Recursos y Referencias

### Documentación Oficial
- Django: https://docs.djangoproject.com/
- Etsy API: https://developers.etsy.com/documentation/
- PostgreSQL: https://www.postgresql.org/docs/
- Celery: https://docs.celeryproject.org/

### Registro de Desarrollador Etsy
- Portal: https://www.etsy.com/developers/register
- Documentación OAuth: https://developers.etsy.com/documentation/essentials/authentication

### Herramientas
- GitHub: https://github.com
- Hetzner: https://www.hetzner.com
- DigitalOcean: https://www.digitalocean.com
- Let's Encrypt: https://letsencrypt.org/