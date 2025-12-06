# Copilot Instructions for Savoro.App

Django restaurant management system with monorepo architecture, inspired by NestJS patterns.

## Architecture Overview

### Layered Architecture (Controller → Service → Repository)

Each domain module follows this strict flow:

```python
# 1. Controller: HTTP request handling (apps/backend/modules/dish/controller.py)
@Controller("dishes")
class DishController(BaseController):
    def __init__(self):
        self.service = DishService()  # Manual instantiation (DI planned)

    def create(self, request: HttpRequest) -> HttpResponse:
        form = DishForm(request.POST, request.FILES)
        if form.is_valid():
            dish = self.service.create(form.cleaned_data)  # Delegate to service
            return self.success_response(request, "Created", redirect_url="dish:list")

# 2. Service: Business logic (apps/backend/modules/dish/service.py)
@Injectable()
class DishService(BaseService):
    def __init__(self):
        self.repository = DishRepository()

    def create(self, data: Dict[str, Any]) -> Dish:
        if self.repository.exists_by_name(data.get("name", "")):
            raise BadRequestException("Name already exists")
        return self.repository.create(**data)

# 3. Repository: Data access (apps/backend/modules/dish/repository.py)
@Injectable()
class DishRepository(BaseRepository[Dish]):
    def __init__(self):
        super().__init__(Dish)

    def exists_by_name(self, name: str, exclude_id: Optional[int] = None) -> bool:
        queryset = self.model.objects.filter(name=name, deleted=False)
        if exclude_id:
            queryset = queryset.exclude(pk=exclude_id)
        return queryset.exists()
```

**Critical Rules:**

- Controllers NEVER access repositories directly - always through services
- Services contain ALL business logic (validation, coordination)
- Repositories handle ONLY database queries (no business rules)
- Use `@Injectable()` and `@Controller()` decorators (DI framework coming)

### Module Structure

Each feature lives in `apps/backend/modules/{feature}/`:

```
modules/dish/
├── models.py          # Django model inheriting from BaseModel/NamedModel
├── repository.py      # DishRepository(BaseRepository[Dish])
├── service.py         # DishService with business logic
├── controller.py      # DishController with HTTP handlers
├── forms.py           # Django forms for validation
├── views.py           # Thin adapter to controller methods
├── urls.py            # URL routing
└── templates/dish/    # Module-specific templates
```

**Frontend assets** live separately in `apps/frontend/src/{feature}/`:

```
apps/frontend/src/dish/
├── css/
│   ├── list.css
│   └── detail.css
└── js/
    ├── list.js        # Event handlers, MutationObserver
    └── filters.js     # Filter logic
```

### Soft Delete Pattern

ALL models inherit from `BaseModel` with soft delete:

```python
# core/base/models.py
class BaseModel(models.Model):
    deleted = models.BooleanField(default=False)
    delete_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

# Never use .delete() - always soft delete via repository
repository.delete(id)  # Sets deleted=True, not physical delete
```

## Critical Workflows

### Development Setup

```bash
# First time
pnpm run setup        # Installs deps, runs migrations, builds frontend
pnpm run superuser    # Create admin user

# Load initial data (optional)
pnpm run loaddata  # From workspace root
# Or: cd apps/backend && pipenv run python manage.py loaddata initial_data

# Daily development (2 terminals)
pnpm run dev:frontend # Terminal 1: Vite HMR on :5173
pnpm run dev:backend  # Terminal 2: Django on :8000

# Or use VS Code: Press F5 to start both servers with debugging
```

### Adding a New Module

1. **Create Django app structure:**

   ```bash
   cd apps/backend/modules
   mkdir new_module && cd new_module
   touch __init__.py models.py repository.py service.py controller.py forms.py views.py urls.py apps.py
   ```

2. **Implement layers (bottom-up):**

   - `models.py`: Inherit from `BaseModel` or `NamedModel`
   - `repository.py`: Extend `BaseRepository[YourModel]`
   - `service.py`: Add business logic with `@Injectable()`
   - `controller.py`: HTTP handlers with `@Controller("prefix")`
   - `forms.py`: Django forms for validation
   - `views.py`: Thin adapter calling controller methods
   - `urls.py`: URL patterns

3. **Register module:**

   ```python
   # config/settings/base.py
   INSTALLED_APPS = [
       # ...
       "modules.new_module.apps.NewModuleConfig",
   ]

   # config/urls.py
   urlpatterns = [
       path("new_module/", include("modules.new_module.urls")),
   ]
   ```

4. **Create frontend assets:**
   ```bash
   cd apps/frontend/src
   mkdir -p new_module/{css,js}
   # Vite auto-discovers entry points in src/*/{css,js}/*.{css,js}
   ```

### Running Migrations

```bash
# Create migrations
cd apps/backend
pipenv run python manage.py makemigrations

# Apply migrations
pnpm run migrate  # From workspace root
```

### Working with Fixtures (Initial Data)

```bash
# Load initial data (categories, tags, dishes)
python manage.py loaddata initial_data

# Export current data to fixture
python manage.py dumpdata category dish food_tag --indent 2 > fixtures/my_data.json

# Reset database and reload
python manage.py flush --noinput
python manage.py loaddata initial_data
```

Django fixtures use JSON format with automatic relation resolution:

- **ForeignKey**: Reference by PK (`"category": 1`)
- **ManyToMany**: List of PKs (`"tags": [1, 2, 3]`)
- Files in `apps/backend/fixtures/*.json` are auto-discovered

### Building for Production

```bash
pnpm run build:prod  # Cleans, builds frontend, collects static, migrates
```

## Code Conventions

### Python Type Safety

Use type hints everywhere:

```python
from typing import Optional, Dict, Any
from django.db.models import QuerySet

def find_filtered(
    self,
    search_query: Optional[str] = None,
    category_id: Optional[int] = None,
) -> QuerySet[Dish]:
    queryset = self.repository.find_all_with_relations()
    if search_query:
        normalized_query = normalize_text(search_query)
        # ...
    return queryset
```

### Exception Handling

Use custom HTTP exceptions from `core/exceptions/http.py`:

```python
from core import NotFoundException, BadRequestException, ConflictException

def find_one(self, dish_id: int) -> Dish:
    dish = self.repository.find_by_id(dish_id)
    if not dish:
        raise NotFoundException(f"Dish with ID {dish_id} not found")
    return dish
```

### Accent-Insensitive Search

Always use `normalize_text()` for search:

```python
from core.utils import normalize_text

def search(self, query: str):
    normalized_query = normalize_text(query)  # "Café" → "cafe"
    all_items = list(self.repository.find_all())
    return [
        item for item in all_items
        if normalized_query in normalize_text(item.name)
    ]
```

### Chilean Localization

Numbers, dates, and currency are Chilean-formatted:

```python
# config/formats/es_CL.py
THOUSAND_SEPARATOR = "."  # 12.345
DECIMAL_SEPARATOR = ","   # 12,67

# Templates
{{ dish.price|currency }}           # $12.345
{{ dish.created_at|date:"d/m/Y" }}  # 25/11/2025
```

## Frontend Patterns

### JavaScript: NO Global Scope Pollution

**NEVER** expose functions on `window`. Use Custom Events:

```javascript
// ❌ WRONG
export function displayToast(message, tag) { ... }
window.displayToast = displayToast;  // Don't do this!

// ✅ CORRECT
export function displayToast(message, tag) {
    M.toast({ html: message, classes: tag });
}

document.addEventListener('toast:show', (event) => {
    const { message, tag } = event.detail;
    displayToast(message, tag);
});

// In template
<script>
  document.dispatchEvent(new CustomEvent('toast:show', {
    detail: { message: 'Success!', tag: 'success' }
  }));
</script>
```

### MutationObserver for Dynamic Content

Use MutationObserver to initialize events on AJAX-loaded content:

```javascript
// dish/js/card-initializer.js
export function initializeCard(cardElement) {
  if (cardElement.dataset.eventsAttached === "true") return;

  cardElement.addEventListener("click", function (e) {
    if (!e.target.closest(".card-action a")) {
      window.location.href = this.dataset.href;
    }
  });

  cardElement.dataset.eventsAttached = "true";
}

const observer = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    mutation.addedNodes.forEach((node) => {
      if (node.nodeType === Node.ELEMENT_NODE) {
        const cards = node.classList.contains("card")
          ? [node]
          : Array.from(node.querySelectorAll(".card"));
        cards.forEach(initializeCard);
      }
    });
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("dishContainer");
  if (container) {
    observer.observe(container, { childList: true, subtree: true });
  }
});
```

### Vite Path Aliases

Use aliases for clean imports:

```javascript
// ❌ Ugly
import { displayToast } from '../../../../shared/js/messages.js';

// ✅ Clean
import { displayToast } from '@shared/js/messages.js';

// Configured in vite.config.js
resolve: {
    alias: {
        '@shared': resolve(__dirname, 'src/shared'),
    }
}
```

## Key Files Reference

- **Settings:** `apps/backend/config/settings/base.py` (shared), `development.py`, `production.py`
- **Base classes:** `apps/backend/core/base/{models,repositories,services,controllers}.py`
- **Decorators:** `apps/backend/core/decorators/nest_style.py` (`@Injectable()`, `@Controller()`)
- **Exceptions:** `apps/backend/core/exceptions/http.py`
- **Mixins:** `apps/backend/core/mixins/{message,pagination,filter,export}.py`
- **Utilities:** `apps/backend/core/utils/text.py` (`normalize_text()`)
- **Vite config:** `apps/frontend/vite.config.js` (auto-scans `src/` for entry points)
- **Formats:** `apps/backend/config/formats/es_CL.py`

## Common Tasks

### Access current user in controllers

```python
def create(self, request: HttpRequest) -> HttpResponse:
    user = request.user  # Django's authenticated user
```

### Prefetch relations to avoid N+1

```python
def find_all_with_relations(self) -> QuerySet[Dish]:
    return self.find_all().prefetch_related("tags", "category")
```

### Form validation with custom validators

```python
from core.validators import validate_name, validate_price

class DishForm(forms.ModelForm):
    name = forms.CharField(validators=[validate_name])
    price = forms.DecimalField(validators=[validate_price])
```

### AJAX/JSON responses

```python
from django.http import JsonResponse

return JsonResponse({
    "html": render_to_string("dish/partials/list.html", context),
    "has_next": paginated.has_next(),
})
```

See `docs/ARCHITECTURE.md` for deeper architectural details and `docs/JAVASCRIPT_PATTERNS.md` for frontend patterns.
