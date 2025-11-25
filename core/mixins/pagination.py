"""
Pagination mixin
"""

from django.http import HttpRequest
from django.core.paginator import Paginator, EmptyPage
from typing import Any


class PaginationMixin:
    """Mixin for pagination"""

    @staticmethod
    def paginate(queryset: Any, request: HttpRequest, per_page: int = 20):
        """Paginate queryset"""
        page = request.GET.get("page", 1)
        paginator = Paginator(queryset, per_page)

        try:
            items = paginator.page(page)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        return items
