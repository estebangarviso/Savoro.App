"""
Authentication Controller - HTTP request handler for Authentication
"""

from __future__ import annotations

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse

from config.settings import LOGIN_URL, LOGOUT_REDIRECT_URL, LOGIN_REDIRECT_URL
from core import BaseController, Controller, MessageMixin
from .forms import LoginForm
from .service import AuthenticationService


@Controller("authentication")
class AuthenticationController(BaseController, MessageMixin):
    """
    Authentication Controller
    Handles HTTP requests for authentication operations
    """

    def __init__(self):
        self.service = AuthenticationService()

    def login_view(self, request: HttpRequest) -> HttpResponse:
        """Handle user login"""
        # Redirect if already authenticated
        if request.user.is_authenticated:
            return redirect(LOGIN_REDIRECT_URL)

        if request.method == "POST":
            form = LoginForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()

                # Login user
                login(request, user)

                # Handle remember me
                if not form.cleaned_data.get("remember_me"):
                    request.session.set_expiry(0)

                # Get user display name
                display_name = self.service.get_user_display_name(user)

                # Success message
                return self.success_response(
                    request,
                    f"¡Bienvenido {display_name}!",
                    redirect_url=request.GET.get("next", "dish:list"),
                )
            else:
                return self.error_response(
                    request,
                    "Usuario o contraseña incorrectos.",
                    redirect_url=LOGIN_URL,
                )
        else:
            form = LoginForm()

        return render(
            request, "authentication/login.html", {"form": form, "add_seo_meta": False}
        )

    def logout_view(self, request: HttpRequest) -> HttpResponse:
        """Handle user logout"""
        logout(request)
        return self.success_response(
            request,
            "Has cerrado sesión correctamente.",
            redirect_url=LOGOUT_REDIRECT_URL,
        )
