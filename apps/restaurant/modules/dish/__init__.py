"""
Dish Module - Contains all dish-related logic
Similar to a NestJS module structure:
- dish.service.ts -> dish_service.py
- dish.controller.ts -> dish_controller.py
- dish.repository.ts -> dish_repository.py
- dto/ -> dto/
"""

from .dish_service import DishService
from .dish_repository import DishRepository
from .dish_controller import DishController

__all__ = ["DishService", "DishRepository", "DishController"]
