"""
Template tags for Vite integration
"""

from django import template
from django.conf import settings
from django.templatetags.static import static as django_static
from django.utils.safestring import mark_safe
import json
import os

register = template.Library()


@register.simple_tag
def vite_asset(path: str) -> str:
    """
    Load Vite asset in development or production mode.

    Usage in templates:
        {% load vite_tags %}
        {% vite_asset "authentication/css/login.css" %}
        {% vite_asset "authentication/js/login.js" %}

    Args:
        path: Path to the asset relative to the static directory

    Returns:
        Full URL to the asset
    """
    if getattr(settings, "VITE_DEV_MODE", False):
        # Development mode: load from Vite dev server
        vite_url = getattr(settings, "VITE_DEV_SERVER_URL", "http://localhost:5173")
        return f"{vite_url}/static/{path}"

    # Production mode: load from manifest
    manifest_path = os.path.join(
        settings.BASE_DIR, "../frontend/staticfiles/manifest.json"
    )

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        # Look for the file in manifest
        if path in manifest:
            file_path = manifest[path]["file"]
            return f"{settings.STATIC_URL}{file_path}"
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        pass

    # Fallback: return the path as-is
    return f"{settings.STATIC_URL}{path}"


@register.simple_tag(name="static")
def static(path: str) -> str:
    """
    Override Django's static tag to work with Vite in development mode.

    For CSS/JS files: Uses Vite dev server in development, manifest in production
    For other files (images, etc.): Falls back to Django's default static handler

    Usage (no changes needed in existing templates):
        {% load vite_tags %}
        {% static "authentication/css/login.css" %}
        {% static "shared/images/logo.png" %}

    Args:
        path: Path to the asset relative to the static directory

    Returns:
        Full URL to the asset
    """
    # Check if it's a CSS or JS file that Vite handles
    if path.endswith((".css", ".js")):
        return vite_asset(path)

    # For other files (images, fonts, etc.), use Django's default static
    return django_static(path)


@register.simple_tag
def vite_hmr() -> str:
    """
    Inject Vite HMR client in development mode.

    Usage in base template:
        {% load vite_tags %}
        {% vite_hmr %}

    Returns:
        Script tag for Vite HMR client in development, empty string in production
    """
    if getattr(settings, "VITE_DEV_MODE", False):
        vite_url = getattr(settings, "VITE_DEV_SERVER_URL", "http://localhost:5173")
        return mark_safe(
            f'<script type="module" src="{vite_url}/@vite/client"></script>'
        )
    return ""
