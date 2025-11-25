"""
Category controller - HTTP handlers
"""

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from core import BaseController, MessageMixin, PaginationMixin
from core.exceptions.http import NotFoundException
from modules.category.forms import CategoryForm
from .service import CategoryService


class CategoryController(BaseController, MessageMixin, PaginationMixin):
    """Controller for Category HTTP endpoints"""

    def __init__(self):
        self.service = CategoryService()

    def index(self, request: HttpRequest) -> HttpResponse:
        """List all categories with infinite scroll support"""
        # Get search query and page from request
        search_query = request.GET.get("search", "")
        status_filter = request.GET.get("status", "")
        page = request.GET.get("page", 1)

        # Get filtered categories with statistics
        all_categories = self.service.find_filtered_with_stats(
            search_query=search_query if search_query else None,
            is_active=status_filter if status_filter else None,
        )

        # Paginate results
        paginator = Paginator(all_categories, 12)  # 12 items per page
        categories = paginator.get_page(page)

        # Check if this is an AJAX request for infinite scroll
        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

        if is_ajax:
            # Return JSON response with HTML fragments
            html = render_to_string(
                "category/partials/category_cards.html",
                {"categories": categories},
                request=request,
            )
            return JsonResponse(
                {
                    "html": html,
                    "has_next": categories.has_next(),
                    "next_page": (
                        categories.next_page_number() if categories.has_next() else None
                    ),
                }
            )

        # Regular page load
        return render(
            request,
            "category/list.html",
            {
                "categories": categories,
                "search_query": search_query,
                "status_filter": status_filter,
                "total_count": paginator.count,
                "has_next": categories.has_next(),
            },
        )

    def show(self, request: HttpRequest, category_id: int) -> HttpResponse:
        """Show category details"""
        category = self.service.find_one(category_id)
        return render(request, "category/detail.html", {"category": category})

    def create(self, request: HttpRequest) -> HttpResponse:
        """Create new category"""
        if request.method == "POST":
            form = CategoryForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    category = self.service.create(form.cleaned_data)
                    return self.success_response(
                        request,
                        f"Categoría '{category.name}' creado exitosamente",
                        redirect_url="category:detail",
                        redirect_obj=category,
                    )
                except Exception as e:
                    return self.error_response(request, str(e))
        else:
            form = CategoryForm()

        return render(
            request,
            "category/form.html",
            {
                "form": form,
                "redirect": "category:list",
            },
        )

    def update(self, request: HttpRequest, category_id: int) -> HttpResponse:
        """Update ca"""
        try:
            category = self.service.find_one(category_id)
        except NotFoundException as e:
            return self.error_response(request, str(e), redirect_url="category:list")
        if request.method == "POST":
            form = CategoryForm(request.POST, request.FILES, instance=category)
            if form.is_valid():
                try:
                    updated_category = self.service.update(
                        category_id, form.cleaned_data
                    )
                    return self.success_response(
                        request,
                        f"Categoría '{updated_category.name}' actualizado",
                        redirect_url="category:detail",
                        redirect_obj=updated_category,
                    )
                except Exception as e:
                    return self.error_response(request, str(e))
        else:
            form = CategoryForm(instance=category)

        return render(
            request,
            "category/form.html",
            {
                "form": form,
                "redirect": "category:detail",
            },
        )

    def destroy(self, request: HttpRequest, category_id: int) -> HttpResponse:
        """Delete category"""
        try:
            category = self.service.find_one(category_id)
        except NotFoundException as e:
            return self.error_response(request, str(e), redirect_url="category:list")

        if request.method == "POST":
            try:
                self.service.delete(category_id)
                return self.success_response(
                    request,
                    "Categoría eliminada exitosamente",
                    redirect_url="category:list",
                )
            except Exception as e:
                return self.error_response(
                    request,
                    str(e),
                    redirect_url="category:detail",
                    redirect_obj=category,
                )

        # GET: Mostrar confirmación
        return render(
            request,
            "category/delete.html",
            {"category": category},
        )
