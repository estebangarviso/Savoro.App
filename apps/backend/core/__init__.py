"""
Core framework - Base abstractions for all modules

Usage:
    from core import BaseModel, Injectable, NotFoundException

Note: Imports are structured to avoid Django AppRegistryNotReady errors
"""

from __future__ import annotations

from typing import TYPE_CHECKING

# Decorators can be imported directly (no Django dependency)
from .decorators.nest_style import Controller, Injectable
# Exceptions can be imported directly (no Django dependency)
from .exceptions.http import (BadRequestException, ConflictException,
                              HttpException, NotFoundException,
                              UnauthorizedException)

# For type checking, import everything
if TYPE_CHECKING:
    from .base.controllers import BaseController
    from .base.forms import BaseModelForm, BaseSearchForm
    from .base.models import BaseModel, NamedModel
    from .base.repositories import BaseRepository
    from .base.services import BaseService
    from .mixins.export import ExportMixin
    from .mixins.filter import FilterMixin
    from .mixins.message import MessageMixin
    from .mixins.pagination import PaginationMixin
    from .validators.capacity import CapacityValidator
    from .validators.name import NameValidator
    from .validators.price import PriceValidator

__all__ = [
    # Base Classes
    "BaseModel",
    "NamedModel",
    "BaseRepository",
    "BaseService",
    "BaseController",
    "BaseModelForm",
    "BaseSearchForm",
    # Mixins
    "MessageMixin",
    "PaginationMixin",
    "FilterMixin",
    "ExportMixin",
    # Validators
    "NameValidator",
    "PriceValidator",
    "CapacityValidator",
    # Exceptions
    "HttpException",
    "NotFoundException",
    "BadRequestException",
    "UnauthorizedException",
    "ConflictException",
    # Decorators
    "Injectable",
    "Controller",
]


def __getattr__(name: str):
    """Lazy import to avoid Django AppRegistryNotReady errors"""
    if name == "BaseModel" or name == "NamedModel":
        from .base.models import BaseModel, NamedModel

        return BaseModel if name == "BaseModel" else NamedModel
    elif name == "BaseRepository":
        from .base.repositories import BaseRepository

        return BaseRepository
    elif name == "BaseService":
        from .base.services import BaseService

        return BaseService
    elif name == "BaseController":
        from .base.controllers import BaseController

        return BaseController
    elif name == "BaseModelForm":
        from .base.forms import BaseModelForm

        return BaseModelForm
    elif name == "BaseSearchForm":
        from .base.forms import BaseSearchForm

        return BaseSearchForm
    elif name == "MessageMixin":
        from .mixins.message import MessageMixin

        return MessageMixin
    elif name == "PaginationMixin":
        from .mixins.pagination import PaginationMixin

        return PaginationMixin
    elif name == "FilterMixin":
        from .mixins.filter import FilterMixin

        return FilterMixin
    elif name == "ExportMixin":
        from .mixins.export import ExportMixin

        return ExportMixin
    elif name == "NameValidator":
        from .validators.name import NameValidator

        return NameValidator
    elif name == "PriceValidator":
        from .validators.price import PriceValidator

        return PriceValidator
    elif name == "CapacityValidator":
        from .validators.capacity import CapacityValidator

        return CapacityValidator

    raise AttributeError(f"module 'core' has no attribute '{name}'")
