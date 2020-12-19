from app.models.parsed_ua import ParsedUA
from furl.furl import furl
from app.utils.referer_parser import Referer
from fastapi.exceptions import HTTPException
from app.models.location import Country
from typing import Dict, List, Optional, Tuple, Union

from arrow.arrow import Arrow
from pydantic import IPvAnyAddress
from sqlalchemy import and_, func
from sqlalchemy.orm import Query, Session

from app.crud.base import CRUDBase
from app.models.domain import Domain
from app.models.event import Event, EventType, ReferrerMediumType
from app.schemas.analytics import (
    AnalyticsData,
    AnalyticsDataTypes,
    AnalyticsType,
    BrowserStat,
    BrowserData,
    CountryData,
    CountryStat,
    DeviceData,
    DeviceStat,
    OSData,
    OSStat,
    PageViewData,
)
from app.schemas.event import EventCreate, EventUpdate
from app.utils.geolocation import get_ip_gelocation


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

    @staticmethod
    def _get_url_components(url: str) -> Dict:
        furled_url = furl(url)
        path = str(furled_url.path)
        url_params = dict(
            furled_url.args
        )  # TODO: furl.args is multidict, this conversion is lossy
        return {"url_params": url_params, "path": path}

    @staticmethod
    def _get_referrer_info(ref: Optional[str], curr_url: Optional[str] = None):
        referrer_medium, referrer_name = ReferrerMediumType.UNKNOWN, None
        if ref:
            parsed_ref = Referer(ref, curr_url)
            referrer_medium = ReferrerMediumType(parsed_ref.medium)
            referrer_name = parsed_ref.referer
        return {
            "referrer_name": referrer_name,
            "referrer_medium": referrer_medium,
        }

    @staticmethod
    def _get_parsed_ua(ua_string: str) -> Dict:
        if ua_string:
            return ParsedUA.from_ua_string(ua_string).dict()
        return {}

    def build_db_obj(self, event_in: EventCreate) -> Event:
        obj_in_data = event_in.dict()
        obj_in_data = {
            **obj_in_data,
            **self._get_geolocation_info(event_in.ip_address),
            **self._get_referrer_info(event_in.referrer, event_in.url),
            **(self._get_parsed_ua(event_in.ua_string)),
            **self._get_url_components(event_in.url),
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
            elif field == AnalyticsType.BROWSERS:
                data.append(self._get_browsers_data(base_page_views_query))
            elif field == AnalyticsType.COUNTRY:
                data.append(self._get_countries_data(base_page_views_query))
            elif field == AnalyticsType.OS:
                data.append(self._get_os_data(base_page_views_query))
            elif field == AnalyticsType.DEVICES:
                data.append(self._get_device_data(base_page_views_query))
            else:
                raise HTTPException(status_code=400)

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
    def _get_browsers_data(base_query) -> BrowserData:
        rows = (
            base_query.group_by(Event.browser_family)
            .with_entities(Event.browser_family, func.count())
            .limit(10)
            .all()
        )
        return BrowserData(
            browser_families=[
                BrowserStat(name=row[0], total_visits=row[1]) for row in rows
            ]
        )

    @staticmethod
    def _get_countries_data(base_query: Query) -> CountryData:
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

    @staticmethod
    def _get_os_data(base_query: Query) -> OSData:
        rows: List[Tuple[str, str, int]] = (
            base_query.group_by(Event.os_family)
            .with_entities(Event.os_family, func.count())
            .limit(10)
            .all()
        )
        return OSData(
            os_families=[OSStat(name=row[0], total_visits=row[1]) for row in rows]
        )

    @staticmethod
    def _get_device_data(base_query) -> DeviceData:
        rows = (
            base_query.group_by(Event.device_family)
            .with_entities(Event.device_family, func.count())
            .limit(10)
            .all()
        )
        return DeviceData(
            device_families=[
                DeviceStat(name=row[0], total_visits=row[1]) for row in rows
            ]
        )


event = CRUDEvent(Event)
