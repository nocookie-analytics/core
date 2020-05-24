from enum import Enum
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy_enum34 import EnumType
from sqlalchemy.dialects.postgresql import JSONB, ENUM

from app.db.base_class import Base


class EventType(Enum):
    page_view = 'page_view'
    custom = 'custom'


EventTypeEnum = EnumType(EventType)


class Event(Base):
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(TIMESTAMP, primary_key=True)

    visitor_id = Column(Integer, ForeignKey("visitor.id"))
    visitor = relationship("Visitor", back_populates="events")

    event_type = Column(EventTypeEnum, nullable=False)

    ua_string = Column(String)
    path = Column(String)
    url_params = Column(JSONB)

    page_title = Column(String)
    status_code = Column(Integer)
    load_time_ms = Column(Integer)
    page_size_bytes = Column(Integer)
    referrer = Column(String)
    user_timezone = Column(String)
