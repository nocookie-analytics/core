from typing import List

from arrow.arrow import Arrow
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.domain import Domain
from app.models.event import Event
from app.schemas.analytics import (
    AnalyticsData,
    AnalyticsType,
    BrowsersData,
    PageViewData,
    AnalyticsDataTypes,
)
from app.schemas.event import EventCreate, EventUpdate
from app.utils import get_ip_gelocation


class CRUDEvent(CRUDBase[Event, EventCreate, EventUpdate]):
    def add_geolocation_info(self, event: Event) -> None:
        if event.ip_address:
            geolocation = get_ip_gelocation(event.ip_address)
            if not geolocation:
                return
            city_id = geolocation.city.geoname_id
            country_code = geolocation.country.iso_code
            continent_code = geolocation.continent.code
            if city_id:
                event.ip_city_id = city_id
            if country_code:
                event.ip_country_iso_code = country_code
            event.ip_continent_code = continent_code

    def create_with_domain(
        self,
        db: Session,
        *,
        obj_in: EventCreate,
        domain_id: int,
    ) -> Event:
        """
        Create an event
        """
        obj_in_data = obj_in.dict()
        obj_in_data["page_view_id"] = obj_in_data["page_view_id"].hex
        db_obj = self.model(**obj_in_data, domain_id=domain_id)
        self.add_geolocation_info(db_obj)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_analytics_from_fields(
        self,
        db: Session,
        *,
        fields: List[AnalyticsType],
        start: Arrow,
        end: Arrow,
        domain: Domain,
    ) -> AnalyticsData:
        data: List[AnalyticsDataTypes] = []
        for field in fields:
            if field == AnalyticsType.PAGEVIEWS:
                data.append(self._get_page_views(db, domain, start, end))
            if field == AnalyticsType.BROWSERS:
                data.append(self._get_browsers_data(db, domain, start, end))
        return AnalyticsData(start=start, end=end, data=data)

    def _get_page_views(
        self, db: Session, domain: Domain, start: Arrow, end: Arrow
    ) -> PageViewData:
        return PageViewData()

    def _get_browsers_data(
        self, db: Session, domain: Domain, start: Arrow, end: Arrow
    ) -> BrowsersData:
        return BrowsersData()


event = CRUDEvent(Event)
