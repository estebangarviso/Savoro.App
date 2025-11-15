"""
Dish Repository - Data access layer for Dish entity
Similar to TypeORM Repository in NestJS
"""

from typing import Optional, List
from django.db.models import QuerySet, Q
from ...common import BaseRepository, Injectable
from ...models import Dish


@Injectable()
class DishRepository(BaseRepository[Dish]):
    """
    Repository for Dish entity
    Handles all database operations for dishes
    """

    def __init__(self):
        super().__init__(Dish)

    def find_all_with_relations(self) -> QuerySet[Dish]:
        """Find all dishes with related data preloaded"""
        return self.find_all().prefetch_related("tags", "category")

    def find_by_category(self, category_id: int) -> QuerySet[Dish]:
        """Find all dishes by category"""
        return self.find_all().filter(category_id=category_id)

    def find_by_tag(self, tag_id: int) -> QuerySet[Dish]:
        """Find all dishes by tag"""
        return self.find_all().filter(tags__id=tag_id).distinct()

    def search_by_name_or_description(self, query: str) -> QuerySet[Dish]:
        """Search dishes by name or description"""
        return self.find_all().filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    def find_without_category(self) -> QuerySet[Dish]:
        """Find dishes without category"""
        return self.find_all().filter(category__isnull=True)

    def find_active(self) -> QuerySet[Dish]:
        """Find only active dishes"""
        return self.find_all().filter(is_active=True)

    def exists_by_name(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """Check if dish with name exists"""
        queryset = self.model.objects.filter(name=name, deleted=False)
        if exclude_id:
            queryset = queryset.exclude(pk=exclude_id)
        return queryset.exists()
