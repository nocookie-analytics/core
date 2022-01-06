from datetime import datetime, timedelta
import string
from typing import Sequence

import arrow
from hypothesis import given
from hypothesis.extra.pytz import timezones
from hypothesis.strategies import datetimes, integers, text, timedeltas, uuids
from pydantic.types import UUID4
import pytest
from sqlalchemy.orm import Session

from app import crud
from app.models.domain import Domain
from app.models.event import EventType, ReferrerMediumType
from app.schemas.analytics import AnalyticsType
from app.schemas.event import CustomEventCreate, PageViewEventCreate
from app.tests.utils.domain import create_random_domain
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
        event_in = PageViewEventCreate(
            url=url,
            referrer="abc",
            user_timezone="Europe/Amsterdam",
            ua_string="Mozilla/5.0 (X11; Linux x86_64; rv:9000.0) Gecko/20100101 Firefox/9000.0",
            page_view_id=str(page_view_id),
            ip=mock_ip_address,
            width=1920,
            height=1080,
        )
        event = crud.event.create_with_domain(db=db, obj_in=event_in, domain=domain)
        assert event.domain_id == domain.id
        assert event.browser_family == "Firefox"
        assert event.ip_country
        assert event.ip_continent_code
        assert event.visitor_fingerprint
        assert event.width == 1920
        assert event.height == 1080

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

    def test_override_referrer(
        self,
        db: Session,
        mock_read_only_domain: Domain,
        mock_ip_address: str,
    ) -> None:
        referrer = "https://www.facebook.com/"
        event = create_random_page_view_event(
            db,
            domain=mock_read_only_domain,
            ip_address=mock_ip_address,
            create_overrides={
                "referrer": referrer,
                "url": f"https://{mock_read_only_domain.domain_name}/path?ref=override",
            },
        )
        assert event.referrer_name == "override"
        assert event.referrer_medium == ReferrerMediumType.UNKNOWN

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

    def test_session(
        self,
        db: Session,
        mock_ip_address: str,
    ) -> None:
        domain = create_random_domain(db)
        event = create_random_page_view_event(
            db,
            domain=domain,
            ip_address=mock_ip_address,
        )
        assert event.seconds_since_last_visit.total_seconds() == 0
        assert event.session_start == event.timestamp

        event2 = create_random_page_view_event(
            db,
            domain=domain,
            ip_address=mock_ip_address,
        )
        assert event2.session_start == event.timestamp
        assert event2.seconds_since_last_visit.total_seconds() > 0


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


class TestCustomEvent:
    @given(
        uuids(version=4), text(string.printable, min_size=2, max_size=50), integers()
    )
    def test_create_custom_event(
        self,
        db: Session,
        mock_read_only_domain: Domain,
        page_view_id: UUID4,
        event_name: str,
        event_value: int,
    ):
        url = f"http://{mock_read_only_domain.domain_name}/somepath"
        event_in = CustomEventCreate(
            url=url,
            page_view_id=page_view_id,
            event_name=event_name,
            event_value=event_value,
        )
        event = crud.event.create_with_domain(
            db=db, obj_in=event_in, domain=mock_read_only_domain
        )
        assert event
        assert event.event_type == EventType.custom
        assert event.page_view_id == str(event_in.page_view_id)
        assert event.event_name == event_in.event_name
        assert event.event_value == event_in.event_value
