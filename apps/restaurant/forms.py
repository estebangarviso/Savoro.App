from django import forms
from .models import Dish, Category, Menu, Table, Order, Reservation


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ["name", "description", "price", "category", "image", "tags"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "tags": forms.CheckboxSelectMultiple(),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ["name", "description", "dishes"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "dishes": forms.CheckboxSelectMultiple(),
        }


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ["name", "capacity"]


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["customer_name", "table", "reservation_datetime", "number_of_guests"]
        widgets = {
            "reservation_datetime": forms.DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["table", "customer_name", "status", "dishes"]
        widgets = {
            "dishes": forms.CheckboxSelectMultiple(),
        }


class LoginForm(forms.Form):
    username = forms.CharField(label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
