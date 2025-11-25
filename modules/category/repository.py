"""
Category Repository - Data access layer for Category entity
Similar to TypeORM Repository in NestJS
"""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from django.db.models import QuerySet, Count, Q, Prefetch
from core import BaseRepository, Injectable
from .models import Category

if TYPE_CHECKING:
    from modules.dish.models import Dish


@Injectable()
class CategoryRepository(BaseRepository[Category]):
    """
    Repository for Category entity
    Handles all database operations for categories
    """

    def __init__(self):
        super().__init__(Category)

    def find_all_with_dish_count(self) -> QuerySet[Category]:
        """Find all categories with dish count annotation"""
        return (
            self.find_all()
            .annotate(dish_count=Count("dishes", filter=Q(dishes__deleted=False)))
            .order_by("-dish_count", "name")
        )

    def find_all_with_dishes(
        self, dishes_queryset: QuerySet[Dish]
    ) -> QuerySet[Category]:
        """Find all active categories with specific dishes preloaded"""
        return (
            self.find_all()
            .filter(is_active=True)
            .prefetch_related(Prefetch("dishes", queryset=dishes_queryset))
            .order_by("name")
        )

    def search_by_name(self, query: str) -> QuerySet[Category]:
        """Search categories by name"""
        return self.find_all().filter(name__icontains=query)

    def exists_by_name(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """Check if category with name exists"""
        queryset = self.model.objects.filter(name=name, deleted=False)
        if exclude_id:
            queryset = queryset.exclude(pk=exclude_id)
        return queryset.exists()

    def has_dishes(self, category_id: int) -> bool:
        """Check if category has associated dishes"""
        from modules.dish.models import Dish

        return Dish.objects.filter(category_id=category_id, deleted=False).exists()
