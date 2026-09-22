"""
Static destination data and in-memory lookup helpers.

Values here stand in for real database records until the Django models
in `web.backend.django.duckapp.destinations` are migrated and wired up.
"""

from dataclasses import dataclass, replace


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
    """Bootstrap Icons class suffix, e.g. "bi-droplet-fill" (no "bi " prefix)."""
    accent: str
    is_saved: bool = False


# Static destination catalog
DESTINATIONS: list[Destination] = [
    Destination(1, "Victoria Falls", "Victoria Falls", "Nature",
                "One of the world's largest waterfalls, straddling the Zambezi River.",
                "bi-droplet-fill", "#008FFA"),
    Destination(2, "Great Zimbabwe", "Masvingo", "Historical",
                "Stone-built ruins of the medieval capital that gave the country its name.",
                "bi-bank", "#00B373"),
    Destination(3, "Matobo Hills", "Bulawayo", "Nature",
                "Ancient granite kopjes, rock art, and Cecil Rhodes' grave.",
                "bi-tree-fill", "#F2A900"),
    Destination(4, "Hwange National Park", "Hwange", "Wildlife",
                "Zimbabwe's largest game reserve, home to large elephant herds.",
                "bi-binoculars-fill", "#8B5CF6"),
    Destination(5, "Mana Pools", "Mashonaland West", "Wildlife",
                "UNESCO-listed floodplain known for walking safaris among wildlife.",
                "bi-binoculars-fill", "#F2545B"),
    Destination(6, "Lake Kariba", "Kariba", "Lake",
                "One of the world's largest man-made lakes, popular for houseboats.",
                "bi-water", "#0EA5E9"),
    Destination(7, "Chimanimani", "Manicaland", "Mountains",
                "Rugged mountain trails and border-hugging scenery in the east.",
                "bi-signpost-split-fill", "#22C55E"),
    Destination(8, "Chinhoyi Caves", "Chinhoyi", "Nature",
                "Limestone caves with a striking cobalt-blue sinkhole pool.",
                "bi-moon-stars-fill", "#0EA5E9"),
]


# Retrieval operations
def list_destinations() -> list[Destination]:
    """
    Returns all destinations in the static catalog.
    """
    return list(DESTINATIONS)


def list_categories() -> list[str]:
    """
    Returns the distinct categories present in the catalog, in display order.
    """
    seen: list[str] = []

    # Collect unique categories preserving first-seen order
    for destination in DESTINATIONS:
        if destination.category not in seen:
            seen.append(destination.category)

    return seen


def get_destination(destination_id: int) -> Destination | None:
    """
    Returns a single destination by id, or None if it does not exist.
    """
    for destination in DESTINATIONS:
        if destination.destination_id == destination_id:
            return destination

    return None


def search_destinations(query: str = "", category: str = "") -> list[Destination]:
    """
    Filters the catalog by a free-text query and/or category.

    Args:
        query: Case-insensitive text matched against name and location.
        category: Exact category to filter by, ignored when empty.

    Returns:
        Matching destinations.
    """
    results = list(DESTINATIONS)
    normalized_query = query.strip().lower()

    # Filter by free-text match on name or location
    if normalized_query:
        results = [
            destination for destination in results
            if normalized_query in destination.name.lower()
            or normalized_query in destination.location.lower()
        ]

    # Filter by exact category
    if category:
        results = [destination for destination in results if destination.category == category]

    return results

def recommend_destinations(
    destination_id: int,
    limit: int = 3,
) -> list[Destination]:
    """
    Returns related destinations, prioritizing the same category.

    Args:
        destination_id: ID of the destination currently being viewed.
        limit: Maximum number of recommendations to return.

    Returns:
        Recommended destinations, excluding the current destination.
    """
    destination = get_destination(destination_id)

    # Stop when the destination does not exist or no results are requested
    if destination is None or limit <= 0:
        return []

    # Put destinations from the same category first
    same_category = [
        item
        for item in DESTINATIONS
        if item.destination_id != destination_id
        and item.category == destination.category
    ]

    # Use other destinations to fill any remaining recommendation spaces
    other_destinations = [
        item
        for item in DESTINATIONS
        if item.destination_id != destination_id
        and item.category != destination.category
    ]

    return (same_category + other_destinations)[:limit]

def list_saved_destinations() -> list[Destination]:
    """
    Returns destinations currently marked as saved.
    """
    return [destination for destination in DESTINATIONS if destination.is_saved]


# Mutation operations
def toggle_saved(destination_id: int) -> Destination | None:
    """
    Flips the saved state for a destination in place.

    Returns:
        The updated destination, or None if it does not exist.
    """
    for index, destination in enumerate(DESTINATIONS):
        if destination.destination_id == destination_id:
            # Replace with a copy carrying the flipped saved state
            DESTINATIONS[index] = replace(destination, is_saved=not destination.is_saved)
            return DESTINATIONS[index]

    return None
