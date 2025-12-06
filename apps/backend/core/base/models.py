"""
Base model classes with timestamps and soft delete
"""

from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, Tuple, Type
from django.db import models
from django.conf import settings


class BaseModelMeta(models.base.ModelBase):
    """
    Metaclass that automatically adds db_table with prefix to models
    """

    def __new__(
        mcs: Type["BaseModelMeta"],
        name: str,
        bases: Tuple[type, ...],
        namespace: Dict[str, Any],
        **kwargs: Any,
    ) -> Type[models.Model]:
        # Create the class first
        cls = super().__new__(mcs, name, bases, namespace, **kwargs)

        # Only process concrete models (not abstract)
        if not cls._meta.abstract:  # type: ignore[attr-defined]
            # Get app_label and model_name from Django's Meta
            app_label: str = cls._meta.app_label  # type: ignore[attr-defined]
            model_name: str = cls._meta.model_name  # type: ignore[attr-defined]

            # Check if db_table was explicitly set by comparing with Django's default
            # Django's default format is: {app_label}_{model_name}
            default_table_name = f"{app_label}_{model_name}"
            current_table_name = cls._meta.db_table  # type: ignore[attr-defined]

            # Only set db_table if it's still using Django's default
            if current_table_name == default_table_name:
                # Get the table prefix from settings
                prefix = settings.DB_TABLE_PREFIX
                # Generate table name: savoro_dish, savoro_category, etc.
                cls._meta.db_table = f"{prefix}_{model_name}"  # type: ignore[attr-defined]

        return cls  # type: ignore[return]


class BaseModel(models.Model, metaclass=BaseModelMeta):
    """
    Base model with timestamps and soft delete
    Used by all domain entities

    Automatically generates db_table name with prefix from DB_TABLE_PREFIX setting
    Example: Dish model -> savoro_dish table
    """

    id: int

    created_at: models.DateTimeField[datetime, datetime] = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación",
    )
    updated_at: models.DateTimeField[datetime, datetime] = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización",
    )
    delete_at: models.DateTimeField[datetime | None, datetime | None] = (
        models.DateTimeField(
            blank=True,
            null=True,
            verbose_name="Fecha de eliminación",
        )
    )
    deleted: models.BooleanField[bool, bool] = models.BooleanField(
        default=False,
        verbose_name="Eliminado",
    )
    is_active: models.BooleanField[bool, bool] = models.BooleanField(
        default=True,
        verbose_name="Activo",
    )

    class Meta:
        abstract = True


class NamedModel(BaseModel):
    """
    Base model for entities with name
    Examples: Category, Table, Dish, etc.
    """

    name: models.CharField[str, str] = models.CharField(
        max_length=150, verbose_name="Nombre"
    )

    class Meta(BaseModel.Meta):
        abstract = True

    def __str__(self) -> str:
        return str(self.name)
