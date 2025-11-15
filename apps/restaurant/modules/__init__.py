"""
Restaurant Module - Main module that aggregates all features
Similar to AppModule in NestJS
"""

from .dish import DishController
from .category import CategoryController

__all__ = ["DishController", "CategoryController"]
