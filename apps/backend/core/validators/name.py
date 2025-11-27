"""
Reusable validators for business logic
"""

from django.core.exceptions import ValidationError
from decimal import Decimal
from typing import Any


class NameValidator:
    """Validate name fields"""

    @staticmethod
    def validate(name: str, min_length: int = 3, max_length: int = 150) -> str:
        """Validate name"""
        if not name or not name.strip():
            raise ValidationError("Name cannot be empty")

        name = name.strip()

        if len(name) < min_length:
            raise ValidationError(f"Name must be at least {min_length} characters")

        if len(name) > max_length:
            raise ValidationError(f"Name cannot exceed {max_length} characters")

        return name


class PriceValidator:
    """Validate price fields"""

    @staticmethod
    def validate(price: Any, min_price: Decimal = Decimal("0.01")) -> Decimal:
        """Validate price"""
        try:
            price = Decimal(str(price))
        except Exception:
            raise ValidationError("Invalid price format")

        if price < min_price:
            raise ValidationError(f"Price must be at least {min_price}")

        return price


class CapacityValidator:
    """Validate capacity fields"""

    @staticmethod
    def validate(capacity: int, min_capacity: int = 1, max_capacity: int = 100) -> int:
        """Validate capacity"""
        try:
            capacity = int(capacity)
        except Exception:
            raise ValidationError("Invalid capacity format")

        if capacity < min_capacity:
            raise ValidationError(f"Capacity must be at least {min_capacity}")

        if capacity > max_capacity:
            raise ValidationError(f"Capacity cannot exceed {max_capacity}")

        return capacity
