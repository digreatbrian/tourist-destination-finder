"""
Business services for destination discovery and saved places.
"""

from models.destination import Destination
from services.destination_repository import DestinationRepository


class DestinationService:
    """
    Business logic boundary for destination filtering/recommendations.
    """

    def __init__(self, repository: DestinationRepository) -> None:
        """
        Initializes the destination service.

        Args:
            repository: Repository used to persist and retrieve destinations.
        """
        self.repository = repository

    def get_destinations(self, search_term: str = "") -> list[Destination]:
        """
        Returns destinations matching the optional search term.

        Args:
            search_term: Text used to filter destination results.

        Returns:
            Matching destination records.
        """
        return self.repository.list_destinations(search_term)

    def get_saved_destinations(self) -> list[Destination]:
        """
        Returns destinations saved by the user.

        Returns:
            Saved destination records.
        """
        return self.repository.list_saved_destinations()

    def save_destination(self, destination_id: int) -> None:
        """
        Saves a destination for later viewing.

        Args:
            destination_id: Database identifier of the destination to save.
        """
        self.repository.save_destination(destination_id)

    def remove_saved_destination(self, destination_id: int) -> None:
        """
        Removes a destination from the saved places list.

        Args:
            destination_id: Database identifier of the destination to remove.
        """
        self.repository.remove_saved_destination(destination_id)
