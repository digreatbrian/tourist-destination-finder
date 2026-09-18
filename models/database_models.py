"""
SQLAlchemy models for destinations and saved places.
"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    """


class DestinationRecord(Base):
    """
    Stores a tourist destination in the database.
    """

    __tablename__ = "destinations"
    __table_args__ = (
        UniqueConstraint("name", "location", name="uq_destination_name_location"),
        Index("idx_destinations_category", "category"),
        Index("idx_destinations_location", "location"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    location: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(2000), default="", nullable=False)
    image_url: Mapped[str] = mapped_column(String(1000), default="", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    saved_entry: Mapped["SavedDestinationRecord | None"] = relationship(
        back_populates="destination",
        uselist=False,
        cascade="all, delete-orphan",
    )


class SavedDestinationRecord(Base):
    """
    Stores a user's saved destination reference.
    """

    __tablename__ = "saved_destinations"

    destination_id: Mapped[int] = mapped_column(
        ForeignKey("destinations.id", ondelete="CASCADE"),
        primary_key=True,
    )
    saved_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    destination: Mapped[DestinationRecord] = relationship(
        back_populates="saved_entry"
    )
