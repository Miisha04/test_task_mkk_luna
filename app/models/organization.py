from sqlalchemy import (
    String,
    Integer,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from ..database import Base
if TYPE_CHECKING:
    from .activity import Activity
    from .building import Building
    from .phone import Phone
    

class Organization(Base):

    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    building_id: Mapped[int] = mapped_column(
        ForeignKey("buildings.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    building: Mapped["Building"] = relationship(back_populates="organizations")
    phones: Mapped[list["Phone"]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan"
    )
    activities: Mapped[list["Activity"]] = relationship(
        secondary="organization_activities",
        back_populates="organizations"
    )
