"""
Price validators
"""

from django.core.exceptions import ValidationError
from decimal import Decimal


class PriceValidator:
    """Validator for price fields"""

    @staticmethod
    def validate_positive(value: Decimal):
        """Validate price is positive"""
        if value <= 0:
            raise ValidationError("Price must be greater than zero")

    @staticmethod
    def validate_max_digits(value: Decimal, max_digits: int = 8):
        """Validate max digits"""
        if len(str(value).replace(".", "")) > max_digits:
            raise ValidationError(f"Price cannot have more than {max_digits} digits")
