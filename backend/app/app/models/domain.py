from __future__ import annotations
from typing import TYPE_CHECKING, List

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.sqltypes import DateTime

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .event import Event


class Domain(Base):
    id = Column(Integer, primary_key=True, index=True)

    domain_name = Column(String, index=True, unique=True)
    events: List[Event] = relationship("Event", lazy="dynamic")

    owner_id = Column(Integer, ForeignKey("user.id"))
    owner: User = relationship("User", back_populates="domains")

    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
