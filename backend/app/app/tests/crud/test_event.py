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
            referrer="abc",
            user_timezone="Europe/Amsterdam",
            ua_string="Mozilla/5.0 (X11; Linux x86_64; rv:9000.0) Gecko/20100101 Firefox/9000.0",
            page_view_id=str(page_view_id),
            ip=mock_ip_address,
        )
        event = crud.event.create_with_domain(db=db, obj_in=event_in, domain=domain)
        assert event.domain_id == domain.id
        assert event.browser_family == "Firefox"
        assert event.ip_country
        assert event.ip_continent_code
        assert event.visitor_fingerprint

    @pytest.mark.parametrize(
        "referrer, expected_referrer_medium, expected_referrer_name",
        [
            ("https://www.google.com", ReferrerMediumType.SEARCH, "Google"),
            ("https://www.facebook.com", ReferrerMediumType.SOCIAL, "Facebook"),
            ("https://mail.google.com", ReferrerMediumType.EMAIL, "Gmail"),
            (
                "https://somerandomdomain.com",
                ReferrerMediumType.UNKNOWN,
                "somerandomdomain.com",
            ),
            ("INTERNAL", ReferrerMediumType.INTERNAL, None),
            ("", ReferrerMediumType.UNKNOWN, None),
            (None, ReferrerMediumType.UNKNOWN, None),
        ],
    )
    def test_create_page_view_event_referrer(
        self,
        db: Session,
        mock_read_only_domain: Domain,
        mock_ip_address: str,
        referrer: str,
        expected_referrer_medium: ReferrerMediumType,
        expected_referrer_name: str,
    ) -> None:
        domain = mock_read_only_domain
        if referrer == "INTERNAL":
            referrer = f"https://{mock_read_only_domain.domain_name}"
        event = create_random_page_view_event(
            db,
            domain=domain,
            ip_address=mock_ip_address,
            create_overrides={
                "referrer": referrer,
                "url": f"https://{mock_read_only_domain.domain_name}/path",
            },
        )
        assert event.referrer_medium == expected_referrer_medium
        assert event.referrer_name == expected_referrer_name

    def test_create_url_components(
        self,
        db: Session,
        mock_read_only_domain: Domain,
        mock_ip_address: str,
    ) -> None:
        domain = mock_read_only_domain
        event = create_random_page_view_event(
            db,
            domain=domain,
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
        fields = [AnalyticsType.SUMMARY, AnalyticsType.BROWSERS]
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
        assert analytics_data.summary
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
