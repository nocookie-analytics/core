from datetime import timedelta
from uuid import uuid4

from fastapi.testclient import TestClient
from hypothesis import given, settings as hypothesis_settings
from hypothesis.provisional import urls
import pytest
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.event import Event, EventType
from app.tests.utils.domain import create_random_domain


def create_pageview_event(db, **kwargs):
    domain = create_random_domain(db)
    url = f"https://{domain.domain_name}/path?query=123"
    event = {
        "et": EventType.page_view.value,
        "url": url,
        "ref": None,
        "tz": "Europe/Amsterdam",
        "ip_country_iso_code": "US",
        "ip_continent_code": "NA",
        **kwargs,
    }
    return event


@given(urls())
@hypothesis_settings(deadline=timedelta(milliseconds=500))
@pytest.mark.usefixtures("override_testclient")
def test_create_page_view_event(client: TestClient, db: Session, url: str) -> None:
    data = create_pageview_event(db, ref=url)
    response = client.get(f"{settings.API_V1_STR}/e/", params=data)
    assert response.status_code == 200, response.json()
    content = response.json()
    assert content["success"] is True
    assert content["pvid"]


@pytest.mark.usefixtures("override_testclient")
def test_create_page_view_event_no_ref(client: TestClient, db: Session) -> None:
    data = create_pageview_event(db, ref="")
    response = client.get(f"{settings.API_V1_STR}/e/", params=data)
    assert response.status_code == 200, response.json()
    content = response.json()
    assert content["success"] is True
    assert content["pvid"]


@pytest.mark.skip(
    "This route only accepts page views now, metric events are not being recorded"
)
@pytest.mark.usefixtures("override_testclient")
def test_create_metric_event_invalid_uuid(client: TestClient, db: Session) -> None:
    data = create_pageview_event(db, et=EventType.metric.value, pvid="invalid-uuid")
    response = client.get(f"{settings.API_V1_STR}/e/", params=data)
    assert response.status_code == 422, response.json()


@pytest.mark.skip(
    "This route only accepts page views now, metric events are not being recorded"
)
@pytest.mark.usefixtures("override_testclient")
def test_create_metric_event(client: TestClient, db: Session) -> None:
    pvid = uuid4()
    data = create_pageview_event(db, et=EventType.metric.value, pvid=pvid)
    response = client.get(f"{settings.API_V1_STR}/e/", params=data)
    assert response.status_code == 200, response.json()
    content = response.json()
    assert content["success"] is True
    assert content["pvid"] == str(pvid)


class TestCustomEvent:
    @pytest.mark.usefixtures("override_testclient")
    def test_create_custom_event_fail_no_pageview_id(
        self, client: TestClient, db: Session
    ) -> None:
        response = client.get(f"{settings.API_V1_STR}/e/custom", params={})
        assert response.status_code == 400
        content = response.json()
        assert content["detail"]

    @pytest.mark.usefixtures("override_testclient")
    def test_create_custom_event_fail_no_event_name(
        self, client: TestClient, db: Session
    ) -> None:
        response = client.get(
            f"{settings.API_V1_STR}/e/custom", params={"page_view_id": str(uuid4())}
        )
        assert response.status_code == 400
        content = response.json()
        assert content["detail"]

    @pytest.mark.usefixtures("override_testclient")
    def test_create_custom_event(self, client: TestClient, db: Session) -> None:
        pvid = uuid4()
        domain = create_random_domain(db)
        url = f"https://{domain.domain_name}/path?query=123"
        response = client.get(
            f"{settings.API_V1_STR}/e/custom",
            params={"page_view_id": str(pvid), "event_name": "click", "url": url},
        )
        assert response.status_code == 200, response.json()
        content = response.json()
        assert content["success"] is True

        event: Event = (
            db.query(Event)
            .filter(
                Event.page_view_id == str(pvid), Event.event_type == EventType.custom
            )
            .scalar()
        )
        assert event
        assert event.event_type == EventType.custom
        # Custom events should not get any fields that we set with page views, we test a few of them just in case
        assert event.browser_family is None
        assert event.device_type is None
        assert event.ip_country_iso_code is None
