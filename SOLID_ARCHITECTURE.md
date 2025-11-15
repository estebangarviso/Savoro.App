# Arquitectura SOLID - Sistema de Filtros de Platos y Categorías

## Principios SOLID Aplicados

### 1. **Single Responsibility Principle (SRP)**
Cada clase/módulo tiene una única responsabilidad:

#### Servicios Backend (`apps/restaurant/services.py`)

**Servicios de Platos:**
- **`DishFilterService`**: Responsable únicamente de aplicar filtros a querysets
  - Métodos separados para cada tipo de filtro (búsqueda, categoría, tags)
  - No sabe cómo se construyen los querysets base
  
- **`DishQueryService`**: Responsable de construir queries optimizadas
  - Maneja prefetch de relaciones
  - Provee querysets base configurados
  
- **`CategoryQueryService`**: Responsable de queries de categorías con platos
  - Especializado en obtener categorías con sus platos
  
- **`FilterContextBuilder`**: Responsable de construir el contexto para vistas de platos
  - Orquesta los servicios anteriores
  - Extrae parámetros de la request
  - Construye el diccionario de contexto completo

**Servicios de Categorías:**
- **`CategoryFilterService`**: Responsable de aplicar filtros a categorías
  - Filtrado por búsqueda de texto
  
- **`CategoryStatsService`**: Responsable de estadísticas de categorías
  - Conteo de platos asociados
  - Ordenamiento por relevancia
  
- **`CategoryContextBuilder`**: Responsable de construir el contexto para vistas de categorías
  - Orquesta filtros y estadísticas
  - Construye el contexto completo

#### Assets Frontend

**Platos:**
- **`static/css/restaurant-index.css`**: Estilos solo para la vista de índice de platos
- **`static/css/restaurant-detail.css`**: Estilos solo para la vista de detalle de platos
- **`static/js/restaurant-filters.js`**: Lógica de interacción de filtros de platos

**Categorías:**
- **`static/css/category-list.css`**: Estilos solo para la vista de listado de categorías
- **`static/js/category-filters.js`**: Lógica de interacción de filtros de categorías

### 2. **Open/Closed Principle (OCP)**
El sistema está abierto a extensión pero cerrado a modificación:

```python
# Para agregar un nuevo tipo de filtro a platos, solo extendemos DishFilterService
class DishFilterService:
    @staticmethod
    def _apply_price_filter(queryset, min_price, max_price):
        """Nuevo filtro sin modificar código existente"""
        return queryset.filter(price__gte=min_price, price__lte=max_price)

# Para agregar filtros a categorías
class CategoryFilterService:
    @staticmethod
    def _apply_status_filter(queryset, is_active):
        """Nuevo filtro de estado"""
        return queryset.filter(is_active=is_active)
```

### 3. **Liskov Substitution Principle (LSP)**
Los servicios pueden intercambiarse sin romper el código:

```python
# Todos los servicios de filtrado retornan QuerySets
# Pueden componerse sin problemas
filtered = DishFilterService.apply_filters(
    DishQueryService.get_base_queryset(),
    search_query="pizza"
)
```

### 4. **Interface Segregation Principle (ISP)**
Interfaces pequeñas y específicas:

- Cada servicio expone solo los métodos necesarios
- Los métodos privados (prefijo `_`) ocultan detalles de implementación
- Las vistas solo usan `FilterContextBuilder.build_filter_context()`

### 5. **Dependency Inversion Principle (DIP)**
Las vistas dependen de abstracciones (servicios), no de implementaciones concretas:

```python
# La vista no sabe cómo se filtran los datos
def index(request):
    context = FilterContextBuilder.build_filter_context(request)
    return render(request, "restaurant/index.html", context)
```

## Estructura de Archivos

```
apps/restaurant/
├── services.py                 # Servicios de lógica de negocio (BACKEND)
├── views.py                    # Vistas delgadas (CONTROLLER)
└── templates/restaurant/
    ├── index.html              # Vista de listado de platos
    ├── detail.html             # Vista de detalle de platos
    └── category/
        └── category_list.html  # Vista de listado de categorías

static/
├── css/
│   ├── restaurant-index.css    # Estilos de índice de platos (PRESENTATION)
│   ├── restaurant-detail.css   # Estilos de detalle de platos (PRESENTATION)
│   └── category-list.css       # Estilos de listado de categorías (PRESENTATION)
└── js/
    ├── restaurant-filters.js   # Lógica de filtros de platos (INTERACTION)
    └── category-filters.js     # Lógica de filtros de categorías (INTERACTION)
```

## Ventajas de esta Arquitectura

### Mantenibilidad
- Cambios en filtros: solo modificar `DishFilterService`
- Cambios en estilos: solo modificar archivos CSS
- Cambios en UI: solo modificar JavaScript

### Testabilidad
```python
# Cada servicio puede probarse independientemente
def test_search_filter():
    dishes = DishFilterService.apply_filters(
        Dish.objects.all(),
        search_query="pizza"
    )
    assert dishes.count() > 0

def test_category_stats():
    categories = CategoryStatsService.get_categories_with_dish_count()
    assert all(hasattr(cat, 'dish_count') for cat in categories)
```

### Reusabilidad
```python
# Los servicios pueden usarse en otras vistas o APIs
def api_dishes(request):
    dishes = DishQueryService.get_filtered_dishes(
        search_query=request.GET.get('q')
    )
    return JsonResponse(list(dishes.values()))

def api_categories(request):
    categories = CategoryStatsService.get_filtered_categories_with_stats(
        search_query=request.GET.get('q')
    )
    return JsonResponse(list(categories.values()))
```

### Extensibilidad
Para agregar nuevos filtros:

1. **Agregar método en `DishFilterService`**:
```python
@staticmethod
def _apply_price_range_filter(queryset, min_price, max_price):
    return queryset.filter(price__range=(min_price, max_price))
```

2. **Actualizar `FilterContextBuilder`**:
```python
min_price = request.GET.get('min_price')
max_price = request.GET.get('max_price')
if min_price and max_price:
    filtered_dishes = DishFilterService._apply_price_range_filter(
        filtered_dishes, min_price, max_price
    )
```

3. **Agregar campo en template**:
```html
<input type="number" name="min_price" placeholder="Precio mínimo">
<input type="number" name="max_price" placeholder="Precio máximo">
```

## Separación de Responsabilidades

### Backend (Python)
- **Servicios**: Lógica de negocio pura
- **Vistas**: Coordinación y respuesta HTTP
- **Modelos**: Representación de datos

### Frontend (HTML/CSS/JS)
- **HTML**: Estructura semántica
- **CSS**: Presentación visual separada por vista
- **JavaScript**: Interactividad y comportamiento

## Beneficios de la Separación CSS/JS

1. **Cacheabilidad**: Los archivos estáticos pueden cachearse
2. **Performance**: Los estilos se cargan solo cuando se necesitan
3. **Organización**: Fácil localizar estilos de cada vista
4. **Reutilización**: Clases CSS pueden compartirse entre vistas
5. **Mantenimiento**: Cambios CSS no requieren tocar HTML

## Convenciones de Nomenclatura

### Clases CSS
- Nombres descriptivos: `.filter-card`, `.dish-card`, `.price-tag`
- Modificadores: `.category-header-uncategorized`
- Estados: `.status-active`, `.status-inactive`

### Funciones JavaScript
- Verbos descriptivos: `initializeFilters()`, `submitFilterForm()`
- Prefijos claros: `attach...`, `initialize...`

### Servicios Python
- Sufijos descriptivos: `...Service`, `...Builder`
- Métodos privados con `_`: `_apply_search_filter()`
