from app.utils import get_ip_gelocation
from typing import Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.event import Event, EventType
from app.schemas.event import EventCreate, EventUpdate


class CRUDEvent(CRUDBase[Event, EventCreate, EventUpdate]):
    def add_geolocation_info(self, event: Event) -> None:
        if event.ip_address:
            geolocation = get_ip_gelocation(event.ip_address)
            if not geolocation:
                return
            city_id = geolocation.city.geoname_id
            country_code = geolocation.country.iso_code
            if city_id:
                event._ip_city_id = city_id
            if country_code:
                event._ip_country_iso_code = country_code

    def create_with_domain(
        self, db: Session, *, obj_in: EventCreate, domain_id: int,
    ) -> Event:
        """
        Create an event
        """
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data, domain_id=domain_id)
        self.add_geolocation_info(db_obj)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


event = CRUDEvent(Event)
