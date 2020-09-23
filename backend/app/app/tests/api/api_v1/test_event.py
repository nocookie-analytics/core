from app.models.event import EventType
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.domain import create_random_domain
from app.tests.utils.utils import random_lower_string


def test_create_event(client: TestClient, db: Session) -> None:
    domain = create_random_domain(db)
    data = {
        "domain_name": domain.domain_name,
        "uid": random_lower_string(),
        "et": EventType.page_view.value,
        "uas": "Firefox",
        "url": "https://gaganpreet.in/",
        "pt": "Hello World Page Title",
        "sc": 200,
        "ltms": 10,
        "psb": 300000,
        "ref": None,
        "ut": "Europe/Amsterdam",
    }
    response = client.get(f"{settings.API_V1_STR}/e/", params=data)
    print(response.text)
    assert response.status_code == 200
    content = response.json()
    assert content["success"] == True
