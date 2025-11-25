# Savoro.App

<p align="center">
  <a href="https://docs.djangoproject.com/en/4.2/intro/overview/" target="blank"><img src="https://static.djangoproject.com/img/logos/django-logo-negative.svg" width="120" alt="Django Logo" /></a>
</p>

<p align="center">
Sistema de gestión de restaurante desarrollado con Django y Materialize CSS.
</p>

## 📋 Requisitos Previos

- **Python 3.10 - 3.13** instalado y configurado en el PATH del sistema → [Descargar Python](https://www.python.org/downloads/)
- **pipenv** para gestión de entornos virtuales → [Instalar pipenv](https://pipenv.pypa.io/en/latest/installation.html)
- **pnpm** (opcional, para desarrollo frontend) → [Instalar pnpm](https://pnpm.io/installation)

Verifica tu versión de Python:
```bash
python --version  # o python3 --version
```

> **Nota**: Si tu sistema usa `python3` en lugar de `python`, especifica la ruta al ejecutar pipenv:  
> `pipenv --python python3 install` o `pipenv --python $(which python3) shell`

## ✨ Características

- 🍽️ **Gestión de Platos**: CRUD completo con imágenes, precios, categorías y etiquetas
- 📋 **Categorías**: Organización de platos por categorías con estadísticas
- 🏷️ **Etiquetas**: Sistema de tags para clasificación alimentaria (vegano, sin gluten, etc.)
- 👤 **Autenticación**: Sistema de login/logout con decoradores de permisos
- 🔍 **Búsqueda Avanzada**: Búsqueda sin acentos con normalización de texto
- 🎨 **UI Moderna**: Interfaz responsive con Materialize CSS y animaciones
- 📊 **Panel Admin**: Administración completa con Django Admin
- 🗑️ **Soft Delete**: Eliminación lógica (no física) en todos los modelos
- 🌐 **Localización**: Formato chileno para fechas, números y moneda
- ⚡ **Vite Build**: Assets optimizados con HMR y code splitting
- 🔒 **Type Safety**: Type hints extensivos en Python con pylint
- 🧩 **Arquitectura Modular**: Estructura inspirada en NestJS (Controller → Service → Repository)

## 🚀 Inicio Rápido

### Primera vez (Setup completo)

```bash
# Opción 1: Script de shell
./scripts/setup.sh

# Opción 2: Makefile
make setup

# Opción 3: npm
pnpm run setup
```

Luego crea un superusuario:
```bash
pipenv run python manage.py createsuperuser
# o
make superuser
```

### Desarrollo

```bash
# Opción 1: Script de shell (recomendado)
./scripts/start-dev.sh

# Opción 2: Makefile
make dev

# Opción 3: npm
pnpm run start:dev
```

### Producción

```bash
# Opción 1: Script de shell
./scripts/build-prod.sh

# Opción 2: Makefile
make prod

# Opción 3: npm
pnpm run start:prod
```

Accede a la aplicación en http://localhost:8000

> **💡 Tip**: El proyecto incluye **3 formas** de ejecutar comandos:  
> `./scripts/script.sh` (shell) | `make comando` (Makefile) | `pnpm run comando` (npm)  
> Elige la que prefieras. Ver [Referencia Completa](docs/COMMANDS.md)

## 📚 Documentación

- **[Guía de Instalación](docs/SETUP.md)** - Instrucciones detalladas de configuración
- **[Arquitectura del Proyecto](docs/ARCHITECTURE.md)** - Estructura, patrones de diseño y tecnologías
- **[Guía de Contribución](docs/CONTRIBUTING.md)** - Git Flow, convenciones y estándares
- **[Referencia de Comandos](docs/COMMANDS.md)** - Lista completa de comandos disponibles

## 🛠️ Tecnologías Principales

**Backend**: Django 4.2+ • Python 3.10+ • SQLite (dev) / PostgreSQL (prod)  
**Frontend**: Materialize CSS 1.0.0 • Vanilla JavaScript (ES Modules) • CSS Variables  
**Build Tools**: Vite • pnpm • pipenv  
**DevTools**: pylint • black • isort • djlint • ESLint • Prettier

## 🤝 Contribuir

Seguimos [Git Flow](docs/CONTRIBUTING.md#flujo-de-trabajo-git-flow) y [Conventional Commits](https://www.conventionalcommits.org/). Consulta la [Guía de Contribución](docs/CONTRIBUTING.md) para más detalles.

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
