# Referencia de Comandos - Savoro.App

## 🚀 Comandos Principales

Todos los comandos se ejecutan desde la raíz del proyecto usando **pnpm**.

### Configuración y Desarrollo

| Comando                 | Descripción                                                |
| ----------------------- | ---------------------------------------------------------- |
| `pnpm run setup`        | Configuración inicial completa del proyecto                |
| `pnpm run dev`          | Compilar assets + collectstatic + iniciar Django           |
| `pnpm run dev:frontend` | Iniciar Vite dev server con HMR (localhost:5173)           |
| `pnpm run dev:backend`  | Iniciar solo Django server (localhost:8000)                |
| `pnpm run build:prod`   | Build de producción completo (Vite + Django + migraciones) |
| `pnpm run build`        | Solo compilar assets con Vite                              |
| `pnpm run build:watch`  | Compilar assets en modo watch                              |
| `pnpm run clean`        | Limpiar archivos generados de Vite                         |
| `pnpm run migrate`      | Ejecutar migraciones de Django                             |
| `pnpm run loaddata`     | Cargar datos iniciales desde fixtures                      |
| `pnpm run superuser`    | Crear superusuario                                         |
| `pnpm run test`         | Ejecutar tests de Django                                   |
| `pnpm run lint`         | Verificar código (Python + JavaScript)                     |
| `pnpm run lint:fix`     | Corregir errores automáticamente                           |
| `pnpm run format`       | Formatear código (Python + JavaScript)                     |

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

| Comando                                               | Descripción                           |
| ----------------------------------------------------- | ------------------------------------- |
| `python apps/backend/manage.py loaddata initial_data` | Cargar datos iniciales desde fixtures |
| `python apps/backend/manage.py dumpdata <app.model>`  | Exportar datos a JSON                 |
| `python apps/backend/manage.py flush`                 | Limpiar base de datos completamente   |
| `python apps/backend/manage.py loaddata <fixture>`    | Cargar fixtures personalizados        |

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
| `mypy .`                                   | Verificar tipos de Python |
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

## Gestión de Fixtures (Datos Iniciales)

Django proporciona comandos nativos para exportar e importar datos en formato JSON. Esto es útil para compartir datos de ejemplo entre entornos o crear datos iniciales.

### Cargar Fixtures

```bash
# Cargar fixture de datos iniciales (categorías, tags, platos)
python apps/backend/manage.py loaddata initial_data

# Cargar múltiples fixtures
python apps/backend/manage.py loaddata categories dishes tags

# Cargar desde ruta específica
python apps/backend/manage.py loaddata fixtures/custom_data.json
```

### Exportar Datos (dumpdata)

```bash
# Exportar todos los datos de una app
python apps/backend/manage.py dumpdata dish --indent 2 > fixtures/dishes.json

# Exportar modelo específico
python apps/backend/manage.py dumpdata category.category --indent 2 > fixtures/categories.json

# Exportar múltiples apps
python apps/backend/manage.py dumpdata category dish food_tag --indent 2 > fixtures/restaurant_data.json

# Exportar excluyendo apps (útil para evitar auth, sessions, etc.)
python apps/backend/manage.py dumpdata --exclude auth --exclude contenttypes --indent 2 > fixtures/data.json

# Exportar usando natural keys (usa identificadores naturales en lugar de PKs)
python apps/backend/manage.py dumpdata --natural-foreign --natural-primary --indent 2 > fixtures/natural_data.json
```

### Limpiar y Repoblar Base de Datos

```bash
# Eliminar todos los datos pero mantener estructura
python apps/backend/manage.py flush --noinput

# Limpiar y cargar datos iniciales
python apps/backend/manage.py flush --noinput && python apps/backend/manage.py loaddata initial_data

# Reset completo (borrar DB, recrear, migrar y poblar)
rm apps/backend/db.sqlite3
python apps/backend/manage.py migrate
python apps/backend/manage.py loaddata initial_data
```

### Estructura de Fixtures

Los fixtures están en formato JSON con la siguiente estructura:

```json
[
  {
    "model": "app.modelname",
    "pk": 1,
    "fields": {
      "field1": "value",
      "foreign_key_field": 2,
      "many_to_many_field": [1, 2, 3]
    }
  }
]
```

**Manejo de relaciones:**
- **ForeignKey**: Usa el PK del objeto relacionado
- **ManyToMany**: Lista de PKs de objetos relacionados
- Django respeta el orden y resuelve dependencias automáticamente

## Atajos Útiles

### Desarrollo Rápido

```bash
# Activar entorno y ejecutar servidor
pipenv shell && python apps/backend/manage.py runserver

# Migraciones completas
python apps/backend/manage.py makemigrations && python apps/backend/manage.py migrate

# Limpiar y repoblar base de datos
python apps/backend/manage.py flush --noinput && python apps/backend/manage.py loaddata initial_data

# Exportar datos actuales a fixture
python apps/backend/manage.py dumpdata category dish food_tag --indent 2 > fixtures/my_data.json
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
cd apps/backend && pylint **/*.py && mypy .
```
