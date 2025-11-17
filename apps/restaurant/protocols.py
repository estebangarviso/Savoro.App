"""
Protocol definitions for restaurant application.
These protocols define contracts for data structures used in models and seeding.
Following Dependency Inversion Principle (SOLID) and Interface Segregation Principle.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Protocol, runtime_checkable, TypedDict

if TYPE_CHECKING:
    from apps.restaurant.models import Dish, Table


# -------------------------------------------------------------------------
#   BASE PROTOCOLS
# -------------------------------------------------------------------------


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


@runtime_checkable
class HasDeleted(Protocol):
    """Protocol for objects with a deleted field"""

    deleted: bool
    delete_at: datetime | None


@runtime_checkable
class HasActive(Protocol):
    """Protocol for objects with an active field"""

    is_active: bool


# -------------------------------------------------------------------------
#   MODEL DATA PROTOCOLS (for seeding - using TypedDict for dict literals)
# -------------------------------------------------------------------------


class DishSeedData(TypedDict):
    """
    TypedDict for dish seed data structure.
    Used for type-safe seeding of Dish model with dictionary literals.
    """

    name: str
    description: str
    price: float
    category: int  # Index reference to category list
    tags: list[int]  # Index references to tag list


class MenuSeedData(TypedDict):
    """
    TypedDict for menu seed data structure.
    Used for type-safe seeding of Menu model with dictionary literals.
    """

    name: str
    description: str
    dishes: list[Dish]  # List of dish objects


class TableSeedData(TypedDict):
    """
    TypedDict for table seed data structure.
    Used for type-safe seeding of Table model with dictionary literals.
    """

    name: str
    capacity: int


class ReservationSeedData(TypedDict):
    """
    TypedDict for reservation seed data structure.
    Used for type-safe seeding of Reservation model with dictionary literals.
    """

    table: Table  # Table object
    customer_name: str
    reservation_datetime: datetime
    number_of_guests: int


class OrderSeedData(TypedDict):
    """
    TypedDict for order seed data structure.
    Used for type-safe seeding of Order model with dictionary literals.
    """

    table: Table  # Table object
    customer_name: str
    dishes: list[Dish]  # List of dish objects
    status: str  # OrderStatus enum value
    is_paid: bool


# -------------------------------------------------------------------------
#   MODEL PROTOCOLS (for runtime type checking and abstractions)
# -------------------------------------------------------------------------


@runtime_checkable
class DishProtocol(HasId, HasName, HasTimestamps, Protocol):
    """
    Protocol defining the contract for Dish model.
    Combines ID, name, and timestamp protocols.
    """

    description: str
    price: Decimal
    category: CategoryProtocol | None

    def get_absolute_url(self) -> str: ...


@runtime_checkable
class CategoryProtocol(HasId, HasName, HasTimestamps, Protocol):
    """
    Protocol defining the contract for Category model.
    """

    ...


@runtime_checkable
class FoodTagProtocol(HasId, HasName, HasTimestamps, Protocol):
    """
    Protocol defining the contract for FoodTag model.
    """

    ...


@runtime_checkable
class MenuProtocol(HasId, HasName, HasTimestamps, Protocol):
    """
    Protocol defining the contract for Menu model.
    """

    description: str

    def get_absolute_url(self) -> str: ...


@runtime_checkable
class TableProtocol(HasId, HasName, HasTimestamps, Protocol):
    """
    Protocol defining the contract for Table model.
    """

    capacity: int


@runtime_checkable
class ReservationProtocol(HasId, HasTimestamps, Protocol):
    """
    Protocol defining the contract for Reservation model.
    """

    table: TableProtocol
    customer_name: str
    reservation_datetime: datetime
    number_of_guests: int


@runtime_checkable
class OrderProtocol(HasId, HasTimestamps, Protocol):
    """
    Protocol defining the contract for Order model.
    """

    table: TableProtocol
    customer_name: str
    status: str
    is_paid: bool
    total_amount: Decimal

    def calculate_total(self) -> Decimal: ...
