from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.domain import create_random_domain


def test_create_item(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"title": "Foo", "description": "Fighters"}
    response = client.post(
        f"{settings.API_V1_STR}/domains/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "owner_id" in content


def test_read_item(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    item = create_random_domain(db)
    response = client.get(
        f"{settings.API_V1_STR}/domains/{item.id}", headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == item.title
    assert content["description"] == item.description
    assert content["id"] == item.id
    assert content["owner_id"] == item.owner_id
