from app.tests.utils.utils import random_lower_string
from app.tests.utils.user import create_random_user, user_authentication_headers
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.domain import create_random_domain


def test_create_domain(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"domain_name": "foo.com"}
    response = client.post(
        f"{settings.API_V1_STR}/domains/",
        headers=superuser_token_headers,
        json=data,
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
        f"{settings.API_V1_STR}/domains/{domain.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["domain_name"] == domain.domain_name
    assert content["id"] == domain.id
    assert content["owner_id"] == domain.owner_id


def test_update_domain(client: TestClient, db: Session) -> None:
    password = random_lower_string()
    user = create_random_user(db, password=password)
    domain = create_random_domain(db, owner_id=user.id)
    headers = user_authentication_headers(
        client=client, email=user.email, password=password
    )
    assert domain.public is False
    response = client.put(
        f"{settings.API_V1_STR}/domains/{domain.id}",
        headers=headers,
        json={"public": True},
    )
    assert response.status_code == 200, response.text
    db.refresh(domain)

    assert domain.public is True


def test_update_domain_by_name(client: TestClient, db: Session) -> None:
    password = random_lower_string()
    user = create_random_user(db, password=password)
    domain = create_random_domain(db, owner_id=user.id)
    headers = user_authentication_headers(
        client=client, email=user.email, password=password
    )
    assert domain.public is False
    response = client.put(
        f"{settings.API_V1_STR}/domains/by-name/{domain.domain_name}",
        headers=headers,
        json={"public": True},
    )
    assert response.status_code == 200, response.text
    db.refresh(domain)

    assert domain.public is True
