"""
FoodTag model - Domain entity
"""

from core.base.models import NamedModel


class FoodTag(NamedModel):
    """
    Food tag entity
    Tags for dietary restrictions, allergens, etc.
    Examples: Vegan, Gluten-free, Spicy, Nuts, Dairy
    """

    class Meta(NamedModel.Meta):
        verbose_name = "Etiqueta alimentaria"
        verbose_name_plural = "Etiquetas alimentarias"
        ordering = ["name"]
        app_label = "food_tag"
        db_table = "savoro_food_tag"
