from django import template
from decimal import Decimal

register = template.Library()


@register.filter
def currency(value: float | int | Decimal | str, symbol: str = "$") -> str:
    """
    Formatea un valor numérico como moneda chilena.
    Formato: $ 1.000 (sin decimales, separador de miles con punto)
    """
    try:
        # Convertir a Decimal para manejar correctamente los números
        if isinstance(value, str):
            value = Decimal(value)
        elif not isinstance(value, Decimal):
            value = Decimal(str(value))

        # Redondear a entero (sin decimales)
        value = int(value)

        # Formatear con separador de miles usando punto
        formatted = f"{value:,}".replace(",", ".")

        return f"{symbol} {formatted}"
    except (ValueError, TypeError, Exception):
        # On error, ensure we return a string to match the filter signature
        return str(value)
