from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.domain import DomainCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_domain(
    db: Session, *, owner_id: Optional[int] = None
) -> models.Domain:
    if owner_id is None:
        user = create_random_user(db)
        owner_id = user.id
    domain_name = f"{random_lower_string()}.com"
    item_in = DomainCreate(domain_name=domain_name, id=id)
    return crud.domain.create_with_owner(db=db, obj_in=item_in, owner_id=owner_id)
