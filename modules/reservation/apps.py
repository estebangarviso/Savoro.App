"""
Reservation app configuration
"""
from django.apps import AppConfig


class ReservationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.reservation"
    label = "reservation"
    verbose_name = "Reservation"
