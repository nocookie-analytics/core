from datetime import datetime, timedelta
from typing import Sequence

import arrow
from hypothesis import given
from hypothesis.extra.pytz import timezones
from hypothesis.strategies import datetimes, timedeltas, uuids
import pytest
from sqlalchemy.orm import Session

from app import crud
from app.models.domain import Domain
from app.models.event import EventType, ReferrerMediumType
from app.schemas.analytics import AnalyticsType
from app.schemas.event import EventCreate
from app.tests.utils.event import create_random_page_view_event
from app.tests.utils.utils import paths

aware_datetimes = datetimes(
    timezones=timezones(), max_value=datetime(2099, 1, 1), allow_imaginary=False
)


class TestCreatePageViewEvent:
    @given(uuids(version=4), paths())
    def test_create_page_view_event(
        self,
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
            url=url,
            page_title="Title",
            page_size_bytes=150,
            referrer="abc",
            user_timezone="Europe/Amsterdam",
            ua_string="Mozilla/5.0 (X11; Linux x86_64; rv:9000.0) Gecko/20100101 Firefox/9000.0",
            download_time=5000,
            time_to_first_byte=5000,
            total_time=5000,
            page_view_id=str(page_view_id),
            ip_city_id=5,
            ip_country_iso_code="US",
            ip_continent_code="NA",
        )
        event = crud.event.create_with_domain(
            db=db, obj_in=event_in, domain_id=domain.id
        )
        assert event.domain_id == domain.id
        assert event.ua_string == event_in.ua_string
        assert event.browser_family == "Firefox"
        assert event.ip_city
        assert event.ip_country
        assert event.ip_continent_code

    def test_create_page_view_event_referrer(
        self,
        db: Session,
        mock_read_only_domain: Domain,
        mock_ip_address: str,
    ) -> None:
        domain = mock_read_only_domain
        event = create_random_page_view_event(
            db,
            domain_id=domain.id,
            ip_address=mock_ip_address,
            create_overrides={"referrer": "https://www.google.com/"},
        )
        assert event.referrer_medium == ReferrerMediumType.SEARCH
        assert event.referrer_name == "Google"

    def test_create_url_components(
        self,
        db: Session,
        mock_read_only_domain: Domain,
        mock_ip_address: str,
    ) -> None:
        domain = mock_read_only_domain
        event = create_random_page_view_event(
            db,
            domain_id=domain.id,
            ip_address=mock_ip_address,
            create_overrides={
                "url": "https://www.example.com/page?utm_content=buffercf3b2&utm_medium=social&utm_source=facebook.com&utm_campaign=buffer"
            },
        )
        assert event.utm_content == "buffercf3b2"
        assert event.utm_medium == "social"
        assert event.utm_campaign == "buffer"
        assert event.utm_source == "facebook.com"


class TestGetAnalytics:
    @given(
        aware_datetimes,
        timedeltas(min_value=timedelta(hours=1), max_value=timedelta(days=180)),
    )
    def test_get_analytics(
        self,
        db: Session,
        read_write_domain: Domain,
        start: datetime,
        duration: timedelta,
    ) -> None:
        start = arrow.get(start)
        end = start + duration
        fields = [AnalyticsType.PAGEVIEWS, AnalyticsType.BROWSERS]
        analytics_data = crud.event.get_analytics_from_fields(
            db=db,
            domain=read_write_domain,
            start=start,
            fields=fields,
            end=end,
        )
        assert analytics_data.start == start
        assert analytics_data.end == end
        assert len(
            set(analytics_data.dict(exclude_unset=True).keys()) - set(["start", "end"])
        ) == len(fields)
        assert analytics_data.pageviews
        assert isinstance(analytics_data.browser_families, Sequence)


@pytest.mark.parametrize("field", AnalyticsType)
def test_get_analytics_from_fields(
    db: Session, mock_read_only_domain: Domain, field: AnalyticsType
):
    end = arrow.now()
    start = end - timedelta(days=1)
    result = crud.event.get_analytics_from_fields(
        db, domain=mock_read_only_domain, fields=[field], start=start, end=end
    )
    assert len(set(result.dict(exclude_unset=True).keys()) - set(["start", "end"])) == 1
    assert getattr(result, field.value) is not None, field.value
