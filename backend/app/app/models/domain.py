from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Domain(Base):
    id = Column(Integer, primary_key=True, index=True)
    domain_name = Column(String, index=True)

    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="domains")

    visitors = relationship("Visitor", back_populates='domain')
