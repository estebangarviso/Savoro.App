# Guía de Instalación - Savoro.App

Esta guía proporciona instrucciones detalladas para configurar el entorno de desarrollo de Savoro.App.

## Prerrequisitos

### Python

- **Versión requerida**: Python 3.10 hasta 3.13 (según `Pipfile`)
- Python debe estar instalado y configurado en el PATH del sistema
- **Descargar**: [python.org/downloads](https://www.python.org/downloads/)

**Verificar instalación de Python:**
```bash
# Verificar versión de Python
python --version  # o python3 --version

# Verificar que Python está en el PATH
which python  # macOS/Linux
where python  # Windows
```

**Instalación de Python por sistema operativo:**

- **macOS**: `brew install python@3.12` ([Homebrew](https://brew.sh/))
- **Ubuntu/Debian**: `sudo apt install python3.12 python3.12-venv`
- **Windows**: Descargar desde [python.org](https://www.python.org/downloads/) (marcar "Add Python to PATH")

### Pipenv

- **Gestor de entornos virtuales y dependencias** para Python
- **Documentación**: [pipenv.pypa.io](https://pipenv.pypa.io/en/latest/)

**Instalar pipenv:**
```bash
pip install pipenv  # o pip3 install pipenv

# Verificar instalación
pipenv --version
```

### Otros requisitos

- **Node.js 20+**: [nodejs.org](https://nodejs.org/) (opcional, para desarrollo frontend)
- **pnpm**: [pnpm.io/installation](https://pnpm.io/installation) (opcional, gestor de paquetes JavaScript)
- **Git**: [git-scm.com/downloads](https://git-scm.com/downloads)

## Guía de Inicio Rápido

### Setup Automático (Recomendado)

```bash
# Configuración completa del proyecto
pnpm run setup

# Cargar datos iniciales (opcional)
pnpm run loaddata

# Crear superusuario
pnpm run superuser

# Iniciar desarrollo
pnpm run dev
```

### Setup Manual

### 1. Configurar Entorno Python

```bash
# Crear y activar entorno virtual
pipenv shell

# Instalar dependencias Python
pipenv install
```

**Si tu sistema usa `python3` en lugar de `python`:**

Algunos sistemas (especialmente macOS y Linux) tienen `python3` en el PATH pero no `python`. En estos casos, especifica la versión de Python al crear el entorno:

```bash
# Opción 1: Especificar python3
pipenv --python python3 install
pipenv --python python3 shell

# Opción 2: Especificar ruta completa
pipenv --python $(which python3) install
pipenv --python $(which python3) shell

# Opción 3: Especificar versión específica
pipenv --python 3.12 install
```

### 2. Configurar Base de Datos

```bash
# Ejecutar migraciones
python apps/backend/manage.py makemigrations
python apps/backend/manage.py migrate

# Crear superusuario
python apps/backend/manage.py createsuperuser
# Usuario recomendado: admin
# Email: admin@savoro.app
# Password: (tu contraseña segura)

# Poblar datos de prueba (opcional)
# Carga fixtures con categorías, etiquetas y platos de ejemplo
pnpm run loaddata
# O manualmente: python apps/backend/manage.py loaddata initial_data
```

**Configuración de entornos:**

El proyecto usa diferentes settings según el entorno:

```bash
# Desarrollo (default)
python apps/backend/manage.py runserver --settings=config.settings.development

# Producción
python apps/backend/manage.py runserver --settings=config.settings.production

# O configurar variable de entorno
export DJANGO_SETTINGS_MODULE=config.settings.development
```

Archivos de configuración:

- `apps/backend/config/settings/base.py`: Configuración compartida
- `apps/backend/config/settings/development.py`: Debug activado, SQLite
- `apps/backend/config/settings/production.py`: Debug desactivado, PostgreSQL

### 3. Configurar Frontend (Opcional)

```bash
# Instalar dependencias Node.js
cd apps/frontend
pnpm install

# Compilar assets con Vite (producción)
pnpm run build

# O ejecutar en modo desarrollo con recarga en caliente
pnpm run dev

# Verificar código JavaScript
pnpm run lint

# Formatear código
pnpm run format
```

**Sobre Vite:**

Vite es el empaquetador de módulos utilizado para compilar y optimizar los archivos JavaScript y CSS. Escanea automáticamente los archivos en `src/*/static/` y genera:

- **Archivos minificados** para producción
- **Sourcemaps** (`.js.map`, `.css.map`) para debugging
- **Manifest** (`.vite/manifest.json`) para mapeo de assets

**Modos de desarrollo:**

```bash
# Desarrollo con HMR (Hot Module Replacement)
pnpm run dev          # Inicia servidor en localhost:5173

# Compilación con vigilancia de cambios
pnpm run build:watch  # Recompila automáticamente al guardar

# Vista previa de build de producción
pnpm run preview      # Sirve build en localhost:4173
```

Los assets compilados se generan en `apps/frontend/staticfiles/` y se integran automáticamente con Django.

### 4. Ejecutar Servidor

```bash
python apps/backend/manage.py runserver
```

Acceder a:

- **Aplicación**: http://localhost:8000
- **Admin**: http://localhost:8000/admin

## Solución de Problemas

### Error al instalar Pillow
Si encuentras errores al instalar Pillow, asegúrate de tener las dependencias del sistema instaladas:

**macOS**:
```bash
brew install libjpeg zlib
```

**Ubuntu/Debian**:
```bash
sudo apt-get install python3-dev libjpeg-dev zlib1g-dev
```

### Base de datos bloqueada
Si SQLite está bloqueada, asegúrate de cerrar todas las conexiones activas o reinicia el servidor.

### Puerto 8000 ocupado
Si el puerto 8000 está en uso, puedes especificar otro puerto:
```bash
python apps/backend/manage.py runserver 8001
```
