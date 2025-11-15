from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "restaurant"

urlpatterns = (
    [
        # Authentication
        path("", views.login_view, name="login"),
        path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
        # Dishes
        path("dishes/", views.index, name="index"),
        path("dishes/new/", views.create, name="create"),
        path("dishes/<int:dish_id>/", views.detail, name="detail"),
        path("dishes/<int:dish_id>/edit/", views.update, name="update"),
        path("dishes/<int:dish_id>/delete/", views.delete, name="delete"),
        # Categories
        path("categories/", views.category_list, name="category_list"),
        path("categories/new/", views.category_create, name="category_create"),
        path(
            "categories/<int:category_id>/edit/",
            views.category_update,
            name="category_update",
        ),
        path(
            "categories/<int:category_id>/delete/",
            views.category_delete,
            name="category_delete",
        ),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
