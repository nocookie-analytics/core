from typing import Dict, List, Optional, Union

from arrow.arrow import Arrow
from pydantic import IPvAnyAddress
from sqlalchemy import and_, func
from sqlalchemy.orm import Query, Session

from app.crud.base import CRUDBase
from app.models.domain import Domain
from app.models.event import Event, EventType
from app.schemas.analytics import (
    AnalyticsData,
    AnalyticsDataTypes,
    AnalyticsType,
    Browser,
    BrowsersData,
    PageViewData,
)
from app.schemas.event import EventCreate, EventUpdate
from app.utils import get_ip_gelocation


class CRUDEvent(CRUDBase[Event, EventCreate, EventUpdate]):
    @staticmethod
    def _get_geolocation_info(
        ip_address: IPvAnyAddress,
    ) -> Dict[str, Optional[Union[int, str]]]:
        data: Dict[str, Optional[Union[str, int]]] = {}
        if ip_address:
            geolocation = get_ip_gelocation(str(ip_address))
            if not geolocation:
                return data
            city_id = geolocation.city.geoname_id
            country_code = geolocation.country.iso_code
            continent_code = geolocation.continent.code
            if city_id:
                data["ip_city_id"] = city_id
            if country_code:
                data["ip_country_iso_code"] = country_code
            data["ip_continent_code"] = continent_code
        return data

    def build_db_obj(self, event_in: EventCreate) -> Event:
        obj_in_data = event_in.dict(exclude={"metric", "parsed_ua"})
        obj_in_data = {
            **obj_in_data,
            **self._get_geolocation_info(event_in.ip_address),
            **(event_in.parsed_ua.dict() if event_in.parsed_ua else {}),
            "page_view_id": event_in.page_view_id.hex,
        }
        print(obj_in_data)
        db_obj = self.model(**obj_in_data)
        return db_obj

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
        db_obj = self.build_db_obj(obj_in)
        db_obj.domain_id = domain_id
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

    @staticmethod
    def _page_views_in_date_range(domain: Domain, start: Arrow, end: Arrow) -> Query:
        return domain.events.filter(
            and_(Event.timestamp >= start.datetime, Event.timestamp <= end.datetime)
        ).filter(Event.event_type == EventType.page_view)

    def _get_page_views(
        self, db: Session, domain: Domain, start: Arrow, end: Arrow
    ) -> PageViewData:
        count = self._page_views_in_date_range(domain, start, end).count()
        return PageViewData(pageviews=count)

    def _get_browsers_data(
        self, db: Session, domain: Domain, start: Arrow, end: Arrow
    ) -> BrowsersData:

        rows = (
            self._page_views_in_date_range(domain, start, end)
            .group_by(Event.browser_family)
            .with_entities(Event.browser_family, func.count())
            .all()
        )
        return BrowsersData(
            browsers=[Browser(name=row[0], total_visits=row[1]) for row in rows]
        )


event = CRUDEvent(Event)
