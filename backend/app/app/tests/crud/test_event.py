import pytest
from app.models.event import EventType
from sqlalchemy.orm import Session

from app import crud
from app.schemas.event import EventCreate
from app.tests.utils.domain import create_random_domain


def test_create_event(db: Session) -> None:
    domain = create_random_domain(db)
    event_in = EventCreate(
        uid="abc",
        event_type=EventType.page_view,
        path="/abc",
        url_params={},
        page_title="Title",
        status_code=404,
        load_time_ms=111,
        page_size_bytes=150,
        referrer="abc",
        user_timezone="Europe/Amsterdam",
        ua_string="firefox",
    )
    print(EventType.page_view)
    print(event_in.event_type)

    event = crud.event.create_with_domain(db=db, obj_in=event_in, domain_id=domain.id)
    assert event.domain_id == domain.id
    assert event.ua_string == obj_in.ua_string
