# Roadmap Detallado - Próximos Pasos

## 🎯 FASE 1: MVP (Minimum Viable Product)

### Milestone 1.1: Estructura de Aplicaciones Django

**Objetivo**: Crear las apps necesarias y definir modelos base

#### Tareas
- [ ] Crear app `accounts` (gestión de usuarios)
  ```bash
  python manage.py startapp accounts
  ```
- [ ] Crear app `stores` (tiendas Etsy)
  ```bash
  python manage.py startapp stores
  ```
- [ ] Crear app `products` (productos e inventario)
  ```bash
  python manage.py startapp products
  ```
- [ ] Crear app `sales` (ventas y órdenes)
  ```bash
  python manage.py startapp sales
  ```
- [ ] Registrar apps en `config/settings.py` → `INSTALLED_APPS`
- [ ] Commit: `git commit -m "feat: create django apps structure"`

**Entregables**:
- 4 apps Django creadas
- Apps registradas en settings
- Estructura de carpetas organizada

---

### Milestone 1.2: Modelos de Base de Datos

**Objetivo**: Definir modelos principales y relaciones

#### Modelo: User (accounts/models.py)
```python
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### Modelo: Store (stores/models.py)
```python
class Store(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stores')
    etsy_shop_id = models.CharField(max_length=100, unique=True)
    shop_name = models.CharField(max_length=255)
    
    # OAuth tokens (cifrados en producción)
    access_token = models.TextField()
    refresh_token = models.TextField()
    token_expires_at = models.DateTimeField()
    
    # Configuración
    is_active = models.BooleanField(default=True)
    sync_enabled = models.BooleanField(default=True)
    sync_interval = models.IntegerField(default=15)  # minutos
    last_sync = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### Modelo: Product (products/models.py)
```python
class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    etsy_listing_id = models.CharField(max_length=100)
    
    # Información del producto
    sku = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    # Inventario
    quantity = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=5)
    
    # Estado
    is_active = models.BooleanField(default=True)
    last_synced = models.DateTimeField(auto_now=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['store', 'etsy_listing_id']
```

#### Modelo: Sale (sales/models.py)
```python
class Sale(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('processing', 'Procesando'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada'),
    ]
    
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='sales')
    etsy_receipt_id = models.CharField(max_length=100)
    
    # Información de la venta
    buyer_name = models.CharField(max_length=255)
    buyer_email = models.EmailField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    # Estado
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    sale_date = models.DateTimeField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['store', 'etsy_receipt_id']

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
```

#### Tareas de Modelos
- [ ] Crear modelos en cada app
- [ ] Configurar User personalizado en settings: `AUTH_USER_MODEL = 'accounts.User'`
- [ ] Crear migraciones: `python manage.py makemigrations`
- [ ] Aplicar migraciones: `python manage.py migrate`
- [ ] Registrar modelos en admin.py de cada app
- [ ] Commit: `git commit -m "feat: add database models"`

**Entregables**:
- 5 modelos principales creados
- Migraciones aplicadas
- Modelos registrados en admin

---

### Milestone 1.3: Configuración Modular de Settings

**Objetivo**: Separar configuración en base/dev/prod

#### Estructura
```
config/
├── settings/
│   ├── __init__.py
│   ├── base.py          # Configuración común
│   ├── development.py   # Desarrollo local
│   └── production.py    # Producción
├── urls.py
├── wsgi.py
└── asgi.py
```

#### Archivos

**base.py** (configuración común)
- Imports y PATH
- SECRET_KEY desde .env
- INSTALLED_APPS
- MIDDLEWARE
- TEMPLATES
- DATABASES base (PostgreSQL)
- AUTH_PASSWORD_VALIDATORS
- Internacionalización
- STATIC/MEDIA configuración

**development.py**
```python
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Email backend de consola (imprime en terminal)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Django Debug Toolbar (instalar: pip install django-debug-toolbar)
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']
```

**production.py**
```python
from .base import *

DEBUG = False
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Seguridad
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True

# Email real
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
```

#### Tareas
- [ ] Crear carpeta `config/settings/`
- [ ] Mover contenido de `settings.py` a `base.py`
- [ ] Crear `development.py` y `production.py`
- [ ] Modificar `manage.py` para usar settings de desarrollo
- [ ] Actualizar `.env` con variable `DJANGO_SETTINGS_MODULE`
- [ ] Commit: `git commit -m "refactor: modular settings structure"`

**Entregables**:
- Settings organizados en 3 archivos
- Configuración específica para dev/prod
- manage.py actualizado

---

### Milestone 1.4: Sistema de Autenticación

**Objetivo**: Login, registro y gestión de usuarios

#### Tareas
- [ ] Crear vistas de registro (`accounts/views.py`)
- [ ] Crear vistas de login/logout
- [ ] Crear templates (login.html, register.html, dashboard.html)
- [ ] Configurar URLs de autenticación
- [ ] Agregar formularios personalizados (`accounts/forms.py`)
- [ ] Agregar validación de email
- [ ] Crear tests básicos de autenticación
- [ ] Commit: `git commit -m "feat: user authentication system"`

**Entregables**:
- Sistema completo de registro/login
- Templates básicos funcionales
- Tests de autenticación

---

### Milestone 1.5: Integración OAuth con Etsy

**Objetivo**: Permitir a usuarios conectar sus tiendas Etsy

#### Pre-requisitos
- [ ] Crear cuenta en Etsy Developer Portal
- [ ] Crear aplicación en Etsy
- [ ] Obtener Client ID y Client Secret
- [ ] Configurar Redirect URI
- [ ] Agregar credenciales a `.env`

#### Flujo OAuth - Archivos Necesarios

**stores/views.py**
```python
from django.shortcuts import redirect
from decouple import config
import requests

def etsy_auth_init(request):
    """Inicia proceso OAuth con Etsy"""
    client_id = config('ETSY_CLIENT_ID')
    redirect_uri = config('ETSY_REDIRECT_URI')
    scope = 'listings_r transactions_r'
    
    auth_url = f"https://www.etsy.com/oauth/connect?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"
    
    return redirect(auth_url)

def etsy_auth_callback(request):
    """Recibe callback de Etsy y obtiene tokens"""
    code = request.GET.get('code')
    
    # Intercambiar code por access token
    token_url = "https://api.etsy.com/v3/public/oauth/token"
    data = {
        'grant_type': 'authorization_code',
        'client_id': config('ETSY_CLIENT_ID'),
        'code': code,
        'redirect_uri': config('ETSY_REDIRECT_URI'),
        'code_verifier': request.session.get('code_verifier')  # Implementar PKCE
    }
    
    response = requests.post(token_url, data=data)
    tokens = response.json()
    
    # Guardar tokens en BD (Store model)
    # ... lógica de guardado
    
    return redirect('dashboard')
```

**stores/utils.py** (manejo de tokens)
```python
from datetime import datetime, timedelta
import requests
from decouple import config

def refresh_etsy_token(store):
    """Refresca el access token de Etsy"""
    token_url = "https://api.etsy.com/v3/public/oauth/token"
    data = {
        'grant_type': 'refresh_token',
        'client_id': config('ETSY_CLIENT_ID'),
        'refresh_token': store.refresh_token
    }
    
    response = requests.post(token_url, data=data)
    tokens = response.json()
    
    store.access_token = tokens['access_token']
    store.refresh_token = tokens['refresh_token']
    store.token_expires_at = datetime.now() + timedelta(seconds=tokens['expires_in'])
    store.save()
    
    return store

def get_valid_token(store):
    """Obtiene un token válido, refrescando si es necesario"""
    if store.token_expires_at <= datetime.now():
        store = refresh_etsy_token(store)
    return store.access_token
```

#### Tareas
- [ ] Implementar vistas de OAuth (init y callback)
- [ ] Implementar PKCE (Proof Key for Code Exchange) para seguridad
- [ ] Crear utilidades de manejo de tokens
- [ ] Agregar cifrado de tokens en BD (usar `cryptography` library)
- [ ] Crear vista para listar tiendas conectadas
- [ ] Crear vista para desconectar tienda
- [ ] Agregar URLs de OAuth
- [ ] Tests de flujo OAuth
- [ ] Commit: `git commit -m "feat: Etsy OAuth integration"`

**Entregables**:
- Flujo OAuth completo y funcional
- Tokens almacenados de forma segura
- Refresh automático de tokens

---

### Milestone 1.6: Comando de Sincronización Manual

**Objetivo**: Crear comando Django para sincronizar datos de Etsy

#### Estructura
```
stores/management/
└── commands/
    ├── __init__.py
    └── sync_etsy.py
```

#### Comando sync_etsy.py
```python
from django.core.management.base import BaseCommand
from stores.models import Store
from products.models import Product
from sales.models import Sale, SaleItem
import requests
from stores.utils import get_valid_token

class Command(BaseCommand):
    help = 'Sincroniza productos y ventas desde Etsy'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--store-id',
            type=int,
            help='ID de tienda específica a sincronizar',
        )
        parser.add_argument(
            '--products-only',
            action='store_true',
            help='Solo sincronizar productos',
        )
        parser.add_argument(
            '--sales-only',
            action='store_true',
            help='Solo sincronizar ventas',
        )
    
    def handle(self, *args, **options):
        stores = Store.objects.filter(sync_enabled=True, is_active=True)
        
        if options['store_id']:
            stores = stores.filter(id=options['store_id'])
        
        for store in stores:
            self.stdout.write(f"Sincronizando tienda: {store.shop_name}")
            
            if not options['sales_only']:
                self.sync_products(store)
            
            if not options['products_only']:
                self.sync_sales(store)
            
            store.last_sync = timezone.now()
            store.save()
    
    def sync_products(self, store):
        """Sincroniza productos de Etsy"""
        token = get_valid_token(store)
        headers = {'Authorization': f'Bearer {token}'}
        
        url = f"https://openapi.etsy.com/v3/application/shops/{store.etsy_shop_id}/listings"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            listings = response.json()['results']
            
            for listing in listings:
                Product.objects.update_or_create(
                    store=store,
                    etsy_listing_id=listing['listing_id'],
                    defaults={
                        'title': listing['title'],
                        'description': listing['description'],
                        'price': listing['price']['amount'],
                        'currency': listing['price']['currency_code'],
                        'quantity': listing['quantity'],
                        'is_active': listing['state'] == 'active',
                    }
                )
            
            self.stdout.write(self.style.SUCCESS(f"✓ {len(listings)} productos sincronizados"))
        else:
            self.stdout.write(self.style.ERROR(f"✗ Error: {response.status_code}"))
    
    def sync_sales(self, store):
        """Sincroniza ventas de Etsy"""
        # Implementación similar para sales
        pass
```

#### Tareas
- [ ] Crear estructura de management commands
- [ ] Implementar `sync_etsy.py` completo
- [ ] Implementar sincronización de productos
- [ ] Implementar sincronización de ventas
- [ ] Agregar logging detallado
- [ ] Agregar manejo de errores y reintentos
- [ ] Crear modelo SyncLog para historial
- [ ] Tests del comando
- [ ] Commit: `git commit -m "feat: Etsy sync management command"`

**Uso del comando**:
```bash
# Sincronizar todas las tiendas
python manage.py sync_etsy

# Sincronizar tienda específica
python manage.py sync_etsy --store-id=1

# Solo productos
python manage.py sync_etsy --products-only

# Solo ventas
python manage.py sync_etsy --sales-only
```

**Entregables**:
- Comando de sincronización funcional
- Sincronización de productos
- Sincronización de ventas
- Logging y manejo de errores

---

### Milestone 1.7: Vistas y Templates Básicos

**Objetivo**: Interfaz para ver y editar inventario

#### Estructura de Templates
```
templates/
├── base.html
├── accounts/
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
├── stores/
│   ├── store_list.html
│   ├── store_connect.html
│   └── store_detail.html
├── products/
│   ├── product_list.html
│   ├── product_detail.html
│   └── product_edit.html
└── sales/
    ├── sale_list.html
    └── sale_detail.html
```

#### Vistas Principales

**products/views.py**
```python
from django.views.generic import ListView, DetailView, UpdateView
from .models import Product

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 20
    
    def get_queryset(self):
        # Filtrar por tiendas del usuario
        return Product.objects.filter(
            store__owner=self.request.user
        ).select_related('store')

class ProductUpdateView(UpdateView):
    model = Product
    fields = ['quantity', 'price', 'low_stock_threshold']
    template_name = 'products/product_edit.html'
    
    def get_queryset(self):
        return Product.objects.filter(store__owner=self.request.user)
```

#### Tareas
- [ ] Crear template base con navbar
- [ ] Implementar vistas de listado (productos, ventas)
- [ ] Implementar vistas de detalle
- [ ] Implementar vistas de edición
- [ ] Agregar paginación
- [ ] Agregar filtros y búsqueda
- [ ] Agregar CSS básico (Bootstrap o Tailwind)
- [ ] Tests de vistas
- [ ] Commit: `git commit -m "feat: basic views and templates"`

**Entregables**:
- Templates funcionales y navegables
- CRUD básico de productos
- Listado de ventas
- UI responsiva básica

---

### Milestone 1.8: Sistema de Notificaciones por Email

**Objetivo**: Enviar emails cuando el stock esté bajo

#### Implementación

**products/signals.py**
```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Product

@receiver(post_save, sender=Product)
def check_low_stock(sender, instance, **kwargs):
    if instance.quantity <= instance.low_stock_threshold:
        send_low_stock_email(instance)

def send_low_stock_email(product):
    subject = f"⚠️ Stock bajo: {product.title}"
    message = f"""
    El producto "{product.title}" tiene stock bajo.
    
    Stock actual: {product.quantity}
    Umbral mínimo: {product.low_stock_threshold}
    Tienda: {product.store.shop_name}
    
    Por favor, reponer inventario.
    """
    
    send_mail(
        subject,
        message,
        'noreply@etsyinventory.com',
        [product.store.owner.email],
        fail_silently=False,
    )
```

#### Tareas
- [ ] Crear signals.py en app products
- [ ] Implementar verificación de stock bajo
- [ ] Crear templates de email HTML
- [ ] Configurar email backend en development
- [ ] Agregar preferencias de notificación al modelo User
- [ ] Crear vista para configurar notificaciones
- [ ] Tests de notificaciones
- [ ] Commit: `git commit -m "feat: low stock email notifications"`

**Entregables**:
- Notificaciones automáticas de stock bajo
- Templates de email profesionales
- Configuración de preferencias

---

### Milestone 1.9: Pre-commit Hooks y Linters

**Objetivo**: Automatizar verificación de calidad de código

#### Instalación

```bash
pip install black flake8 isort pre-commit
pip freeze > requirements.txt
```

#### Archivos de Configuración

**.pre-commit-config.yaml**
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.8.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/PyCQA/flake8
    rev: 7.1.1
    hooks:
      - id: flake8
        args: ['--max-line-length=100', '--extend-ignore=E203,W503']

  - repo: https://github.com/PyCQA/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ['--profile', 'black']
```

**pyproject.toml**
```toml
[tool.black]
line-length = 100
target-version = ['py311']
include = '\.pyi?
exclude = '''
/(
    \.git
  | \.venv
  | venv
  | migrations
)/
'''

[tool.isort]
profile = "black"
line_length = 100
skip_gitignore = true
```

**setup.cfg** (para flake8)
```ini
[flake8]
max-line-length = 100
extend-ignore = E203, W503
exclude =
    .git,
    __pycache__,
    venv,
    migrations,
    */migrations/*
```

#### Tareas
- [ ] Instalar herramientas de linting
- [ ] Crear archivos de configuración
- [ ] Instalar pre-commit hooks: `pre-commit install`
- [ ] Ejecutar en todos los archivos: `pre-commit run --all-files`
- [ ] Corregir errores de linting
- [ ] Commit: `git commit -m "chore: add pre-commit hooks and linters"`

**Comandos útiles**:
```bash
# Formatear código con black
black .

# Ordenar imports
isort .

# Verificar con flake8
flake8 .

# Ejecutar pre-commit manualmente
pre-commit run --all-files
```

**Entregables**:
- Pre-commit configurado
- Código formateado consistentemente
- Linters ejecutándose automáticamente

---

### Milestone 1.10: Tests Básicos

**Objetivo**: Cobertura de tests para funcionalidades principales

#### Estructura de Tests
```
products/tests/
├── __init__.py
├── test_models.py
├── test_views.py
├── test_sync.py
└── test_signals.py
```

#### Ejemplo: test_models.py
```python
from django.test import TestCase
from accounts.models import User
from stores.models import Store
from products.models import Product
from datetime import datetime, timedelta

class ProductModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.store = Store.objects.create(
            owner=self.user,
            etsy_shop_id='12345',
            shop_name='Test Shop',
            access_token='test_token',
            refresh_token='test_refresh',
            token_expires_at=datetime.now() + timedelta(days=30)
        )
    
    def test_product_creation(self):
        product = Product.objects.create(
            store=self.store,
            etsy_listing_id='54321',
            title='Test Product',
            price=19.99,
            quantity=10
        )
        self.assertEqual(product.title, 'Test Product')
        self.assertEqual(product.quantity, 10)
    
    def test_low_stock_threshold(self):
        product = Product.objects.create(
            store=self.store,
            etsy_listing_id='54321',
            title='Test Product',
            quantity=3,
            low_stock_threshold=5
        )
        self.assertTrue(product.quantity <= product.low_stock_threshold)
```

#### Tareas
- [ ] Instalar pytest-django: `pip install pytest-django pytest-cov`
- [ ] Crear archivo `pytest.ini`
- [ ] Escribir tests de modelos
- [ ] Escribir tests de vistas
- [ ] Escribir tests de comando sync
- [ ] Escribir tests de signals
- [ ] Configurar cobertura de tests
- [ ] Commit: `git commit -m "test: add comprehensive test suite"`

**Ejecutar tests**:
```bash
# Todos los tests
python manage.py test

# Con pytest
pytest

# Con cobertura
pytest --cov=. --cov-report=html
```

**Entregables**:
- Suite de tests completa
- Cobertura >70%
- Tests automatizables en CI

---

## 🎯 FASE 2: AUTOMATIZACIÓN Y CI/CD

### Milestone 2.1: GitHub Repository Setup

#### Tareas
- [ ] Crear repositorio en GitHub
- [ ] Agregar remote: `git remote add origin https://github.com/usuario/etsy-inventory-saas.git`
- [ ] Push inicial: `git push -u origin main`
- [ ] Crear rama develop: `git checkout -b develop`
- [ ] Push develop: `git push -u origin develop`
- [ ] Configurar branch protection rules en GitHub
- [ ] Crear README.md completo
- [ ] Crear LICENSE (MIT)
- [ ] Crear CONTRIBUTING.md
- [ ] Commit: en GitHub directamente

**Entregables**:
- Repositorio público/privado en GitHub
- README profesional
- Licencia agregada

---

### Milestone 2.2: GitHub Actions - CI

**Objetivo**: Ejecutar linters y tests automáticamente en cada PR

#### Archivo .github/workflows/ci.yml
```yaml
name: CI

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Cache dependencies
      uses: actions/cache@v4
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run linters
      run: |
        black --check .
        isort --check-only .
        flake8 .
    
    - name: Run tests
      env:
        SECRET_KEY: 'test-secret-key-for-ci'
        DEBUG: 'False'
        DB_NAME: 'test_db'
        DB_USER: 'postgres'
        DB_PASSWORD: 'postgres'
        DB_HOST: 'localhost'
        DB_PORT: '5432'
      run: |
        python manage.py check
        pytest --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v4
      with:
        file: ./coverage.xml
```

#### Tareas
- [ ] Crear carpeta `.github/workflows/`
- [ ] Crear archivo `ci.yml`
- [ ] Probar workflow en una PR de prueba
- [ ] Configurar badges en README
- [ ] Commit: `git commit -m "ci: add GitHub Actions workflow"`

**Entregables**:
- CI ejecutándose en cada PR
- Linters y tests automáticos
- Badges de status en README

---

### Milestone 2.3: Configuración de Cron para Sincronización

**Objetivo**: Ejecutar sync_etsy cada 15 minutos automáticamente

#### Crear Script Wrapper

**scripts/sync_cron.sh**
```bash
#!/bin/bash
cd /home/yamil/proyectos/etsy-inventory-saas
source venv/bin/activate
python manage.py sync_etsy >> logs/sync.log 2>&1
```

#### Configurar Crontab

```bash
# Editar crontab
crontab -e

# Agregar línea (ejecutar cada 15 minutos)
*/15 * * * * /home/yamil/proyectos/etsy-inventory-saas/scripts/sync_cron.sh
```

#### Tareas
- [ ] Crear carpeta `scripts/`
- [ ] Crear `sync_cron.sh`
- [ ] Dar permisos de ejecución: `chmod +x scripts/sync_cron.sh`
- [ ] Crear carpeta `logs/`
- [ ] Configurar crontab
- [ ] Probar ejecución manual del script
- [ ] Monitorear logs después de 15 minutos
- [ ] Commit: `git commit -m "chore: add cron script for sync"`

**Entregables**:
- Script de sincronización automática
- Cron configurado
- Logs rotando correctamente

---

### Milestone 2.4: Deploy a VPS (Preparación)

**Objetivo**: Preparar archivos de configuración para deploy

#### Archivos Necesarios

**requirements/base.txt**
```
Django==5.2.7
psycopg2-binary==2.9.9
python-decouple==3.8
gunicorn==22.0.0
requests==2.32.3
```

**requirements/production.txt**
```
-r base.txt
sentry-sdk==2.14.0  # Monitoreo de errores
```

**config/gunicorn_config.py**
```python
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2
errorlog = "/var/log/gunicorn/error.log"
accesslog = "/var/log/gunicorn/access.log"
loglevel = "info"
```

**deploy/nginx.conf**
```nginx
server {
    listen 80;
    server_name tudominio.com www.tudominio.com;
    
    client_max_body_size 10M;
    
    location /static/ {
        alias /var/www/etsy-inventory/static/;
    }
    
    location /media/ {
        alias /var/www/etsy-inventory/media/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**deploy/systemd/gunicorn.service**
```ini
[Unit]
Description=Gunicorn daemon for Etsy Inventory SaaS
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/etsy-inventory
Environment="PATH=/var/www/etsy-inventory/venv/bin"
ExecStart=/var/www/etsy-inventory/venv/bin/gunicorn \
    --config /var/www/etsy-inventory/config/gunicorn_config.py \
    config.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

**deploy/install.sh** (script de instalación en VPS)
```bash
#!/bin/bash
set -e

echo "🚀 Instalando Etsy Inventory SaaS en producción..."

# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install -y python3.11 python3.11-venv python3.11-dev \
    postgresql postgresql-contrib libpq-dev \
    nginx git supervisor

# Crear usuario de aplicación
sudo useradd -m -s /bin/bash etsyapp || true

# Crear directorios
sudo mkdir -p /var/www/etsy-inventory
sudo mkdir -p /var/log/gunicorn

# Clonar repositorio
cd /var/www
sudo git clone https://github.com/usuario/etsy-inventory-saas.git etsy-inventory

# Cambiar permisos
sudo chown -R etsyapp:etsyapp /var/www/etsy-inventory
sudo chown -R etsyapp:etsyapp /var/log/gunicorn

# Entorno virtual
cd /var/www/etsy-inventory
sudo -u etsyapp python3.11 -m venv venv
sudo -u etsyapp venv/bin/pip install --upgrade pip
sudo -u etsyapp venv/bin/pip install -r requirements/production.txt

# Configurar PostgreSQL
sudo -u postgres psql << EOF
CREATE DATABASE etsy_inventory_prod;
CREATE USER etsy_prod_user WITH PASSWORD 'CAMBIAR_PASSWORD_SEGURO';
GRANT ALL PRIVILEGES ON DATABASE etsy_inventory_prod TO etsy_prod_user;
GRANT ALL ON SCHEMA public TO etsy_prod_user;
GRANT CREATE ON SCHEMA public TO etsy_prod_user;
EOF

echo "✅ Instalación base completada"
echo "⚠️  Próximos pasos manuales:"
echo "1. Copiar .env de producción a /var/www/etsy-inventory/"
echo "2. Ejecutar: sudo -u etsyapp venv/bin/python manage.py migrate"
echo "3. Ejecutar: sudo -u etsyapp venv/bin/python manage.py collectstatic"
echo "4. Copiar nginx.conf a /etc/nginx/sites-available/"
echo "5. Copiar gunicorn.service a /etc/systemd/system/"
echo "6. sudo systemctl start gunicorn && sudo systemctl enable gunicorn"
echo "7. sudo systemctl restart nginx"
echo "8. Configurar SSL con certbot"
```

**deploy/env.production.example**
```bash
# Django
SECRET_KEY=GENERAR_CLAVE_SEGURA_ALEATORIA
DEBUG=False
ALLOWED_HOSTS=tudominio.com,www.tudominio.com

# Database
DB_NAME=etsy_inventory_prod
DB_USER=etsy_prod_user
DB_PASSWORD=PASSWORD_SUPER_SEGURO
DB_HOST=localhost
DB_PORT=5432

# Etsy API
ETSY_CLIENT_ID=tu_client_id_real
ETSY_CLIENT_SECRET=tu_client_secret_real
ETSY_REDIRECT_URI=https://tudominio.com/auth/etsy/callback/

# Email
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=tu_api_key_de_sendgrid

# Sentry (opcional)
SENTRY_DSN=https://tu-sentry-dsn
```

#### Tareas
- [ ] Crear carpeta `requirements/` con base.txt y production.txt
- [ ] Crear `config/gunicorn_config.py`
- [ ] Crear carpeta `deploy/` con todos los archivos
- [ ] Crear `deploy/install.sh` y dar permisos: `chmod +x`
- [ ] Crear `deploy/env.production.example`
- [ ] Documentar proceso de deploy en README
- [ ] Commit: `git commit -m "deploy: add production configuration files"`

**Entregables**:
- Archivos de configuración listos para producción
- Script de instalación automatizado
- Documentación de deploy

---

### Milestone 2.5: GitHub Actions - CD (Deploy Automático)

**Objetivo**: Deploy automático a VPS en push a main

#### Archivo .github/workflows/deploy.yml
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]
  workflow_dispatch:  # Permite ejecutar manualmente

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Deploy to VPS
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.VPS_HOST }}
        username: ${{ secrets.VPS_USER }}
        key: ${{ secrets.VPS_SSH_KEY }}
        script: |
          cd /var/www/etsy-inventory
          
          # Backup base de datos
          sudo -u postgres pg_dump etsy_inventory_prod > /tmp/backup_$(date +%Y%m%d_%H%M%S).sql
          
          # Actualizar código
          sudo -u etsyapp git pull origin main
          
          # Actualizar dependencias
          sudo -u etsyapp venv/bin/pip install -r requirements/production.txt
          
          # Ejecutar migraciones
          sudo -u etsyapp venv/bin/python manage.py migrate --noinput
          
          # Colectar archivos estáticos
          sudo -u etsyapp venv/bin/python manage.py collectstatic --noinput
          
          # Reiniciar Gunicorn
          sudo systemctl restart gunicorn
          
          # Verificar salud
          sleep 5
          curl -f http://localhost:8000/health/ || exit 1
          
          echo "✅ Deploy completado exitosamente"
```

#### Health Check Endpoint

**config/urls.py** (agregar)
```python
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'ok'})

urlpatterns = [
    # ... otras URLs
    path('health/', health_check, name='health'),
]
```

#### Configurar Secrets en GitHub

En GitHub → Settings → Secrets and variables → Actions:
- `VPS_HOST`: IP o dominio del VPS
- `VPS_USER`: Usuario SSH (ej: etsyapp)
- `VPS_SSH_KEY`: Clave privada SSH

#### Tareas
- [ ] Crear workflow `deploy.yml`
- [ ] Configurar SSH keys en VPS
- [ ] Agregar secrets en GitHub
- [ ] Crear endpoint `/health/`
- [ ] Probar deploy manual
- [ ] Documentar proceso de rollback
- [ ] Commit: `git commit -m "ci: add automated deployment workflow"`

**Entregables**:
- Deploy automático funcionando
- Health checks configurados
- Rollback documentado

---

## 🎯 FASE 3: MEJORAS Y ESCALABILIDAD

### Milestone 3.1: Migración a Celery + Redis

**Objetivo**: Reemplazar cron con tareas asíncronas

#### Instalación

```bash
pip install celery redis django-celery-beat django-celery-results
pip freeze > requirements.txt
```

#### Archivos de Configuración

**config/celery.py**
```python
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

app = Celery('etsy_inventory')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Configurar beat schedule
app.conf.beat_schedule = {
    'sync-etsy-every-15-minutes': {
        'task': 'stores.tasks.sync_all_stores',
        'schedule': crontab(minute='*/15'),
    },
    'refresh-tokens-daily': {
        'task': 'stores.tasks.refresh_expiring_tokens',
        'schedule': crontab(hour=2, minute=0),  # 2 AM diario
    },
}
```

**config/__init__.py**
```python
from .celery import app as celery_app

__all__ = ('celery_app',)
```

**stores/tasks.py**
```python
from celery import shared_task
from django.utils import timezone
from .models import Store
from products.models import Product
import requests

@shared_task
def sync_all_stores():
    """Sincroniza todas las tiendas activas"""
    stores = Store.objects.filter(sync_enabled=True, is_active=True)
    
    for store in stores:
        sync_single_store.delay(store.id)
    
    return f"Iniciada sincronización de {stores.count()} tiendas"

@shared_task
def sync_single_store(store_id):
    """Sincroniza una tienda específica"""
    try:
        store = Store.objects.get(id=store_id)
        
        # Sincronizar productos
        sync_products(store)
        
        # Sincronizar ventas
        sync_sales(store)
        
        store.last_sync = timezone.now()
        store.save()
        
        return f"✅ Tienda {store.shop_name} sincronizada"
    except Exception as e:
        return f"❌ Error en tienda {store_id}: {str(e)}"

@shared_task
def refresh_expiring_tokens():
    """Refresca tokens que expiran pronto"""
    from datetime import timedelta
    
    expiring_soon = timezone.now() + timedelta(days=7)
    stores = Store.objects.filter(token_expires_at__lte=expiring_soon)
    
    for store in stores:
        refresh_store_token.delay(store.id)
    
    return f"Refrescando tokens de {stores.count()} tiendas"

@shared_task
def refresh_store_token(store_id):
    """Refresca el token de una tienda"""
    # Implementación del refresh
    pass
```

**settings/base.py** (agregar)
```python
# Celery Configuration
CELERY_BROKER_URL = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
```

#### Tareas
- [ ] Instalar Celery, Redis y dependencias
- [ ] Configurar `celery.py`
- [ ] Crear tasks en `stores/tasks.py`
- [ ] Configurar Redis en settings
- [ ] Instalar Redis en servidor: `sudo apt install redis-server`
- [ ] Crear systemd services para celery worker y beat
- [ ] Migrar lógica del comando sync_etsy a tasks
- [ ] Tests de tasks
- [ ] Commit: `git commit -m "feat: migrate to Celery + Redis"`

**Ejecutar Celery localmente**:
```bash
# Worker
celery -A config worker -l info

# Beat (scheduler)
celery -A config beat -l info

# Ambos en desarrollo
celery -A config worker -B -l info
```

**Entregables**:
- Celery funcionando con Redis
- Tareas programadas automáticamente
- Workers escalables

---

### Milestone 3.2: Docker y Docker Compose

**Objetivo**: Containerizar la aplicación

#### Dockerfile
```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements/production.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiar código
COPY . .

# Crear usuario no-root
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["gunicorn", "--config", "config/gunicorn_config.py", "config.wsgi:application"]
```

#### docker-compose.yml
```yaml
version: '3.8'

services:
  db:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    build: .
    command: gunicorn --config config/gunicorn_config.py config.wsgi:application
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy

  celery_worker:
    build: .
    command: celery -A config worker -l info
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - db
      - redis

  celery_beat:
    build: .
    command: celery -A config beat -l info
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - db
      - redis

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./deploy/nginx.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/var/www/static
      - media_volume:/var/www/media
      - ./deploy/ssl:/etc/nginx/ssl
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

#### .dockerignore
```
venv/
__pycache__/
*.pyc
.git/
.env
db.sqlite3
*.log
.vscode/
.idea/
node_modules/
```

#### Tareas
- [ ] Crear `Dockerfile`
- [ ] Crear `docker-compose.yml`
- [ ] Crear `.dockerignore`
- [ ] Probar build: `docker-compose build`
- [ ] Probar ejecución: `docker-compose up`
- [ ] Documentar comandos Docker en README
- [ ] Commit: `git commit -m "feat: add Docker support"`

**Comandos útiles**:
```bash
# Build y ejecutar
docker-compose up -d --build

# Ver logs
docker-compose logs -f web

# Ejecutar migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser

# Detener todo
docker-compose down

# Limpiar volúmenes
docker-compose down -v
```

**Entregables**:
- Aplicación completamente containerizada
- Docker Compose funcional
- Documentación de Docker

---

### Milestone 3.3: Webhooks de Etsy

**Objetivo**: Recibir actualizaciones en tiempo real desde Etsy

#### Implementación

**stores/views.py** (agregar)
```python
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import hmac
import hashlib

@csrf_exempt
def etsy_webhook(request):
    """Endpoint para webhooks de Etsy"""
    if request.method != 'POST':
        return HttpResponse(status=405)
    
    # Verificar firma HMAC
    signature = request.headers.get('X-Etsy-Signature')
    if not verify_webhook_signature(request.body, signature):
        return HttpResponse(status=403)
    
    payload = json.loads(request.body)
    event_type = payload.get('event_type')
    
    # Procesar según tipo de evento
    if event_type == 'listing.updated':
        handle_listing_update.delay(payload)
    elif event_type == 'receipt.created':
        handle_new_sale.delay(payload)
    
    return HttpResponse(status=200)

def verify_webhook_signature(payload, signature):
    """Verifica la firma HMAC del webhook"""
    secret = config('ETSY_CLIENT_SECRET').encode()
    expected = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
```

**stores/tasks.py** (agregar)
```python
@shared_task
def handle_listing_update(payload):
    """Procesa actualización de producto"""
    listing_id = payload['data']['listing_id']
    shop_id = payload['shop_id']
    
    try:
        store = Store.objects.get(etsy_shop_id=shop_id)
        product = Product.objects.get(
            store=store,
            etsy_listing_id=listing_id
        )
        
        # Actualizar producto
        product.quantity = payload['data']['quantity']
        product.price = payload['data']['price']
        product.save()
        
        return f"✅ Producto {listing_id} actualizado"
    except Exception as e:
        return f"❌ Error: {str(e)}"

@shared_task
def handle_new_sale(payload):
    """Procesa nueva venta"""
    # Implementación similar
    pass
```

#### Registro de Webhooks en Etsy

**stores/utils.py** (agregar)
```python
def register_etsy_webhook(store, event_type):
    """Registra webhook en Etsy"""
    url = f"https://openapi.etsy.com/v3/application/shops/{store.etsy_shop_id}/webhooks"
    
    headers = {
        'Authorization': f'Bearer {get_valid_token(store)}',
        'Content-Type': 'application/json',
    }
    
    data = {
        'callback_uri': f"https://tudominio.com/webhooks/etsy/",
        'event_type': event_type,
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()
```

#### Tareas
- [ ] Crear endpoint de webhook
- [ ] Implementar verificación HMAC
- [ ] Crear tasks para procesar eventos
- [ ] Registrar webhooks en Etsy (via código o manualmente)
- [ ] Probar con webhooks de prueba de Etsy
- [ ] Agregar logging de webhooks
- [ ] Tests de webhooks
- [ ] Commit: `git commit -m "feat: add Etsy webhooks support"`

**Entregables**:
- Webhooks funcionando
- Actualizaciones en tiempo real
- Sistema robusto de verificación

---

### Milestone 3.4: Dashboard y Métricas

**Objetivo**: Panel con estadísticas y gráficos

#### Vistas del Dashboard

**dashboard/views.py**
```python
from django.views.generic import TemplateView
from django.db.models import Sum, Count, Avg
from datetime import datetime, timedelta

class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Resumen general
        context['total_products'] = Product.objects.filter(
            store__owner=user
        ).count()
        
        context['low_stock_products'] = Product.objects.filter(
            store__owner=user,
            quantity__lte=F('low_stock_threshold')
        ).count()
        
        # Ventas del mes
        month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0)
        context['sales_this_month'] = Sale.objects.filter(
            store__owner=user,
            sale_date__gte=month_start
        ).aggregate(
            total=Sum('total_amount'),
            count=Count('id')
        )
        
        # Productos más vendidos
        context['top_products'] = SaleItem.objects.filter(
            sale__store__owner=user,
            sale__sale_date__gte=month_start
        ).values('product__title').annotate(
            total_sold=Sum('quantity')
        ).order_by('-total_sold')[:10]
        
        # Gráfico de ventas (últimos 30 días)
        context['sales_chart_data'] = self.get_sales_chart_data(user)
        
        return context
    
    def get_sales_chart_data(self, user):
        """Datos para gráfico de ventas diarias"""
        days = 30
        data = []
        
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            sales = Sale.objects.filter(
                store__owner=user,
                sale_date__date=date.date()
            ).aggregate(total=Sum('total_amount'))
            
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'total': float(sales['total'] or 0)
            })
        
        return list(reversed(data))
```

#### Template con Chart.js

**templates/dashboard/index.html**
```html
{% extends 'base.html' %}

{% block content %}
<div class="dashboard">
    <h1>Dashboard</h1>
    
    <!-- Tarjetas de resumen -->
    <div class="stats-grid">
        <div class="stat-card">
            <h3>Total Productos</h3>
            <p class="stat-number">{{ total_products }}</p>
        </div>
        
        <div class="stat-card alert">
            <h3>Stock Bajo</h3>
            <p class="stat-number">{{ low_stock_products }}</p>
        </div>
        
        <div class="stat-card">
            <h3>Ventas del Mes</h3>
            <p class="stat-number">${{ sales_this_month.total|floatformat:2 }}</p>
            <small>{{ sales_this_month.count }} órdenes</small>
        </div>
    </div>
    
    <!-- Gráfico de ventas -->
    <div class="chart-container">
        <h2>Ventas Últimos 30 Días</h2>
        <canvas id="salesChart"></canvas>
    </div>
    
    <!-- Productos más vendidos -->
    <div class="top-products">
        <h2>Productos Más Vendidos</h2>
        <table>
            <thead>
                <tr>
                    <th>Producto</th>
                    <th>Cantidad Vendida</th>
                </tr>
            </thead>
            <tbody>
                {% for item in top_products %}
                <tr>
                    <td>{{ item.product__title }}</td>
                    <td>{{ item.total_sold }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const ctx = document.getElementById('salesChart').getContext('2d');
const salesChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: {{ sales_chart_data|safe|json_script:"chart-labels" }}.map(d => d.date),
        datasets: [{
            label: 'Ventas ($)',
            data: {{ sales_chart_data|safe|json_script:"chart-data" }}.map(d => d.total),
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Ventas Diarias'
            }
        }
    }
});
</script>
{% endblock %}
```

#### Tareas
- [ ] Crear app `dashboard`
- [ ] Implementar vistas con métricas
- [ ] Crear templates con Chart.js
- [ ] Agregar CSS para cards y gráficos
- [ ] Implementar caché para queries pesadas
- [ ] Crear exportación a CSV/Excel
- [ ] Tests de dashboard
- [ ] Commit: `git commit -m "feat: add analytics dashboard"`

**Entregables**:
- Dashboard funcional con métricas
- Gráficos interactivos
- Exportación de datos

---

## 🎯 FASE 4: PRODUCCIÓN Y MANTENIMIENTO

### Milestone 4.1: Monitorización y Logging

**Objetivo**: Sistema completo de logs y alertas

#### Configuración de Logging

**settings/base.py**
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs/django.log',
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'stores': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
        },
    },
}
```

#### Integración con Sentry

```bash
pip install sentry-sdk
```

**settings/production.py**
```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=config('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)
```

#### Tareas
- [ ] Configurar logging robusto
- [ ] Integrar Sentry para errores
- [ ] Configurar rotación de logs
- [ ] Crear alertas por email para errores críticos
- [ ] Implementar health checks avanzados
- [ ] Documentar troubleshooting
- [ ] Commit: `git commit -m "feat: add monitoring and logging"`

**Entregables**:
- Sistema de logging completo
- Sentry configurado
- Alertas automáticas

---

### Milestone 4.2: Backups Automatizados

**Objetivo**: Backups diarios de BD y archivos

#### Script de Backup

**scripts/backup.sh**
```bash
#!/bin/bash
set -e

# Configuración
BACKUP_DIR="/var/backups/etsy-inventory"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="etsy_inventory_prod"
RETENTION_DAYS=30

# Crear directorio si no existe
mkdir -p $BACKUP_DIR

# Backup de PostgreSQL
echo "📦 Creando backup de base de datos..."
sudo -u postgres pg_dump $DB_NAME | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Backup de archivos media
echo "📦 Creando backup de archivos media..."
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /var/www/etsy-inventory/media/

# Eliminar backups antiguos
echo "🗑️  Eliminando backups antiguos..."
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +$RETENTION_DAYS -delete
find $BACKUP_DIR -name "media_*.tar.gz" -mtime +$RETENTION_DAYS -delete

# Subir a S3 (opcional)
if [ ! -z "$AWS_S3_BUCKET" ]; then
    echo "☁️  Subiendo a S3..."
    aws s3 cp $BACKUP_DIR/db_$DATE.sql.gz s3://$AWS_S3_BUCKET/backups/
    aws s3 cp $BACKUP_DIR/media_$DATE.tar.gz s3://$AWS_S3_BUCKET/backups/
fi

echo "✅ Backup completado: $DATE"
```

#### Configurar Cron para Backups

```bash
# Ejecutar diariamente a las 3 AM
0 3 * * * /var/www/etsy-inventory/scripts/backup.sh >> /var/log/backups.log 2>&1
```

#### Script de Restauración

**scripts/restore.sh**
```bash
#!/bin/bash

if [ -z "$1" ]; then
    echo "Uso: ./restore.sh FECHA (formato: YYYYMMDD_HHMMSS)"
    exit 1
fi

DATE=$1
BACKUP_DIR="/var/backups/etsy-inventory"
DB_NAME="etsy_inventory_prod"

echo "⚠️  ADVERTENCIA: Esto sobrescribirá la base de datos actual"
read -p "¿Continuar? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

# Restaurar BD
echo "🔄 Restaurando base de datos..."
gunzip -c $BACKUP_DIR/db_$DATE.sql.gz | sudo -u postgres psql $DB_NAME

# Restaurar media
echo "🔄 Restaurando archivos media..."
tar -xzf $BACKUP_DIR/media_$DATE.tar.gz -C /

echo "✅ Restauración completada"
```

#### Tareas
- [ ] Crear script de backup
- [ ] Crear script de restauración
- [ ] Configurar cron para backups diarios
- [ ] Probar proceso de restauración
- [ ] Documentar procedimiento de recuperación
- [ ] Configurar S3 o almacenamiento remoto (opcional)
- [ ] Commit: `git commit -m "ops: add automated backup system"`

**Entregables**:
- Backups automáticos diarios
- Script de restauración probado
- Documentación de DR (Disaster Recovery)

---

### Milestone 4.3: Seguridad Avanzada

**Objetivo**: Hardening de seguridad

#### Checklist de Seguridad

**Django Security**
```python
# settings/production.py

# HTTPS y cookies
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Headers de seguridad
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# CORS (si es necesario)
CORS_ALLOWED_ORIGINS = [
    "https://tudominio.com",
]

# CSP (Content Security Policy)
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "https://cdn.jsdelivr.net")
CSP_STYLE_SRC = ("'self'", "https://cdn.jsdelivr.net")
```

#### Cifrado de Tokens en BD

**stores/models.py** (modificar)
```python
from cryptography.fernet import Fernet
from django.conf import settings

class Store(models.Model):
    # ... otros campos
    
    _access_token = models.TextField(db_column='access_token')
    _refresh_token = models.TextField(db_column='refresh_token')
    
    @property
    def access_token(self):
        """Descifra el access token"""
        f = Fernet(settings.ENCRYPTION_KEY)
        return f.decrypt(self._access_token.encode()).decode()
    
    @access_token.setter
    def access_token(self, value):
        """Cifra el access token antes de guardar"""
        f = Fernet(settings.ENCRYPTION_KEY)
        self._access_token = f.encrypt(value.encode()).decode()
    
    # Similar para refresh_token
```

**Generar encryption key**:
```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
# Agregar a .env como ENCRYPTION_KEY
```

#### Rate Limiting

```bash
pip install django-ratelimit
```

**stores/views.py**
```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', method='POST')
def etsy_auth_init(request):
    # ... código existente
    pass
```

#### Tareas
- [ ] Implementar todos los headers de seguridad
- [ ] Cifrar tokens OAuth en BD
- [ ] Implementar rate limiting
- [ ] Configurar CSP (Content Security Policy)
- [ ] Instalar django-csp
- [ ] Habilitar 2FA para admin (django-otp)
- [ ] Auditoría de seguridad con `python manage.py check --deploy`
- [ ] Documentar políticas de seguridad
- [ ] Commit: `git commit -m "security: implement advanced security measures"`

**Entregables**:
- Aplicación endurecida contra ataques comunes
- Tokens cifrados
- Rate limiting activo

---

### Milestone 4.4: Performance y Optimización

**Objetivo**: Mejorar velocidad y eficiencia

#### Optimización de Queries

**products/views.py**
```python
# ANTES (N+1 queries)
products = Product.objects.filter(store__owner=request.user)
for product in products:
    print(product.store.shop_name)  # Query por cada producto

# DESPUÉS (1 query)
products = Product.objects.filter(
    store__owner=request.user
).select_related('store')
```

#### Caché con Redis

**settings/production.py**
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': config('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'etsy_inventory',
        'TIMEOUT': 300,  # 5 minutos
    }
}
```

**dashboard/views.py** (con caché)
```python
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

@method_decorator(cache_page(60 * 15), name='dispatch')  # 15 minutos
class DashboardView(TemplateView):
    # ... código existente
    pass
```

#### Índices de BD

**products/models.py**
```python
class Product(models.Model):
    # ... campos existentes
    
    class Meta:
        unique_together = ['store', 'etsy_listing_id']
        indexes = [
            models.Index(fields=['store', 'is_active']),
            models.Index(fields=['quantity']),
            models.Index(fields=['last_synced']),
        ]
```

#### Compresión y Minificación

```bash
pip install django-compressor django-htmlmin
```

**settings/production.py**
```python
INSTALLED_APPS += [
    'compressor',
    'htmlmin',
]

# Compressor
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

# HTML Minification
HTML_MINIFY = True
```

#### Tareas
- [ ] Identificar queries N+1 con django-debug-toolbar
- [ ] Agregar select_related/prefetch_related donde necesario
- [ ] Implementar caché con Redis
- [ ] Agregar índices de BD apropiados
- [ ] Configurar compresión de assets
- [ ] Optimizar imágenes (Pillow, webp)
- [ ] Implementar lazy loading de imágenes
- [ ] Tests de performance
- [ ] Commit: `git commit -m "perf: optimize queries and caching"`

**Entregables**:
- Queries optimizadas
- Caché implementado
- Tiempos de carga reducidos

---

### Milestone 4.5: Documentación Completa

**Objetivo**: Documentación profesional para mantenimiento

#### README.md Completo

```markdown
# Etsy Inventory SaaS

[![CI](https://github.com/usuario/etsy-inventory-saas/workflows/CI/badge.svg)](https://github.com/usuario/etsy-inventory-saas/actions)
[![Coverage](https://codecov.io/gh/usuario/etsy-inventory-saas/branch/main/graph/badge.svg)](https://codecov.io/gh/usuario/etsy-inventory-saas)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Sistema SaaS para sincronizar y gestionar inventario de tiendas Etsy.

## 🚀 Características

- Sincronización automática con Etsy cada 15 minutos
- Gestión de inventario multi-tienda
- Notificaciones de stock bajo
- Dashboard con métricas y gráficos
- API REST para integraciones
- Webhooks en tiempo real

## 📋 Requisitos

- Python 3.11+
- PostgreSQL 14+
- Redis 7+
- Node.js 18+ (para assets)

## 🛠️ Instalación

### Desarrollo Local

[Instrucciones detalladas paso a paso]

### Docker

[Instrucciones con docker-compose]

### Producción

[Link a documentación de deploy]

## 📖 Documentación

- [Guía de Usuario](docs/user-guide.md)
- [Guía de Desarrollo](docs/development.md)
- [API Documentation](docs/api.md)
- [Deployment Guide](docs/deployment.md)

## 🧪 Testing

[Comandos de tests]

## 📝 Licencia

MIT License - ver [LICENSE](LICENSE)

## 👥 Contribuir

Ver [CONTRIBUTING.md](CONTRIBUTING.md)
```

#### Documentos Adicionales

**docs/development.md**
- Setup de entorno local
- Estructura del proyecto
- Guías de código
- Cómo agregar features

**docs/api.md**
- Endpoints disponibles
- Autenticación
- Ejemplos de requests/responses
- Rate limits

**docs/deployment.md**
- Guía paso a paso de deploy
- Configuración de servidor
- SSL/HTTPS
- Troubleshooting común

**docs/user-guide.md**
- Cómo conectar tienda Etsy
- Uso del dashboard
- Configuración de notificaciones
- FAQ

**CONTRIBUTING.md**
```markdown
# Guía de Contribución

## Proceso de Desarrollo

1. Fork el repositorio
2. Crear rama feature: `git checkout -b feature/AmazingFeature`
3. Commit cambios: `git commit -m 'feat: add AmazingFeature'`
4. Push a la rama: `git push origin feature/AmazingFeature`
5. Abrir Pull Request

## Estándares de Código

- Seguir PEP 8
- Usar Black para formateo
- Tests obligatorios para nuevas features
- Cobertura mínima 70%

## Mensajes de Commit

Usar conventional commits:
- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Documentación
- `test:` Tests
- `refactor:` Refactorización
- `chore:` Mantenimiento
```

**CHANGELOG.md**
```markdown
# Changelog

Todos los cambios notables se documentarán aquí.

## [Unreleased]

## [1.0.0] - 2025-XX-XX

### Added
- Sincronización automática con Etsy
- Dashboard de métricas
- Sistema de notificaciones
- OAuth con Etsy
- Deploy automático con GitHub Actions

### Changed
- Migración de cron a Celery

### Fixed
- Corrección de bug en refresh de tokens
```

#### Tareas
- [ ] Completar README.md con badges
- [ ] Crear docs/ con guías completas
- [ ] Escribir CONTRIBUTING.md
- [ ] Mantener CHANGELOG.md actualizado
- [ ] Generar documentación de API (Swagger/OpenAPI)
- [ ] Crear video tutorial (opcional)
- [ ] Commit: `git commit -m "docs: add comprehensive documentation"`

**Entregables**:
- Documentación completa y profesional
- Guías para usuarios y desarrolladores
- FAQ y troubleshooting

---

## 🎯 FASE 5: FEATURES AVANZADOS (OPCIONAL)

### Ideas para Expansión Futura

#### Multi-tenancy
- Soporte para múltiples usuarios/empresas
- Aislamiento de datos por tenant
- Planes de suscripción (Free, Pro, Enterprise)

#### API Pública
- API REST completa
- Autenticación con API keys
- Documentación con Swagger
- SDK para Python/JavaScript

#### Integraciones Adicionales
- Amazon Handmade
- eBay
- Shopify
- WooCommerce

#### Features Avanzados
- Forecasting de inventario con ML
- Recomendaciones de precios
- Análisis de competencia
- Generación automática de reportes PDF

#### Mobile App
- App nativa iOS/Android
- Push notifications
- Escaneo de códigos de barras
- Gestión offline

---

## 📊 MÉTRICAS DE COMPLETITUD

### Fase 1: MVP (Esencial)
- [ ] 1.1 - Estructura de Apps
- [ ] 1.2 - Modelos de BD
- [ ] 1.3 - Settings Modular
- [ ] 1.4 - Autenticación
- [ ] 1.5 - OAuth Etsy
- [ ] 1.6 - Comando Sync
- [ ] 1.7 - Vistas y Templates
- [ ] 1.8 - Notificaciones Email
- [ ] 1.9 - Pre-commit Hooks
- [ ] 1.10 - Tests Básicos

### Fase 2: Automatización (Importante)
- [ ] 2.1 - GitHub Repo
- [ ] 2.2 - GitHub Actions CI
- [ ] 2.3 - Cron Config
- [ ] 2.4 - Deploy Prep
- [ ] 2.5 - GitHub Actions CD

### Fase 3: Escalabilidad (Recomendado)
- [ ] 3.1 - Celery + Redis
- [ ] 3.2 - Docker
- [ ] 3.3 - Webhooks Etsy
- [ ] 3.4 - Dashboard Avanzado

### Fase 4: Producción (Crítico para producción)
- [ ] 4.1 - Monitoring
- [ ] 4.2 - Backups
- [ ] 4.3 - Seguridad
- [ ] 4.4 - Performance
- [ ] 4.5 - Documentación

---

## 🔗 RECURSOS ÚTILES

### Tutoriales y Guías
- Django Official Tutorial: https://docs.djangoproject.com/en/stable/intro/tutorial01/
- Etsy API Quickstart: https://developers.etsy.com/documentation/tutorials/quickstart
- OAuth 2.0 Explained: https://oauth.net/2/
- Celery Best Practices: https://docs.celeryproject.org/en/stable/userguide/tasks.html

### Herramientas
- Django Debug Toolbar: https://django-debug-toolbar.readthedocs.io/
- Django Extensions: https://django-extensions.readthedocs.io/
- Postman (API testing): https://www.postman.com/
- pgAdmin (PostgreSQL GUI): https://www.pgadmin.org/

### Comunidades
- r/django: https://www.reddit.com/r/django/
- Django Forum: https://forum.djangoproject.com/
- Stack Overflow Django: https://stackoverflow.com/questions/tagged/django

---

## 💡 CONSEJOS FINALES

### Mejores Prácticas
1. **Commits frecuentes**: Haz commits pequeños y frecuentes
2. **Tests primero**: Escribe tests antes de features complejas
3. **Code review**: Revisa tu código antes de merge
4. **Documentación**: Documenta mientras desarrollas, no después
5. **Seguridad**: Nunca commits secretos, siempre usa .env

### Errores Comunes a Evitar
- ❌ Subir .env a Git
- ❌ No hacer backups antes de deploy
- ❌ Queries N+1 sin optimizar
- ❌ No manejar errores de API externa
- ❌ Hardcodear URLs y valores
- ❌ No validar inputs de usuario
- ❌ Olvidar migrations después de cambiar modelos

### Orden Sugerido de Implementación
1. **Semana 1-2**: Milestones 1.1 a 1.4 (Setup + Auth)
2. **Semana 3-4**: Milestones 1.5 a 1.7 (Etsy + Sync + UI)
3. **Semana 5**: Milestones 1.8 a 1.10 (Notif + Linters + Tests)
4. **Semana 6**: Milestones 2.1 a 2.3 (GitHub + CI + Cron)
5. **Semana 7**: Milestones 2.4 a 2.5 (Deploy)
6. **Semana 8+**: Fase 3 y 4 según necesidad

---

## 📞 SOPORTE

Para preguntas o problemas durante el desarrollo:

1. Revisa la documentación en `docs/`
2. Busca en Issues de GitHub
3. Pregunta en Django Forum
4. Consulta Stack Overflow

¡Buena suerte con tu proyecto! 🚀