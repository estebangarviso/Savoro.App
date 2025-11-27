"""
Dish Service - Business logic layer for Dish
Similar to NestJS Service (@Injectable())
"""

from __future__ import annotations

from typing import Optional, Dict, Any
from django.db.models import QuerySet
from core import BaseService, Injectable, NotFoundException, BadRequestException
from core.utils import normalize_text
from .models import Dish
from .repository import DishRepository


# Lazy imports to avoid circular dependencies
def _get_category_model():
    from modules.category.models import Category

    return Category


def _get_food_tag_model():
    from modules.food_tag.models import FoodTag

    return FoodTag


@Injectable()
class DishService(BaseService):
    """
    Service for Dish business logic
    Contains all dish-related operations and validations
    """

    def __init__(self):
        self.repository = DishRepository()

    # ========================================================================
    # QUERY METHODS
    # ========================================================================

    def find_all(self) -> QuerySet[Dish]:
        """Get all dishes with relations"""
        return self.repository.find_all_with_relations()

    def find_one(self, dish_id: int) -> Dish:
        """Get dish by ID"""
        dish = self.repository.find_by_id(dish_id)
        if not dish:
            raise NotFoundException(f"Plato con ID {dish_id} no encontrado")
        return dish

    def find_filtered(
        self,
        search_query: Optional[str] = None,
        category_id: Optional[int] = None,
        tag_id: Optional[int] = None,
    ) -> QuerySet[Dish]:
        """
        Get filtered dishes
        Applies multiple filters based on provided parameters
        """
        queryset = self.repository.find_all_with_relations()

        if search_query:
            # Normalize search query for accent-insensitive search
            normalized_query = normalize_text(search_query)

            # Get all dishes and filter in Python for accent-insensitive search
            all_dishes = list(queryset)
            filtered_dishes = [
                dish
                for dish in all_dishes
                if normalized_query in normalize_text(dish.name)
                or normalized_query in normalize_text(dish.description or "")
            ]

            # Convert back to queryset by getting the IDs
            if filtered_dishes:
                dish_ids = [dish.id for dish in filtered_dishes]
                queryset = queryset.filter(id__in=dish_ids)
            else:
                # Return empty queryset
                queryset = queryset.none()

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if tag_id:
            queryset = queryset.filter(tags__id=tag_id).distinct()

        return queryset

    def find_by_category(self, category_id: int) -> QuerySet[Dish]:
        """Get dishes by category"""
        return self.repository.find_by_category(category_id)

    def find_without_category(self) -> QuerySet[Dish]:
        """Get dishes without category"""
        return self.repository.find_without_category()

    # ========================================================================
    # MUTATION METHODS
    # ========================================================================

    def create(self, data: Dict[str, Any]) -> Dish:
        """
        Create new dish
        Validates data before creation
        """
        # Validate name uniqueness
        if self.repository.exists_by_name(data.get("name", "")):
            raise BadRequestException(
                f"Ya existe un plato con el nombre '{data['name']}'"
            )

        # Validate category if provided
        if "category_id" in data and data["category_id"]:
            Category = _get_category_model()
            if not Category.objects.filter(
                pk=data["category_id"], deleted=False
            ).exists():
                raise BadRequestException("Categoría inválida")

        # Create dish
        tags = data.pop("tags", [])
        dish = self.repository.create(**data)

        # Add tags if provided
        if tags:
            from typing import cast

            FoodTag = _get_food_tag_model()

            dish.tags.set(cast(list[FoodTag], tags))  # type: ignore[misc]

        return dish

    def update(self, dish_id: int, data: Dict[str, Any]) -> Dish:
        """
        Update dish
        Validates data before update
        """
        # Check if dish exists
        dish = self.find_one(dish_id)

        # Validate name uniqueness if name is being changed
        if "name" in data and data["name"] != dish.name:
            if self.repository.exists_by_name(data["name"], exclude_id=dish_id):
                raise BadRequestException(
                    f"Ya existe un plato con el nombre '{data['name']}'"
                )

        # Validate category if provided
        if "category_id" in data and data["category_id"]:
            Category = _get_category_model()
            if not Category.objects.filter(
                pk=data["category_id"], deleted=False
            ).exists():
                raise BadRequestException("Categoría inválida")

        # Update tags if provided
        tags = data.pop("tags", None)
        if tags is not None:
            from typing import cast

            FoodTag = _get_food_tag_model()

            dish.tags.set(cast(list[FoodTag], tags))  # type: ignore[misc]

        # Update dish
        updated_dish = self.repository.update(dish_id, **data)
        if not updated_dish:
            raise NotFoundException(f"Plato con ID {dish_id} no encontrado")

        return updated_dish

    def delete(self, dish_id: int) -> bool:
        """
        Delete dish (soft delete)
        """
        # Check if dish exists
        self.find_one(dish_id)

        # Perform soft delete
        return self.repository.delete(dish_id)

    def toggle_active(self, dish_id: int) -> Dish:
        """Toggle dish active status"""
        dish = self.find_one(dish_id)
        dish.is_active = not dish.is_active
        dish.save()
        return dish

    # ========================================================================
    # STATISTICS AND AGGREGATIONS
    # ========================================================================

    def count_all(self) -> int:
        """Get total count of dishes"""
        return self.repository.find_all().count()

    def count_by_category(self, category_id: int) -> int:
        """Get count of dishes in category"""
        return self.repository.find_by_category(category_id).count()

    def count_active(self) -> int:
        """Get count of active dishes"""
        return self.repository.find_active().count()
