from app.models.location import Country
from typing import Dict, List, Optional, Tuple, Union

from arrow.arrow import Arrow
from pydantic import IPvAnyAddress
from sqlalchemy import and_, func
from sqlalchemy.orm import Query, Session, selectinload

from app.crud.base import CRUDBase
from app.models.domain import Domain
from app.models.event import Event, EventType
from app.schemas.analytics import (
    AnalyticsData,
    AnalyticsDataTypes,
    AnalyticsType,
    BrowserStat,
    BrowsersData,
    CountryData,
    CountryStat,
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
            base_page_views_query = self._page_views_in_date_range(domain, start, end)
            if field == AnalyticsType.PAGEVIEWS:
                data.append(self._get_page_views(base_page_views_query))
            if field == AnalyticsType.BROWSERS:
                data.append(self._get_browsers_data(base_page_views_query))
        return AnalyticsData(start=start, end=end, data=data)

    @staticmethod
    def _page_views_in_date_range(domain: Domain, start: Arrow, end: Arrow) -> Query:
        return domain.events.filter(
            and_(Event.timestamp >= start.datetime, Event.timestamp <= end.datetime)
        ).filter(Event.event_type == EventType.page_view)

    @staticmethod
    def _get_page_views(base_query: Query) -> PageViewData:
        return PageViewData(pageviews=base_query.count())

    @staticmethod
    def _get_browsers_data(base_query) -> BrowsersData:
        rows = (
            base_query.group_by(Event.browser_family)
            .with_entities(Event.browser_family, func.count())
            .limit(10)
            .all()
        )
        return BrowsersData(
            browsers=[BrowserStat(name=row[0], total_visits=row[1]) for row in rows]
        )

    @staticmethod
    def _get_countries_data(base_query: Query):
        rows: List[Tuple[str, str, int]] = (
            base_query.group_by(Event.ip_country_iso_code, Country.name)
            .with_entities(Event.ip_country_iso_code, Country.name, func.count())
            .limit(10)
            .all()
        )
        return CountryData(
            countries=[
                CountryStat(country_code=row[0], name=row[1], total_visits=row[2])
                for row in rows
            ]
        )


event = CRUDEvent(Event)
