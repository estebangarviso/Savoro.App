"""
FoodTag admin configuration
"""

from django.contrib import admin
from .models import FoodTag


@admin.register(FoodTag)
class FoodTagAdmin(admin.ModelAdmin):  # type: ignore
    list_display = ["name", "is_active", "created_at"]
    list_filter = ["is_active"]
    search_fields = ["name"]
