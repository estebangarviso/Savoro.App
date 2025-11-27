"""
FoodTag app configuration
"""
from django.apps import AppConfig


class FoodTagConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.food_tag"
    label = "food_tag"
    verbose_name = "Etiquetas Alimentarias"
