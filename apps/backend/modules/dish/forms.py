"""
Dish forms
"""

from typing import Any
from django import forms
from django.forms import Widget
from core.base.forms import BaseModelForm, BaseSearchForm
from .models import Dish, Category


class DishForm(BaseModelForm):
    class Meta(BaseModelForm.Meta):
        model = Dish
        fields = ["name", "description", "price", "category", "image", "tags"]
        widgets: dict[str, Widget] = {
            "description": forms.Textarea(
                attrs={"rows": 4, "class": "materialize-textarea"}
            ),
            "tags": forms.CheckboxSelectMultiple(),
        }


class DishSearchForm(BaseSearchForm):
    """Form for searching dishes"""

    category = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={"class": "browser-default"}),
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        categories = Category.objects.all()
        category_field = self.fields["category"]
        if isinstance(category_field, forms.ChoiceField):
            category_field.choices = [("", "Todas las categorías")] + [
                (c.id, c.name) for c in categories
            ]
