# Modular Architecture - NestJS Style for Django

## 🏗️ Architecture Overview

This project follows a **modular architecture** inspired by **NestJS**, applying separation of concerns and dependency injection patterns to Django.

## 📂 Directory Structure

```
apps/restaurant/
├── common/                         # Shared utilities (like @nestjs/common)
│   └── __init__.py                # Base classes, interfaces, decorators
│
├── modules/                        # Feature modules
│   ├── dish/                      # Dish module
│   │   ├── __init__.py           # Module exports
│   │   ├── dish_repository.py    # Data access layer
│   │   ├── dish_service.py       # Business logic layer
│   │   └── dish_controller.py    # HTTP request handler
│   │
│   └── category/                  # Category module
│       ├── __init__.py           # Module exports
│       ├── category_repository.py # Data access layer
│       ├── category_service.py    # Business logic layer
│       └── category_controller.py # HTTP request handler
│
├── models.py                      # Django models (entities)
├── forms.py                       # Django forms (DTOs)
└── views.py                       # View adapters (delegates to controllers)
```

## 🎯 Design Patterns

### 1. **Module Pattern**
Each feature (dish, category) is encapsulated in its own module:
```
dish/
  - DishRepository    # Data access
  - DishService       # Business logic
  - DishController    # HTTP handling
```

### 2. **Repository Pattern**
Repositories handle all database operations:
```python
@Injectable()
class DishRepository(BaseRepository[Dish]):
    def find_all_with_relations(self) -> QuerySet[Dish]:
        return self.find_all().prefetch_related('tags', 'category')
```

### 3. **Service Pattern**
Services contain business logic and validations:
```python
@Injectable()
class DishService(BaseService):
    def create(self, data: Dict[str, Any]) -> Dish:
        # Validate
        if self.repository.exists_by_name(data.get('name')):
            raise BadRequestException("Dish already exists")
        
        # Create
        return self.repository.create(**data)
```

### 4. **Controller Pattern**
Controllers handle HTTP requests:
```python
@Controller('dishes')
class DishController(BaseController):
    @staticmethod
    @login_required(login_url="/")
    def index(request: HttpRequest) -> HttpResponse:
        controller = DishController()
        dishes = controller.service.find_all()
        return render(request, 'template.html', {'dishes': dishes})
```

## 🔧 Core Components

### Base Classes (common/__init__.py)

#### **BaseRepository[T]**
- Generic repository for CRUD operations
- Similar to TypeORM's BaseRepository
- Methods: `find_all()`, `find_by_id()`, `create()`, `update()`, `delete()`

#### **BaseService**
- Base class for services
- Contains business logic
- Marked with `@Injectable()` decorator

#### **BaseController**
- Base class for controllers
- Handles HTTP requests
- Marked with `@Controller(prefix)` decorator

### Decorators

#### **@Injectable()**
Marks a class as injectable (for documentation):
```python
@Injectable()
class DishService(BaseService):
    pass
```

#### **@Controller(prefix)**
Marks a class as a controller:
```python
@Controller('dishes')
class DishController(BaseController):
    pass
```

### Interfaces (Protocols)

#### **IRepository[T]**
Interface for repository pattern

#### **IService**
Interface for service pattern

#### **IFilterService[T]**
Interface for filter services

### Exceptions

- `HttpException` - Base HTTP exception
- `NotFoundException` - 404 errors
- `BadRequestException` - 400 errors
- `UnauthorizedException` - 401 errors

## 📝 Layer Responsibilities

### 1. **Repository Layer** (Data Access)
- Direct database access
- Query optimization
- No business logic
- Returns QuerySets or model instances

**Example:**
```python
class DishRepository(BaseRepository[Dish]):
    def find_by_category(self, category_id: int) -> QuerySet[Dish]:
        return self.find_all().filter(category_id=category_id)
```

### 2. **Service Layer** (Business Logic)
- Business validations
- Transaction management
- Uses repositories
- Throws business exceptions
- No HTTP knowledge

**Example:**
```python
class DishService(BaseService):
    def create(self, data: Dict[str, Any]) -> Dish:
        # Validation
        if self.repository.exists_by_name(data['name']):
            raise BadRequestException("Dish already exists")
        
        # Business logic
        return self.repository.create(**data)
```

### 3. **Controller Layer** (HTTP Handling)
- HTTP request/response
- Delegates to services
- Renders templates
- Handles user messages
- No business logic

**Example:**
```python
class DishController(BaseController):
    @staticmethod
    def create(request: HttpRequest) -> HttpResponse:
        controller = DishController()
        if request.method == 'POST':
            try:
                controller.service.create(form.cleaned_data)
                messages.success(request, 'Created successfully')
            except Exception as e:
                messages.error(request, str(e))
```

## 🔄 Request Flow

```
HTTP Request
    ↓
Django View (adapter)
    ↓
Controller.method()
    ↓
Service.operation()
    ↓
Repository.query()
    ↓
Database
```

**Example flow for creating a dish:**

1. `POST /dishes/create` → `views.dish_create(request)`
2. `views.dish_create()` → `DishController.create(request)`
3. `DishController.create()` → `dish_service.create(data)`
4. `DishService.create()` → Validates + `dish_repository.create(data)`
5. `DishRepository.create()` → `Dish.objects.create(**data)`
6. Returns created dish up the chain
7. Controller renders response with message

## 🎨 Benefits of This Architecture

### 1. **Separation of Concerns**
- Each layer has a single responsibility
- Easy to understand and maintain

### 2. **Testability**
```python
def test_dish_service_create():
    service = DishService()
    dish = service.create({'name': 'Test Dish'})
    assert dish.name == 'Test Dish'
```

### 3. **Reusability**
Services can be used by:
- Multiple controllers
- Background tasks
- Management commands
- APIs

### 4. **Maintainability**
- Changes in one layer don't affect others
- Easy to locate bugs
- Clear code organization

### 5. **Scalability**
- Easy to add new modules
- Can split into microservices later
- Clear module boundaries

## 🔌 Dependency Injection (Implicit)

While Django doesn't have native DI like NestJS, we simulate it:

```python
class DishService:
    def __init__(self):
        self.repository = DishRepository()  # Manual injection

class DishController:
    def __init__(self):
        self.service = DishService()        # Manual injection
```

## 📦 Module Independence

Each module is self-contained:
- Can be moved to a separate app
- Can be reused in other projects
- Dependencies are explicit

## 🔐 Security Patterns

Controllers handle authentication:
```python
@login_required(login_url="/")
def create(request: HttpRequest) -> HttpResponse:
    # Only authenticated users reach this point
```

Services handle authorization:
```python
def delete(self, dish_id: int) -> bool:
    # Business rule: can't delete if has orders
    if self.has_active_orders(dish_id):
        raise BadRequestException("Cannot delete dish with orders")
```

## 🚀 Adding a New Module

1. **Create module directory:**
```bash
mkdir apps/restaurant/modules/order
```

2. **Create repository:**
```python
# order_repository.py
@Injectable()
class OrderRepository(BaseRepository[Order]):
    pass
```

3. **Create service:**
```python
# order_service.py
@Injectable()
class OrderService(BaseService):
    def __init__(self):
        self.repository = OrderRepository()
```

4. **Create controller:**
```python
# order_controller.py
@Controller('orders')
class OrderController(BaseController):
    def __init__(self):
        self.service = OrderService()
```

5. **Export from module:**
```python
# __init__.py
from .order_service import OrderService
from .order_repository import OrderRepository
from .order_controller import OrderController
```

6. **Create views adapter:**
```python
# views.py
def order_list(request):
    return OrderController.list(request)
```

## 📊 Comparison with NestJS

| NestJS          | Django (This Architecture) |
| --------------- | -------------------------- |
| `@Module()`     | Module directory           |
| `@Injectable()` | `@Injectable()` decorator  |
| `@Controller()` | `@Controller()` decorator  |
| `TypeOrmModule` | Django ORM + Repositories  |
| `Repository<T>` | `BaseRepository[T]`        |
| DI Container    | Manual instantiation       |
| `@Get()`        | Static method + decorator  |
| DTOs            | Forms + BaseDTO            |
| Exceptions      | Custom exceptions          |

## 🎓 Best Practices

1. **Keep controllers thin** - Only HTTP handling
2. **Services contain logic** - All business rules
3. **Repositories are dumb** - Just data access
4. **Use type hints** - Better IDE support
5. **Write docstrings** - Document public methods
6. **Handle exceptions** - Use custom exceptions
7. **Test each layer** - Unit tests for each layer
8. **Avoid circular imports** - Import at method level if needed

## 📚 Further Reading

- [NestJS Architecture](https://docs.nestjs.com/first-steps)
- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)
- [Service Layer Pattern](https://martinfowler.com/eaaCatalog/serviceLayer.html)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
