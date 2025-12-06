# Django Fixtures - Datos Iniciales

Este directorio contiene fixtures de Django en formato JSON para poblar la base de datos con datos de ejemplo.

## ¿Qué son los Fixtures?

Los fixtures son archivos que contienen datos serializados que Django puede cargar en la base de datos. Son útiles para:

- **Datos iniciales**: Poblar la aplicación con datos de ejemplo
- **Testing**: Crear datos consistentes para pruebas
- **Desarrollo**: Compartir datos entre el equipo
- **Migración**: Mover datos entre entornos

## Archivos Disponibles

### `initial_data.json`

Contiene datos completos del restaurante:

- **12 etiquetas alimentarias** (Vegano, Sin Gluten, Picante, etc.)
- **10 categorías** (Entradas, Ensaladas, Sopas, Pastas, etc.)
- **31 platos** con descripciones, precios y relaciones

## Uso Básico

### Cargar Datos

```bash
# Desde apps/backend/
python manage.py loaddata initial_data

# O desde la raíz del proyecto
cd apps/backend && python manage.py loaddata initial_data
```

Django automáticamente:

- ✅ Busca en `fixtures/` de cada app instalada
- ✅ Resuelve relaciones ForeignKey y ManyToMany
- ✅ Respeta el orden de dependencias
- ✅ Ignora duplicados (si usas PKs explícitos)

### Limpiar y Repoblar

```bash
# Eliminar todos los datos
python manage.py flush --noinput

# Cargar datos iniciales
python manage.py loaddata initial_data

# O en un solo comando
python manage.py flush --noinput && python manage.py loaddata initial_data
```

## Crear Nuevos Fixtures

### Exportar Datos Actuales

```bash
# Exportar todo
python manage.py dumpdata --indent 2 > fixtures/my_data.json

# Exportar apps específicas
python manage.py dumpdata category dish food_tag --indent 2 > fixtures/restaurant_data.json

# Exportar un modelo específico
python manage.py dumpdata dish.dish --indent 2 > fixtures/dishes.json

# Excluir apps del sistema
python manage.py dumpdata --exclude auth --exclude contenttypes --indent 2 > fixtures/clean_data.json
```

### Opciones Útiles

- `--indent 2`: Formatea el JSON con indentación
- `--natural-foreign`: Usa natural keys en lugar de PKs para ForeignKeys
- `--natural-primary`: Usa natural keys como identificadores principales
- `--exclude <app>`: Excluye apps específicas

## Estructura del Fixture

```json
[
  {
    "model": "app.modelname",
    "pk": 1,
    "fields": {
      "name": "Ejemplo",
      "description": "Descripción",
      "category": 2,           // ForeignKey (PK del objeto relacionado)
      "tags": [1, 2, 3],       // ManyToMany (lista de PKs)
      "deleted": false,
      "is_active": true
    }
  }
]
```

## Manejo de Relaciones

### ForeignKey

```json
{
  "model": "dish.dish",
  "pk": 1,
  "fields": {
    "name": "Pizza Margherita",
    "category": 7  // PK de la categoría "Pizzas"
  }
}
```

### ManyToMany

```json
{
  "model": "dish.dish",
  "pk": 1,
  "fields": {
    "name": "Ensalada Vegana",
    "tags": [1, 3, 11]  // PKs de "Vegano", "Sin Gluten", "Orgánico"
  }
}
```

### Orden de Carga

Django carga los fixtures en el orden que aparecen en el archivo. **Importante**: Asegúrate de que los objetos referenciados (FKs) se definan **antes** que los objetos que los referencian.

Orden correcto:

1. `food_tag.foodtag` (sin dependencias)
2. `category.category` (sin dependencias)
3. `dish.dish` (depende de category y food_tag)

## Consejos y Mejores Prácticas

### ✅ Hacer

- Usar `--indent 2` para legibilidad
- Versionarlos en git
- Documentar el propósito de cada fixture
- Usar PKs explícitos para estabilidad
- Excluir apps del sistema (`auth`, `contenttypes`, `sessions`)

### ❌ Evitar

- Incluir datos sensibles (passwords, API keys)
- Exportar tablas de sistema (`django_migrations`, `auth_permission`)
- Fixtures demasiado grandes (dividir por dominio)
- PKs auto-generados (pueden causar conflictos)

## Flujo de Trabajo Recomendado

### Desarrollo

```bash
# 1. Crear datos manualmente en Django Admin
# 2. Exportar a fixture
python manage.py dumpdata category dish food_tag --indent 2 > fixtures/latest_data.json

# 3. Compartir con el equipo (commit a git)
git add fixtures/latest_data.json
git commit -m "feat: add new dishes to fixtures"
```

### Reset de Base de Datos

```bash
# Opción 1: Flush (mantiene estructura)
python manage.py flush --noinput
python manage.py loaddata initial_data

# Opción 2: Reset completo (borra db.sqlite3)
rm db.sqlite3
python manage.py migrate
python manage.py loaddata initial_data
python manage.py createsuperuser
```

## Troubleshooting

### Error: "No fixture named 'X' found"

Django busca fixtures en:

- `<app>/fixtures/`
- Directorios en `FIXTURE_DIRS` (settings)

Asegúrate de que el archivo existe en la ruta correcta.

### Error: "IntegrityError: FOREIGN KEY constraint failed"

El fixture intenta referenciar un objeto que no existe. Revisa el orden de carga o asegúrate de que todos los objetos referenciados estén en el fixture.

### Error: "DeserializationError: Invalid model"

El formato del fixture es incorrecto o el modelo no existe. Verifica:

- Sintaxis JSON válida
- Nombres de modelos correctos (`app.modelname`)
- Apps instaladas en `INSTALLED_APPS`

## Referencias

- [Django Fixtures Documentation](https://docs.djangoproject.com/en/4.2/howto/initial-data/)
- [dumpdata Command](https://docs.djangoproject.com/en/4.2/ref/django-admin/#dumpdata)
- [loaddata Command](https://docs.djangoproject.com/en/4.2/ref/django-admin/#loaddata)
