"""
SQLAlchemy repository for tourist destinations and saved places.
"""

from sqlalchemy import or_, select

from models.database_models import DestinationRecord, SavedDestinationRecord
from models.destination import Destination
from services.database import Database


DEFAULT_DESTINATIONS = (
    {
        "name": "Victoria Falls",
        "location": "Zimbabwe",
        "category": "Nature",
        "description": "One of the world's largest and most spectacular waterfalls.",
        "image_url": "",
    },
)


class DestinationRepository:
    """
    Provides SQLAlchemy persistence operations for destination records.
    """

    def __init__(self, database: Database | None = None) -> None:
        """
        Initializes the repository and ensures starter data exists.

        Args:
            database: Optional database instance, primarily useful for tests
                and alternate application data locations.
        """
        self.database = database or Database()

        # Add the initial catalog without duplicating existing records
        self.seed_destinations()

    def list_destinations(self, search_term: str = "") -> list[Destination]:
        """
        Returns destinations matching an optional name, location, or category.

        Args:
            search_term: Case-insensitive text used to filter destinations.

        Returns:
            Destinations ordered alphabetically by name.
        """
        normalized_search_term = search_term.strip()
        search_pattern = f"%{normalized_search_term}%"
        statement = select(DestinationRecord).where(
            or_(
                DestinationRecord.name.ilike(search_pattern),
                DestinationRecord.location.ilike(search_pattern),
                DestinationRecord.category.ilike(search_pattern),
            )
        ).order_by(DestinationRecord.name)

        with self.database.create_session() as session:
            records = session.scalars(statement).all()

        return [self._to_destination(record) for record in records]

    def list_saved_destinations(self) -> list[Destination]:
        """
        Returns all destinations saved by the user.

        Returns:
            Saved destinations ordered from most recently saved.
        """
        statement = (
            select(DestinationRecord)
            .join(SavedDestinationRecord)
            .order_by(SavedDestinationRecord.saved_at.desc(), DestinationRecord.name)
        )

        with self.database.create_session() as session:
            records = session.scalars(statement).all()

        return [self._to_destination(record) for record in records]

    def save_destination(self, destination_id: int) -> None:
        """
        Saves a destination, ignoring repeated save requests.

        Args:
            destination_id: Database identifier of the destination to save.

        Raises:
            ValueError: If the destination does not exist.
        """
        with self.database.create_session() as session:
            destination = session.get(DestinationRecord, destination_id)
            if destination is None:
                raise ValueError(f"Destination {destination_id} does not exist.")

            saved_destination = session.get(SavedDestinationRecord, destination_id)
            if saved_destination is None:
                session.add(SavedDestinationRecord(destination=destination))

            session.commit()

    def remove_saved_destination(self, destination_id: int) -> None:
        """
        Removes a destination from the saved places list.

        Args:
            destination_id: Database identifier of the destination to remove.
        """
        with self.database.create_session() as session:
            saved_destination = session.get(SavedDestinationRecord, destination_id)
            if saved_destination is not None:
                session.delete(saved_destination)
                session.commit()

    def seed_destinations(self) -> None:
        """
        Inserts the built-in destination catalog when records are absent.
        """
        with self.database.create_session() as session:
            for destination_data in DEFAULT_DESTINATIONS:
                existing_destination = session.scalar(
                    select(DestinationRecord).where(
                        DestinationRecord.name == destination_data["name"],
                        DestinationRecord.location == destination_data["location"],
                    )
                )
                if existing_destination is None:
                    session.add(DestinationRecord(**destination_data))

            session.commit()

    @staticmethod
    def _to_destination(record: DestinationRecord) -> Destination:
        """
        Converts a SQLAlchemy record into the application model.

        Args:
            record: SQLAlchemy destination record.

        Returns:
            A destination model.
        """
        return Destination(
            destination_id=record.id,
            name=record.name,
            location=record.location,
            category=record.category,
            description=record.description,
            image_url=record.image_url,
        )
