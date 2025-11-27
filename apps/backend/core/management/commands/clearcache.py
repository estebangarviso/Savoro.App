"""
Clear cache command - Clear all caches
"""

from typing import Any
from django.core.management.base import BaseCommand
from django.core.cache import caches


class Command(BaseCommand):
    help = "Clear cache"

    def handle(self, *args: Any, **options: Any):
        for backend_name in caches:
            caches[backend_name].clear()
            self.stdout.write(f"Cleared cache '{backend_name}'.")
