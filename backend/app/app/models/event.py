from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Event(Base):
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(TIMESTAMP, primary_key=True)

    visitor_id = Column(Integer, ForeignKey("visitor.id"))
    visitor = relationship("Visitor", back_populates="events")
