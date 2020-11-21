import uuid
from app.models.event import EventType
from sqlalchemy.orm import Session

from app import crud
from app.schemas.event import EventCreate
from app.tests.utils.domain import create_random_domain


def test_create_page_view_event(db: Session, mock_ip_address) -> None:
    domain = create_random_domain(db)
    event_in = EventCreate(
        event_type=EventType.page_view,
        path="/abc",
        url="https://google.com",
        url_params={},
        page_title="Title",
        page_size_bytes=150,
        referrer="abc",
        user_timezone="Europe/Amsterdam",
        ua_string="Mozilla/5.0 (X11; Linux x86_64; rv:9000.0) Gecko/20100101 Firefox/9000.0",
        download_time=5000,
        time_to_first_byte=5000,
        total_time=5000,
        ip_address=mock_ip_address,
        page_view_id=uuid.uuid4(),
    )
    event = crud.event.create_with_domain(db=db, obj_in=event_in, domain_id=domain.id)
    assert event.domain_id == domain.id
    assert event.ua_string == event_in.ua_string
    assert event.parsed_ua
    assert event.parsed_ua.browser_family == "Firefox"
    assert event.ip_city
    assert event.ip_country
    assert event.ip_continent_code
