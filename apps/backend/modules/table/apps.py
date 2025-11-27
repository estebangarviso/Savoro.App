"""
Table app configuration
"""
from django.apps import AppConfig


class TableConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.table"
    label = "table"
    verbose_name = "Table"
