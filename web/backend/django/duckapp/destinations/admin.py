"""
Django admin registration for the destinations app.
"""

from django.contrib import admin

from .models import Destination, SavedDestination


admin.site.register(Destination)
admin.site.register(SavedDestination)
