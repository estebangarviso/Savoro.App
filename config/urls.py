"""
URL configuration for restaurant project.
"""

from django.conf import settings
from django.conf.urls.static import static  # type: ignore
from django.contrib import admin
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import URLPattern, URLResolver, include, path
from config.settings import LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL


def root_redirect(request: HttpRequest) -> HttpResponseRedirect:
    if not request.user.is_authenticated:
        return redirect(LOGOUT_REDIRECT_URL)
    return redirect(LOGIN_REDIRECT_URL)


urlpatterns: list[URLResolver | URLPattern] = [
    path("admin/", admin.site.urls),
    # Authentication
    path("", include("modules.authentication.urls")),
    # Domain modules
    path("dishes/", include("modules.dish.urls")),
    path("categories/", include("modules.category.urls")),
    # Redirect root to login
    path("", root_redirect),
]

# Serve static and media files in development
if settings.DEBUG:
    # Serve media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve static files from STATIC_ROOT (compiled Vite assets)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
