"""
Category forms
"""

from core.base.forms import BaseModelForm
from .models import Category


class CategoryForm(BaseModelForm):
    """Form for creating/updating categories"""

    class Meta(BaseModelForm.Meta):
        model = Category
        fields = ["name", "is_active"]
