from app.utils import sqlalchemy_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.event import Event, EventType
from app.schemas.event import EventCreate, EventUpdate


class CRUDEvent(CRUDBase[Event, EventCreate, EventUpdate]):
    def create_with_domain(
        self, db: Session, *, obj_in: EventCreate, domain_id: int, ip_address: str,
    ) -> Event:
        """
        Create an event
        """
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data, ip_address=ip_address, domain_id=domain_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


event = CRUDEvent(Event)
