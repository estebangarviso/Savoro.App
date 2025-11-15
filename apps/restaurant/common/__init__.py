"""
Common module - Base interfaces, decorators and utilities
Similar to NestJS @nestjs/common
"""

from typing import Protocol, TypeVar, Generic, Optional, Dict, Any
from abc import ABC, abstractmethod
from django.db.models import QuerySet
from django.db import models

T = TypeVar("T")


# ============================================================================
# INTERFACES (Protocols)
# ============================================================================


class IService(Protocol):
    """Base interface for all services"""

    pass


class IRepository(Protocol[T]):
    """Base interface for repositories (similar to TypeORM Repository)"""

    def find_all(self) -> QuerySet[T]:  # type: ignore
        """Find all entities"""
        ...

    def find_by_id(self, id: int) -> Optional[T]:
        """Find entity by ID"""
        ...

    def create(self, data: Dict[str, Any]) -> T:
        """Create new entity"""
        ...

    def update(self, id: int, data: Dict[str, Any]) -> T:
        """Update entity"""
        ...

    def delete(self, id: int) -> bool:
        """Delete entity"""
        ...


class IFilterService(Protocol[T]):
    """Interface for filter services"""

    def apply_filters(self, queryset: QuerySet[T], **filters: Any) -> QuerySet[T]:  # type: ignore
        """Apply filters to queryset"""
        ...


# ============================================================================
# BASE CLASSES
# ============================================================================


class BaseRepository(Generic[T], ABC):
    """
    Base repository implementation (similar to TypeORM BaseRepository)
    Provides common CRUD operations
    """

    def __init__(self, model_class: type[models.Model]):
        self.model = model_class

    def find_all(self) -> QuerySet[T]:  # type: ignore
        """Find all non-deleted entities"""
        return self.model.objects.filter(deleted=False)  # type: ignore

    def find_by_id(self, id: int) -> Optional[T]:
        """Find entity by ID"""
        try:
            return self.model.objects.get(pk=id, deleted=False)  # type: ignore
        except self.model.DoesNotExist:
            return None

    def create(self, **data: Any) -> T:
        """Create new entity"""
        return self.model.objects.create(**data)  # type: ignore

    def update(self, id: int, **data: Any) -> Optional[T]:
        """Update entity"""
        instance = self.find_by_id(id)
        if instance:
            for key, value in data.items():
                setattr(instance, key, value)
            instance.save()
        return instance

    def delete(self, id: int) -> bool:
        """Soft delete entity"""
        instance = self.find_by_id(id)
        if instance:
            instance.deleted = True
            instance.save()
            return True
        return False


class BaseService(ABC):
    """
    Base service class (similar to NestJS Injectable services)
    Services contain business logic
    """

    pass


class BaseController(ABC):
    """
    Base controller class (similar to NestJS Controllers)
    Controllers handle HTTP requests and delegate to services
    """

    pass


# ============================================================================
# DECORATORS (similar to NestJS decorators)
# ============================================================================


class Injectable:
    """
    Decorator to mark a class as injectable (similar to @Injectable() in NestJS)
    In Django, this is mostly for documentation and can be extended for DI
    """

    def __init__(self, scope: str = "singleton"):
        self.scope = scope

    def __call__(self, cls):
        cls._injectable = True
        cls._scope = self.scope
        return cls


class Controller:
    """
    Decorator to mark a class as a controller (similar to @Controller() in NestJS)
    """

    def __init__(self, prefix: str = ""):
        self.prefix = prefix

    def __call__(self, cls):
        cls._controller = True
        cls._prefix = self.prefix
        return cls


# ============================================================================
# DTOs (Data Transfer Objects)
# ============================================================================


class BaseDTO(ABC):
    """
    Base class for DTOs (similar to NestJS DTOs with class-validator)
    """

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert DTO to dictionary"""
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create DTO from dictionary"""
        pass


# ============================================================================
# EXCEPTIONS (similar to NestJS HttpException)
# ============================================================================


class HttpException(Exception):
    """Base HTTP exception"""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundException(HttpException):
    """Not found exception (404)"""

    def __init__(self, message: str = "Not Found"):
        super().__init__(message, 404)


class BadRequestException(HttpException):
    """Bad request exception (400)"""

    def __init__(self, message: str = "Bad Request"):
        super().__init__(message, 400)


class UnauthorizedException(HttpException):
    """Unauthorized exception (401)"""

    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, 401)
