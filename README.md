# Savoro.App

<p align="center">
  <a href="https://docs.djangoproject.com/en/4.2/intro/overview/" target="blank"><img src="https://static.djangoproject.com/img/logos/django-logo-negative.svg" width="120" alt="Django Logo" /></a>
</p>

<p align="center">
Sistema de gestión de restaurante con arquitectura monorepo.
</p>

## 📦 Estructura del Monorepo

```
SavoroApp/
├── apps/
│   ├── backend/        # Django REST API
│   └── frontend/       # Vite + Materialize CSS assets
├── docs/               # Documentación técnica
└── scripts/            # Scripts de automatización
```

## 🚀 Inicio Rápido

### Setup Completo

Configura backend (Django + Python) y frontend (Vite + Node) automáticamente:

```bash
# Opción 1: Script de shell (recomendado)
./scripts/setup.sh

# Opción 2: Makefile
make setup

# Opción 3: pnpm
pnpm run setup
```

Luego crea un superusuario para acceder al admin:

```bash
make superuser
# o
pipenv run python apps/backend/manage.py createsuperuser
```

### Desarrollo

Inicia servidor Django + build watcher de Vite:

```bash
# Opción 1: Script de shell (recomendado)
./scripts/start-dev.sh

# Opción 2: Makefile
make dev

# Opción 3: pnpm
pnpm run start:dev
```

Accede a la aplicación en **http://localhost:8000**

### Producción

Compila assets optimizados y ejecuta con configuración de producción:

```bash
# Opción 1: Script de shell
./scripts/build-prod.sh

# Opción 2: Makefile
make prod

# Opción 3: pnpm
pnpm run start:prod
```

## 🏗️ Aplicaciones

### [Backend (Django)](apps/backend/README.md)

API REST y panel de administración con arquitectura modular inspirada en NestJS:

- **Tecnologías**: Django 4.2+, Python 3.10-3.13, SQLite/PostgreSQL
- **Patrón**: Controller → Service → Repository
- **Módulos**: `dish`, `category`, `food_tag`, `authentication`, `order`, `reservation`, `menu`, `table`
- **Características**: Soft delete, localización chilena, type safety, validaciones custom

**Comandos principales**:
```bash
cd apps/backend
pipenv shell                # Activar entorno virtual
python manage.py migrate    # Aplicar migraciones
python manage.py runserver  # Iniciar servidor
```

Ver [apps/backend/README.md](apps/backend/README.md) para documentación completa del backend.

### [Frontend (Vite)](apps/frontend/README.md)

Build system y assets con Vite + Materialize CSS:

- **Tecnologías**: Vite 5.4+, Materialize CSS 1.0, ESLint, Prettier
- **Características**: HMR, code splitting, tree shaking, minificación
- **Integración**: Genera assets que Django sirve desde `staticfiles/`

**Comandos principales**:
```bash
cd apps/frontend
pnpm install           # Instalar dependencias
pnpm run dev           # Dev server con HMR (port 5173)
pnpm run build         # Compilar para producción
pnpm run build:watch   # Compilar con vigilancia de cambios
```

Ver [apps/frontend/README.md](apps/frontend/README.md) para documentación completa del frontend.

## 📚 Documentación

- **[Guía de Instalación](docs/SETUP.md)** - Setup detallado de entornos Python y Node
- **[Arquitectura del Proyecto](docs/ARCHITECTURE.md)** - Patrones de diseño, estructura modular
- **[Guía de Contribución](docs/CONTRIBUTING.md)** - Git Flow, Conventional Commits
- **[Referencia de Comandos](docs/COMMANDS.md)** - Comandos Django, pnpm, Make
- **[Patrones JavaScript](docs/JAVASCRIPT_PATTERNS.md)** - Custom Events, MutationObserver

## ✨ Características Principales

### Backend

- 🍽️ **Gestión de Platos**: CRUD con imágenes, categorías y etiquetas
- 📋 **Categorías y Tags**: Organización con estadísticas
- 👤 **Autenticación**: Login/logout con decoradores de permisos
- 🔍 **Búsqueda Avanzada**: Normalización de texto sin acentos
- 🗑️ **Soft Delete**: Eliminación lógica en todos los modelos
- 🌐 **Localización**: Formato chileno para fechas y moneda

### Frontend

- 🎨 **UI Moderna**: Materialize CSS con animaciones
- ⚡ **Vite Build**: Assets optimizados con sourcemaps
- 🔥 **HMR**: Hot Module Replacement en desarrollo
- 📦 **Code Splitting**: Lazy loading de módulos
- 🧩 **Modular**: Custom Events para comunicación entre módulos

## 🛠️ Tecnologías

| Categoría      | Tecnología                      |
| -------------- | ------------------------------- |
| **Backend**    | Django 4.2+, Python 3.10-3.13   |
| **Frontend**   | Vite 5.4+, Materialize CSS 1.0  |
| **Database**   | SQLite (dev), PostgreSQL (prod) |
| **Build**      | Vite, ESBuild                   |
| **Package**    | pipenv (Python), pnpm (Node)    |
| **Linting**    | pylint, ESLint, Prettier        |
| **Automation** | Make, Shell scripts             |

## 💡 Comandos Útiles

### Gestión Global

```bash
# Setup completo (backend + frontend)
./scripts/setup.sh

# Desarrollo (Django server + Vite watch)
./scripts/start-dev.sh

# Producción (build + Django production)
./scripts/build-prod.sh
```

### Backend (Django)

```bash
# Desde raíz del proyecto
make migrate          # Aplicar migraciones
make superuser        # Crear admin
make shell            # Django shell

# O directo con pipenv
pipenv run python apps/backend/manage.py runserver
```

### Frontend (Vite)

```bash
# Desde apps/frontend/
pnpm run dev          # Dev server con HMR
pnpm run build        # Build de producción
pnpm run lint         # Verificar código
pnpm run format       # Formatear archivos
```

## 📋 Requisitos

- **Python 3.10 - 3.13**: Backend Django → [Descargar](https://www.python.org/downloads/)
- **pipenv**: Gestión de entornos Python → [Instalar](https://pipenv.pypa.io/en/latest/installation.html)
- **Node.js 18+**: Build frontend → [Descargar](https://nodejs.org/)
- **pnpm**: Gestor de paquetes rápido → [Instalar](https://pnpm.io/installation)

Verifica tus versiones:
```bash
python --version    # >= 3.10
pipenv --version
node --version      # >= 20
pnpm --version
```

## 📖 Flujo de Trabajo

1. **Instala las dependencias**: `make setup`
2. **Crea un superusuario**: `make superuser`
3. **Opciones de desarrollo**:
   1. **Modo Debug**: Presiona `F5` en VS Code para ejecutar la aplicación en modo *Full Stack Debug*. Esto inicia tanto el frontend como el backend en modo depuración, permitiendo establecer breakpoints en Python y JavaScript sin necesidad de agregar `debugger;` en el código JS.
   2. **Modo Normal**:
       1. **Inicia el frontend**: `make hmr`
       2. **Inicia el backend**: `make dev`
       3. **Accede al panel de administración**: <http://localhost:8000/admin>
       4. **Edita el frontend**: Los cambios en `apps/frontend/src/` se reflejan automáticamente.
       5. **Edita el backend**: Al guardar archivos `.py`, Django recarga el servidor automáticamente.

## 🤝 Contribuir

Ver [CONTRIBUTING.md](docs/CONTRIBUTING.md) para:

- Git Flow (feature/hotfix/release)
- Conventional Commits
- Estándares de código
- Testing guidelines

## 📄 Licencia

[Especificar licencia aquí]
