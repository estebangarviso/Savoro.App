"""
Authentication Service - Business logic layer for Authentication
Similar to NestJS Service (@Injectable())
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from django.contrib.auth import authenticate
from core import BaseService, Injectable, BadRequestException

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser


@Injectable()
class AuthenticationService(BaseService):
    """
    Service for Authentication business logic
    Contains all authentication-related operations and validations
    """

    def authenticate_user(
        self, username: str, password: str
    ) -> AbstractBaseUser | None:
        """
        Authenticate user with username and password
        Returns user if credentials are valid, None otherwise
        """
        user = authenticate(username=username, password=password)
        return user

    def validate_credentials(self, username: str, password: str) -> None:
        """
        Validate credentials format
        Raises BadRequestException if invalid
        """
        if not username or not password:
            raise BadRequestException("Usuario y contraseña son requeridos")

        if len(username) < 3:
            raise BadRequestException("El usuario debe tener al menos 3 caracteres")

        if len(password) < 4:
            raise BadRequestException("La contraseña debe tener al menos 4 caracteres")

    def get_user_display_name(self, user: Any) -> str:
        """Get user's display name (full name or username)"""
        if hasattr(user, "get_full_name") and callable(user.get_full_name):
            full_name = user.get_full_name()
            if full_name:
                return str(full_name)
        return str(user.get_username())
