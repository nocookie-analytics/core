from app.tests.utils.event import (
    create_random_metric_event,
    create_random_page_view_event,
)
from app.models.domain import Domain
from datetime import datetime, timedelta
from app.schemas.analytics import AnalyticsType
import uuid
import arrow

from app.models.event import EventType
from sqlalchemy.orm import Session

from app import crud
from app.schemas.event import EventCreate
from app.tests.utils.domain import create_random_domain
from hypothesis import given
from hypothesis.extra.pytz import timezones
from hypothesis.strategies import datetimes, timedeltas

aware_datetimes = datetimes(timezones=timezones())


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
    assert event.browser_family == "Firefox"
    assert event.ip_city
    assert event.ip_country
    assert event.ip_continent_code


@given(
    aware_datetimes,
    timedeltas(min_value=timedelta(hours=1), max_value=timedelta(days=180)),
)
def test_get_analytics(
    db: Session,
    mock_read_only_domain: Domain,
    start: datetime,
    duration: timedelta,
) -> None:
    start = arrow.get(start)
    end = start + duration
    fields = [AnalyticsType.PAGEVIEWS, AnalyticsType.BROWSERS]
    analytics_data = crud.event.get_analytics_from_fields(
        db=db,
        domain=mock_read_only_domain,
        start=start,
        fields=fields,
        end=end,
    )
    assert analytics_data.start == start
    assert analytics_data.end == end
    assert analytics_data.data
    data = analytics_data.data
    assert len(data) == len(fields)
    for field_data in data:
        assert field_data.type


def test_get_pageviews(db: Session, mock_ip_address):
    # With one page view event
    domain = create_random_domain(db)
    create_random_page_view_event(db, domain_id=domain.id, ip_address=mock_ip_address)
    data = crud.event._get_page_views(
        db, domain, arrow.now() - timedelta(days=1), arrow.now()
    )
    assert data.pageviews == 1

    # With two page view events
    create_random_page_view_event(db, domain_id=domain.id, ip_address=mock_ip_address)
    data = crud.event._get_page_views(
        db, domain, arrow.now() - timedelta(days=1), arrow.now()
    )
    assert data.pageviews == 2

    # With two page view events and one metric event
    create_random_metric_event(db, domain_id=domain.id, ip_address=mock_ip_address)
    data = crud.event._get_page_views(
        db, domain, arrow.now() - timedelta(days=1), arrow.now()
    )
    assert data.pageviews == 2


def test_get_browsers(db: Session, mock_ip_address):
    domain = create_random_domain(db)
    create_random_page_view_event(db, domain_id=domain.id, ip_address=mock_ip_address)
    data = crud.event._get_browsers_data(
        db, domain, arrow.now() - timedelta(days=1), arrow.now()
    )
    assert len(data.browsers) == 1
    assert data.browsers[0].name
    assert data.browsers[0].total_visits
