"""
Settings module __init__.py
Loads settings based on environment
"""

import os

# Determine which settings to use
ENV = os.environ.get("DJANGO_ENV", "development")

if ENV == "production":
    from .production import *

    print("Loaded production settings")
elif ENV == "development":
    from .development import *

    print("Loaded development settings")
else:
    from .development import *

    print("Loaded default development settings")
