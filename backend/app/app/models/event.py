from enum import Enum

from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Index
from sqlalchemy.sql.schema import PrimaryKeyConstraint
from sqlalchemy_enum34 import EnumType

from app.db.base_class import Base


class EventType(Enum):
    page_view = "page_view"
    custom = "custom"


EventTypeEnum = EnumType(EventType, name="event_type")


class Event(Base):
    timestamp = Column(TIMESTAMP, default=func.now())
    id = Column(Integer, autoincrement=True)

    domain_id = Column(Integer, ForeignKey("domain.id", name="fk_event_domain_id"))
    domain = relationship("Domain")

    uid = Column(String)
    raw_data = Column(JSONB)

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

    ix_domain_timestamp = Index("ix_domain_timestamp", domain_id, timestamp)

    # Choosing this as a primary key so the table is partitioned by domain first, then timestamp
    # but the combination of domain and timestamp won't be unique, serial id makes it so
    __table_args__ = (PrimaryKeyConstraint(domain_id, timestamp, id), {})
