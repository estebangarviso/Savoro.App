# Referencia de Comandos - Savoro.App

## 🚀 Comandos Simplificados (Recomendado)

Hay **3 formas** de ejecutar los comandos principales:

### 1. Scripts de Shell (Más visual)

Ubicados en `scripts/` para mantener el proyecto organizado.

| Comando                   | Descripción                                                |
| ------------------------- | ---------------------------------------------------------- |
| `./scripts/setup.sh`      | Configuración inicial completa del proyecto                |
| `./scripts/start-dev.sh`  | Compilar assets + collectstatic + iniciar Django           |
| `./scripts/build-prod.sh` | Build de producción completo (Vite + Django + migraciones) |

> **💡 Nota**: Los scripts de limpieza son **dinámicos** y detectan automáticamente  
> todos los módulos en `modules/` y `shared/` sin necesidad de actualizarlos manualmente.

### 2. Makefile (Más limpio)

| Comando          | Descripción                        |
| ---------------- | ---------------------------------- |
| `make help`      | Ver todos los comandos disponibles |
| `make setup`     | Configuración inicial completa     |
| `make dev`       | Iniciar desarrollo                 |
| `make prod`      | Build de producción                |
| `make build`     | Solo compilar assets               |
| `make clean`     | Limpiar archivos generados         |
| `make migrate`   | Ejecutar migraciones               |
| `make superuser` | Crear superusuario                 |
| `make test`      | Ejecutar tests                     |
| `make lint`      | Verificar código                   |
| `make format`    | Formatear código                   |
| `make watch`     | Vite en modo watch                 |

### 3. Scripts npm

| Comando               | Descripción                         |
| --------------------- | ----------------------------------- |
| `pnpm run setup`      | Instalar dependencias + migraciones |
| `pnpm run start:dev`  | Build + collectstatic + runserver   |
| `pnpm run start:prod` | Build de producción + collectstatic |

---

## 🛠️ Comandos Detallados

## Comandos Python/Django

### Gestión de Entorno

| Comando                   | Descripción                                        |
| ------------------------- | -------------------------------------------------- |
| `pipenv shell`            | Activar entorno virtual                            |
| `pipenv install --dev`    | Instalar dependencias para producción y desarrollo |
| `pipenv install --deploy` | Instalar dependencias para producción              |
| `pipenv update`           | Actualizar dependencias                            |

### Servidor y Base de Datos

| Comando                                        | Descripción                            |
| ---------------------------------------------- | -------------------------------------- |
| `python apps/backend/manage.py runserver`      | Iniciar servidor de desarrollo         |
| `python apps/backend/manage.py runserver 8001` | Iniciar servidor en puerto específico  |
| `python apps/backend/manage.py migrate`        | Aplicar migraciones a la base de datos |
| `python apps/backend/manage.py makemigrations` | Crear nuevas migraciones               |
| `python apps/backend/manage.py showmigrations` | Mostrar estado de migraciones          |
| `python apps/backend/manage.py dbshell`        | Abrir shell de base de datos           |

### Gestión de Usuarios

| Comando                                         | Descripción                 |
| ----------------------------------------------- | --------------------------- |
| `python apps/backend/manage.py createsuperuser` | Crear usuario administrador |
| `python apps/backend/manage.py changepassword`  | Cambiar contraseña          |

### Datos y Contenido

| Comando                                   | Descripción            |
| ----------------------------------------- | ---------------------- |
| `python apps/backend/manage.py seed_data` | Poblar datos iniciales |
| `python apps/backend/manage.py flush`     | Limpiar base de datos  |
| `python apps/backend/manage.py loaddata`  | Cargar fixtures        |
| `python apps/backend/manage.py dumpdata`  | Exportar datos         |

### Archivos Estáticos

| Comando                                       | Descripción                  |
| --------------------------------------------- | ---------------------------- |
| `python apps/backend/manage.py collectstatic` | Recopilar archivos estáticos |
| `python apps/backend/manage.py findstatic`    | Buscar archivo estático      |

### Testing y Calidad

| Comando                                    | Descripción               |
| ------------------------------------------ | ------------------------- |
| `python apps/backend/manage.py test`       | Ejecutar todos los tests  |
| `python apps/backend/manage.py test <app>` | Ejecutar tests de una app |
| `pylint **/*.py`                           | Análisis estático         |

### Utilidades

| Comando                                  | Descripción                 |
| ---------------------------------------- | --------------------------- |
| `python apps/backend/manage.py shell`    | Shell interactivo de Django |
| `python apps/backend/manage.py check`    | Verificar proyecto          |
| `python apps/backend/manage.py startapp` | Crear nueva aplicación      |

## Comandos JavaScript/Node

### Gestión de Paquetes

| Comando                            | Descripción             |
| ---------------------------------- | ----------------------- |
| `cd apps/frontend && pnpm install` | Instalar dependencias   |
| `cd apps/frontend && pnpm update`  | Actualizar dependencias |
| `cd apps/frontend && pnpm add`     | Agregar paquete         |

### Build y Desarrollo (Vite)

| Comando                                    | Descripción                                          |
| ------------------------------------------ | ---------------------------------------------------- |
| `cd apps/frontend && pnpm run dev`         | Iniciar servidor Vite con HMR (localhost:5173)       |
| `cd apps/frontend && pnpm run build`       | Compilar assets para producción con sourcemaps       |
| `cd apps/frontend && pnpm run build:watch` | Compilar en modo vigilancia (recompila al guardar)   |
| `cd apps/frontend && pnpm run preview`     | Vista previa de build de producción (localhost:4173) |

### Linting y Formateo

| Comando                                     | Descripción                                 |
| ------------------------------------------- | ------------------------------------------- |
| `cd apps/frontend && pnpm run lint`         | Verificar código JavaScript con ESLint      |
| `cd apps/frontend && pnpm run lint:fix`     | Corregir errores JavaScript automáticamente |
| `cd apps/frontend && pnpm run format`       | Formatear código (JS, CSS, HTML, JSON)      |
| `cd apps/frontend && pnpm run format:check` | Verificar formato sin modificar archivos    |

## Comandos Git Flow

### Inicialización

```bash
git flow init
```

### Features

```bash
# Crear feature
git flow feature start <nombre>

# Publicar feature
git flow feature publish <nombre>

# Finalizar feature
git flow feature finish <nombre>
```

### Hotfixes

```bash
# Crear hotfix
git flow hotfix start <versión>

# Finalizar hotfix
git flow hotfix finish <versión>
```

### Releases

```bash
# Crear release
git flow release start <versión>

# Finalizar release
git flow release finish <versión>
```

## Atajos Útiles

### Desarrollo Rápido

```bash
# Activar entorno y ejecutar servidor
pipenv shell && python apps/backend/manage.py runserver

# Migraciones completas
python apps/backend/manage.py makemigrations && python apps/backend/manage.py migrate

# Limpiar y repoblar base de datos
python apps/backend/manage.py flush --noinput && python apps/backend/manage.py seed_data
```

### Testing

```bash
# Tests con coverage
cd apps/backend
coverage run --source='.' manage.py test
coverage report

# Tests específicos
python apps/backend/manage.py test modules.dish.tests
```

### Formateo de Código

```bash
# Formatear todo
cd apps/frontend && pnpm run format
cd apps/backend && black . && isort .

# Verificar todo
cd apps/frontend && pnpm run lint
cd apps/backend && pylint **/*.py
```
