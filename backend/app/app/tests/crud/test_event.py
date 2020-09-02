from sqlalchemy.orm import Session

from app import crud
from app.schemas.event import EventCreate
from app.tests.utils.domain import create_random_domain
from app.tests.utils.utils import random_lower_string


def test_create_event(db: Session) -> None:
    event_name = random_lower_string()
    event_in = EventCreate(event_name=event_name)
    domain = create_random_domain(db)
    event = crud.event.create_with_domain(db=db, obj_in=event_in, domain_id=domain.id)
    assert event.domain_id == domain.id
    assert event.ua_string == obj_in.ua_string
