"""
Dish Controller - HTTP request handler for Dish
"""

from __future__ import annotations

from typing import Dict, Any
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.template.loader import render_to_string

# Try to import core helpers; if unavailable (e.g. static analysis), provide minimal fallbacks
from core import (
    BaseController,
    Controller,
    MessageMixin,
    PaginationMixin,
    FilterMixin,
    NotFoundException,
)

from .forms import DishForm
from .service import DishService
from modules.category.service import CategoryService
from modules.food_tag.models import FoodTag


@Controller("dishes")
class DishController(BaseController, MessageMixin, PaginationMixin, FilterMixin):
    """
    Dish Controller
    Handles HTTP requests for dish operations
    """

    def __init__(self):
        self.service = DishService()
        self.category_service = CategoryService()

    def index(self, request: HttpRequest) -> HttpResponse:
        """List all dishes with filters and infinite scroll support"""
        # Get filters from request
        search_query = request.GET.get("search", "")
        category_id = request.GET.get("category", "")
        tag_id = request.GET.get("tag", "")
        page = request.GET.get("page", 1)

        # Apply filters
        dishes = self.service.find_filtered(
            search_query=search_query if search_query else None,
            category_id=int(category_id) if category_id else None,
            tag_id=int(tag_id) if tag_id else None,
        )

        # Get all categories with dishes for this queryset
        categories = self.category_service.find_all_with_dishes(dishes)

        # Get uncategorized dishes
        uncategorized_dishes = list(dishes.filter(category__isnull=True))

        # Create a list of "sections" (category + dishes or uncategorized)
        sections = []
        for category in categories:
            # Only add sections that have dishes
            category_dishes = list(category.dishes.all())
            if category_dishes:
                sections.append(
                    {
                        "type": "category",
                        "category": category,
                        "dishes": category_dishes,
                    }
                )

        if uncategorized_dishes:
            sections.append({"type": "uncategorized", "dishes": uncategorized_dishes})

        # Paginate sections instead of individual dishes
        paginator = Paginator(sections, 3)  # 3 sections (categories) per page
        paginated_sections = paginator.get_page(page)

        # Check if this is an AJAX request for infinite scroll
        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

        if is_ajax:
            # Return JSON response with HTML fragments
            html = render_to_string(
                "dish/partials/dish_sections.html",
                {
                    "sections": paginated_sections,
                },
                request=request,
            )
            return JsonResponse(
                {
                    "html": html,
                    "has_next": paginated_sections.has_next(),
                    "next_page": (
                        paginated_sections.next_page_number()
                        if paginated_sections.has_next()
                        else None
                    ),
                }
            )

        # Regular page load
        # Get all categories and tags for filters
        all_categories = self.category_service.find_all()
        all_tags = FoodTag.objects.all()

        context: Dict[str, Any] = {
            "sections": paginated_sections,
            "all_categories": all_categories,
            "all_tags": all_tags,
            "search_query": search_query,
            "category_filter": category_id,
            "tag_filter": tag_id,
            "has_next": paginated_sections.has_next(),
        }

        return render(request, "dish/list.html", context)

    def show(self, request: HttpRequest, dish_id: int) -> HttpResponse:
        """Show dish details"""
        try:
            dish = self.service.find_one(dish_id)
            return render(request, "dish/detail.html", {"dish": dish})
        except NotFoundException as e:
            return self.error_response(request, str(e), redirect_url="dish:list")

    def create(self, request: HttpRequest) -> HttpResponse:
        """Create new dish"""
        if request.method == "POST":
            form = DishForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    dish = self.service.create(form.cleaned_data)
                    return self.success_response(
                        request,
                        f"Plato '{dish.name}' creado exitosamente",
                        redirect_url="dish:list",
                    )
                except Exception as e:
                    return self.error_response(request, str(e))
        else:
            form = DishForm()

        return render(
            request,
            "dish/form.html",
            {
                "form": form,
                "redirect": "dish:list",
            },
        )

    def update(self, request: HttpRequest, dish_id: int) -> HttpResponse:
        """Update dish"""
        try:
            dish = self.service.find_one(dish_id)
        except NotFoundException as e:
            return self.error_response(request, str(e), redirect_url="dish:list")

        if request.method == "POST":
            form = DishForm(request.POST, request.FILES, instance=dish)
            if form.is_valid():
                try:
                    updated_dish = self.service.update(dish_id, form.cleaned_data)
                    return self.success_response(
                        request,
                        f"Plato '{updated_dish.name}' actualizado",
                        redirect_url="dish:list",
                    )
                except Exception as e:
                    return self.error_response(request, str(e))
        else:
            form = DishForm(instance=dish)

        return render(
            request,
            "dish/form.html",
            {
                "form": form,
                "redirect": "dish:detail",
            },
        )

    def destroy(self, request: HttpRequest, dish_id: int) -> HttpResponse:
        """Delete dish"""
        try:
            dish = self.service.find_one(dish_id)
        except NotFoundException as e:
            return self.error_response(request, str(e), redirect_url="dish:list")

        if request.method == "POST":
            try:
                self.service.delete(dish_id)
                return self.success_response(
                    request, "Plato eliminado exitosamente", redirect_url="dish:list"
                )
            except Exception as e:
                return self.error_response(
                    request,
                    str(e),
                    redirect_url="dish:detail",
                    redirect_obj=dish,
                )

        # GET: Mostrar confirmación
        return render(
            request,
            "dish/delete.html",
            {"dish": dish},
        )
