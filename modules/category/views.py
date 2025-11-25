"""
Category views - Thin adapters to controller
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from .controller import CategoryController


controller = CategoryController()


def list_categories(request: HttpRequest) -> HttpResponse:
    """List all categories"""
    return controller.index(request)


def detail_category(request: HttpRequest, category_id: int) -> HttpResponse:
    """Get category details"""
    return controller.show(request, category_id)


@login_required
def create_category(request: HttpRequest) -> HttpResponse:
    """Create a new category"""
    return controller.create(request)


@login_required
def update_category(request: HttpRequest, category_id: int) -> HttpResponse:
    """Update an existing category"""
    return controller.update(request, category_id)


@login_required
def delete_category(request: HttpRequest, category_id: int) -> HttpResponse:
    """Delete a category"""
    return controller.destroy(request, category_id)
