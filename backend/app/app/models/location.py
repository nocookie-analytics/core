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
    country_id = ForeignKey("country.id")
    country: Country = relationship("Country")  # type: ignore


class Country(Base):
    id = Column(String(length=2))  # ISO Country code
    name = Column(String)
