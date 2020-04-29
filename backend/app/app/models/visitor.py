from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Visitor(Base):
    id = Column(Integer, primary_key=True, index=True)

    domain_id = Column(Integer, ForeignKey("domain.id"))
    domain = relationship("Domain", back_populates="visitors")

    events = relationship("Event", back_populates="visitor")
