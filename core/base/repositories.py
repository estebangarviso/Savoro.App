"""
Base repository pattern with generic CRUD operations
"""

from __future__ import annotations
from typing import Generic, TypeVar, Optional, Any, TYPE_CHECKING
from abc import ABC
from django.db.models import QuerySet, Model

if TYPE_CHECKING:
    from typing import Type

T = TypeVar("T", bound=Model)


class BaseRepository(Generic[T], ABC):
    """
    Generic repository with CRUD operations
    Type-safe data access layer
    """

    def __init__(self, model_class: Type[T]):
        self.model = model_class

    def find_all(self) -> QuerySet[T]:
        """Find all entities"""
        return self.model.objects.all()

    def find_by_id(self, id: int) -> Optional[T]:
        """Find entity by ID"""
        try:
            return self.model.objects.get(id=id)
        except self.model.DoesNotExist:
            return None

    def create(self, **kwargs: Any) -> T:
        """Create new entity"""
        return self.model.objects.create(**kwargs)

    def update(self, id: int, **kwargs: Any) -> Optional[T]:
        """Update entity by ID"""
        entity = self.find_by_id(id)
        if not entity:
            return None

        for key, value in kwargs.items():
            setattr(entity, key, value)
        entity.save()
        return entity

    def delete(self, id: int) -> bool:
        """Delete entity"""
        entity = self.find_by_id(id)
        if not entity:
            return False

        if hasattr(entity, "deleted"):
            entity.deleted = True  # type: ignore
            entity.save()
        else:
            entity.delete()
        return True
