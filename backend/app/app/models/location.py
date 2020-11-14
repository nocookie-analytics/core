from __future__ import annotations

from sqlalchemy import NUMERIC, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class City(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    asciiname = Column(String)
    latitude = Column(NUMERIC)
    longitude = Column(NUMERIC)
    country_id = Column(
        String(length=2), ForeignKey("country.id", name="fk_event_country_id")
    )
    country: Country = relationship("Country")  # type: ignore

    def __repr__(self):
        return f"<City (name={self.name}, id={self.id})>"


class Country(Base):
    id = Column(String(length=2), primary_key=True)  # ISO Country code
    name = Column(String)

    def __repr__(self):
        return f"<Country (name={self.name}, id={self.id})>"
