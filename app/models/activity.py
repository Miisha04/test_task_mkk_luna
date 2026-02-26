from sqlalchemy import (
    String,
    Integer,
    ForeignKey,
    CheckConstraint,
    Table,
    Column
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from ..database import Base
if TYPE_CHECKING:
    from organization import Organization


class Activity(Base):

    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("activities.id", ondelete="CASCADE"),
        nullable=True
    )

    parent: Mapped["Activity"] = relationship(
        remote_side=[id],
        back_populates="children"
    )

    children: Mapped[list["Activity"]] = relationship(
        back_populates="parent",
        cascade="all, delete"
    )

    organizations: Mapped["Organization"] = relationship(
        secondary="organization_activities",
        back_populates="activities"
    )

    __table_args__=(
        CheckConstraint("level BETWEEN 1 AND 3", name="check_activity_level"),
    )


organization_activities = Table(
    "organization_activities",
    Base.metadata,
    Column(
        "organization_id",
        ForeignKey("organizations.id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "activity_id",
        ForeignKey("activities.id", ondelete="CASCADE"),
        primary_key=True
    ),
)