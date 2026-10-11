"""
Views for the destination discovery app.

Each view returns a Page component directly — Duck's Lively engine
handles rendering, so there are no separate template files.
"""

import json
import logging
import time
from typing import Any
from urllib.parse import urlsplit

from django.core.cache import cache
from duck.http.response import JsonResponse
from duck.views import csrf_exempt

from web.services import ai as ai_service
from web.ui.pages.detail import DestinationDetailPage
from web.ui.pages.home import HomePage
from web.ui.pages.saved import SavedPage
from web.ui.pages.search import SearchPage


logger = logging.getLogger(__name__)
AI_REQUESTS_PER_MINUTE = 20


def _error_response(code: str, message: str, status: int) -> JsonResponse:
    """
    Creates a consistent JSON API error response.
    """
    return JsonResponse(
        content={"error": {"code": code, "message": message}},
        status_code=status,
    )


def _read_json_body(request: Any) -> tuple[dict | None, JsonResponse | None]:
    """
    Parses a bounded JSON request body and returns its object payload.
    """
    body = request.content if hasattr(request, "content") else request.body
    if len(body) > 16_384:
        return None, _error_response(
            "request_too_large",
            "The request body must not exceed 16 KB.",
            413,
        )

    try:
        payload = json.loads(body)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None, _error_response(
            "invalid_json",
            "The request body must be valid JSON.",
            400,
        )

    if not isinstance(payload, dict):
        return None, _error_response(
            "invalid_json",
            "The JSON request body must be an object.",
            400,
        )

    return payload, None


def _validate_text(
    value: Any,
    field: str,
    maximum_length: int,
) -> tuple[str | None, JsonResponse | None]:
    """
    Validates and trims a required user-provided text field.
    """
    if not isinstance(value, str) or not value.strip():
        return None, _error_response(
            "invalid_request",
            f"'{field}' must be a non-empty string.",
            400,
        )

    value = value.strip()
    if len(value) > maximum_length:
        return None, _error_response(
            "invalid_request",
            f"'{field}' must not exceed {maximum_length} characters.",
            400,
        )

    return value, None


def _origin_error(request: Any) -> JsonResponse | None:
    """
    Rejects browser requests originating from a different site.
    """
    origin = request.headers.get("Origin")
    if not origin:
        return None

    try:
        parsed_origin = urlsplit(origin)
    except ValueError:
        parsed_origin = None

    request_host = request.headers.get("Host", "")
    if (
        parsed_origin is None
        or parsed_origin.scheme not in {"http", "https"}
        or not parsed_origin.netloc
        or parsed_origin.path
        or parsed_origin.query
        or parsed_origin.fragment
        or parsed_origin.netloc.casefold() != request_host.casefold()
    ):
        return _error_response(
            "origin_not_allowed",
            "AI requests must come from the same site.",
            403,
        )

    return None


def _rate_limit_error(request: Any) -> JsonResponse | None:
    """
    Limits each client IP to 20 AI requests per minute.
    """
    client_ip = request.META.get("REMOTE_ADDR", "unknown")
    window = int(time.time() // 60)
    cache_key = f"ai-api:{client_ip}:{window}"

    if cache.add(cache_key, 1, timeout=60):
        return None

    try:
        request_count = cache.incr(cache_key)
    except ValueError:
        if cache.add(cache_key, 1, timeout=60):
            return None
        request_count = cache.incr(cache_key)

    if request_count <= AI_REQUESTS_PER_MINUTE:
        return None

    return _error_response(
        "rate_limit_exceeded",
        "Too many AI requests. Please try again in a minute.",
        429,
    )


def ai_capabilities(request):
    """
    Describes the AI assistance available to the app client.
    """
    return JsonResponse(content={
        "configured": ai_service.is_configured(),
        "capabilities": [
            {
                "id": "destination_recommendations",
                "description": (
                    "Suggests Zimbabwe destinations from the catalog based "
                    "on travel interests and preferences."
                ),
                "method": "POST",
                "path": "/api/ai/recommendations",
            },
            {
                "id": "travel_questions",
                "description": (
                    "Answers questions about listed destinations and how to "
                    "use search, categories, destination details, and saved places."
                ),
                "method": "POST",
                "path": "/api/ai/chat",
            },
        ],
    })


@csrf_exempt
def ai_recommendations(request):
    """
    Returns catalog-backed destination recommendations for trip preferences.
    """
    payload, error = _read_json_body(request)
    if error:
        return error

    error = _origin_error(request)
    if error:
        return error

    preferences, error = _validate_text(
        payload.get("preferences"),
        "preferences",
        2000,
    )
    if error:
        return error

    limit = payload.get("limit", 5)
    if type(limit) is not int or not 1 <= limit <= 10:
        return _error_response(
            "invalid_request",
            "'limit' must be an integer from 1 to 10.",
            400,
        )

    error = _rate_limit_error(request)
    if error:
        return error

    try:
        recommendations = ai_service.recommend_destinations(preferences, limit)
    except ai_service.AIConfigurationError as error:
        return _error_response("ai_not_configured", str(error), 503)
    except ai_service.AIServiceError:
        logger.exception("AI destination recommendations failed.")
        return _error_response(
            "ai_provider_error",
            "AI recommendations are temporarily unavailable.",
            502,
        )

    return JsonResponse(content={"recommendations": recommendations})


@csrf_exempt
def ai_chat(request):
    """
    Answers a travel or app-usage question with destination catalog context.
    """
    payload, error = _read_json_body(request)
    if error:
        return error

    error = _origin_error(request)
    if error:
        return error

    message, error = _validate_text(payload.get("message"), "message", 2000)
    if error:
        return error

    history = payload.get("history", [])
    if not isinstance(history, list) or len(history) > 10:
        return _error_response(
            "invalid_request",
            "'history' must be a list with at most 10 messages.",
            400,
        )

    normalized_history = []
    for item in history:
        if not isinstance(item, dict) or item.get("role") not in {
            "user",
            "assistant",
        }:
            return _error_response(
                "invalid_request",
                "Each history item must have a 'user' or 'assistant' role.",
                400,
            )

        content, error = _validate_text(item.get("content"), "history content", 2000)
        if error:
            return error

        normalized_history.append({"role": item["role"], "content": content})

    error = _rate_limit_error(request)
    if error:
        return error

    try:
        answer = ai_service.answer_travel_question(message, normalized_history)
    except ai_service.AIConfigurationError as error:
        return _error_response("ai_not_configured", str(error), 503)
    except ai_service.AIServiceError:
        logger.exception("AI travel assistant request failed.")
        return _error_response(
            "ai_provider_error",
            "AI assistance is temporarily unavailable.",
            502,
        )

    return JsonResponse(content={"answer": answer})


def home(request):
    """
    Renders the home page.
    """
    return HomePage(request=request)


def search(request):
    """
    Renders the search results page.
    """
    return SearchPage(request=request)


def saved(request):
    """
    Renders the saved destinations page.
    """
    return SavedPage(request=request)


def destination_detail(request):
    """
    Renders a single destination's detail page.
    """
    return DestinationDetailPage(request=request)
