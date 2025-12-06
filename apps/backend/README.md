# Savoro.App - Backend (Django)

<p align="center">
  <a href="https://docs.djangoproject.com/en/4.2/intro/overview/" target="blank"><img src="https://static.djangoproject.com/img/logos/django-logo-negative.svg" width="120" alt="Django Logo" /></a>
</p>

<p align="center">
Backend del sistema de gestión de restaurante desarrollado con Django.
</p>

> **📦 Monorepo**: Este es el backend. Para el frontend Vite, ver [`apps/frontend/README.md`](../frontend/README.md). Para información general, ver el [README principal](../../README.md).

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
pnpm run setup
```

Luego crea un superusuario:
```bash
pnpm run superuser
```

### Desarrollo

```bash
pnpm run dev:backend
```

### Producción

```bash
pnpm run build:prod
```

Accede a la aplicación en http://localhost:8000

> **💡 Tip**: Todos los comandos se ejecutan desde el workspace raíz usando `pnpm run <comando>`.  
> Ver [Referencia Completa](../../docs/COMMANDS.md)

## 📚 Documentación

- **[Guía de Instalación](../../docs/SETUP.md)** - Instrucciones detalladas de configuración
- **[Arquitectura del Proyecto](../../docs/ARCHITECTURE.md)** - Estructura, patrones de diseño y tecnologías
- **[Guía de Contribución](../../docs/CONTRIBUTING.md)** - Git Flow, convenciones y estándares
- **[Referencia de Comandos](../../docs/COMMANDS.md)** - Lista completa de comandos disponibles

## 🛠️ Tecnologías Principales

**Backend**: Django 4.2+ • Python 3.10+ • SQLite (dev) / PostgreSQL (prod)  
**Frontend**: Materialize CSS 1.0.0 • Vanilla JavaScript (ES Modules) • CSS Variables  
**Build Tools**: Vite • pnpm • pipenv  
**DevTools**: mypy * pylint • black • isort • djlint • ESLint • Prettier

## 🤝 Contribuir

Seguimos [Git Flow](docs/CONTRIBUTING.md#flujo-de-trabajo-git-flow) y [Conventional Commits](https://www.conventionalcommits.org/). Consulta la [Guía de Contribución](docs/CONTRIBUTING.md) para más detalles.

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
