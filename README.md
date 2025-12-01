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
└── docs/               # Documentación técnica
```

## 🚀 Inicio Rápido

```bash
# 1. Instalar dependencias
pnpm run setup

# 2. Crear superusuario
pnpm run superuser

# 3. Iniciar desarrollo (2 terminales)
pnpm run dev:frontend  # Terminal 1: JavaScript Debug Terminal
pnpm run dev:backend   # Terminal 2: Django server
```

**Acceso:** <http://localhost:8000> (Django) | <http://localhost:5173> (Vite HMR)

> 💡 **VS Code:** Presiona `F5` para iniciar en modo *Full Stack Debug* automáticamente

## 🏗️ Aplicaciones

| App          | Tecnologías                    | Documentación                       |
| ------------ | ------------------------------ | ----------------------------------- |
| **Backend**  | Django 4.2+, Python 3.10-3.13  | [Ver docs](apps/backend/README.md)  |
| **Frontend** | Vite 5.4+, Materialize CSS 1.0 | [Ver docs](apps/frontend/README.md) |

**Patrón Backend:** Controller → Service → Repository (inspirado en NestJS)  
**Características:** Soft delete, localización chilena, type safety, HMR

## 💡 Comandos Principales

```bash
# Desarrollo
pnpm run dev:frontend      # Vite dev server (puerto 5173)
pnpm run dev:backend       # Django server (puerto 8000)

# Producción
pnpm run build:prod        # Build completo + migraciones

# Utilidades
pnpm run migrate           # Aplicar migraciones
pnpm run superuser         # Crear admin
pnpm run lint              # Verificar código
pnpm run test              # Ejecutar tests
```

Ver [Referencia Completa de Comandos](docs/COMMANDS.md)

## 📚 Documentación

- **[Guía de Instalación](docs/SETUP.md)** - Requisitos y configuración detallada
- **[Arquitectura del Proyecto](docs/ARCHITECTURE.md)** - Patrones y estructura modular
- **[Referencia de Comandos](docs/COMMANDS.md)** - Comandos Django, pnpm y workflows
- **[Guía de Contribución](docs/CONTRIBUTING.md)** - Git Flow y estándares
- **[Patrones JavaScript](docs/JAVASCRIPT_PATTERNS.md)** - Custom Events y MutationObserver

## 🛠️ Stack Tecnológico

| Categoría       | Tecnología                      |
| --------------- | ------------------------------- |
| Backend         | Django 4.2+, Python 3.10-3.13   |
| Frontend        | Vite 5.4+, Materialize CSS 1.0  |
| Database        | SQLite (dev), PostgreSQL (prod) |
| Package Manager | pipenv (Python), pnpm (Node)    |
| Automation      | pnpm workspaces                 |

## 📋 Requisitos

- **Python 3.10-3.13** → [python.org](https://www.python.org/downloads/)
- **pipenv** → [pipenv.pypa.io](https://pipenv.pypa.io/en/latest/installation.html)
- **Node.js 20+** → [nodejs.org](https://nodejs.org/)
- **pnpm** → [pnpm.io](https://pnpm.io/installation)

```bash
# Verificar instalación
python --version && pipenv --version
node --version && pnpm --version
```

## 📖 Flujo de Desarrollo

### Opción A: Modo Debug (Recomendado)
Presiona `F5` en VS Code → Inicia frontend + backend con breakpoints activos

### Opción B: Modo Manual
1. **Terminal 1** (JavaScript Debug Terminal): `pnpm run dev:frontend`
2. **Terminal 2**: `pnpm run dev:backend`
3. Accede a <http://localhost:8000/admin>

**HMR activo:** Cambios en `apps/frontend/src/` y `.py` se recargan automáticamente

## 🤝 Contribuir

Ver [CONTRIBUTING.md](docs/CONTRIBUTING.md) para Git Flow, Conventional Commits y estándares de código.

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE)
