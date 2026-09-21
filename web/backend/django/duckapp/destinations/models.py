"""
Django models for destinations and saved places.

Schema ported from the previous Kivy app's SQLAlchemy models
(`DestinationRecord`, `SavedDestinationRecord`) to Duck's Django backend.
Run `manage.py makemigrations destinations` and `migrate` before use —
the UI currently reads from `web.services.destinations` static data.
"""

from django.db import models


class Destination(models.Model):
    """
    Stores a tourist destination in the database.
    """

    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.CharField(max_length=2000, blank=True, default="")
    image_url = models.CharField(max_length=1000, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("name", "location")
        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["location"]),
        ]

    def __str__(self) -> str:
        """
        Returns a readable label for admin and shell use.
        """
        return f"{self.name} ({self.location})"


class SavedDestination(models.Model):
    """
    Stores a user's saved destination reference.
    """

    destination = models.OneToOneField(
        Destination,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="saved_entry",
    )
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """
        Returns a readable label for admin and shell use.
        """
        return f"Saved: {self.destination.name}"
