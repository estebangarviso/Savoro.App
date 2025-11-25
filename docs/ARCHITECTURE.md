# Arquitectura del Proyecto - Savoro.App

## Índice

1. [Estructura del Proyecto](#estructura-del-proyecto)
2. [Arquitectura Modular](#arquitectura-modular)
3. [Arquitectura CSS](#arquitectura-css)
4. [Patrones de Diseño](#patrones-de-diseño)
5. [Convenciones de Código](#convenciones-de-código)
6. [Tecnologías](#tecnologías)

## Arquitectura Modular

El proyecto sigue una **arquitectura modular** donde cada feature es un módulo independiente y autocontenido.

### Estructura de un Módulo

Cada módulo sigue este patrón (ejemplo: `modules/dish/`):

```
dish/
├── __init__.py           # Exporta DishService, DishRepository, DishController
├── models.py             # Modelo Dish (entidad de dominio)
├── repository.py         # DishRepository (acceso a datos)
├── service.py            # DishService (lógica de negocio)
├── controller.py         # DishController (manejo HTTP)
├── views.py              # Adapter delgado a controller
├── forms.py              # DishForm (validación)
├── urls.py               # URLs del módulo
├── migrations/           # Migraciones de DB
├── templates/dish/       # Templates específicos
│   ├── list.html
│   ├── detail.html
│   └── form.html
└── static/dish/          # Assets del módulo
    ├── css/
    │   ├── list.css
    │   └── detail.css
    └── js/
        ├── list.js
        └── filters.js
```

### Flujo de Datos en un Módulo

```
HTTP Request
     ↓
urls.py → views.py (adapter)
     ↓
controller.py (maneja request/response)
     ↓
service.py (lógica de negocio)
     ↓
repository.py (acceso a datos)
     ↓
models.py (ORM)
     ↓
Database
```

### Módulos Actuales

#### Módulos Completos
- **authentication**: Login/logout con Django auth
- **category**: CRUD de categorías con búsqueda y estadísticas
- **dish**: CRUD de platos con filtros, búsqueda y relaciones
- **food_tag**: Gestión de etiquetas alimentarias

#### Módulos en Desarrollo
- **menu**: Gestión de menús
- **order**: Sistema de órdenes
- **reservation**: Reservas de mesas
- **table**: Gestión de mesas

### Core: Funcionalidad Compartida

El directorio `core/` contiene clases base y utilidades reutilizables:

```
core/
├── base/                 # Clases base abstractas
│   ├── models.py         # BaseModel, NamedModel
│   ├── services.py       # BaseService
│   ├── repositories.py   # BaseRepository[T]
│   ├── controllers.py    # BaseController
│   └── forms.py          # BaseForm
├── decorators/           # @Injectable(), @Controller()
├── exceptions/           # NotFoundException, BadRequestException
├── mixins/               # MessageMixin, ExportMixin, etc.
├── protocols/            # Type protocols para type checking
├── validators/           # Validadores reutilizables
└── utils/                # Utilidades (normalize_text, etc.)
```

### Ventajas de la Arquitectura Modular

1. **Desacoplamiento**: Módulos independientes, cambios localizados
2. **Reutilización**: Core compartido evita duplicación
3. **Escalabilidad**: Fácil agregar nuevos módulos
4. **Testing**: Módulos testeables en aislamiento
5. **Organización**: Código organizado por feature, no por tipo
6. **Colaboración**: Equipos pueden trabajar en módulos diferentes

## Estructura del Proyecto

```
SavoroApp/
├── config/                 # Configuración Django
│   ├── settings/           # Settings por entorno (dev/prod/base)
│   │   ├── base.py         # Configuración compartida
│   │   ├── development.py  # Settings de desarrollo
│   │   └── production.py   # Settings de producción
│   ├── formats/            # Formatos localizados (es_CL)
│   ├── urls.py             # URLs principales
│   └── wsgi.py             # WSGI application
├── core/                   # Funcionalidad base reutilizable
│   ├── base/               # Clases base abstractas
│   │   ├── models.py       # BaseModel, NamedModel (timestamps, soft delete)
│   │   ├── services.py     # BaseService (lógica de negocio)
│   │   ├── repositories.py # BaseRepository (acceso a datos)
│   │   ├── controllers.py  # BaseController (manejo de HTTP)
│   │   └── forms.py        # BaseForm (validación de formularios)
│   ├── decorators/         # Decoradores personalizados
│   │   └── nest_style.py   # @Injectable(), @Controller() (estilo NestJS)
│   ├── exceptions/         # Excepciones HTTP
│   │   └── http.py         # NotFoundException, BadRequestException, etc.
│   ├── mixins/             # Mixins para vistas
│   │   ├── message.py      # MessageMixin (mensajes flash)
│   │   ├── export.py       # ExportMixin (exportación de datos)
│   │   ├── pagination.py   # PaginationMixin (paginación)
│   │   └── filter.py       # FilterMixin (filtros)
│   ├── protocols/          # Protocolos de tipo (type checking)
│   │   └── domain.py       # Interfaces de modelos (DishProtocol, CategoryProtocol)
│   ├── validators/         # Validadores personalizados
│   │   ├── name.py         # Validación de nombres
│   │   ├── price.py        # Validación de precios
│   │   └── capacity.py     # Validación de capacidad
│   └── utils/              # Utilidades generales
│       └── text.py         # Normalización de texto (acentos)
├── modules/                # Módulos de dominio (feature modules)
│   ├── authentication/     # Login/logout
│   │   ├── views.py        # Vistas de autenticación
│   │   ├── urls.py         # URLs del módulo
│   │   └── forms.py        # LoginForm
│   ├── category/           # Gestión de categorías
│   │   ├── models.py       # Modelo Category
│   │   ├── repository.py   # CategoryRepository
│   │   ├── service.py      # CategoryService (lógica de negocio)
│   │   ├── controller.py   # CategoryController (HTTP handlers)
│   │   ├── views.py        # Views adapter (delega a controller)
│   │   ├── forms.py        # CategoryForm
│   │   ├── urls.py         # URLs del módulo
│   │   └── static/         # Assets específicos del módulo
│   ├── dish/               # Gestión de platos
│   │   ├── models.py       # Modelo Dish
│   │   ├── repository.py   # DishRepository
│   │   ├── service.py      # DishService
│   │   ├── controller.py   # DishController
│   │   ├── views.py        # Views adapter
│   │   ├── forms.py        # DishForm
│   │   ├── urls.py         # URLs del módulo
│   │   ├── templates/      # Templates específicos
│   │   └── static/         # Assets (CSS/JS) del módulo
│   ├── food_tag/           # Etiquetas de comida
│   │   ├── models.py       # Modelo FoodTag
│   │   ├── repository.py   # FoodTagRepository
│   │   └── service.py      # FoodTagService
│   ├── menu/               # Menús (en desarrollo)
│   ├── order/              # Órdenes (en desarrollo)
│   ├── reservation/        # Reservas (en desarrollo)
│   └── table/              # Mesas (en desarrollo)
├── shared/                 # Recursos compartidos
│   ├── static/shared/      # Assets globales
│   │   ├── css/            # CSS variables, base, components
│   │   ├── js/             # JavaScript compartido (messages, utils)
│   │   └── images/         # Imágenes globales
│   ├── templates/          # Templates base
│   └── templatetags/       # Template tags personalizados
├── staticfiles/            # Assets compilados (generados por Vite)
├── media/                  # Archivos subidos por usuarios
├── scripts/                # Scripts de automatización
│   ├── setup.sh            # Setup inicial
│   ├── start-dev.sh        # Desarrollo
│   └── build-prod.sh       # Build producción
└── docs/                   # Documentación
    ├── ARCHITECTURE.md     # Este archivo
    ├── SETUP.md            # Guía de instalación
    ├── CONTRIBUTING.md     # Guía de contribución
    ├── COMMANDS.md         # Referencia de comandos
    └── JAVASCRIPT_PATTERNS.md # Patrones JavaScript
```

## Arquitectura CSS

El proyecto utiliza **Vite** como empaquetador de módulos para compilar y optimizar assets:

### Sistema de Build con Vite

- **Escaneo automático**: Vite escanea dinámicamente `modules/*/static/` y `shared/static/` para descubrir entry points
- **Materialize CSS**: Importado como dependencia de Node.js y bundleado automáticamente
- **ES Modules**: Uso de `import`/`export` estándar de JavaScript
- **Sourcemaps**: Generación automática de `.js.map` y `.css.map` para debugging
- **Code Splitting**: Materialize se extrae en un chunk compartido para evitar duplicación

### Estructura de Assets

El proyecto implementa un sistema de diseño modular y DRY:

- **`variables.css`**: Variables CSS globales (colores, espaciado, sombras)
- **`base.css`**: Estilos base y resets
- **`filters.css`**: Componentes de filtros reutilizables
- **`cards.css`**: Estilos de tarjetas compartidos
- **`buttons.css`**: Botones comunes

**Orden de carga**: `variables.css` → `base.css` → componentes → módulos

### Rutas de Assets en Templates

Después del build, los archivos estáticos se generan con rutas limpias:

**CSS:**
```django
{% load static %}
<!-- Shared CSS -->
<link rel="stylesheet" href="{% static 'shared/css/variables.css' %}">
<link rel="stylesheet" href="{% static 'shared/css/base.css' %}">
<link rel="stylesheet" href="{% static 'shared/css/components.css' %}">

<!-- Module-specific CSS -->
<link rel="stylesheet" href="{% static 'dish/css/list.css' %}">
<link rel="stylesheet" href="{% static 'category/css/detail.css' %}">
```

**JavaScript:**
```django
<!-- Shared JS (Materialize + utilities) -->
<script type="module" src="{% static 'shared/js/main.js' %}"></script>

<!-- Module-specific JS -->
<script type="module" src="{% static 'dish/js/filters.js' %}"></script>
<script type="module" src="{% static 'category/js/list.js' %}"></script>
```

**Estructura de salida en `staticfiles/`:**
```
staticfiles/
├── .vite/
│   └── manifest.json           # Mapeo de assets para integración Django
├── js/
│   └── chunks/
│       └── materialize-*.js    # Chunk compartido de Materialize
├── shared/
│   ├── css/
│   │   ├── variables.css
│   │   ├── base.css
│   │   ├── components.css
│   │   └── ...
│   └── js/
│       ├── main.js
│       ├── main.js.map
│       └── ...
├── dish/
│   ├── css/
│   │   ├── list.css
│   │   └── detail.css
│   └── js/
│       ├── filters.js
│       ├── filters.js.map
│       └── ...
└── category/
    ├── css/
    └── js/
```

## Patrones de Diseño

### Backend

#### Arquitectura en Capas (Layered Architecture)

El proyecto sigue una arquitectura en capas inspirada en NestJS con separación clara de responsabilidades:

```
┌─────────────────────────────────────┐
│  Views Layer (Django Views)         │  ← Delgada, solo routing
│  - Adapters a controllers           │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Controller Layer                   │  ← Maneja HTTP requests
│  - DishController                   │
│  - CategoryController               │
│  - Decoradores: @Controller()       │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Service Layer                      │  ← Lógica de negocio
│  - DishService                      │
│  - CategoryService                  │
│  - Validaciones de negocio          │
│  - Decoradores: @Injectable()       │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Repository Layer                   │  ← Acceso a datos
│  - DishRepository                   │
│  - CategoryRepository               │
│  - Queries complejas                │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Model Layer (Django ORM)           │  ← Entidades de dominio
│  - Dish, Category, FoodTag          │
│  - BaseModel (timestamps, soft delete)│
└─────────────────────────────────────┘
```

#### Repository Pattern
Separación de lógica de acceso a datos. Cada módulo tiene su propio `repository.py` que encapsula las operaciones de la base de datos.

**Características:**
- Hereda de `BaseRepository[T]` (genérico tipado)
- Métodos estándar: `find_all()`, `find_by_id()`, `create()`, `update()`, `delete()`
- Soft delete por defecto (marca `deleted=True`)
- Queries específicas del dominio

```python
# Ejemplo: modules/dish/repository.py
from core import BaseRepository, Injectable
from .models import Dish

@Injectable()
class DishRepository(BaseRepository[Dish]):
    def __init__(self):
        super().__init__(Dish)
    
    def find_all_with_relations(self) -> QuerySet[Dish]:
        """Precarga relaciones para evitar N+1 queries"""
        return self.find_all().prefetch_related("tags", "category")
    
    def find_by_category(self, category_id: int) -> QuerySet[Dish]:
        return self.find_all().filter(category_id=category_id)
    
    def exists_by_name(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """Verifica unicidad de nombre"""
        queryset = self.model.objects.filter(name=name, deleted=False)
        if exclude_id:
            queryset = queryset.exclude(pk=exclude_id)
        return queryset.exists()
```

#### Service Layer
Lógica de negocio independiente. Los servicios coordinan operaciones entre repositorios y aplican reglas de negocio.

**Responsabilidades:**
- Validaciones de negocio complejas
- Coordinación de múltiples repositorios
- Transformación de datos
- Lanzamiento de excepciones de negocio

```python
# Ejemplo: modules/dish/service.py
from core import BaseService, Injectable, NotFoundException, BadRequestException
from .repository import DishRepository

@Injectable()
class DishService(BaseService):
    def __init__(self):
        self.repository = DishRepository()
    
    def create(self, data: Dict[str, Any]) -> Dish:
        # Validación de negocio: nombre único
        if self.repository.exists_by_name(data.get("name", "")):
            raise BadRequestException(
                f"Ya existe un plato con el nombre '{data['name']}'"
            )
        
        # Validación de relaciones
        if "category_id" in data and data["category_id"]:
            if not Category.objects.filter(pk=data["category_id"]).exists():
                raise BadRequestException("Categoría inválida")
        
        # Crear plato
        tags = data.pop("tags", [])
        dish = self.repository.create(**data)
        
        # Asignar relaciones many-to-many
        if tags:
            dish.tags.set(tags)
        
        return dish
    
    def find_one(self, dish_id: int) -> Dish:
        dish = self.repository.find_by_id(dish_id)
        if not dish:
            raise NotFoundException(f"Plato con ID {dish_id} no encontrado")
        return dish
```

#### Controller Pattern
Controladores para cada módulo que manejan la lógica HTTP.

**Responsabilidades:**
- Parsear request (query params, body, files)
- Validar formularios Django
- Delegar a servicios
- Manejar excepciones y convertirlas en respuestas HTTP
- Retornar respuestas (render, redirect, JSON)

```python
# Ejemplo: modules/dish/controller.py
from core import BaseController, Controller
from django.contrib.auth.decorators import login_required
from .service import DishService
from .forms import DishForm

@Controller("dishes")
class DishController(BaseController):
    def __init__(self):
        self.service = DishService()
    
    @staticmethod
    @login_required(login_url="/")
    def create(request: HttpRequest) -> HttpResponse:
        controller = DishController()
        
        if request.method == "POST":
            form = DishForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    controller.service.create(form.cleaned_data)
                    messages.success(request, "Plato creado exitosamente")
                    return redirect("dish:list")
                except Exception as e:
                    messages.error(request, str(e))
        else:
            form = DishForm()
        
        return render(request, "dish/form.html", {"form": form})
```

#### Decoradores Estilo NestJS

Inspirados en NestJS, estos decoradores marcan clases con metadatos:

```python
# core/decorators/nest_style.py
@Injectable()  # Marca una clase como injectable (service, repository)
class DishService:
    pass

@Controller("dishes")  # Marca una clase como controller
class DishController:
    pass
```

**TODO: Implementación de Dependency Injection**

Actualmente, las dependencias se instancian manualmente en los constructores:

```python
# Estado actual
class DishController:
    def __init__(self):
        self.service = DishService()  # Instanciación manual

class DishService:
    def __init__(self):
        self.repository = DishRepository()  # Instanciación manual
```

**Plan futuro**: Implementar un sistema de DI inspirado en NestJS/Spring:

```python
# Implementación futura con DI
class DishController:
    def __init__(self, service: DishService):
        self.service = service  # Inyectado automáticamente

class DishService:
    def __init__(self, repository: DishRepository):
        self.repository = repository  # Inyectado automáticamente

# Container de DI (similar a @Module en NestJS)
@Module(
    controllers=[DishController],
    providers=[DishService, DishRepository]
)
class DishModule:
    pass
```

**Beneficios esperados:**
- ✅ Mayor testabilidad (fácil mock de dependencias)
- ✅ Desacoplamiento de implementaciones
- ✅ Configuración centralizada de dependencias
- ✅ Scopes configurables (singleton, transient, request)
- ✅ Lazy loading de servicios

**Librerías a considerar:**
- `injector` (Python DI framework)
- `dependency-injector` (Container-based DI)
- Implementación custom basada en decoradores

#### Excepciones HTTP

Excepciones personalizadas para errores de negocio:

```python
# core/exceptions/http.py
class NotFoundException(HttpException):     # 404
class BadRequestException(HttpException):   # 400
class UnauthorizedException(HttpException): # 401
class ConflictException(HttpException):     # 409

# Uso en servicios
def find_one(self, dish_id: int) -> Dish:
    dish = self.repository.find_by_id(dish_id)
    if not dish:
        raise NotFoundException(f"Plato con ID {dish_id} no encontrado")
    return dish
```

#### Modelos Base con Soft Delete

Todos los modelos heredan de `BaseModel` o `NamedModel`:

```python
# core/base/models.py
class BaseModel(models.Model):
    """Timestamps y soft delete"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delete_at = models.DateTimeField(blank=True, null=True)
    deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        abstract = True

class NamedModel(BaseModel):
    """Modelo base con nombre"""
    name = models.CharField(max_length=150)
    
    class Meta:
        abstract = True
```

#### Mixins para Vistas

Funcionalidad reutilizable para vistas:

```python
# core/mixins/
- MessageMixin: Manejo de mensajes flash
- ExportMixin: Exportación de datos (CSV, PDF)
- PaginationMixin: Paginación de resultados
- FilterMixin: Aplicación de filtros
```

#### Protocolos (Type Checking)

Interfaces para type hints con runtime checking:

```python
# core/protocols/domain.py
from typing import Protocol, runtime_checkable

@runtime_checkable
class DishProtocol(HasId, HasName, HasTimestamps, Protocol):
    description: str
    price: Decimal
    category: Optional[CategoryProtocol]
    
    def get_absolute_url(self) -> str: ...
```

#### Validadores Personalizados

Validadores reutilizables para modelos y formularios:

```python
# core/validators/
- name.py: Validación de nombres (longitud, caracteres permitidos)
- price.py: Validación de precios (mínimo, máximo, decimales)
- capacity.py: Validación de capacidad (números positivos)
```

#### Form Validation
Validación centralizada con Django Forms en cada módulo.

```python
# modules/dish/forms.py
class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ["name", "description", "price", "category", "image", "tags"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "tags": forms.CheckboxSelectMultiple(),
        }
```

### Frontend

#### Component-Based CSS
Estilos modulares reutilizables que se pueden componer.

**Estructura:**
```css
/* shared/static/shared/css/variables.css */
:root {
  --primary-color: #2196F3;
  --success-color: #4CAF50;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --border-radius: 4px;
  --shadow-sm: 0 2px 4px rgba(0,0,0,0.1);
}

/* shared/static/shared/css/components/cards.css */
.card {
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-sm);
}

/* modules/dish/static/dish/css/list.css */
.dish-card {
  /* Extiende card con estilos específicos */
}
```

#### Vanilla JS Modules
JavaScript organizado sin frameworks, usando módulos ES6.

**Características:**
- ES Modules (`import`/`export`)
- Custom Events para comunicación template ↔ JS
- MutationObserver para contenido dinámico
- Path aliases para imports limpios (`@shared/js/messages.js`)
- NO contamina el scope global (`window`)

**Ejemplo:**
```javascript
// shared/static/shared/js/messages.js
export function displayToast(message, tag) {
  M.toast({ html: message, classes: tag });
}

// Listener para Custom Events
document.addEventListener('toast:show', (event) => {
  const { message, tag } = event.detail;
  displayToast(message, tag);
});

// Uso desde template
<script>
  document.dispatchEvent(new CustomEvent('toast:show', {
    detail: { message: 'Éxito', tag: 'success' }
  }));
</script>
```

#### Progressive Enhancement
Funcionalidad base sin JS, mejoras progresivas con JavaScript.

- Formularios funcionan sin JS (submit estándar)
- Cards clicables con `<a>` como fallback
- Filtros con submit de formulario estándar
- JavaScript mejora la UX (toasts, confirmaciones, AJAX)

#### Mobile First
Diseño responsive desde móvil hacia escritorio.

```css
/* Base: móvil */
.card { width: 100%; }

/* Tablet */
@media (min-width: 768px) {
  .card { width: 50%; }
}

/* Desktop */
@media (min-width: 1024px) {
  .card { width: 33.33%; }
}
```

## Convenciones de Código

### Python
- **PEP 8**: Estilo estándar Python
- **Type Hints**: Anotaciones de tipo en funciones
- **Docstrings**: Documentación en clases y funciones complejas

### JavaScript
- **ESLint**: Configuración con reglas Prettier
- **ES2021**: Sintaxis moderna JavaScript con ES Modules
- **Naming**: camelCase para variables, PascalCase para clases
- **Imports**: Uso de path aliases configurados en jsconfig.json
  ```javascript
  import M from 'materialize-css';           // Dependencia npm
  import { displayToast } from '@shared/js/messages.js'; // Alias de ruta
  import '@shared/css/variables.css';         // Import de CSS
  ```

### CSS
- **BEM-like**: Clases descriptivas (.card-header, .filter-btn)
- **CSS Variables**: Variables para valores reutilizables
- **Mobile First**: Media queries de menor a mayor

## Tecnologías

### Backend
- **Django 4.2+**: Framework web Python
- **Python 3.10+**: Lenguaje de programación
- **SQLite**: Base de datos (desarrollo)
- **PostgreSQL**: Base de datos (producción recomendada)
- **Pillow**: Procesamiento de imágenes
- **django-widget-tweaks**: Renderizado de formularios

### Frontend
- **Materialize CSS 1.0.0**: Framework de componentes UI
- **Vanilla JavaScript**: Sin dependencias jQuery
- **CSS Variables**: Sistema de diseño modular
- **Vite**: Empaquetador de módulos y build tool
- **ESLint + Prettier**: Linting y formateo de código

### DevTools
- **pipenv**: Gestión de entornos virtuales
- **pnpm**: Gestor de paquetes Node.js
- **Vite**: Build tool y dev server
- **pylint**: Linter para Python
- **django-stubs**: Type hints para Django
- **djlint**: Linter para templates Django

## Características Especiales

### Búsqueda sin Acentos

El proyecto implementa búsqueda insensible a acentos usando normalización de texto:

```python
# core/utils/text.py
import unicodedata

def normalize_text(text: str) -> str:
    """
    Normaliza texto removiendo acentos para búsquedas
    'Café' → 'cafe'
    'Niño' → 'nino'
    """
    nfd_form = unicodedata.normalize('NFD', text.lower())
    return ''.join(
        char for char in nfd_form
        if unicodedata.category(char) != 'Mn'
    )

# Uso en servicios
def search(self, query: str):
    normalized_query = normalize_text(query)
    all_items = list(self.repository.find_all())
    return [
        item for item in all_items
        if normalized_query in normalize_text(item.name)
    ]
```

### Localización Chilena

Formato de números, fechas y moneda adaptado a Chile:

```python
# config/formats/es_CL.py
USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = "."
DECIMAL_SEPARATOR = ","
NUMBER_GROUPING = 3

# Ejemplo: 12345.67 → 12.345,67

# Template tags
{{ dish.price|currency }}  # $12.345
{{ dish.created_at|date:"d/m/Y" }}  # 25/11/2025
```

### Soft Delete

Todos los modelos implementan soft delete (no se borran físicamente):

```python
# Al "eliminar"
dish.deleted = True
dish.delete_at = timezone.now()
dish.save()

# Queries excluyen eliminados automáticamente
repository.find_all()  # WHERE deleted=False
```

### Type Safety

El proyecto usa type hints extensivamente:

```python
# Type hints en modelos
class Dish(NamedModel):
    price: models.DecimalField[Decimal, Decimal]
    category: models.ForeignKey[Category]
    tags: models.ManyToManyField[FoodTag, FoodTag]

# Type hints en servicios
def find_one(self, dish_id: int) -> Dish:
    ...

# Protocols para interfaces
@runtime_checkable
class DishProtocol(Protocol):
    name: str
    price: Decimal
```

### Validación Multi-Capa

Validación en múltiples niveles:

1. **Frontend**: HTML5 validation, Materialize CSS feedback
2. **Django Forms**: Validación de campos y datos
3. **Validadores personalizados**: En `core/validators/`
4. **Servicios**: Validación de negocio (unicidad, relaciones)
5. **Base de datos**: Constraints y validaciones de integridad

### Assets con Vite

Build moderno y optimizado:

- **Hot Module Replacement (HMR)**: Cambios instantáneos sin refresh
- **Code Splitting**: Chunks optimizados
- **Tree Shaking**: Solo código usado
- **Minification**: Código minificado en producción
- **Sourcemaps**: Debug facilitado
