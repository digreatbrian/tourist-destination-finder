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
    path("/api/ai/capabilities", views.ai_capabilities, "ai_capabilities", ["GET"]),
    path(
        "/api/ai/recommendations",
        views.ai_recommendations,
        "ai_recommendations",
        ["POST"],
    ),
    path("/api/ai/chat", views.ai_chat, "ai_chat", ["POST"]),
]
