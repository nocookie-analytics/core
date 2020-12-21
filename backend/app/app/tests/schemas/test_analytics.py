import pytest
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session

from app.models.event import Event, EventType
from app.schemas.analytics import (
    AnalyticsType,
    BrowserStat,
    CountryStat,
    OSStat,
    PageViewsPerDayStat,
    PageViewStat,
    ReferrerMediumStat,
    ReferrerNameStat,
)
from app.tests.utils.domain import create_random_domain
from app.tests.utils.event import (
    create_random_metric_event,
    create_random_page_view_event,
)


@pytest.mark.parametrize("test_input", ["a,b,c", "invalid", "", "a"])
def test_from_csv_string(test_input):
    with pytest.raises(HTTPException):
        AnalyticsType.from_csv_string(test_input)


def test_from_csv_string_valid():
    assert AnalyticsType.from_csv_string("pageviews") == [AnalyticsType.PAGEVIEWS]

    assert AnalyticsType.from_csv_string("pageviews,pageviews") == [
        AnalyticsType.PAGEVIEWS
    ]

    parsed = AnalyticsType.from_csv_string("pageviews,browser_families")
    expected = [AnalyticsType.PAGEVIEWS, AnalyticsType.BROWSERS]
    assert set(parsed) == set(expected)


def test_get_pageviews(db: Session, mock_ip_address):
    # With one page view event
    domain = create_random_domain(db)
    create_random_page_view_event(db, domain_id=domain.id, ip_address=mock_ip_address)
    base_query = domain.events.filter(Event.event_type == EventType.page_view)
    data = PageViewStat.from_base_query(base_query)
    per_day_data = PageViewsPerDayStat.from_base_query(base_query)
    assert data.total_visits == 1
    assert per_day_data[0].total_visits == 1

    # With two page view events
    create_random_page_view_event(db, domain_id=domain.id, ip_address=mock_ip_address)
    data = PageViewStat.from_base_query(base_query)
    per_day_data = PageViewsPerDayStat.from_base_query(base_query)
    assert data.total_visits == 2
    assert per_day_data[0].total_visits == 2

    # With two page view events and one metric event
    create_random_metric_event(db, domain_id=domain.id, ip_address=mock_ip_address)
    data = PageViewStat.from_base_query(base_query)
    per_day_data = PageViewsPerDayStat.from_base_query(base_query)
    assert data.total_visits == 2
    assert len(per_day_data) == 1
    assert per_day_data[0].total_visits == 2


def test_get_browsers(db: Session, mock_ip_address):
    domain = create_random_domain(db)
    create_random_page_view_event(db, domain_id=domain.id, ip_address=mock_ip_address)
    base_query = domain.events.filter(Event.event_type == EventType.page_view)
    data = BrowserStat.from_base_query(base_query)
    assert len(data) == 1
    assert data[0].name
    assert data[0].total_visits


def test_get_countries(db: Session, mock_ip_address):
    domain = create_random_domain(db)
    create_random_page_view_event(db, domain_id=domain.id, ip_address=mock_ip_address)
    base_query = domain.events.filter(Event.event_type == EventType.page_view)
    data = CountryStat.from_base_query(base_query)
    assert len(data) == 1
    assert data[0].country_code
    assert data[0].name
    assert data[0].total_visits


def test_get_os(db: Session, mock_ip_address):
    domain = create_random_domain(db)
    create_random_page_view_event(db, domain_id=domain.id, ip_address=mock_ip_address)
    base_query = domain.events.filter(Event.event_type == EventType.page_view)
    data = OSStat.from_base_query(base_query)
    assert len(data) == 1
    assert data[0].name
    assert data[0].total_visits


def test_get_referrers(db: Session, mock_ip_address):
    domain = create_random_domain(db)
    create_random_page_view_event(
        db,
        domain_id=domain.id,
        ip_address=mock_ip_address,
        create_overrides={"referrer": "https://www.google.com/"},
    )
    base_query = domain.events.filter(Event.event_type == EventType.page_view)
    name_data = ReferrerNameStat.from_base_query(base_query)
    assert len(name_data) == 1
    assert name_data[0].medium == "search"
    assert name_data[0].name == "Google"
    assert name_data[0].total_visits == 1

    medium_data = ReferrerMediumStat.from_base_query(base_query)
    assert len(medium_data) == 1
    assert medium_data[0].medium == "search"
    assert medium_data[0].total_visits == 1
