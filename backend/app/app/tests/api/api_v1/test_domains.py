from typing import Dict
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


def test_update_domain_by_name(
    client: TestClient, db: Session, normal_user_token_headers: Dict[str, str]
) -> None:
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
    content = response.json()
    db.refresh(domain)
    assert content["public"] is True, content

    response = client.put(
        f"{settings.API_V1_STR}/domains/by-name/{domain.domain_name}",
        headers=normal_user_token_headers,
        json={"public": True},
    )
    assert response.status_code == 400


def test_get_domain_by_name(
    client: TestClient, db: Session, normal_user_token_headers: Dict[str, str]
) -> None:
    password = random_lower_string()
    user = create_random_user(db, password=password)
    domain = create_random_domain(db, owner_id=user.id)
    headers = user_authentication_headers(
        client=client, email=user.email, password=password
    )
    response = client.get(
        f"{settings.API_V1_STR}/domains/by-name/{domain.domain_name}",
        headers=headers,
    )
    assert response.status_code == 200, response.text
    content = response.json()
    assert content["public"] == domain.public
    assert content["domain_name"] == domain.domain_name

    # Fetching domain belonging to another user should be an error
    response = client.get(
        f"{settings.API_V1_STR}/domains/by-name/{domain.domain_name}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400


def test_delete_domain(
    client: TestClient, db: Session, normal_user_token_headers: Dict[str, str]
) -> None:
    password = random_lower_string()
    user = create_random_user(db, password=password)
    domain = create_random_domain(db, owner_id=user.id)
    assert not domain.delete_at
    headers = user_authentication_headers(
        client=client, email=user.email, password=password
    )
    # Trying to delete domain belonging to another user should be an error
    response = client.delete(
        f"{settings.API_V1_STR}/domains/by-name/{domain.domain_name}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400

    # Delete a domain belonging to the user itself should be successful
    response = client.delete(
        f"{settings.API_V1_STR}/domains/by-name/{domain.domain_name}",
        headers=headers,
    )
    assert response.status_code == 200, response.text
    db.refresh(domain)
    assert domain.delete_at

    # A deleted domain shouldn't be fetchable anymore
    response = client.get(
        f"{settings.API_V1_STR}/domains/by-name/{domain.domain_name}",
        headers=headers,
    )
    assert response.status_code == 404
