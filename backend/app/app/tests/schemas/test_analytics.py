import pytest
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session

from app.models.event import Event, EventType
from app.schemas.analytics import (
    AggregatePerDayStat,
    AggregateStat,
    AnalyticsType,
    PageViewStat,
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


class AggregatePerDayStatTest:
    def test_get_pageviews(self, db: Session, mock_ip_address):
        # With one page view event
        domain = create_random_domain(db)
        create_random_page_view_event(
            db, domain_id=domain.id, ip_address=mock_ip_address
        )
        base_query = domain.events.filter(Event.event_type == EventType.page_view)
        data = PageViewStat.from_base_query(base_query)
        per_day_data = AggregatePerDayStat.from_base_query(base_query)
        assert data.total_visits == 1
        assert per_day_data[0].total_visits == 1

        # With two page view events
        create_random_page_view_event(
            db, domain_id=domain.id, ip_address=mock_ip_address
        )
        data = PageViewStat.from_base_query(base_query)
        per_day_data = AggregatePerDayStat.from_base_query(base_query)
        assert data.total_visits == 2
        assert per_day_data[0].total_visits == 2

        # With two page view events and one metric event
        create_random_metric_event(db, domain_id=domain.id, ip_address=mock_ip_address)
        data = PageViewStat.from_base_query(base_query)
        per_day_data = AggregatePerDayStat.from_base_query(base_query)
        assert data.total_visits == 2
        assert len(per_day_data) == 1
        assert per_day_data[0].total_visits == 2


class TestAggregateStat:
    def test_aggregate_stat(self, db: Session, mock_ip_address):
        domain = create_random_domain(db)
        create_random_page_view_event(
            db, domain_id=domain.id, ip_address=mock_ip_address
        )
        base_query = domain.events.filter(Event.event_type == EventType.page_view)
        data = AggregateStat.from_base_query(base_query, Event.os_family)
        assert len(data) == 1
        assert data[0].value
        assert data[0].total_visits == 1

    def test_aggregate_stat_filter_none(self, db: Session, mock_ip_address):
        domain = create_random_domain(db)
        create_random_page_view_event(
            db,
            domain_id=domain.id,
            ip_address=mock_ip_address,
            create_overrides={"referrer": "https://www.google.com/"},
        )
        create_random_page_view_event(
            db,
            domain_id=domain.id,
            ip_address=mock_ip_address,
            create_overrides={},
        )
        base_query = domain.events.filter(Event.event_type == EventType.page_view)
        data = AggregateStat.from_base_query(
            base_query, Event.referrer_name, filter_none=True
        )
        assert len(data) == 1
        assert data[0].value
        assert data[0].total_visits == 1
