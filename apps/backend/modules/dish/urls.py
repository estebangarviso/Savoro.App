"""
Dish URLs
"""

from django.urls import path
from . import views

app_name = "dish"

urlpatterns = [
    path("", views.list_dishes, name="list"),
    path("new/", views.create_dish, name="create"),
    path("<int:dish_id>/", views.detail_dish, name="detail"),
    path("<int:dish_id>/edit/", views.update_dish, name="update"),
    path("<int:dish_id>/delete/", views.delete_dish, name="delete"),
]
