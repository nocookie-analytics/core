from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Tuple

from sqlalchemy import (
    NUMERIC,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    PrimaryKeyConstraint,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID, ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Enum as SQLAlchemyEnum

from app.db.base_class import Base

if TYPE_CHECKING:
    from .domain import Domain
    from .location import City, Country


class EventType(Enum):
    page_view = "page_view"
    metric = "metric"
    custom = "custom"


class ReferrerMediumType(Enum):
    UNKNOWN = "unknown"
    INTERNAL = "internal"
    EMAIL = "email"
    SOCIAL = "social"
    SEARCH = "search"


class MetricType(Enum):
    LCP = "lcp"
    FID = "fid"
    FP = "fp"
    CLS = "cls"
    LCP_FINAL = "lcpFinal"


EventTypeEnum = ENUM(
    EventType, name="event_type", values_callable=lambda x: [e.value for e in x]
)
ReferrerMediumTypeEnum = ENUM(
    ReferrerMediumType,
    name="referrer_medium_type",
    values_callable=lambda x: [e.value for e in x],
)
MetricTypeEnum = SQLAlchemyEnum(MetricType, native_enum=False)


class Event(Base):
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    id = Column(Integer, autoincrement=True)
    page_view_id = Column(UUID, nullable=False)

    domain_id = Column(Integer, ForeignKey("domain.id", name="fk_event_domain_id"))
    domain: Domain = relationship("Domain")  # type: ignore

    event_type = Column(EventTypeEnum, nullable=False)

    ip_city_id = Column(Integer, ForeignKey("city.id", name="fk_event_city_id"))
    ip_city: City = relationship("City")  # type: ignore
    ip_country_iso_code = Column(
        String(length=2), ForeignKey("country.id", name="fk_event_country_id")
    )
    ip_country: Country = relationship("Country")  # type: ignore
    ip_continent_code = Column(String(length=2))
    ip_timezone = Column(String)

    ua_string = Column(String)

    browser_family = Column(String)
    browser_version_major = Column(String)
    browser_version_minor = Column(String)

    os_family = Column(String)
    os_version_major = Column(String)
    os_version_minor = Column(String)

    device_family = Column(String)
    device_brand = Column(String)
    device_model = Column(String)

    is_mobile = Column(Boolean)
    is_tablet = Column(Boolean)
    is_touch_capable = Column(Boolean)
    is_pc = Column(Boolean)
    is_bot = Column(Boolean)

    url = Column(String)
    path = Column(String)

    metric_name = Column(MetricTypeEnum)
    metric_value = Column(NUMERIC)

    url_params = Column(JSONB)

    utm_source = Column(String)
    utm_medium = Column(String)
    utm_campaign = Column(String)
    utm_term = Column(String)
    utm_content = Column(String)

    page_title = Column(String)

    page_size_bytes = Column(Integer)
    referrer = Column(String)
    referrer_medium = Column(ReferrerMediumTypeEnum)
    referrer_name = Column(String)
    user_timezone = Column(String)
    user_timezone_offset = Column(Integer)

    # All time values in microseconds
    download_time = Column(NUMERIC)
    time_to_first_byte = Column(NUMERIC)
    total_time = Column(NUMERIC)

    ix_domain_timestamp = Index("ix_domain_timestamp", domain_id, timestamp)
    ix_timestamp = Index("ix_timestamp", timestamp)
    ix_browser_family = Index("ix_browser_family", domain_id, browser_family, timestamp)
    ix_location = Index(
        "ix_location", domain_id, ip_country_iso_code, ip_city_id, timestamp
    )
    ix_os_family = Index(
        "ix_os_family",
        domain_id,
        os_family,
        os_version_major,
        os_version_minor,
        timestamp,
    )
    ix_device_family = Index("ix_device_family", domain_id, device_family, timestamp)
    ix_device_brand = Index("ix_device_brand", domain_id, device_brand, timestamp)
    ix_device_model = Index("ix_device_model", domain_id, device_model, timestamp)
    ix_custom_metric = Index("ix_custom_metric", domain_id, metric_name, timestamp)
    ix_referrer = Index(
        "ix_referrer", domain_id, referrer_medium, referrer_name, timestamp
    )
    ix_path = Index("id_path", domain_id, path, timestamp)

    __table_args__: Tuple = (
        ix_domain_timestamp,
        Index(
            "ix_utm_source",
            domain_id,
            utm_source,
            timestamp,
            postgresql_where=utm_source.isnot(None),
        ),
        Index(
            "ix_utm_medium",
            domain_id,
            utm_medium,
            timestamp,
            postgresql_where=utm_medium.isnot(None),
        ),
        Index(
            "ix_utm_campaign",
            domain_id,
            utm_campaign,
            timestamp,
            postgresql_where=utm_campaign.isnot(None),
        ),
        Index(
            "ix_utm_term",
            domain_id,
            utm_term,
            timestamp,
            postgresql_where=utm_term.isnot(None),
        ),
        Index(
            "ix_utm_content",
            domain_id,
            utm_content,
            timestamp,
            postgresql_where=utm_content.isnot(None),
        ),
        ix_timestamp,
        # Choosing this as a primary key so the table is partitioned by domain first,
        # then timestamp but the combination of domain and timestamp won't be unique,
        # serial id makes it so
        PrimaryKeyConstraint(domain_id, timestamp, id),
        {},
    )

    def __repr__(self):
        return f"Event<<Domain: {self.domain.domain_name}>: {self.event_type}>"
