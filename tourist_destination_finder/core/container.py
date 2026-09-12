from tourist_destination_finder.services.destination_repository import DestinationRepository
from tourist_destination_finder.services.destination_service import DestinationService


class AppContainer:
    """Simple dependency container."""

    def __init__(self):
        self.destination_repository = DestinationRepository()
        self.destination_service = DestinationService(self.destination_repository)
