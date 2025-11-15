"""
Dish Controller - HTTP request handler for Dish
Similar to NestJS Controller (@Controller('dishes'))
"""

from typing import Dict, Any
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from ...common import BaseController, Controller
from ...forms import DishForm
from .dish_service import DishService
from ..category.category_service import CategoryService


@Controller("dishes")
class DishController(BaseController):
    """
    Controller for Dish endpoints
    Handles HTTP requests and delegates to DishService
    """

    def __init__(self):
        self.service = DishService()
        self.category_service = CategoryService()

    # ========================================================================
    # GET ENDPOINTS
    # ========================================================================

    @staticmethod
    @login_required(login_url="/")
    def index(request: HttpRequest) -> HttpResponse:
        """
        GET /dishes
        List all dishes with filters
        """
        controller = DishController()

        # Extract filter parameters
        search_query = request.GET.get("search", "")
        category_filter = request.GET.get("category", "")
        tag_filter = request.GET.get("tag", "")

        # Get filtered dishes
        filtered_dishes = controller.service.find_filtered(
            search_query=search_query if search_query else None,
            category_id=int(category_filter) if category_filter else None,
            tag_id=int(tag_filter) if tag_filter else None,
        )

        # Get categories with filtered dishes
        categories = controller.category_service.find_all_with_dishes(filtered_dishes)

        # Get uncategorized dishes
        uncategorized_dishes = filtered_dishes.filter(category__isnull=True)

        # Get filter options
        all_categories = controller.category_service.find_all()
        all_tags = controller.service.repository.model.tags.through.objects.all()

        context = {
            "categories": categories,
            "uncategorized_dishes": uncategorized_dishes,
            "all_categories": all_categories,
            "all_tags": all_tags,
            "search_query": search_query,
            "category_filter": category_filter,
            "tag_filter": tag_filter,
        }

        return render(request, "restaurant/index.html", context)

    @staticmethod
    @login_required(login_url="/")
    def detail(request: HttpRequest, dish_id: int) -> HttpResponse:
        """
        GET /dishes/:id
        Get dish details
        """
        controller = DishController()

        try:
            dish = controller.service.find_one(dish_id)
            return render(request, "restaurant/detail.html", {"dish": dish})
        except Exception as e:
            messages.error(request, str(e))
            return redirect("restaurant:index")

    # ========================================================================
    # CREATE ENDPOINT
    # ========================================================================

    @staticmethod
    @login_required(login_url="/")
    def create(request: HttpRequest) -> HttpResponse:
        """
        GET/POST /dishes/create
        Create new dish
        """
        controller = DishController()

        if request.method == "POST":
            form = DishForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    controller.service.create(form.cleaned_data)
                    messages.success(request, "Plato creado exitosamente")
                    return redirect("restaurant:index")
                except Exception as e:
                    messages.error(request, str(e))
        else:
            form = DishForm()

        context = {
            "form": form,
            "title": "Crear Plato",
            "cancel_url": "restaurant:index",
            "button_text": "Crear",
        }

        return render(request, "restaurant/form.html", context)

    # ========================================================================
    # UPDATE ENDPOINT
    # ========================================================================

    @staticmethod
    @login_required(login_url="/")
    def update(request: HttpRequest, dish_id: int) -> HttpResponse:
        """
        GET/POST /dishes/:id/update
        Update dish
        """
        controller = DishController()

        try:
            dish = controller.service.find_one(dish_id)
        except Exception as e:
            messages.error(request, str(e))
            return redirect("restaurant:index")

        if request.method == "POST":
            form = DishForm(request.POST, request.FILES, instance=dish)
            if form.is_valid():
                try:
                    controller.service.update(dish_id, form.cleaned_data)
                    messages.success(request, "Plato actualizado exitosamente")
                    return redirect("restaurant:detail", dish_id=dish.id)
                except Exception as e:
                    messages.error(request, str(e))
        else:
            form = DishForm(instance=dish)

        from django.urls import reverse

        context = {
            "form": form,
            "title": "Editar Plato",
            "cancel_url": reverse("restaurant:detail", kwargs={"dish_id": dish_id}),
            "button_text": "Actualizar",
        }

        return render(request, "restaurant/form.html", context)

    # ========================================================================
    # DELETE ENDPOINT
    # ========================================================================

    @staticmethod
    @login_required(login_url="/")
    def delete(request: HttpRequest, dish_id: int) -> HttpResponse:
        """
        GET/POST /dishes/:id/delete
        Delete dish
        """
        controller = DishController()

        if request.method == "POST":
            try:
                controller.service.delete(dish_id)

                # Return JSON for AJAX requests
                if request.headers.get("Content-Type") == "application/json":
                    return JsonResponse(
                        {"success": True, "message": "Plato eliminado exitosamente"}
                    )

                messages.success(request, "Plato eliminado exitosamente")
            except Exception as e:
                # Return JSON for AJAX requests
                if request.headers.get("Content-Type") == "application/json":
                    return JsonResponse({"success": False, "message": str(e)})

                messages.error(request, str(e))

            return redirect("restaurant:index")

        # GET request - show confirmation page
        try:
            dish = controller.service.find_one(dish_id)
        except Exception as e:
            messages.error(request, str(e))
            return redirect("restaurant:index")

        return render(request, "restaurant/dish_delete_confirm.html", {"dish": dish})
