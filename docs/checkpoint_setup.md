# Checkpoint: Configuración Inicial Completada ✅

**Fecha de checkpoint**: Octubre 2025  
**Estado**: Setup de entorno de desarrollo completado

---

## 🖥️ Entorno de Desarrollo

### Sistema Operativo
- **OS**: Windows 11 (Versión 24H2)
- **WSL**: WSL 2 con Ubuntu 22.04 LTS
- **Usuario WSL**: `yamil`
- **Contraseña WSL**: `123456`

### Software Instalado

#### Python
- **Versión**: Python 3.11.13
- **Ubicación**: `/usr/bin/python3.11`
- **Repositorio**: PPA deadsnakes
- **Paquetes instalados**: python3.11, python3.11-venv, python3.11-dev

#### Git
- **Versión**: 2.43.0
- **Configuración**:
  - `user.name`: Yamil
  - `user.email`: yamilpalmiero@gmail.com
  - `init.defaultBranch`: main

#### PostgreSQL
- **Versión**: PostgreSQL 16.10
- **Estado**: Servicio activo
- **Comando de inicio**: `sudo service postgresql start`

#### Visual Studio Code
- **Conexión**: WSL integrado (ver "WSL: Ubuntu" en esquina inferior izquierda)
- **Extensiones instaladas**:
  - WSL (Microsoft)
  - Python (Microsoft)
- **Intérprete seleccionado**: `./venv/bin/python` (Python 3.11.13)

---

## 📁 Estructura del Proyecto

### Ubicación
```
/home/yamil/proyectos/etsy-inventory-saas/
```

**Acceso desde Windows**: `\\wsl$\Ubuntu\home\yamil\proyectos\etsy-inventory-saas`

### Estructura de Archivos Actual

```
etsy-inventory-saas/
├── venv/                    # Entorno virtual (NO versionado)
├── config/                  # Configuración Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py         # ✅ Configurado con PostgreSQL y .env
│   ├── urls.py
│   └── wsgi.py
├── manage.py               # CLI de Django
├── .env                    # Variables de entorno (NO versionado)
├── .gitignore             # ✅ Configurado
├── requirements.txt       # Dependencias Python
└── .git/                  # Repositorio Git
```

---

## 🐍 Entorno Virtual Python

### Activación
```bash
# Siempre ejecutar desde la carpeta del proyecto
cd ~/proyectos/etsy-inventory-saas
source venv/bin/activate
```

**Indicador**: Prompt mostrará `(venv)` al inicio

### Dependencias Instaladas

```
Django==5.2.7
psycopg2-binary==2.9.x
python-decouple==3.8
asgiref==3.8.1
sqlparse==0.5.x
```

**Archivo**: `requirements.txt`

---

## 🗄️ Base de Datos PostgreSQL

### Configuración de BD

- **Nombre de BD**: `etsy_inventory_db`
- **Usuario**: `etsy_user`
- **Contraseña**: `password_seguro_123`
- **Host**: `localhost`
- **Puerto**: `5432`

### Comandos PostgreSQL Útiles

```bash
# Iniciar servicio
sudo service postgresql start

# Entrar a consola PostgreSQL
sudo -u postgres psql

# Conectarse a la BD del proyecto
\c etsy_inventory_db

# Salir
\q
```

### Permisos Configurados
✅ Usuario `etsy_user` tiene permisos completos sobre:
- Base de datos `etsy_inventory_db`
- Schema `public`
- Permiso de CREATE en schema public

---

## ⚙️ Configuración de Django

### settings.py - Cambios Realizados

#### 1. Imports
```python
from pathlib import Path
from decouple import config  # ✅ Agregado
```

#### 2. Secret Key y Debug
```python
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

#### 3. Base de Datos
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}
```

### Archivo .env (Variables de Entorno)

```bash
# Django
SECRET_KEY=django-insecure-cambiar-esto-en-produccion-x7k9m2n4p6q8r0s2t4
DEBUG=True

# Database
DB_NAME=etsy_inventory_db
DB_USER=etsy_user
DB_PASSWORD=password_seguro_123
DB_HOST=localhost
DB_PORT=5432

# Etsy API (pendiente de completar)
ETSY_CLIENT_ID=
ETSY_CLIENT_SECRET=
ETSY_REDIRECT_URI=http://localhost:8000/auth/etsy/callback/

# Email (pendiente de configurar)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```

**⚠️ IMPORTANTE**: Este archivo NO está en Git (protegido por `.gitignore`)

---

## 🗃️ Migraciones y Superusuario

### Migraciones Aplicadas
✅ Migraciones iniciales de Django aplicadas exitosamente:
- contenttypes
- auth
- admin
- sessions

**Comando ejecutado**: `python manage.py migrate`

### Superusuario Creado
✅ Cuenta de administrador creada:
- **Username**: `admin`
- **Email**: `yamilpalmiero@gmail.com`
- **Password**: [la que configuraste]

**Acceso**: http://localhost:8000/admin

---

## 🔄 Control de Versiones Git

### Estado del Repositorio
- **Rama actual**: `main`
- **Commits realizados**: 2

### Historial de Commits

```bash
# Commit 1
git commit -m "init: django project structure"
# Archivos: .gitignore, config/, manage.py, requirements.txt

# Commit 2
git commit -m "config: setup PostgreSQL and environment variables"
# Archivos: config/settings.py (modificado)
```

### Archivos Ignorados (.gitignore)

```gitignore
# Python
__pycache__/
*.py[cod]
venv/
ENV/

# Django
*.log
db.sqlite3
/static/
/media/

# Entorno
.env
.env.local

# IDEs
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

---

## ✅ Verificaciones Completadas

### Tests de Funcionamiento
- [x] Python 3.11 instalado y funcionando
- [x] Git configurado correctamente
- [x] PostgreSQL iniciado y accesible
- [x] Entorno virtual creado y activado
- [x] Django instalado (versión 5.2.7)
- [x] Base de datos creada con permisos correctos
- [x] Migraciones aplicadas sin errores
- [x] Superusuario creado
- [x] Servidor de desarrollo funciona en http://localhost:8000
- [x] Panel de administración accesible en http://localhost:8000/admin
- [x] VS Code conectado a WSL correctamente
- [x] Intérprete de Python seleccionado en VS Code
- [x] Git inicializado con 2 commits

---

## 🚀 Comandos Útiles de Referencia

### Inicio de Sesión de Desarrollo

```bash
# 1. Abrir terminal Ubuntu (WSL)
# 2. Navegar al proyecto
cd ~/proyectos/etsy-inventory-saas

# 3. Activar entorno virtual
source venv/bin/activate

# 4. Asegurar que PostgreSQL esté corriendo
sudo service postgresql start

# 5. Abrir VS Code (opcional)
code .

# 6. Ejecutar servidor de desarrollo
python manage.py runserver
```

### Comandos Django Frecuentes

```bash
# Crear migraciones después de cambiar modelos
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver

# Shell interactivo de Django
python manage.py shell

# Ejecutar tests
python manage.py test
```

### Comandos Git Frecuentes

```bash
# Ver estado
git status

# Ver diferencias
git diff

# Agregar archivos
git add .

# Hacer commit
git commit -m "mensaje descriptivo"

# Ver historial
git log --oneline

# Ver ramas
git branch
```

---

## 🎯 Estado Actual: LISTO PARA DESARROLLO

El entorno está completamente configurado y funcional. Próximo paso: comenzar a desarrollar las aplicaciones y modelos del proyecto.

---

## 📝 Notas Importantes

1. **Siempre activar el entorno virtual** antes de trabajar
2. **Iniciar PostgreSQL** si la terminal fue cerrada (`sudo service postgresql start`)
3. **Nunca subir .env a Git** - contiene secretos
4. **Hacer commits frecuentes** con mensajes descriptivos
5. **Probar cambios antes de hacer commit** con `python manage.py check`