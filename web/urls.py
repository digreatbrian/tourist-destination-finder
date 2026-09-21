"""
URL patterns for the destination discovery app.
"""
from duck.urls import path

from web import views


urlpatterns = [
    path("/", views.home, "home", ["GET"]),
    path("/search", views.search, "search", ["GET"]),
    path("/saved", views.saved, "saved", ["GET"]),
    path("/destination", views.destination_detail, "destination_detail", ["GET"]),
]
