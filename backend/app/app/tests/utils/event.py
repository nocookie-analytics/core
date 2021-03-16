from app.utils.geolocation import get_ip_gelocation
import uuid
from typing import Dict, Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.models.event import EventType, MetricType
from app.schemas.event import EventCreate


def create_random_page_view_event(
    db: Session,
    *,
    domain_id: int,
    ip_address: Optional[str] = None,
    create_overrides: Dict = None,
) -> models.Event:
    if not create_overrides:
        create_overrides = {}
    geolocation = get_ip_gelocation(ip_address)
    params = {
        "event_type": EventType.page_view,
        "url": "https://google.com",
        "page_title": "Title",
        "page_size_bytes": 150,
        "referrer": "abc",
        "user_timezone": "Europe/Amsterdam",
        "ua_string": "Mozilla/5.0 (X11; Linux x86_64; rv:9000.0) Gecko/20100101 Firefox/9000.0",
        "download_time": 5000,
        "time_to_first_byte": 5000,
        "total_time": 5000,
        "page_view_id": uuid.uuid4(),
        "ip_city_id": geolocation.city.geoname_id if geolocation else None,
        "ip_country_iso_code": geolocation.country.iso_code if geolocation else None,
        "ip_continent_code": geolocation.continent.code if geolocation else None,
        **create_overrides,
    }
    event_in = EventCreate(**params)
    return crud.event.create_with_domain(db=db, obj_in=event_in, domain_id=domain_id)


def create_random_metric_event(
    db: Session,
    *,
    domain_id: int,
    ip_address: Optional[str] = None,
    create_overrides: Dict = None,
) -> models.Event:
    geolocation = get_ip_gelocation(ip_address)
    event_in_data = {
        "event_type": EventType.metric,
        "url": "https://google.com",
        "page_title": "Title",
        "page_size_bytes": 150,
        "referrer": "abc",
        "user_timezone": "Europe/Amsterdam",
        "ua_string": "Mozilla/5.0 (X11; Linux x86_64; rv:9000.0) Gecko/20100101 Firefox/9000.0",
        "download_time": 5000,
        "time_to_first_byte": 5000,
        "total_time": 5000,
        "page_view_id": uuid.uuid4(),
        "metric_name": MetricType.LCP,
        "metric_value": 1234,
        "ip_city_id": geolocation.city.geoname_id if geolocation else None,
        "ip_country_iso_code": geolocation.country.iso_code if geolocation else None,
        "ip_continent_code": geolocation.continent.code if geolocation else None,
        **create_overrides,
    }
    event_in = EventCreate(**event_in_data)
    return crud.event.create_with_domain(db=db, obj_in=event_in, domain_id=domain_id)
