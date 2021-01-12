from typing import Dict, List, Optional, Union

from arrow.arrow import Arrow
from fastapi.exceptions import HTTPException
from furl.furl import furl
from pydantic import IPvAnyAddress
from sqlalchemy import and_
from sqlalchemy.orm import Query, Session

from app.crud.base import CRUDBase
from app.models.domain import Domain
from app.models.event import Event, EventType, MetricType, ReferrerMediumType
from app.models.parsed_ua import ParsedUA
from app.schemas.analytics import (
    AnalyticsData,
    AnalyticsType,
    BrowserStat,
    CountryStat,
    DeviceStat,
    MetricStat,
    OSStat,
    PageViewStat,
    PageViewsPerDayStat,
    ReferrerMediumStat,
    ReferrerNameStat,
    UTMCampaignStat,
    UTMContentStat,
    UTMMediumStat,
    UTMSourceStat,
    UTMTermStat,
)
from app.schemas.event import EventCreate, EventUpdate
from app.utils.geolocation import get_ip_gelocation
from app.utils.referer_parser import Referer


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
        utm_param_list = [
            "utm_source",
            "utm_medium",
            "utm_campaign",
            "utm_term",
            "utm_content",
        ]
        utm_params = {}
        for utm_param in utm_param_list:
            utm_params[utm_param] = url_params.pop(utm_param, None)
        return {"url_params": url_params, "path": path, **utm_params}

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
        data = AnalyticsData(start=start, end=end)
        for field in fields:
            base_query = domain.events.filter(
                and_(Event.timestamp >= start.datetime, Event.timestamp <= end.datetime)
            ).filter(Event.event_type == EventType.page_view)
            if field == AnalyticsType.PAGEVIEWS:
                data.pageviews = PageViewStat.from_base_query(base_query)
            elif field == AnalyticsType.PAGEVIEWS_PER_DAY:
                data.pageviews_per_day = PageViewsPerDayStat.from_base_query(base_query)
            elif field == AnalyticsType.BROWSERS:
                data.browser_families = BrowserStat.from_base_query(base_query)
            elif field == AnalyticsType.COUNTRY:
                data.countries = CountryStat.from_base_query(base_query)
            elif field == AnalyticsType.OS:
                data.os_families = OSStat.from_base_query(base_query)
            elif field == AnalyticsType.DEVICES:
                data.device_families = DeviceStat.from_base_query(base_query)
            elif field == AnalyticsType.REFERRER_MEDIUMS:
                data.referrer_mediums = ReferrerMediumStat.from_base_query(base_query)
            elif field == AnalyticsType.REFERRER_NAMES:
                data.referrer_names = ReferrerNameStat.from_base_query(base_query)
            elif field == AnalyticsType.UTM_CAMPAIGNS:
                data.utm_campaigns = UTMCampaignStat.from_base_query(base_query)
            elif field == AnalyticsType.UTM_SOURCES:
                data.utm_sources = UTMSourceStat.from_base_query(base_query)
            elif field == AnalyticsType.UTM_TERMS:
                data.utm_terms = UTMTermStat.from_base_query(base_query)
            elif field == AnalyticsType.UTM_CONTENTS:
                data.utm_contents = UTMContentStat.from_base_query(base_query)
            elif field == AnalyticsType.UTM_MEDIUMS:
                data.utm_mediums = UTMMediumStat.from_base_query(base_query)
            elif field == AnalyticsType.LCP_PER_DAY:
                data.lcp_per_day = MetricStat.from_base_query(
                    base_query, metric_type=MetricType.LCP
                )
            elif field == AnalyticsType.FID_PER_DAY:
                data.lcp_per_day = MetricStat.from_base_query(
                    base_query, metric_type=MetricType.FID
                )
            elif field == AnalyticsType.FP_PER_DAY:
                data.lcp_per_day = MetricStat.from_base_query(
                    base_query, metric_type=MetricType.FP
                )
            elif field == AnalyticsType.CLS_PER_DAY:
                data.lcp_per_day = MetricStat.from_base_query(
                    base_query, metric_type=MetricType.CLS
                )
            else:
                raise HTTPException(status_code=400)

        return data


event = CRUDEvent(Event)
