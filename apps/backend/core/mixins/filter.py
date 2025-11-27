"""
Filter mixin
"""

from django.http import HttpRequest


class FilterMixin:
    """Mixin for common filtering operations"""

    @staticmethod
    def get_filters_from_request(request: HttpRequest, allowed_filters: list) -> dict:
        """Extract filters from request"""
        filters = {}
        for filter_name in allowed_filters:
            value = request.GET.get(filter_name)
            if value:
                filters[filter_name] = value
        return filters
