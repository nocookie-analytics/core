from app.models.event import EventType
from sqlalchemy.orm import Session

from app import crud
from app.schemas.event import EventCreate
from app.tests.utils.domain import create_random_domain


def test_create_event(db: Session) -> None:
    domain = create_random_domain(db)
    event_in = EventCreate(
        event_type=EventType.page_view,
        path="/abc",
        url_params={},
        page_title="Title",
        status_code=404,
        page_size_bytes=150,
        referrer="abc",
        user_timezone="Europe/Amsterdam",
        ua_string="Mozilla/5.0 (X11; Linux x86_64; rv:9000.0) Gecko/20100101 Firefox/9000.0",
        dnslookup_time=5000,
        download_time=5000,
        fetch_time=5000,
        time_to_first_byte=5000,
        total_time=5000,
    )
    event = crud.event.create_with_domain(db=db, obj_in=event_in, domain_id=domain.id)
    assert event.domain_id == domain.id
    assert event.ua_string == event_in.ua_string
    assert event.parsed_ua.browser_family == "Firefox"
