"""
Base model classes with timestamps and soft delete
"""

from __future__ import annotations
from datetime import datetime
from django.db import models


class BaseModel(models.Model):
    """
    Base model with timestamps and soft delete
    Used by all domain entities
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
