"""
Category Controller - HTTP request handler for Category
Similar to NestJS Controller (@Controller('categories'))
"""

from __future__ import annotations

from typing import Dict, Any
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from ...common import BaseController, Controller
from ...forms import CategoryForm
from .category_service import CategoryService


@Controller("categories")
class CategoryController(BaseController):
    """
    Controller for Category endpoints
    Handles HTTP requests and delegates to CategoryService
    """

    def __init__(self):
        self.service = CategoryService()

    # ========================================================================
    # GET ENDPOINTS
    # ========================================================================

    @staticmethod
    @login_required(login_url="/")
    def list(request: HttpRequest) -> HttpResponse:
        """
        GET /categories
        List all categories with filters and statistics
        """
        controller = CategoryController()

        # Extract filter parameters
        search_query = request.GET.get("search", "")

        # Get filtered categories with stats
        categories = controller.service.find_filtered_with_stats(
            search_query=search_query if search_query else None
        )

        context: Dict[str, Any] = {
            "categories": categories,
            "search_query": search_query,
            "total_count": categories.count(),
        }

        return render(request, "restaurant/category/category_list.html", context)

    # ========================================================================
    # CREATE ENDPOINT
    # ========================================================================

    @staticmethod
    @login_required(login_url="/")
    def create(request: HttpRequest) -> HttpResponse:
        """
        GET/POST /categories/create
        Create new category
        """
        controller = CategoryController()

        if request.method == "POST":
            form = CategoryForm(request.POST)
            if form.is_valid():
                try:
                    controller.service.create(form.cleaned_data)
                    messages.success(request, "Categoría creada exitosamente")
                    return redirect("restaurant:category_list")
                except Exception as e:
                    messages.error(request, str(e))
        else:
            form = CategoryForm()

        context: Dict[str, Any] = {
            "form": form,
            "title": "Crear Categoría",
            "cancel_url": "restaurant:category_list",
            "button_text": "Crear",
        }

        return render(request, "restaurant/form.html", context)

    # ========================================================================
    # UPDATE ENDPOINT
    # ========================================================================

    @staticmethod
    @login_required(login_url="/")
    def update(request: HttpRequest, category_id: int) -> HttpResponse:
        """
        GET/POST /categories/:id/update
        Update category
        """
        controller = CategoryController()

        try:
            category = controller.service.find_one(category_id)
        except Exception as e:
            messages.error(request, str(e))
            return redirect("restaurant:category_list")

        if request.method == "POST":
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                try:
                    controller.service.update(category_id, form.cleaned_data)
                    messages.success(request, "Categoría actualizada exitosamente")
                    return redirect("restaurant:category_list")
                except Exception as e:
                    messages.error(request, str(e))
        else:
            form = CategoryForm(instance=category)

        context: Dict[str, Any] = {
            "form": form,
            "title": "Editar Categoría",
            "cancel_url": "restaurant:category_list",
            "button_text": "Actualizar",
        }

        return render(request, "restaurant/form.html", context)

    # ========================================================================
    # DELETE ENDPOINT
    # ========================================================================

    @staticmethod
    @login_required(login_url="/")
    def delete(request: HttpRequest, category_id: int) -> HttpResponse:
        """
        GET/POST /categories/:id/delete
        Delete category
        """
        controller = CategoryController()

        if request.method == "POST":
            try:
                controller.service.delete(category_id)

                # Return JSON for AJAX requests
                if request.headers.get("Content-Type") == "application/json":
                    return JsonResponse(
                        {"success": True, "message": "Categoría eliminada exitosamente"}
                    )

                messages.success(request, "Categoría eliminada exitosamente")
            except Exception as e:
                # Return JSON for AJAX requests
                if request.headers.get("Content-Type") == "application/json":
                    return JsonResponse({"success": False, "message": e})

                messages.error(request, str(e))

            return redirect("restaurant:category_list")

        # GET request - show confirmation page
        try:
            category = controller.service.find_one(category_id)
        except Exception as e:
            messages.error(request, str(e))
            return redirect("restaurant:category_list")

        return render(
            request,
            "restaurant/category/category_delete_confirm.html",
            {"category": category},
        )
