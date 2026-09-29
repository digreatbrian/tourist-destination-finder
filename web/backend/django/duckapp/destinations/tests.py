"""
Tests for destination data, search, and saved-place persistence.
"""

from django.core.management import call_command
from django.test import TestCase

from web.backend.django.duckapp.destinations.management.commands.seed_destinations import (
    DESTINATIONS,
)
from web.backend.django.duckapp.destinations.models import (
    Destination as DestinationRecord,
    SavedDestination,
)
from web.services import destinations as destination_service


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


class DestinationSeedCommandTests(TestCase):
    """
    Verifies the starter catalog is complete and safe to seed repeatedly.
    """

    def test_seed_command_is_idempotent_and_populates_licensed_images(self):
        call_command("seed_destinations")
        initial_count = DestinationRecord.objects.count()

        call_command("seed_destinations")

        self.assertGreaterEqual(initial_count, 20)
        self.assertEqual(initial_count, len(DESTINATIONS))
        self.assertEqual(DestinationRecord.objects.count(), initial_count)
        self.assertTrue(
            DestinationRecord.objects.exclude(image_url="")
            .exclude(image_credit="")
            .exclude(image_source_url="")
            .count()
            >= 20
        )
