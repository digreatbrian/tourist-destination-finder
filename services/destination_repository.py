"""
Database repository for tourist destinations and saved places.
"""

import sqlite3

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
    Provides persistence operations for destination records.
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

        with self.database.connect() as connection:
            rows = connection.execute(
                """
                SELECT id, name, location, category, description, image_url
                FROM destinations
                WHERE name LIKE ? COLLATE NOCASE
                   OR location LIKE ? COLLATE NOCASE
                   OR category LIKE ? COLLATE NOCASE
                ORDER BY name
                """,
                (search_pattern, search_pattern, search_pattern),
            ).fetchall()

        return [self._to_destination(row) for row in rows]

    def list_saved_destinations(self) -> list[Destination]:
        """
        Returns all destinations saved by the user.

        Returns:
            Saved destinations ordered from most recently saved.
        """
        with self.database.connect() as connection:
            rows = connection.execute(
                """
                SELECT d.id, d.name, d.location, d.category,
                       d.description, d.image_url
                FROM destinations AS d
                INNER JOIN saved_destinations AS s ON s.destination_id = d.id
                ORDER BY s.saved_at DESC, d.name
                """
            ).fetchall()

        return [self._to_destination(row) for row in rows]

    def save_destination(self, destination_id: int) -> None:
        """
        Saves a destination, ignoring repeated save requests.

        Args:
            destination_id: Database identifier of the destination to save.

        Raises:
            ValueError: If the destination does not exist.
        """
        with self.database.connect() as connection:
            destination_exists = connection.execute(
                "SELECT 1 FROM destinations WHERE id = ?",
                (destination_id,),
            ).fetchone()
            if destination_exists is None:
                raise ValueError(f"Destination {destination_id} does not exist.")

            connection.execute(
                """
                INSERT OR IGNORE INTO saved_destinations(destination_id)
                VALUES (?)
                """,
                (destination_id,),
            )

    def remove_saved_destination(self, destination_id: int) -> None:
        """
        Removes a destination from the saved places list.

        Args:
            destination_id: Database identifier of the destination to remove.
        """
        with self.database.connect() as connection:
            connection.execute(
                "DELETE FROM saved_destinations WHERE destination_id = ?",
                (destination_id,),
            )

    def seed_destinations(self) -> None:
        """
        Inserts the built-in destination catalog when records are absent.
        """
        with self.database.connect() as connection:
            for destination in DEFAULT_DESTINATIONS:
                connection.execute(
                    """
                    INSERT OR IGNORE INTO destinations(
                        name, location, category, description, image_url
                    )
                    VALUES (:name, :location, :category, :description, :image_url)
                    """,
                    destination,
                )

    @staticmethod
    def _to_destination(row: sqlite3.Row) -> Destination:
        """
        Converts a database row into the application model.

        Args:
            row: SQLite row containing destination columns.

        Returns:
            A destination model.
        """
        return Destination(
            destination_id=row["id"],
            name=row["name"],
            location=row["location"],
            category=row["category"],
            description=row["description"],
            image_url=row["image_url"],
        )
