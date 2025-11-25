"""
Dish model - Domain entity
"""

from __future__ import annotations
from decimal import Decimal
from django.db import models
from django.urls import reverse_lazy
from django.core.validators import MinValueValidator

from core.base.models import NamedModel
from modules.category.models import Category
from modules.food_tag.models import FoodTag


class Dish(NamedModel):
    """
    Dish entity
    Main menu item with price, description, image, category and tags
    """

    description: models.TextField[str, str] = models.TextField(
        blank=True, verbose_name="Descripción"
    )
    price: models.DecimalField[Decimal, Decimal] = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Precio",
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    image = models.ImageField(
        upload_to="dishes/",
        blank=True,
        null=True,
        verbose_name="Imagen",
    )
    category: models.ForeignKey[Category] = models.ForeignKey(
        "category.Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Categoría",
        related_name="dishes",
    )
    tags: models.ManyToManyField[FoodTag, FoodTag] = models.ManyToManyField(
        "food_tag.FoodTag",
        verbose_name="Etiquetas",
        related_name="dishes",
        blank=True,
        db_table="savoro_dish_tags",
    )

    class Meta(NamedModel.Meta):
        verbose_name = "Plato"
        verbose_name_plural = "Platos"
        ordering = ["name"]
        app_label = "dish"
        db_table = "savoro_dish"

    def get_absolute_url(self):
        return reverse_lazy("dish:detail", kwargs={"dish_id": self.pk})
