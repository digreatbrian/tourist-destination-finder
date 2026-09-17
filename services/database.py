"""
SQLAlchemy engine and session setup for the application database.
"""

import os
from pathlib import Path
from typing import Any

from sqlalchemy import create_engine, event
from sqlalchemy.engine import URL, Engine
from sqlalchemy.orm import Session, sessionmaker

from models.database_models import Base


DATABASE_PATH_ENVIRONMENT_VARIABLE = "TOURIST_DESTINATION_DATABASE"
DEFAULT_DATABASE_DIRECTORY = Path.home() / ".tourist_destination_finder"
DEFAULT_DATABASE_PATH = DEFAULT_DATABASE_DIRECTORY / "destinations.db"


class Database:
    """
    Manages the SQLAlchemy engine, sessions, and database schema.
    """

    def __init__(self, database_path: str | Path | None = None) -> None:
        """
        Initializes the SQLAlchemy database configuration.

        Args:
            database_path: Optional path for the SQLite database. When omitted,
                the environment override or the default application directory
                is used.
        """
        configured_path = database_path or os.getenv(
            DATABASE_PATH_ENVIRONMENT_VARIABLE
        )
        self.database_path = Path(configured_path or DEFAULT_DATABASE_PATH).expanduser()

        # Create the parent directory before creating the engine
        self.database_path.parent.mkdir(parents=True, exist_ok=True)

        # Build the engine and session factory
        database_url = URL.create(
            drivername="sqlite",
            database=str(self.database_path),
        )
        self.engine: Engine = create_engine(database_url, future=True)

        # Enable SQLite foreign-key enforcement for every connection
        event.listen(self.engine, "connect", self._enable_foreign_keys)

        self.session_factory = sessionmaker(
            bind=self.engine,
            class_=Session,
            expire_on_commit=False,
        )

        # Create tables declared by the SQLAlchemy models
        self.initialize_schema()

    def create_session(self) -> Session:
        """
        Creates a new SQLAlchemy session.

        Returns:
            A new database session owned by the caller.
        """
        return self.session_factory()

    def initialize_schema(self) -> None:
        """
        Creates all declared database tables if they do not exist.
        """
        Base.metadata.create_all(self.engine)

    @staticmethod
    def _enable_foreign_keys(
        dbapi_connection: Any, connection_record: Any
    ) -> None:
        """
        Enables foreign-key enforcement for a SQLite connection.

        Args:
            dbapi_connection: Raw SQLite connection created by SQLAlchemy.
            connection_record: SQLAlchemy connection pool record.
        """
        cursor = dbapi_connection.cursor()
        try:
            cursor.execute("PRAGMA foreign_keys=ON")
        finally:
            cursor.close()
