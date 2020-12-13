from __future__ import annotations

from sqlalchemy.sql import text

from enum import Enum
from typing import Mapping, TYPE_CHECKING, Tuple

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    NUMERIC,
    String,
    DateTime,
    Boolean,
    func,
    Index,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, INET, UUID
from sqlalchemy_enum34 import EnumType

from app.db.base_class import Base


if TYPE_CHECKING:
    from .location import City, Country
    from .domain import Domain


class EventType(Enum):
    page_view = "page_view"
    metric = "metric"
    custom = "custom"


EventTypeEnum = EnumType(EventType, name="event_type")


class Event(Base):
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    id = Column(Integer, autoincrement=True)
    page_view_id = Column(UUID, nullable=False)

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

    browser_family = Column(String, index=True)
    browser_version_major = Column(String)
    browser_version_minor = Column(String)

    os_family = Column(String, index=True)
    os_version_major = Column(String)
    os_version_minor = Column(String)

    device_family = Column(String, index=True)
    device_brand = Column(String, index=True)
    device_model = Column(String, index=True)

    is_mobile = Column(Boolean)
    is_tablet = Column(Boolean)
    is_touch_capable = Column(Boolean)
    is_pc = Column(Boolean)
    is_bot = Column(Boolean)

    url = Column(String)
    path = Column(String)

    metric_name = Column(String, index=True)
    metric_value = Column(NUMERIC)

    url_params = Column(JSONB, index=True)

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
    ix_timestamp = Index("ix_timestamp", timestamp)

    # Choosing this as a primary key so the table is partitioned by domain first,
    # then timestamp but the combination of domain and timestamp won't be unique,
    # serial id makes it so
    __table_args__: Tuple = (
        ix_domain_timestamp,
        ix_timestamp,
        PrimaryKeyConstraint(domain_id, timestamp, id),
        {},
    )
