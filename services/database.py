"""
SQLite database setup and connection management for the application.
"""

import os
import sqlite3
from pathlib import Path


DATABASE_PATH_ENVIRONMENT_VARIABLE = "TOURIST_DESTINATION_DATABASE"
DEFAULT_DATABASE_DIRECTORY = Path.home() / ".tourist_destination_finder"
DEFAULT_DATABASE_PATH = DEFAULT_DATABASE_DIRECTORY / "destinations.db"


class Database:
    """
    Manages the local SQLite database used by the application.
    """

    def __init__(self, database_path: str | Path | None = None) -> None:
        """
        Initializes the database configuration.

        Args:
            database_path: Optional path for the SQLite database. When omitted,
                the environment override or the default application directory
                is used.
        """
        configured_path = database_path or os.getenv(
            DATABASE_PATH_ENVIRONMENT_VARIABLE
        )
        self.database_path = Path(configured_path or DEFAULT_DATABASE_PATH).expanduser()

        # Create the parent directory before opening the database
        self.database_path.parent.mkdir(parents=True, exist_ok=True)

        # Create tables and indexes required by the repository
        self.initialize_schema()

    def connect(self) -> sqlite3.Connection:
        """
        Opens a configured SQLite connection.

        Returns:
            A SQLite connection configured to return rows by column name.
        """
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def initialize_schema(self) -> None:
        """
        Creates the destination and saved-destination tables if needed.
        """
        with self.connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS destinations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    location TEXT NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT NOT NULL DEFAULT '',
                    image_url TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(name, location)
                );

                CREATE TABLE IF NOT EXISTS saved_destinations (
                    destination_id INTEGER PRIMARY KEY,
                    saved_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (destination_id) REFERENCES destinations(id)
                        ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_destinations_category
                    ON destinations(category);

                CREATE INDEX IF NOT EXISTS idx_destinations_location
                    ON destinations(location);
                """
            )
