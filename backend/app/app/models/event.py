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
from sqlalchemy.dialects.postgresql.base import INTERVAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import and_, text
from sqlalchemy.sql.sqltypes import Enum as SQLAlchemyEnum, Interval

from app.db.base_class import Base

if TYPE_CHECKING:
    from .domain import Domain
    from .location import Country


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


class DeviceType(Enum):
    MOBILE = "mobile"
    DESKTOP = "desktop"
    TABLET = "tablet"


EventTypeEnum = ENUM(
    EventType, name="event_type", values_callable=lambda x: [e.value for e in x]
)
ReferrerMediumTypeEnum = ENUM(
    ReferrerMediumType,
    name="referrer_medium_type",
    values_callable=lambda x: [e.value for e in x],
)
MetricTypeEnum = SQLAlchemyEnum(MetricType, native_enum=False, length=50)
DeviceTypeEnum = SQLAlchemyEnum(
    DeviceType,
    native_enum=False,
    values_callable=lambda x: [e.value for e in x],
    length=50,
)


class Event(Base):
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    id = Column(Integer, autoincrement=True)
    page_view_id = Column(UUID, nullable=False)

    domain_id = Column(Integer, ForeignKey("domain.id", name="fk_event_domain_id"))
    domain: Domain = relationship("Domain")  # type: ignore
    visitor_fingerprint = Column(String)

    event_type = Column(EventTypeEnum, nullable=False)

    ip_country_iso_code = Column(
        String(length=2), ForeignKey("country.id", name="fk_event_country_id")
    )
    ip_country: Country = relationship("Country")  # type: ignore
    ip_continent_code = Column(String(length=2))

    seconds_since_last_visit = Column(INTERVAL)
    session_start = Column(DateTime(timezone=True))

    width = Column(Integer)
    height = Column(Integer)

    metric_name = Column(MetricTypeEnum)
    metric_value = Column(NUMERIC)

    event_name = Column(String)
    event_value = Column(NUMERIC)

    browser_family = Column(String)
    browser_version_major = Column(String)
    os_family = Column(String)
    device_brand = Column(String)
    device_type = Column(DeviceTypeEnum, nullable=True)

    is_bot = Column(Boolean)

    path = Column(String)
    url_params = Column(JSONB)
    referrer_medium = Column(ReferrerMediumTypeEnum)
    referrer_name = Column(String)

    utm_source = Column(String)
    utm_medium = Column(String)
    utm_campaign = Column(String)
    utm_term = Column(String)
    utm_content = Column(String)

    user_timezone = Column(String)

    ix_domain_timestamp = Index("ix_domain_timestamp", domain_id, timestamp)
    ix_timestamp = Index("ix_timestamp", timestamp)
    ix_browser_family = Index("ix_browser_family", domain_id, browser_family, timestamp)
    ix_location = Index("ix_location", domain_id, ip_country_iso_code, timestamp)
    ix_os_family = Index(
        "ix_os_family",
        domain_id,
        os_family,
        timestamp,
    )
    ix_device_brand = Index("ix_device_brand", domain_id, device_brand, timestamp)
    ix_custom_metric = Index("ix_custom_metric", domain_id, metric_name, timestamp)
    ix_referrer = Index(
        "ix_referrer", domain_id, referrer_medium, referrer_name, timestamp
    )
    ix_path = Index("id_path", domain_id, path, timestamp)

    ix_bot = Index("ix_bot", domain_id, is_bot, timestamp)
    ix_device_type = Index(
        "ix_device_type",
        domain_id,
        device_type,
        timestamp,
        postgresql_where=device_type.isnot(None),
    )

    ix_session_start = Index("ix_session_start", domain_id, session_start, timestamp)
    ix_seconds_since_last_visit = Index(
        "ix_seconds_since_last_visit",
        domain_id,
        seconds_since_last_visit,
        timestamp,
        postgresql_where=seconds_since_last_visit > text("interval '0'"),
    )

    __table_args__: Tuple = (
        Index(
            "ix_visitor_fingerprint",
            domain_id,
            visitor_fingerprint,
            timestamp,
            postgresql_where=visitor_fingerprint.isnot(None),
        ),
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
        Index(
            "ix_width_height",
            domain_id,
            width,
            height,
            timestamp,
            postgresql_where=and_(width.isnot(None), height.isnot(None)),
        ),
        Index(
            "ix_event_name",
            domain_id,
            event_name,
            timestamp,
            postgresql_where=event_name.isnot(None),
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
