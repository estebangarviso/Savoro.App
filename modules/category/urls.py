"""
Category URLs
"""

from django.urls import path
from . import views

app_name = "category"

urlpatterns = [
    path("", views.list_categories, name="list"),
    path("<int:category_id>/", views.detail_category, name="detail"),
    path("new/", views.create_category, name="create"),
    path("<int:category_id>/", views.detail_category, name="detail"),
    path("<int:category_id>/edit/", views.update_category, name="update"),
    path("<int:category_id>/delete/", views.delete_category, name="delete"),
]
