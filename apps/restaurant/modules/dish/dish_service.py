"""
Dish Service - Business logic layer for Dish
Similar to NestJS Service (@Injectable())
"""

from typing import Optional, Dict, Any, List
from django.db.models import QuerySet
from ...common import BaseService, Injectable, NotFoundException, BadRequestException
from ...models import Dish, Category, FoodTag
from .dish_repository import DishRepository


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
            raise NotFoundException(f"Dish with ID {dish_id} not found")
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
            queryset = queryset.filter(
                models.Q(name__icontains=search_query)
                | models.Q(description__icontains=search_query)
            )

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
            raise BadRequestException(f"Dish with name '{data['name']}' already exists")

        # Validate category if provided
        if "category_id" in data and data["category_id"]:
            if not Category.objects.filter(
                pk=data["category_id"], deleted=False
            ).exists():
                raise BadRequestException("Invalid category")

        # Create dish
        tags = data.pop("tags", [])
        dish = self.repository.create(**data)

        # Add tags if provided
        if tags:
            dish.tags.set(tags)

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
                    f"Dish with name '{data['name']}' already exists"
                )

        # Validate category if provided
        if "category_id" in data and data["category_id"]:
            if not Category.objects.filter(
                pk=data["category_id"], deleted=False
            ).exists():
                raise BadRequestException("Invalid category")

        # Update tags if provided
        tags = data.pop("tags", None)
        if tags is not None:
            dish.tags.set(tags)

        # Update dish
        updated_dish = self.repository.update(dish_id, **data)
        if not updated_dish:
            raise NotFoundException(f"Dish with ID {dish_id} not found")

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


# Import models for type hints
from django.db import models
