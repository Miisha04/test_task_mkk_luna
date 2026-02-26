from sqlalchemy import (
    String,
    Integer,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from geoalchemy2 import Geography
from geoalchemy2.types import Geography as GeographyType
from typing import TYPE_CHECKING

from ..database import Base
if TYPE_CHECKING:
    from organization import Organization


class Building(Base):

    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    address: Mapped[str] = mapped_column(String, nullable=False)
    coords: Mapped[GeographyType] = mapped_column(
        Geography(geometry_type="POINT", srid=4326),
        nullable=False
    )

    organizations: Mapped[list["Organization"]] = relationship(
        back_populates="building",
        cascade="all, delete"
    )