"""
Base form classes with common functionality
"""

from django import forms
from typing import Any


class BaseModelForm(forms.ModelForm):  # type: ignore
    """
    Base form with common styling and validation
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)  # type: ignore
        # Apply Materialize classes to all fields
        for _, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({"class": "validate"})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({"class": "materialize-textarea"})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({"class": "browser-default"})
            elif isinstance(field.widget, forms.NumberInput):
                field.widget.attrs.update({"class": "validate"})
            elif isinstance(field.widget, forms.EmailInput):
                field.widget.attrs.update({"class": "validate", "type": "email"})

    def clean_name(self) -> str:
        """Common name validation"""
        name = self.cleaned_data.get("name", "")
        if name and len(name) < 3:
            raise forms.ValidationError("Name must be at least 3 characters")
        return name.strip()

    class Meta:
        abstract = True


class BaseSearchForm(forms.Form):
    """
    Base search form
    """

    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search...", "class": "validate"}),
    )
