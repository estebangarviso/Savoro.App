"""
Dish views - Thin adapters to controller
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from .controller import DishController


controller = DishController()


def list_dishes(request: HttpRequest) -> HttpResponse:
    """List all dishes"""
    return controller.index(request)


def detail_dish(request: HttpRequest, dish_id: int) -> HttpResponse:
    """Get dish details"""
    return controller.show(request, dish_id)


@login_required
def create_dish(request: HttpRequest) -> HttpResponse:
    """Create new dish"""
    return controller.create(request)


@login_required
def update_dish(request: HttpRequest, dish_id: int) -> HttpResponse:
    """Update dish"""
    return controller.update(request, dish_id)


@login_required
def delete_dish(request: HttpRequest, dish_id: int) -> HttpResponse:
    """Delete dish"""
    return controller.destroy(request, dish_id)
