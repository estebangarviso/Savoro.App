"""
Order app configuration
"""
from django.apps import AppConfig


class OrderConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.order"
    label = "order"
    verbose_name = "Order"
