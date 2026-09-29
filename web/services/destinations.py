"""
Database-backed destination queries and saved-place operations.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from django.db import transaction
from django.db.models import Q

if TYPE_CHECKING:
    from web.backend.django.duckapp.destinations.models import (
        Destination as DestinationRecord,
        SavedDestination,
    )


CATEGORY_PRESENTATION = {
    "Culture": ("bi-brush-fill", "#F2545B"),
    "Historical": ("bi-bank", "#00B373"),
    "Lake": ("bi-water", "#0EA5E9"),
    "Mountains": ("bi-signpost-split-fill", "#22C55E"),
    "Nature": ("bi-tree-fill", "#22C55E"),
    "Wildlife": ("bi-binoculars-fill", "#8B5CF6"),
}
DEFAULT_PRESENTATION = ("bi-geo-alt-fill", "#008FFA")


@dataclass(frozen=True)
class Destination:
    """
    Represents a tourist destination shown in the app.
    """

    destination_id: int
    name: str
    location: str
    category: str
    description: str
    icon: str
    accent: str
    image_url: str
    image_credit: str
    image_source_url: str
    is_saved: bool = False


def _destination_models() -> tuple[type[DestinationRecord], type[SavedDestination]]:
    """
    Imports Django models lazily so Duck can load its route table before setup.
    """
    from web.backend.django.duckapp.destinations.models import (
        Destination as DestinationRecord,
        SavedDestination,
    )

    return DestinationRecord, SavedDestination


def _to_destination(record: DestinationRecord, is_saved: bool = False) -> Destination:
    """
    Converts a database record to the small display model used by the UI.
    """
    icon, accent = CATEGORY_PRESENTATION.get(
        record.category,
        DEFAULT_PRESENTATION,
    )
    return Destination(
        destination_id=record.pk,
        name=record.name,
        location=record.location,
        category=record.category,
        description=record.description,
        icon=icon,
        accent=accent,
        image_url=record.image_url,
        image_credit=record.image_credit,
        image_source_url=record.image_source_url,
        is_saved=is_saved,
    )


# Retrieval operations
def list_destinations() -> list[Destination]:
    """
    Returns all destinations in database order.
    """
    DestinationRecord, SavedDestination = _destination_models()
    records = list(DestinationRecord.objects.order_by("pk"))
    saved_ids = set(
        SavedDestination.objects.filter(
            destination_id__in=[record.pk for record in records]
        ).values_list("destination_id", flat=True)
    )
    return [
        _to_destination(record, is_saved=record.pk in saved_ids)
        for record in records
    ]


def list_categories() -> list[str]:
    """
    Returns distinct database categories in destination insertion order.
    """
    seen: list[str] = []
    DestinationRecord, _ = _destination_models()

    for category in DestinationRecord.objects.order_by("pk").values_list(
        "category",
        flat=True,
    ):
        if category not in seen:
            seen.append(category)

    return seen


def get_destination(destination_id: int) -> Destination | None:
    """
    Returns a single destination by id, or None if it does not exist.
    """
    DestinationRecord, SavedDestination = _destination_models()
    record = DestinationRecord.objects.filter(pk=destination_id).first()
    if record is None:
        return None

    is_saved = SavedDestination.objects.filter(destination=record).exists()
    return _to_destination(record, is_saved=is_saved)


def search_destinations(query: str = "", category: str = "") -> list[Destination]:
    """
    Filters the catalog by a free-text query and/or category.

    Args:
        query: Case-insensitive text matched against name and location.
        category: Exact category to filter by, ignored when empty.

    Returns:
        Matching destinations.
    """
    normalized_query = query.strip().lower()
    DestinationRecord, SavedDestination = _destination_models()
    records = DestinationRecord.objects.order_by("pk")

    if normalized_query:
        records = records.filter(
            Q(name__icontains=normalized_query)
            | Q(location__icontains=normalized_query)
        )

    if category:
        records = records.filter(category=category)

    records = list(records)
    saved_ids = set(
        SavedDestination.objects.filter(
            destination_id__in=[record.pk for record in records]
        ).values_list("destination_id", flat=True)
    )
    return [
        _to_destination(record, is_saved=record.pk in saved_ids)
        for record in records
    ]


def list_saved_destinations() -> list[Destination]:
    """
    Returns destinations currently marked as saved in the database.
    """
    _, SavedDestination = _destination_models()
    saved_records = SavedDestination.objects.select_related("destination").order_by(
        "saved_at",
        "destination_id",
    )
    return [
        _to_destination(saved.destination, is_saved=True)
        for saved in saved_records
    ]


# Mutation operations
def toggle_saved(destination_id: int) -> Destination | None:
    """
    Persists a global saved-state toggle for a destination.

    Returns:
        The updated destination, or None if it does not exist.
    """
    DestinationRecord, SavedDestination = _destination_models()
    with transaction.atomic():
        record = DestinationRecord.objects.select_for_update().filter(
            pk=destination_id
        ).first()
        if record is None:
            return None

        saved, created = SavedDestination.objects.get_or_create(destination=record)
        if created:
            is_saved = True
        else:
            saved.delete()
            is_saved = False

    return _to_destination(record, is_saved=is_saved)
