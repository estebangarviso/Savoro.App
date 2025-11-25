"""
Capacity validators
"""

from django.core.exceptions import ValidationError


class CapacityValidator:
    """Validator for capacity fields"""

    @staticmethod
    def validate_positive(value: int):
        """Validate capacity is positive"""
        if value <= 0:
            raise ValidationError("Capacity must be greater than zero")

    @staticmethod
    def validate_max(value: int, max_capacity: int = 50):
        """Validate max capacity"""
        if value > max_capacity:
            raise ValidationError(f"Capacity cannot exceed {max_capacity}")
