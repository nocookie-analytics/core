from app.tests.utils.utils import paths
from datetime import datetime, timedelta

import arrow
from hypothesis import given
from hypothesis.extra.pytz import timezones
from hypothesis.strategies import datetimes, timedeltas, uuids
from sqlalchemy.orm import Session

from app import crud
from app.models.domain import Domain
from app.models.event import EventType
from app.schemas.analytics import AnalyticsType
from app.schemas.event import EventCreate
from app.tests.utils.domain import create_random_domain
from app.tests.utils.event import (
    create_random_metric_event,
    create_random_page_view_event,
)

aware_datetimes = datetimes(timezones=timezones())


@given(uuids(version=4), paths())
def test_create_page_view_event(
    db: Session,
    mock_read_only_domain: Domain,
    mock_ip_address: str,
    page_view_id: str,
    path: str,
) -> None:
    domain = mock_read_only_domain
    url = f"http://{domain.domain_name}/{path}"
    event_in = EventCreate(
        event_type=EventType.page_view,
        path=str(path),
        url=url,
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
        page_view_id=str(page_view_id),
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
    base_query = crud.event._page_views_in_date_range(
        domain,
        start=arrow.now() - timedelta(days=1),
        end=arrow.now() + timedelta(days=1),
    )
    data = crud.event._get_page_views(base_query)
    assert data.pageviews == 1

    # With two page view events
    create_random_page_view_event(db, domain_id=domain.id, ip_address=mock_ip_address)
    data = crud.event._get_page_views(base_query)
    assert data.pageviews == 2

    # With two page view events and one metric event
    create_random_metric_event(db, domain_id=domain.id, ip_address=mock_ip_address)
    data = crud.event._get_page_views(base_query)
    assert data.pageviews == 2


def test_get_browsers(db: Session, mock_ip_address):
    domain = create_random_domain(db)
    create_random_page_view_event(db, domain_id=domain.id, ip_address=mock_ip_address)
    base_query = crud.event._page_views_in_date_range(
        domain,
        start=arrow.now() - timedelta(days=1),
        end=arrow.now() + timedelta(days=1),
    )
    data = crud.event._get_browsers_data(base_query)
    assert len(data.browser_families) == 1
    assert data.browser_families[0].name
    assert data.browser_families[0].total_visits


def test_get_countries(db: Session, mock_ip_address):
    domain = create_random_domain(db)
    create_random_page_view_event(db, domain_id=domain.id, ip_address=mock_ip_address)
    base_query = crud.event._page_views_in_date_range(
        domain,
        start=arrow.now() - timedelta(days=1),
        end=arrow.now() + timedelta(days=1),
    )
    data = crud.event._get_countries_data(base_query)
    assert len(data.countries) == 1
    assert data.countries[0].name
    assert len(data.countries[0].country_code) == 2
    assert data.countries[0].total_visits


def test_get_os(db: Session, mock_ip_address):
    domain = create_random_domain(db)
    create_random_page_view_event(db, domain_id=domain.id, ip_address=mock_ip_address)
    base_query = crud.event._page_views_in_date_range(
        domain,
        start=arrow.now() - timedelta(days=1),
        end=arrow.now() + timedelta(days=1),
    )
    data = crud.event._get_os_data(base_query)
    assert len(data.os_families) == 1
    assert data.os_families[0].name
    assert data.os_families[0].total_visits == 1
