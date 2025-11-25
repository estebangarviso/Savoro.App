from django import template
from django.utils.html import format_html
from django.urls import reverse
from decimal import Decimal
from typing import Dict, Any

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


@register.simple_tag
def status_badge(status: str) -> str:
    """Render status badge with color based on status"""
    color_map = {
        "PENDING": "orange",
        "READY": "blue",
        "DELIVERED": "green",
        "CANCELLED": "red",
        "CONFIRMED": "green",
        "ACTIVE": "green",
        "INACTIVE": "grey",
    }

    color = color_map.get(status.upper(), "grey")
    return format_html(
        '<span class="new badge {}" data-badge-caption="">{}</span>', color, status
    )


@register.inclusion_tag("shared/fragments/pagination.html")  # type: ignore[misc]
def render_pagination(page_obj: Any) -> Dict[str, Any]:
    """Render pagination component"""
    return {"page_obj": page_obj}


@register.inclusion_tag("shared/fragments/filter_chip.html")  # type: ignore[misc]
def filter_chip(label: str, value: str, param_name: str):
    """Render filter chip"""
    return {
        "label": label,
        "value": value,
        "param_name": param_name,
    }


@register.simple_tag
def url_with_id(url_name: str, obj: Any = None) -> str:
    """
    Genera una URL de Django con el ID del objeto si es necesario.
    Si el objeto tiene un atributo 'id' con valor, lo usa como argumento.
    Si el objeto no tiene ID (nuevo objeto), genera la URL sin argumentos.
    """
    if obj and hasattr(obj, "id") and obj.id is not None:
        return reverse(
            url_name, kwargs={f"{obj.__class__.__name__.lower()}_id": obj.id}
        )
    return reverse(url_name)
