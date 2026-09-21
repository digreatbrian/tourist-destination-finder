"""
App configuration for the destinations Django app.
"""

from django.apps import AppConfig


class DestinationsConfig(AppConfig):
    """
    Registers the destinations app with Django.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "web.backend.django.duckapp.destinations"
