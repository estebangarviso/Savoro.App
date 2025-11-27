"""
Development settings
"""

# pyright: reportConstantRedefinition=false

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES: dict[str, dict[str, str | Path]] = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Development-specific settings
INTERNAL_IPS = [
    "127.0.0.1",
]

# Email backend for development (console)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Vite Development Server Integration
VITE_DEV_MODE = True
VITE_DEV_SERVER_URL = "http://localhost:5173"

# Static files - point to Vite dev server in development
STATIC_URL = f"{VITE_DEV_SERVER_URL}/static/" if VITE_DEV_MODE else "/static/"
