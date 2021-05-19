from datetime import timedelta
from uuid import uuid4

from fastapi.testclient import TestClient
from hypothesis import given, settings as hypothesis_settings
from hypothesis.provisional import urls
import pytest
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.event import EventType
from app.tests.utils.domain import create_random_domain


def create_event(db, **kwargs):
    domain = create_random_domain(db)
    url = f"https://{domain.domain_name}/path?query=123"
    event = {
        "et": EventType.page_view.value,
        "uas": "Firefox",
        "url": url,
        "pt": "Hello World Page Title",
        "sc": 200,
        "ltms": 10,
        "psb": 300000,
        "ref": None,
        "ut": "Europe/Amsterdam",
        "ip_country_iso_code": "US",
        "ip_continent_code": "NA",
        **kwargs,
    }
    return event


@given(urls())
@hypothesis_settings(deadline=timedelta(milliseconds=500))
@pytest.mark.usefixtures("override_testclient")
def test_create_page_view_event(client: TestClient, db: Session, url: str) -> None:
    data = create_event(db, ref=url)
    response = client.get(f"{settings.API_V1_STR}/e/", params=data)
    assert response.status_code == 200, response.json()
    content = response.json()
    assert content["success"] is True
    assert content["pvid"]


@pytest.mark.usefixtures("override_testclient")
def test_create_page_view_event_no_ref(client: TestClient, db: Session) -> None:
    data = create_event(db, ref="")
    response = client.get(f"{settings.API_V1_STR}/e/", params=data)
    assert response.status_code == 200, response.json()
    content = response.json()
    assert content["success"] is True
    assert content["pvid"]


@pytest.mark.usefixtures("override_testclient")
def test_create_metric_event_invalid_uuid(client: TestClient, db: Session) -> None:
    data = create_event(db, et=EventType.metric.value, pvid="invalid-uuid")
    response = client.get(f"{settings.API_V1_STR}/e/", params=data)
    assert response.status_code == 422, response.json()


@pytest.mark.usefixtures("override_testclient")
def test_create_metric_event(client: TestClient, db: Session) -> None:
    pvid = uuid4()
    data = create_event(db, et=EventType.metric.value, pvid=pvid)
    response = client.get(f"{settings.API_V1_STR}/e/", params=data)
    assert response.status_code == 200, response.json()
    content = response.json()
    assert content["success"] is True
    assert content["pvid"] == str(pvid)


@pytest.mark.usefixtures("override_testclient")
def test_create_custom_event_fail(client: TestClient, db: Session) -> None:
    data = create_event(db, et=EventType.custom.value)
    response = client.get(f"{settings.API_V1_STR}/e/", params=data)
    assert response.status_code == 400
    content = response.json()
    assert content["detail"]


@pytest.mark.usefixtures("override_testclient")
def test_create_page_view_event_invalid_event_type(
    client: TestClient, db: Session
) -> None:
    data = create_event(db, et="invalid_event")
    response = client.get(f"{settings.API_V1_STR}/e/", params=data)
    assert response.status_code == 422, response.text
    content = response.json()
    assert content["detail"]
