from models.destination import Destination


class DestinationRepository:
    """Data access boundary (replace with DB implementation later)."""

    def list_destinations(self):
        return [
            Destination(name="Victoria Falls", location="Zimbabwe", category="Nature"),
        ]
