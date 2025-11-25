"""
Category model - Domain entity
"""

from core.base.models import NamedModel


class Category(NamedModel):
    """
    Category entity
    Used to classify dishes
    """

    class Meta(NamedModel.Meta):
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["name"]
        app_label = "category"
        db_table = "savoro_category"
