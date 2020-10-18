from __future__ import annotations
from app.models.parsed_ua import ParsedUA
from enum import Enum
from typing import TYPE_CHECKING, Tuple
from pydantic.main import BaseModel

from sqlalchemy import Column, ForeignKey, Integer, NUMERIC, String, DateTime
from sqlalchemy.sql.functions import func
from sqlalchemy.dialects.postgresql import JSONB, INET
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Index, PrimaryKeyConstraint
from sqlalchemy_enum34 import EnumType

from app.db.base_class import Base

if TYPE_CHECKING:
    from .domain import Domain


class EventType(Enum):
    page_view = "page_view"
    custom = "custom"


EventTypeEnum = EnumType(EventType, name="event_type")


class Event(Base):
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    id = Column(Integer, autoincrement=True)

    domain_id = Column(Integer, ForeignKey("domain.id", name="fk_event_domain_id"))
    domain: Domain = relationship("Domain")

    event_type = Column(EventTypeEnum, nullable=False)

    ip_address = Column(INET)

    raw_ua_string = Column(String)
    # Note: JSONB doesn't track changes, use sqlalchemy-json lib if needed
    _parsed_ua = Column("parsed_ua", JSONB)

    @property
    def parsed_ua(self):
        return ParsedUA(**self._parsed_ua)

    @parsed_ua.setter
    def parsed_ua(self, parsed_ua):
        self._parsed_ua = parsed_ua.dict()

    url = Column(String)
    path = Column(String)
    url_params = Column(JSONB)

    page_title = Column(String)

    page_size_bytes = Column(Integer)
    referrer = Column(String)
    user_timezone = Column(String)

    # All time values in microseconds
    download_time = Column(NUMERIC)
    time_to_first_byte = Column(NUMERIC)
    total_time = Column(NUMERIC)

    ix_domain_timestamp = Index("ix_domain_timestamp", domain_id, timestamp)

    # Choosing this as a primary key so the table is partitioned by domain first, then timestamp
    # but the combination of domain and timestamp won't be unique, serial id makes it so
    __table_args__: Tuple = (PrimaryKeyConstraint(domain_id, timestamp, id), {})
