from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.domain import create_random_domain


def test_create_event(client: TestClient, db: Session) -> None:
    domain = create_random_domain(db)
    data = {"domain_name": domain.domain_name}
    response = client.get(f"{settings.API_V1_STR}/e/", json=data)
    assert response.status_code == 200
    content = response.json()
    assert content["success"] == True
