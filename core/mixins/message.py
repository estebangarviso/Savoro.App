"""
Message mixin for standardized user messages
"""

from __future__ import annotations
from typing import TYPE_CHECKING

from django.contrib import messages
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.db import models

if TYPE_CHECKING:
    from typing import Optional, Any


class MessageMixin:
    """Mixin for standardized user messages"""

    @staticmethod
    def _build_url_kwargs(obj: Any) -> dict[str, Any]:
        """Build URL kwargs from model instance"""
        if obj and isinstance(obj, models.Model) and hasattr(obj, "id"):
            model_name = obj.__class__.__name__.lower()
            return {f"{model_name}_id": obj.id}
        return {}

    @staticmethod
    def success_response(
        request: HttpRequest,
        message: str,
        redirect_url: Optional[str] = None,
        redirect_obj: Optional[Any] = None,
        url_args: Optional[list[Any]] = None,
        url_kwargs: Optional[dict[str, Any]] = None,
    ) -> HttpResponse:
        """
        Standard success response

        Args:
            request: HTTP request
            message: Success message to display
            redirect_url: URL name to redirect to
            redirect_obj: Model instance to extract ID from (auto-generates url_kwargs)
            url_args: Positional arguments for URL reverse
            url_kwargs: Keyword arguments for URL reverse
        """
        # Check if this is an AJAX request
        is_ajax = (
            request.headers.get("X-Requested-With") == "XMLHttpRequest"
            or "application/json" in request.headers.get("Accept", "")
            or "application/json" in request.headers.get("Content-Type", "")
        )

        if is_ajax:
            return JsonResponse({"success": True, "message": message})

        messages.success(request, message)
        if redirect_url:
            # Auto-generate url_kwargs from redirect_obj if provided
            if redirect_obj and not url_kwargs:
                url_kwargs = MessageMixin._build_url_kwargs(redirect_obj)

            # If url_args or url_kwargs provided, use reverse to build URL
            if url_args or url_kwargs:
                redirect_url = reverse(redirect_url, args=url_args, kwargs=url_kwargs)
            return redirect(redirect_url)
        # If no redirect_url provided, return to referrer or home
        return redirect(request.META.get("HTTP_REFERER", "/"))

    @staticmethod
    def error_response(
        request: HttpRequest,
        message: str,
        redirect_url: Optional[str] = None,
        redirect_obj: Optional[Any] = None,
        url_args: Optional[list[Any]] = None,
        url_kwargs: Optional[dict[str, Any]] = None,
    ) -> HttpResponse:
        """
        Standard error response

        Args:
            request: HTTP request
            message: Error message to display
            redirect_url: URL name to redirect to
            redirect_obj: Model instance to extract ID from (auto-generates url_kwargs)
            url_args: Positional arguments for URL reverse
            url_kwargs: Keyword arguments for URL reverse
        """
        # Check if this is an AJAX request
        is_ajax = (
            request.headers.get("X-Requested-With") == "XMLHttpRequest"
            or "application/json" in request.headers.get("Accept", "")
            or "application/json" in request.headers.get("Content-Type", "")
        )

        if is_ajax:
            return JsonResponse({"success": False, "message": message}, status=400)

        messages.error(request, message)
        if redirect_url:
            # Auto-generate url_kwargs from redirect_obj if provided
            if redirect_obj and not url_kwargs:
                url_kwargs = MessageMixin._build_url_kwargs(redirect_obj)

            # If url_args or url_kwargs provided, use reverse to build URL
            if url_args or url_kwargs:
                redirect_url = reverse(redirect_url, args=url_args, kwargs=url_kwargs)
            return redirect(redirect_url)
        # If no redirect_url provided, return to referrer or home
        return redirect(request.META.get("HTTP_REFERER", "/"))
