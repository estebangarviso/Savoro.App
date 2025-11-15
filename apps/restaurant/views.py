from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from typing import Dict, Any
from .forms import LoginForm

# Import controllers (similar to importing controllers in NestJS routes)
from .modules.dish import DishController
from .modules.category import CategoryController


# ============================================================================
# AUTHENTICATION VIEWS
# ============================================================================


def login_view(request: HttpRequest) -> HttpResponse:
    """Login view - handles user authentication"""
    form = LoginForm(request.POST or None)
    context: Dict[str, Any] = {
        "message": None,
        "form": form,
        "button_text": "Iniciar sesión",
    }
    if request.POST and form.is_valid():
        user = authenticate(**form.cleaned_data)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("restaurant:index")
            else:
                context["message"] = "El usuario ha sido desactivado"
        else:
            context["message"] = "Usuario o contraseña incorrecta"
    return render(request, "restaurant/login.html", context)


@login_required(login_url="/")
def log_out(request: HttpRequest) -> HttpResponse:
    """Logout view - handles user logout"""
    logout(request)
    return redirect("restaurant:login")


# ============================================================================
# DISH VIEWS - Adapters to DishController
# These views act as thin adapters delegating to the controller layer
# Similar to routing in NestJS: route → controller → service → repository
# ============================================================================


def index(request: HttpRequest) -> HttpResponse:
    """GET /dishes - List dishes with filters"""
    return DishController.index(request)


def detail(request: HttpRequest, dish_id: int) -> HttpResponse:
    """GET /dishes/:id - Get dish details"""
    return DishController.detail(request, dish_id)


def create(request: HttpRequest) -> HttpResponse:
    """GET/POST /dishes/create - Create new dish"""
    return DishController.create(request)


def update(request: HttpRequest, dish_id: int) -> HttpResponse:
    """GET/POST /dishes/:id/update - Update dish"""
    return DishController.update(request, dish_id)


def delete(request: HttpRequest, dish_id: int) -> HttpResponse:
    """POST /dishes/:id/delete - Delete dish"""
    return DishController.delete(request, dish_id)


# ============================================================================
# CATEGORY VIEWS - Adapters to CategoryController
# ============================================================================


def category_list(request: HttpRequest) -> HttpResponse:
    """GET /categories - List categories with filters"""
    return CategoryController.list(request)


def category_create(request: HttpRequest) -> HttpResponse:
    """GET/POST /categories/create - Create new category"""
    return CategoryController.create(request)


def category_update(request: HttpRequest, category_id: int) -> HttpResponse:
    """GET/POST /categories/:id/update - Update category"""
    return CategoryController.update(request, category_id)


def category_delete(request: HttpRequest, category_id: int) -> HttpResponse:
    """POST /categories/:id/delete - Delete category"""
    return CategoryController.delete(request, category_id)
