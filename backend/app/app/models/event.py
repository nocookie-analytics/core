from __future__ import annotations
from app.models.parsed_ua import ParsedUA
from enum import Enum
from typing import Mapping, Optional, TYPE_CHECKING, Tuple

from sqlalchemy import Column, ForeignKey, Integer, NUMERIC, String, DateTime
from sqlalchemy.sql.functions import func
from sqlalchemy.dialects.postgresql import JSONB, INET
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Index, PrimaryKeyConstraint
from sqlalchemy_enum34 import EnumType

from app.db.base_class import Base


if TYPE_CHECKING:
    from .location import City, Country
    from .domain import Domain


class EventType(Enum):
    page_view = "page_view"
    custom = "custom"


EventTypeEnum = EnumType(EventType, name="event_type")


class Event(Base):
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    id = Column(Integer, autoincrement=True)

    domain_id = Column(Integer, ForeignKey("domain.id", name="fk_event_domain_id"))
    domain: Domain = relationship("Domain")  # type: ignore

    event_type = Column(EventTypeEnum, nullable=False)

    ip_address = Column(INET)

    ip_city_id = Column(Integer, ForeignKey("city.id", name="fk_event_city_id"))
    ip_city: City = relationship("City")  # type: ignore
    ip_country_iso_code = Column(
        String(length=2), ForeignKey("country.id", name="fk_event_country_id")
    )
    ip_country: Country = relationship("Country")  # type: ignore
    ip_continent_code = Column(String(length=2))
    ip_timezone = Column(String)

    ua_string = Column(String)
    # Note: JSONB doesn't track changes, use sqlalchemy-json lib if needed
    _parsed_ua: Mapping = Column("parsed_ua", JSONB)  # type: ignore

    @property
    def parsed_ua(self) -> Optional[ParsedUA]:
        if self._parsed_ua:
            return ParsedUA(**self._parsed_ua)
        return None

    @parsed_ua.setter
    def parsed_ua(self, parsed_ua):
        if isinstance(parsed_ua, Mapping):
            self._parsed_ua = parsed_ua

    url = Column(String)
    path = Column(String)
    url_params = Column(JSONB)

    page_title = Column(String)

    page_size_bytes = Column(Integer)
    referrer = Column(String)
    user_timezone = Column(String)
    user_timezone_offset = Column(Integer)

    # All time values in microseconds
    download_time = Column(NUMERIC)
    time_to_first_byte = Column(NUMERIC)
    total_time = Column(NUMERIC)

    ix_domain_timestamp = Index("ix_domain_timestamp", domain_id, timestamp)

    # Choosing this as a primary key so the table is partitioned by domain first,
    # then timestamp but the combination of domain and timestamp won't be unique,
    # serial id makes it so
    __table_args__: Tuple = (PrimaryKeyConstraint(domain_id, timestamp, id), {})
