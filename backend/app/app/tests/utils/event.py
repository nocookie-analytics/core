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
        "ip_address": ip_address or "127.0.0.1",
        "page_view_id": uuid.uuid4(),
        **create_overrides,
    }
    event_in = EventCreate(**params)
    return crud.event.create_with_domain(db=db, obj_in=event_in, domain_id=domain_id)


def create_random_metric_event(
    db: Session,
    *,
    domain_id: int,
    ip_address: Optional[str] = None,
) -> models.Event:
    event_in = EventCreate(
        event_type=EventType.metric,
        url="https://google.com",
        page_title="Title",
        page_size_bytes=150,
        referrer="abc",
        user_timezone="Europe/Amsterdam",
        ua_string="Mozilla/5.0 (X11; Linux x86_64; rv:9000.0) Gecko/20100101 Firefox/9000.0",
        download_time=5000,
        time_to_first_byte=5000,
        total_time=5000,
        ip_address=ip_address or "127.0.0.1",
        page_view_id=uuid.uuid4(),
        metric_name=MetricType.LCP,
        metric_value=1234,
    )
    return crud.event.create_with_domain(db=db, obj_in=event_in, domain_id=domain_id)
