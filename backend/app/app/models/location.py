from __future__ import annotations

from sqlalchemy import NUMERIC, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Country(Base):
    id = Column(String(length=2), primary_key=True)  # ISO Country code
    name = Column(String)

    def __repr__(self):
        return f"<Country (name={self.name}, id={self.id})>"
