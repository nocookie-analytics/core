import pytest
from fastapi.testclient import TestClient
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
        **kwargs,
    }
    return event


@pytest.mark.usefixtures("override_testclient")
def test_create_event(client: TestClient, db: Session) -> None:
    data = create_event(db)
    response = client.get(f"{settings.API_V1_STR}/e/", params=data)
    assert response.status_code == 200, response.json()
    content = response.json()
    assert content["success"] is True


@pytest.mark.usefixtures("override_testclient")
def test_create_event_fail(client: TestClient, db: Session) -> None:
    data = create_event(db, et=EventType.custom.value)
    response = client.get(f"{settings.API_V1_STR}/e/", params=data)
    assert response.status_code == 400
    content = response.json()
    assert content["detail"]


@pytest.mark.usefixtures("override_testclient")
def test_create_event_fail(client: TestClient, db: Session) -> None:
    data = create_event(db, et="invalid_event")
    response = client.get(f"{settings.API_V1_STR}/e/", params=data)
    assert response.status_code == 400
    content = response.json()
    assert content["detail"]
