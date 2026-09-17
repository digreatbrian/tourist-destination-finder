"""
Destination data model used by services and screens.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Destination:
    """
    Represents a tourist destination returned by the data layer.
    """

    name: str
    location: str
    category: str
    destination_id: int | None = None
    description: str = ""
    image_url: str = ""
