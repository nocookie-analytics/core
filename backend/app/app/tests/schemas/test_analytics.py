from datetime import date, datetime, timedelta
import pytest
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session

from app.models.event import Event, EventType, MetricType
from app.schemas.analytics import (
    AvgMetricPerDayStat,
    IntervalType,
    LiveVisitorStat,
    PageViewsPerDayStat,
    AggregateStat,
    AnalyticsType,
    SummaryStat,
)
from app.tests.utils.domain import create_random_domain
from app.tests.utils.event import (
    create_random_metric_event,
    create_random_page_view_event,
)


class TestPageViewStat:
    def test_pageviews(self, db: Session, mock_ip_address):
        domain = create_random_domain(db)
        base_query = domain.events.filter(Event.event_type == EventType.page_view)

        data = SummaryStat.from_base_query(db, base_query)
        assert data.total_visits == 0
        assert data.visitors == 0
        assert data.bounce_rate is None

        create_random_page_view_event(db, domain=domain, ip_address=mock_ip_address)
        create_random_page_view_event(db, domain=domain, ip_address=mock_ip_address)
        create_random_metric_event(db, domain=domain, ip_address=mock_ip_address)

        data = SummaryStat.from_base_query(db, base_query)
        assert data.total_visits == 2
        assert data.visitors == 1
        assert data.bounce_rate == 0

        create_random_page_view_event(db, domain=domain, ip_address="127.0.0.1")
        data = SummaryStat.from_base_query(db, base_query)
        assert (
            data.bounce_rate == 50
        )  # At this point in the test: 2 visitors, 1 bounced 1 didn't


class TestPageViewsPerDayStat:
    def test_get_pageviews(self, db: Session, mock_ip_address):
        # With one page view event
        domain = create_random_domain(db)
        create_random_page_view_event(db, domain=domain, ip_address=mock_ip_address)
        base_query = domain.events.filter(Event.event_type == EventType.page_view)
        end = datetime.now()
        start = end - timedelta(days=1)

        per_day_data = PageViewsPerDayStat.from_base_query(
            base_query, start=start, end=end, interval=IntervalType.DAY
        )
        assert len(per_day_data) == 2
        assert per_day_data[-1].total_visits == 1
        assert per_day_data[-1].visitors == 1

        # With two page view events
        create_random_page_view_event(db, domain=domain, ip_address=mock_ip_address)
        per_day_data = PageViewsPerDayStat.from_base_query(
            base_query, start=start, end=end, interval=IntervalType.DAY
        )
        assert len(per_day_data) == 2
        assert per_day_data[-1].total_visits == 2
        assert per_day_data[-1].visitors == 1

        # With two page view events and one metric event
        create_random_metric_event(db, domain=domain, ip_address=mock_ip_address)
        per_day_data = PageViewsPerDayStat.from_base_query(
            base_query, start=start, end=end, interval=IntervalType.DAY
        )
        assert len(per_day_data) == 2
        assert per_day_data[-1].total_visits == 2
        assert per_day_data[-1].visitors == 1

    def test_get_pageviews_per_hour(self, db: Session, mock_ip_address):
        domain = create_random_domain(db)
        create_random_page_view_event(db, domain=domain, ip_address=mock_ip_address)
        base_query = domain.events.filter(Event.event_type == EventType.page_view)
        end = datetime.now()
        start = end - timedelta(days=1)

        per_hour_data = PageViewsPerDayStat.from_base_query(
            base_query, start=start, end=end, interval=IntervalType.HOUR
        )
        assert len(per_hour_data) == 25
        assert per_hour_data[-1].total_visits == 1
        assert per_hour_data[-1].visitors == 1


class TestAggregateStat:
    def test_aggregate_stat(self, db: Session, mock_ip_address):
        domain = create_random_domain(db)
        create_random_page_view_event(db, domain=domain, ip_address=mock_ip_address)
        base_query = domain.events.filter(Event.event_type == EventType.page_view)
        data = AggregateStat.from_base_query(
            base_query, Event.os_family, group_limit=100
        )
        assert len(data) == 1
        assert data[0].value
        assert data[0].total_visits == 1

    def test_aggregate_stat_local_ip(self, db: Session, mock_ip_address):
        domain = create_random_domain(db)
        create_random_page_view_event(db, domain=domain, ip_address="10.0.0.1")
        base_query = domain.events.filter(Event.event_type == EventType.page_view)
        data = AggregateStat.from_base_query(
            base_query, Event.ip_country_iso_code, group_limit=100
        )
        assert len(data) == 1
        assert data[0].value == "Unknown"
        assert data[0].total_visits == 1

    def test_aggregate_stat_filter_none(self, db: Session, mock_ip_address):
        domain = create_random_domain(db)
        create_random_page_view_event(
            db,
            domain=domain,
            ip_address=mock_ip_address,
            create_overrides={"referrer": "https://www.google.com/"},
        )
        create_random_page_view_event(
            db,
            domain=domain,
            ip_address=mock_ip_address,
            create_overrides={},
        )
        base_query = domain.events.filter(Event.event_type == EventType.page_view)
        data = AggregateStat.from_base_query(
            base_query, Event.referrer_name, filter_none=True, group_limit=100
        )
        assert len(data) == 1
        assert data[0].value
        assert data[0].total_visits == 1


class TestAvgMetricPerDayStat:
    def test_avg(self, db, mock_ip_address):
        domain = create_random_domain(db)
        event = create_random_page_view_event(
            db,
            domain=domain,
            ip_address=mock_ip_address,
        )
        create_random_metric_event(
            db,
            domain=domain,
            create_overrides={
                "page_view_id": event.page_view_id,
                "metric_value": 5,
                "metric_name": MetricType.LCP,
            },
        )
        start = datetime.now() - timedelta(days=30)
        end = datetime.now() + timedelta(
            minutes=5
        )  # end date a little longer than now since we'll be adding events in the test
        base_query = domain.events.filter(Event.event_type == EventType.metric).filter(
            Event.timestamp.between(start, end)
        )
        lcp_per_day = AvgMetricPerDayStat.from_base_query(
            base_query, MetricType.LCP, start=start, end=end
        )
        assert len(lcp_per_day) == 31
        for lcp in lcp_per_day[:-1]:
            assert lcp.value == 0
        assert lcp_per_day[-1].value == 5

        create_random_metric_event(
            db,
            domain=domain,
            create_overrides={
                "page_view_id": event.page_view_id,
                "metric_value": 10,
                "metric_name": MetricType.LCP,
            },
        )

        lcp_per_day = AvgMetricPerDayStat.from_base_query(
            base_query, MetricType.LCP, start=start, end=end
        )
        fid_per_day = AvgMetricPerDayStat.from_base_query(
            base_query, MetricType.FID, start=start, end=end
        )
        assert len(lcp_per_day) == 31
        assert len(fid_per_day) == 31
        for lcp, fid in zip(lcp_per_day[:-1], fid_per_day[:-1]):
            assert lcp.value == 0
            assert fid.value == 0
        assert lcp_per_day[-1].value == 7.5
        assert fid_per_day[-1].value == 0


class TestLiveVisitorStat:
    def test_live_visitor_stat(self, db: Session, mock_ip_address):
        domain = create_random_domain(db)
        stat = LiveVisitorStat.from_base_query(
            db.query(Event).filter(Event.domain_id == domain.id)
        )
        assert stat == 0

        create_random_page_view_event(db, domain=domain, ip_address=mock_ip_address)

        stat = LiveVisitorStat.from_base_query(
            db.query(Event).filter(Event.domain_id == domain.id)
        )
        assert stat == 1
