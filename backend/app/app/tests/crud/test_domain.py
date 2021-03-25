from app.models.domain import Domain
import pytest
import sqlalchemy
from sqlalchemy.orm import Session

from app import crud
from app.schemas.domain import DomainCreate, DomainUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def test_create_domain(db: Session) -> None:
    domain_name = random_lower_string()
    domain_in = DomainCreate(domain_name=domain_name)
    user = create_random_user(db)
    domain = crud.domain.create_with_owner(db=db, obj_in=domain_in, owner_id=user.id)
    assert domain.domain_name == domain_name
    assert domain.owner_id == user.id

    # Doing it again should fail due to unique constraint on domain name
    assert (
        crud.domain.create_with_owner(db=db, obj_in=domain_in, owner_id=user.id) == None
    )


def test_get_domain(db: Session) -> None:
    domain_name = random_lower_string()
    domain_in = DomainCreate(domain_name=domain_name)
    user = create_random_user(db)
    domain = crud.domain.create_with_owner(db=db, obj_in=domain_in, owner_id=user.id)
    stored_domain = crud.domain.get(db=db, id=domain.id)
    assert stored_domain
    assert domain.id == stored_domain.id
    assert domain.domain_name == stored_domain.domain_name
    assert domain.owner_id == stored_domain.owner_id


def test_get_domain_by_name(db: Session) -> None:
    domain_name = random_lower_string()
    domain_in = DomainCreate(domain_name=domain_name)
    user = create_random_user(db)
    domain = crud.domain.create_with_owner(db=db, obj_in=domain_in, owner_id=user.id)
    stored_domain = crud.domain.get_by_name(db=db, name=domain.domain_name)
    assert stored_domain
    assert domain.id == stored_domain.id
    assert domain.domain_name == stored_domain.domain_name
    assert domain.owner_id == stored_domain.owner_id


def test_update_domain(db: Session) -> None:
    domain_name = random_lower_string()
    domain_in = DomainCreate(domain_name=domain_name)
    user = create_random_user(db)
    domain = crud.domain.create_with_owner(db=db, obj_in=domain_in, owner_id=user.id)
    domain_name2 = "bar.com"
    domain_update = DomainUpdate(domain_name=domain_name2)
    domain2 = crud.domain.update(db=db, db_obj=domain, obj_in=domain_update)
    assert domain.id == domain2.id
    assert domain.domain_name == domain_name2
    assert domain.owner_id == domain2.owner_id


def test_delete_domain(db: Session) -> None:
    domain_name = random_lower_string()
    domain_in = DomainCreate(domain_name=domain_name)
    user = create_random_user(db)
    domain = crud.domain.create_with_owner(db=db, obj_in=domain_in, owner_id=user.id)
    domain2 = crud.domain.remove(db=db, id=domain.id)
    domain3 = crud.domain.get(db=db, id=domain.id)
    assert domain3 is None
    assert domain2.id == domain.id
    assert domain2.domain_name == domain_name
    assert domain2.owner_id == user.id


def test_public_domain(
    read_write_domain: Domain,
    db: Session,
) -> None:
    user = create_random_user(db)
    for current_user in [None, user]:
        domain = crud.domain.get_by_name_check_permission(
            db, read_write_domain.domain_name, current_user=current_user
        )
        assert not domain, f"{current_user} should be able to access the domain"

    read_write_domain.public = True
    db.add(read_write_domain)
    db.commit()

    for current_user in [None, user]:
        domain = crud.domain.get_by_name_check_permission(
            db, read_write_domain.domain_name, current_user=current_user
        )
        assert domain, f"{current_user} should be able to access the domain"
