from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.domain import create_random_domain


def test_create_domain(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"domain_name": "foo.com"}
    response = client.post(
        f"{settings.API_V1_STR}/domains/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["domain_name"] == data["domain_name"]
    assert "id" in content
    assert "owner_id" in content


def test_read_domain(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    domain = create_random_domain(db)
    response = client.get(
        f"{settings.API_V1_STR}/domains/{domain.id}", headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["domain_name"] == domain.domain_name
    assert content["id"] == domain.id
    assert content["owner_id"] == domain.owner_id
