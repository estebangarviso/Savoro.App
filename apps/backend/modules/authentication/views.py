"""
Authentication views - Thin adapters to controller
"""

from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from .controller import AuthenticationController


controller = AuthenticationController()


def login_view(request: HttpRequest) -> HttpResponse:
    """Handle user login"""
    return controller.login_view(request)


@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    """Handle user logout"""
    return controller.logout_view(request)
