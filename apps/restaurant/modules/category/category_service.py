"""
Category Service - Business logic layer for Category
Similar to NestJS Service (@Injectable())
"""

from __future__ import annotations

from typing import Optional, Dict, Any
from django.db.models import QuerySet
from ...common import BaseService, Injectable, NotFoundException, BadRequestException
from ...models import Category, Dish
from .category_repository import CategoryRepository


@Injectable()
class CategoryService(BaseService):
    """
    Service for Category business logic
    Contains all category-related operations and validations
    """

    def __init__(self):
        self.repository = CategoryRepository()

    # ========================================================================
    # QUERY METHODS
    # ========================================================================

    def find_all(self) -> QuerySet[Category]:
        """Get all categories"""
        return self.repository.find_all()

    def find_one(self, category_id: int) -> Category:
        """Get category by ID"""
        category = self.repository.find_by_id(category_id)
        if not category:
            raise NotFoundException(f"Categoría con ID {category_id} no encontrada")
        return category

    def find_all_with_stats(self) -> QuerySet[Category]:
        """Get all categories with dish count statistics"""
        return self.repository.find_all_with_dish_count()

    def find_filtered_with_stats(
        self, search_query: Optional[str] = None
    ) -> QuerySet[Category]:
        """Get filtered categories with statistics"""
        queryset = self.repository.find_all_with_dish_count()

        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        return queryset

    def find_all_with_dishes(
        self, dishes_queryset: QuerySet[Dish]
    ) -> QuerySet[Category]:
        """Get categories with specific dishes preloaded"""
        return self.repository.find_all_with_dishes(dishes_queryset)

    # ========================================================================
    # MUTATION METHODS
    # ========================================================================

    def create(self, data: Dict[str, Any]) -> Category:
        """
        Create new category
        Validates data before creation
        """
        # Validate name uniqueness
        if self.repository.exists_by_name(data.get("name", "")):
            raise BadRequestException(
                f"Ya existe una categoría con el nombre '{data['name']}'"
            )

        return self.repository.create(**data)

    def update(self, category_id: int, data: Dict[str, Any]) -> Category:
        """
        Update category
        Validates data before update
        """
        # Check if category exists
        category = self.find_one(category_id)

        # Validate name uniqueness if name is being changed
        if "name" in data and data["name"] != category.name:
            if self.repository.exists_by_name(data["name"], exclude_id=category_id):
                raise BadRequestException(
                    f"Ya existe una categoría con el nombre '{data['name']}'"
                )

        # Update category
        updated_category = self.repository.update(category_id, **data)
        if not updated_category:
            raise NotFoundException(f"Categoría con ID {category_id} no encontrada")

        return updated_category

    def delete(self, category_id: int) -> bool:
        """
        Delete category (soft delete)
        Validates that category has no dishes before deletion
        """
        # Check if category exists
        self.find_one(category_id)

        # Check if category has dishes
        if self.repository.has_dishes(category_id):
            raise BadRequestException(
                "No se puede eliminar una categoría con platos asociados"
            )

        # Perform soft delete
        return self.repository.delete(category_id)

    # ========================================================================
    # STATISTICS
    # ========================================================================

    def count_all(self) -> int:
        """Get total count of categories"""
        return self.repository.find_all().count()

    def count_with_dishes(self) -> int:
        """Get count of categories that have dishes"""
        return (
            self.repository.find_all_with_dish_count().filter(dish_count__gt=0).count()
        )
