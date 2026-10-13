"""
Tests for destination data, search, saved places, and AI assistance.
"""

import asyncio
import json
import os
from unittest.mock import Mock, patch

from django.test import TestCase

from web.backend.django.duckapp.destinations.models import (
    Destination as DestinationRecord,
    SavedDestination,
)
from web.prefill_db import DESTINATIONS, seed_destinations
from web.services import ai as ai_service
from web.services import destinations as destination_service
from web.ui.components.ai_assistant import AIAssistant
from web.urls import urlpatterns


class DestinationServiceTests(TestCase):
    """
    Verifies search behavior against database records.
    """

    def setUp(self):
        self.falls = DestinationRecord.objects.create(
            name="Victoria Falls",
            location="Victoria Falls, Matabeleland North",
            category="Nature",
            description="A waterfall on the Zambezi River.",
        )
        self.ruins = DestinationRecord.objects.create(
            name="Great Zimbabwe",
            location="Masvingo, Masvingo",
            category="Historical",
            description="An ancient stone city.",
        )

    def test_search_is_trimmed_case_insensitive_and_matches_name(self):
        results = destination_service.search_destinations("  vIcToRiA  ")

        self.assertEqual([item.destination_id for item in results], [self.falls.pk])

    def test_search_matches_location_and_can_combine_category(self):
        results = destination_service.search_destinations(
            query="masvingo",
            category="Historical",
        )

        self.assertEqual([item.destination_id for item in results], [self.ruins.pk])

    def test_empty_search_returns_all_records(self):
        results = destination_service.search_destinations("   ")

        self.assertEqual(
            [item.destination_id for item in results],
            [self.falls.pk, self.ruins.pk],
        )

    def test_search_with_no_matches_returns_empty_list(self):
        self.assertEqual(
            destination_service.search_destinations("no such place"),
            [],
        )

    def test_toggle_saved_persists_shared_state(self):
        saved = destination_service.toggle_saved(self.falls.pk)

        self.assertIsNotNone(saved)
        self.assertTrue(saved.is_saved)
        self.assertEqual(SavedDestination.objects.count(), 1)
        self.assertEqual(
            destination_service.list_saved_destinations()[0].destination_id,
            self.falls.pk,
        )

        unsaved = destination_service.toggle_saved(self.falls.pk)

        self.assertIsNotNone(unsaved)
        self.assertFalse(unsaved.is_saved)
        self.assertFalse(SavedDestination.objects.exists())


class DestinationSeedTests(TestCase):
    """
    Verifies the starter catalog is complete and safe to seed repeatedly.
    """

    def test_seed_database_is_idempotent_and_populates_licensed_images(self):
        seed_destinations()
        initial_count = DestinationRecord.objects.count()

        seed_destinations()

        self.assertGreaterEqual(initial_count, 20)
        self.assertEqual(initial_count, len(DESTINATIONS))
        self.assertEqual(DestinationRecord.objects.count(), initial_count)
        self.assertGreaterEqual(
            DestinationRecord.objects.exclude(image_url="")
            .exclude(image_credit="")
            .exclude(image_source_url="")
            .count(),
            20,
        )


class AIAssistantServiceTests(TestCase):
    """
    Verifies AI calls are made by app services from the live Lively interaction.
    """

    def setUp(self):
        self.falls = DestinationRecord.objects.create(
            name="Victoria Falls",
            location="Victoria Falls, Matabeleland North",
            category="Nature",
            description="A waterfall on the Zambezi River.",
        )

    def test_recommendations_return_catalog_records_with_ai_reasons(self):
        completion = json.dumps({
            "recommendations": [{
                "destination_id": self.falls.pk,
                "reason": "It matches your interest in waterfalls.",
            }],
        })
        with patch(
            "web.services.ai._request_completion",
            return_value=completion,
        ):
            recommendations = ai_service.recommend_destinations(
                "waterfalls",
                limit=2,
            )

        self.assertEqual(len(recommendations), 1)
        self.assertEqual(recommendations[0]["destination_id"], self.falls.pk)
        self.assertEqual(recommendations[0]["name"], self.falls.name)
        self.assertIn("waterfalls", recommendations[0]["reason"])

    def test_recommendations_reject_ids_outside_the_catalog(self):
        completion = json.dumps({
            "recommendations": [{
                "destination_id": self.falls.pk + 100,
                "reason": "Not in the database.",
            }],
        })
        with (
            patch(
                "web.services.ai._request_completion",
                return_value=completion,
            ),
            self.assertRaises(ai_service.AIServiceError),
        ):
            ai_service.recommend_destinations("waterfalls", limit=2)

    def test_chat_sends_catalog_context_and_component_history_to_provider(self):
        with patch(
            "web.services.ai._request_completion",
            return_value="Victoria Falls is a nature destination.",
        ) as request_completion:
            answer = ai_service.answer_travel_question(
                "Tell me more.",
                history=[{"role": "user", "content": "I like nature."}],
            )

        self.assertEqual(answer, "Victoria Falls is a nature destination.")
        messages = request_completion.call_args.args[0]
        self.assertEqual(messages[1]["role"], "user")
        self.assertEqual(messages[1]["content"], "I like nature.")
        self.assertEqual(messages[2]["content"], "Tell me more.")
        self.assertIn("Victoria Falls", messages[0]["content"])

    def test_provider_request_uses_server_key_and_requires_https(self):
        provider_payload = {
            "choices": [{
                "message": {"content": "A helpful answer."},
            }],
        }
        with (
            patch.dict(os.environ, {
                "AI_API_KEY": "test-key",
                "AI_API_BASE_URL": "https://provider.example/v1/chat/completions",
            }),
            patch("web.services.ai.urlopen") as open_url,
        ):
            response = open_url.return_value.__enter__.return_value
            response.read.return_value = json.dumps(provider_payload).encode()
            answer = ai_service._request_completion([
                {"role": "user", "content": "Hello"},
            ])

        request = open_url.call_args.args[0]
        self.assertEqual(answer, "A helpful answer.")
        self.assertEqual(
            request.get_header("Authorization"),
            "Bearer test-key",
        )

        with (
            patch.dict(os.environ, {
                "AI_API_KEY": "test-key",
                "AI_API_BASE_URL": "http://provider.example/v1/chat/completions",
            }),
            self.assertRaises(ai_service.AIConfigurationError),
        ):
            ai_service._request_completion([])

    def test_ai_is_not_configured_without_a_server_side_key(self):
        with patch.dict(os.environ, {"AI_API_KEY": ""}):
            self.assertFalse(ai_service.is_configured())

    def test_ai_interaction_is_not_exposed_as_an_app_api_route(self):
        self.assertFalse(
            any(route["url"].startswith("/api/ai/") for route in urlpatterns)
        )

    def test_lively_chat_handler_calls_service_and_keeps_session_history(self):
        assistant = object.__new__(AIAssistant)
        assistant.mode = "chat"
        assistant.prompt = "Tell me about Victoria Falls."
        assistant.history = [{"role": "user", "content": "I like nature."}]
        assistant.output = Mock()

        with (
            patch("web.services.ai.is_configured", return_value=True),
            patch(
                "web.services.ai.answer_travel_question",
                return_value="Victoria Falls is a nature destination.",
            ) as answer_question,
        ):
            asyncio.run(assistant.on_submit(None, "click", None, None))

        answer_question.assert_called_once_with(
            "Tell me about Victoria Falls.",
            [{"role": "user", "content": "I like nature."}],
        )
        self.assertEqual(assistant.history[-1], {
            "role": "assistant",
            "content": "Victoria Falls is a nature destination.",
        })
        assistant.output.clear_children.assert_called_once()
        assistant.output.add_child.assert_called()

    def test_lively_recommendation_handler_patches_catalog_results(self):
        assistant = object.__new__(AIAssistant)
        assistant.mode = "recommendations"
        assistant.prompt = "waterfalls"
        assistant.history = []
        assistant.output = Mock()
        recommendations = [{
            "destination_id": self.falls.pk,
            "name": self.falls.name,
            "location": self.falls.location,
            "category": self.falls.category,
            "description": self.falls.description,
            "reason": "It matches your interests.",
        }]

        with (
            patch("web.services.ai.is_configured", return_value=True),
            patch(
                "web.services.ai.recommend_destinations",
                return_value=recommendations,
            ) as recommend,
        ):
            asyncio.run(assistant.on_submit(None, "click", None, None))

        recommend.assert_called_once_with("waterfalls", 5)
        assistant.output.clear_children.assert_called_once()
        self.assertEqual(assistant.output.add_child.call_count, 4)
