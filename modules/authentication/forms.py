"""Authentication forms"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    """Custom login form with Materialize CSS styling"""

    username = forms.CharField(
        label="Usuario",
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "validate", "placeholder": "Ingrese su usuario"}
        ),
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={"class": "validate", "placeholder": "Ingrese su contraseña"}
        ),
    )

    remember_me = forms.BooleanField(label="Recordarme", required=False, initial=False)
