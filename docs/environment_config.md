# Configuración de Entorno - Referencia Rápida

## 🔐 Credenciales y Accesos

### Sistema WSL
```
Usuario: yamil
Password: 123456
```

### PostgreSQL
```
Base de datos: etsy_inventory_db
Usuario: etsy_user
Password: password_seguro_123
Host: localhost
Puerto: 5432
```

### Django Admin
```
URL: http://localhost:8000/admin
Username: admin
Email: yamilpalmiero@gmail.com
Password: [tu password configurada]
```

### Git
```
Nombre: Yamil
Email: yamilpalmiero@gmail.com
Rama por defecto: main
```

---

## 📂 Rutas Importantes

### Proyecto
```bash
# Ruta en Linux (WSL)
/home/yamil/proyectos/etsy-inventory-saas/

# Ruta en Windows (Explorador)
\\wsl$\Ubuntu\home\yamil\proyectos\etsy-inventory-saas

# Acceso rápido desde WSL
cd ~/proyectos/etsy-inventory-saas
```

### Entorno Virtual
```bash
# Ubicación
/home/yamil/proyectos/etsy-inventory-saas/venv/

# Activación
source venv/bin/activate

# Desactivación
deactivate
```

---

## 🔧 Variables de Entorno (.env)

### Archivo Completo Actual

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

# Etsy API (rellenar cuando crees la app en Etsy)
ETSY_CLIENT_ID=
ETSY_CLIENT_SECRET=
ETSY_REDIRECT_URI=http://localhost:8000/auth/etsy/callback/

# Email (configurar cuando sea necesario)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```

### Cómo Usar Variables de Entorno

En cualquier archivo Python del proyecto:

```python
from decouple import config

# Obtener valor
api_key = config('ETSY_CLIENT_ID')

# Con valor por defecto
debug = config('DEBUG', default=False, cast=bool)

# Convertir a entero
port = config('DB_PORT', cast=int)
```

---

## 🗄️ Comandos PostgreSQL

### Gestión del Servicio

```bash
# Iniciar PostgreSQL
sudo service postgresql start

# Verificar estado
sudo service postgresql status

# Detener (no recomendado durante desarrollo)
sudo service postgresql stop

# Reiniciar
sudo service postgresql restart
```

### Acceso a la Base de Datos

```bash
# Acceder como superusuario postgres
sudo -u postgres psql

# Acceder directamente a la BD del proyecto
sudo -u postgres psql -d etsy_inventory_db

# Acceder como etsy_user
psql -U etsy_user -d etsy_inventory_db -h localhost
# Password: password_seguro_123
```

### Comandos Útiles en psql

```sql
-- Listar todas las bases de datos
\l

-- Conectarse a una base de datos
\c etsy_inventory_db

-- Listar tablas
\dt

-- Describir una tabla
\d nombre_tabla

-- Listar usuarios
\du

-- Ejecutar query
SELECT * FROM django_migrations;

-- Salir
\q
```

### Crear Backup

```bash
# Backup de la base de datos
sudo -u postgres pg_dump etsy_inventory_db > backup_$(date +%Y%m%d).sql

# Restaurar desde backup
sudo -u postgres psql etsy_inventory_db < backup_20251005.sql
```

---

## 🐍 Gestión de Dependencias Python

### Ver Dependencias Instaladas

```bash
pip list
pip freeze
```

### Instalar Nueva Dependencia

```bash
# Instalar
pip install nombre-libreria

# Actualizar requirements.txt
pip freeze > requirements.txt

# Hacer commit del cambio
git add requirements.txt
git commit -m "deps: add nombre-libreria"
```

### Reinstalar Todas las Dependencias

```bash
# Útil cuando clonas el proyecto en otra máquina
pip install -r requirements.txt
```

### Actualizar Dependencia

```bash
# Actualizar a última versión
pip install --upgrade nombre-libreria

# Actualizar requirements.txt
pip freeze > requirements.txt
```

---

## 🚀 Flujo de Trabajo Diario

### Inicio de Sesión de Trabajo

```bash
# 1. Abrir terminal Ubuntu (WSL)

# 2. Ir al proyecto
cd ~/proyectos/etsy-inventory-saas

# 3. Activar entorno virtual
source venv/bin/activate

# 4. Iniciar PostgreSQL (si no está corriendo)
sudo service postgresql start

# 5. Abrir VS Code (opcional)
code .

# 6. Crear rama para nueva feature (opcional)
git checkout -b feature/nombre-feature

# 7. Iniciar servidor de desarrollo
python manage.py runserver
```

### Antes de Terminar el Día

```bash
# 1. Detener servidor (Ctrl+C)

# 2. Verificar cambios
git status
git diff

# 3. Hacer commit si hay cambios
git add .
git commit -m "descripción de cambios"

# 4. Push a GitHub (cuando esté configurado)
git push origin nombre-rama

# 5. Desactivar entorno virtual (opcional)
deactivate
```

---

## 🧪 Testing y Calidad de Código

### Ejecutar Tests

```bash
# Todos los tests
python manage.py test

# Tests de una app específica
python manage.py test nombre_app

# Con más detalle
python manage.py test --verbosity=2

# Con cobertura (instalar coverage primero)
coverage run --source='.' manage.py test
coverage report
```

### Verificar Código

```bash
# Check de Django (errores de configuración)
python manage.py check

# Check más estricto
python manage.py check --deploy
```

---

## 🔄 Git - Flujo de Trabajo

### Crear Feature Branch

```bash
# Crear y cambiar a nueva rama
git checkout -b feature/nombre-descriptivo

# Ver en qué rama estás
git branch

# Cambiar de rama
git checkout nombre-rama
```

### Hacer Commits

```bash
# Ver qué cambió
git status
git diff

# Agregar archivos
git add .                    # Todos los archivos
git add archivo.py          # Un archivo específico

# Commit con mensaje
git commit -m "tipo: mensaje descriptivo"

# Tipos de commit sugeridos:
# feat: Nueva funcionalidad
# fix: Corrección de bug
# docs: Documentación
# style: Formato de código
# refactor: Refactorización
# test: Tests
# chore: Mantenimiento
```

### Ver Historial

```bash
# Historial resumido
git log --oneline

# Últimos 5 commits
git log --oneline -5

# Con gráfico de ramas
git log --oneline --graph --all
```

---

## 📦 VS Code - Atajos Útiles

### Atajos de Teclado

```
Ctrl+`              - Abrir/cerrar terminal integrada
Ctrl+Shift+P        - Paleta de comandos
Ctrl+P              - Buscar archivos
Ctrl+Shift+F        - Buscar en todos los archivos
Ctrl+S              - Guardar archivo
Ctrl+Shift+S        - Guardar todos
Ctrl+/              - Comentar/descomentar línea
Alt+↑/↓             - Mover línea arriba/abajo
Ctrl+D              - Seleccionar siguiente ocurrencia
F2                  - Renombrar símbolo
Ctrl+Space          - Autocompletado
```

### Terminal Integrada

```bash
# Abrir VS Code desde terminal
code .

# Abrir archivo específico
code archivo.py

# Abrir explorador de Windows en carpeta actual
explorer.exe .
```

---

## 🌐 URLs del Proyecto (Desarrollo)

```
Sitio principal:     http://localhost:8000/
Panel de admin:      http://localhost:8000/admin/
```

---

## ⚠️ Problemas Comunes y Soluciones

### PostgreSQL no inicia
```bash
sudo service postgresql start
```

### "No module named 'decouple'"
```bash
# Asegúrate de estar en el entorno virtual
source venv/bin/activate
pip install python-decouple
```

### "Permission denied" en PostgreSQL
```bash
sudo -u postgres psql -d etsy_inventory_db
GRANT ALL ON SCHEMA public TO etsy_user;
GRANT CREATE ON SCHEMA public TO etsy_user;
\q
```

### Cambios en .env no se reflejan
```bash
# Reinicia el servidor de Django
# Ctrl+C para detener
python manage.py runserver
```

### VS Code no reconoce imports
```bash
# Verificar que el intérprete correcto esté seleccionado
Ctrl+Shift+P -> "Python: Select Interpreter"
# Seleccionar ./venv/bin/python
```

---

## 📚 Recursos Adicionales

### Documentación
- Django Docs: https://docs.djangoproject.com/
- PostgreSQL Docs: https://www.postgresql.org/docs/
- Python Decouple: https://github.com/HBNetwork/python-decouple
- WSL Docs: https://docs.microsoft.com/en-us/windows/wsl/

### Comunidad
- Django Forum: https://forum.djangoproject.com/
- Stack Overflow: https://stackoverflow.com/questions/tagged/django
- Reddit r/django: https://www.reddit.com/r/django/