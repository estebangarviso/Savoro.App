# Protocol-Based Type System Architecture

This document explains the protocol-based type system implemented in the restaurant application, following SOLID principles and Python best practices.

## Overview

The application uses a combination of **Protocols** and **TypedDict** to provide:
- Strong type safety across the codebase
- Clear contracts for data structures
- Runtime type checking capabilities
- Better IDE autocomplete and type hints

## Architecture Components

### 1. Base Protocols (`protocols.py`)

These define fundamental contracts that models must satisfy:

```python
@runtime_checkable
class HasId(Protocol):
    """Protocol for objects with an ID field"""
    id: int

@runtime_checkable
class HasName(Protocol):
    """Protocol for objects with a name field"""
    name: str

@runtime_checkable
class HasTimestamps(Protocol):
    """Protocol for objects with timestamp fields"""
    created_at: datetime
    updated_at: datetime
```

**Benefits:**
- Composable: Can be combined to create more specific protocols
- Runtime checkable: Can validate at runtime with `isinstance(obj, HasId)`
- Duck typing: Any object with matching attributes satisfies the protocol

### 2. Model Protocols

Define complete contracts for Django models:

```python
@runtime_checkable
class DishProtocol(HasId, HasName, HasTimestamps, Protocol):
    """Protocol defining the contract for Dish model"""
    description: str
    price: Decimal
    category: CategoryProtocol | None
    
    def get_absolute_url(self) -> str: ...
```

**Use Cases:**
- Type hints in service/repository methods
- Runtime validation: `isinstance(dish, DishProtocol)`
- Dependency Inversion: Code depends on protocols, not concrete implementations

### 3. Seed Data TypedDicts

For dictionary literals used in data seeding:

```python
class DishSeedData(TypedDict):
    """TypedDict for dish seed data structure"""
    name: str
    description: str
    price: float
    category: int  # Index reference to category list
    tags: list[int]  # Index references to tag list
```

**Benefits:**
- Type-safe dictionary literals
- IDE autocomplete for dictionary keys
- Validates structure at type-check time
- Works seamlessly with `**dict` unpacking

## Usage Examples

### Example 1: Type-Safe Seeding

```python
from apps.restaurant.protocols import DishSeedData

def _create_dishes(self) -> list[Dish]:
    dishes_data: list[DishSeedData] = [
        {
            "name": "Empanadas de Carne",
            "description": "Delicious empanadas...",
            "price": 4500.00,
            "category": 0,
            "tags": [1, 2],
        },
        # Type checker validates all keys and types!
    ]
    
    dishes = []
    for dish_data in dishes_data:
        dish = Dish.objects.create(
            name=dish_data["name"],  # Type-safe access
            description=dish_data["description"],
            price=dish_data["price"],
        )
        dishes.append(dish)
    
    return dishes
```

### Example 2: Service Layer with Protocols

```python
from apps.restaurant.protocols import DishProtocol, CategoryProtocol

class DishService:
    def get_dishes_by_category(
        self, 
        category: CategoryProtocol
    ) -> list[DishProtocol]:
        """
        Returns dishes for a given category.
        Accepts any object satisfying CategoryProtocol.
        """
        return list(Dish.objects.filter(category=category))
    
    def calculate_menu_total(
        self, 
        dishes: list[DishProtocol]
    ) -> Decimal:
        """
        Calculate total price. Works with any dish-like objects.
        """
        return sum(dish.price for dish in dishes)
```

### Example 3: Runtime Type Validation

```python
from apps.restaurant.protocols import DishProtocol

def process_dish(obj: object) -> None:
    """Process any object that looks like a dish"""
    if isinstance(obj, DishProtocol):
        print(f"Processing dish: {obj.name}")
        print(f"Price: ${obj.price}")
        print(f"URL: {obj.get_absolute_url()}")
    else:
        raise TypeError("Object doesn't satisfy DishProtocol")
```

## Design Principles Applied

### 1. **Dependency Inversion Principle (DIP)**
- High-level modules depend on protocols (abstractions)
- Low-level modules (Django models) implement protocols
- Both depend on abstractions, not concretions

### 2. **Interface Segregation Principle (ISP)**
- Small, focused protocols: `HasId`, `HasName`, `HasTimestamps`
- Clients depend only on protocols they use
- Compose small protocols into larger ones

### 3. **Open/Closed Principle (OCP)**
- Protocols are open for extension (composition)
- Closed for modification (stable interfaces)
- New models can implement existing protocols

### 4. **Liskov Substitution Principle (LSP)**
- Any object satisfying a protocol is substitutable
- Protocol guarantees behavioral contracts
- Duck typing with type safety

## Best Practices

### ✅ DO:
1. **Use TypedDict for dictionary literals** (seeding, API responses)
2. **Use Protocol for abstractions** (service contracts, repositories)
3. **Compose small protocols** (`HasId + HasName + HasTimestamps`)
4. **Make protocols `@runtime_checkable`** when validation needed
5. **Document protocol intent** with clear docstrings

### ❌ DON'T:
1. **Don't use Protocol for dict access** (no `__getitem__`)
2. **Don't over-specify protocols** (keep them minimal)
3. **Don't use protocols where TypedDict is better** (dictionary structures)
4. **Don't forget `from __future__ import annotations`** (forward references)

## Type Safety Benefits

### Before (without protocols):
```python
def get_dishes(category: Any) -> list[Any]:
    """No type safety, no IDE help"""
    return list(Dish.objects.filter(category=category))
```

### After (with protocols):
```python
def get_dishes(category: CategoryProtocol) -> list[DishProtocol]:
    """
    Type-safe, clear contracts, IDE autocomplete.
    Type checker validates all usage.
    """
    return list(Dish.objects.filter(category=category))
```

## Testing with Protocols

Protocols enable easy mocking:

```python
from apps.restaurant.protocols import DishProtocol
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class MockDish:
    """Test double satisfying DishProtocol"""
    id: int
    name: str
    price: Decimal
    description: str = ""
    
    def get_absolute_url(self) -> str:
        return f"/dishes/{self.id}/"

# MockDish automatically satisfies DishProtocol!
mock = MockDish(id=1, name="Test Dish", price=Decimal("10.00"))
assert isinstance(mock, DishProtocol)  # True!
```

## Conclusion

This protocol-based architecture provides:
- ✅ Strong type safety without sacrificing Django's flexibility
- ✅ Clear contracts between layers (controllers → services → repositories)
- ✅ Better IDE support and autocomplete
- ✅ Runtime validation capabilities
- ✅ Easy testing with mock objects
- ✅ SOLID principles compliance

The combination of **Protocol** (for abstractions) and **TypedDict** (for data structures) gives you the best of both worlds: flexibility with safety.
