"""
Dish admin configuration
"""

from django.contrib import admin
from .models import Dish


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):  # type: ignore
    list_display = ["name", "category", "price", "is_active", "created_at"]
    list_filter = ["category", "tags", "is_active", "created_at"]
    search_fields = ["name", "description"]
    filter_horizontal = ["tags"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        ("Información básica", {"fields": ("name", "description", "price")}),
        ("Clasificación", {"fields": ("category", "tags")}),
        ("Media", {"fields": ("image",)}),
        ("Estado", {"fields": ("is_active", "deleted")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
