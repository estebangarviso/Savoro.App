"""
Menu app configuration
"""
from django.apps import AppConfig


class MenuConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.menu"
    label = "menu"
    verbose_name = "Menu"
