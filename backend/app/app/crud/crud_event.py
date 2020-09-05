from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate


class CRUDEvent(CRUDBase[Event, EventCreate, EventUpdate]):
    def create_with_domain(
        self, db: Session, *, obj_in: EventCreate, domain_id: int
    ) -> Event:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, domain_id=domain_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


event = CRUDEvent(Event)
