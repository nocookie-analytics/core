from app.utils.geolocation import get_ip_from_request, get_ip_gelocation
from typing import Dict, List, Optional, Union

from hashlib import sha3_256
from arrow.arrow import Arrow
from fastapi.exceptions import HTTPException
from furl.furl import furl
from pydantic import IPvAnyAddress
from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.crud.base import CRUDBase
from app.models.domain import Domain
from app.models.event import Event, EventType, MetricType, ReferrerMediumType
from app.models.parsed_ua import ParsedUA
from app.schemas.analytics import (
    AvgMetricPerDayStat,
    PageViewsPerDayStat,
    AggregateStat,
    AnalyticsData,
    AnalyticsType,
    PageViewStat,
)
from app.schemas.event import EventCreate, EventUpdate
from app.utils.referer_parser import Referer


class CRUDEvent(CRUDBase[Event, EventCreate, EventUpdate]):
    @staticmethod
    def _get_url_components(url: str) -> Dict:
        furled_url = furl(url)
        path = str(furled_url.path)
        url_params = {}
        params_to_keep = [
            "ref",
            "lang",
            "language",
        ]  # TODO: This can be extended with a domain configurable list, eg: affiliates etc
        for param_name in params_to_keep:
            if param_name in furled_url.args:
                url_params[param_name] = furled_url.args[param_name]
        utm_param_list = [
            "utm_source",
            "utm_medium",
            "utm_campaign",
            "utm_term",
            "utm_content",
        ]
        utm_params = {}
        for utm_param in utm_param_list:
            utm_params[utm_param] = furled_url.args.get(utm_param, None)
        return {"url_params": url_params, "path": path, **utm_params}

    @staticmethod
    def _get_visitor_fingerprint(user_agent: str, domain: Domain, ip: str) -> str:
        data = "-".join([str(domain.id), domain.salt, ip, user_agent])
        return sha3_256(data.encode("utf-8")).hexdigest()

    @staticmethod
    def _get_referrer_info(ref_url: Optional[str], curr_url: Optional[str] = None):
        referrer_medium, referrer_name = ReferrerMediumType.UNKNOWN, None
        try:
            furled_ref = furl(ref_url)
        except ValueError:
            furled_ref = None
        if ref_url:
            parsed_ref = Referer(ref_url, curr_url)
            referrer_medium = ReferrerMediumType(parsed_ref.medium)
            referrer_name = parsed_ref.referer
            if (
                not referrer_name
                and referrer_medium != ReferrerMediumType.INTERNAL
                and furled_ref
            ):
                referrer_name = furled_ref.host
        return {
            "referrer_name": referrer_name,
            "referrer_medium": referrer_medium,
        }

    @staticmethod
    def _get_parsed_ua(ua_string: str) -> Dict:
        if ua_string:
            return ParsedUA.from_ua_string(ua_string).dict()
        return {}

    @staticmethod
    def _get_geolocation_info(
        ip_address: str,
    ) -> Dict[str, Optional[Union[int, str]]]:
        data: Dict[str, Optional[Union[str, int]]] = {}
        if ip_address:
            geolocation = get_ip_gelocation(ip_address)
            if not geolocation:
                return data
            country_code = geolocation.country.iso_code
            continent_code = geolocation.continent.code
            if country_code:
                data["ip_country_iso_code"] = country_code
            data["ip_continent_code"] = continent_code
        return data

    def build_db_obj(self, event_in: EventCreate, domain: Domain) -> Event:
        obj_in_data = {
            **event_in.dict(),
            "page_view_id": event_in.page_view_id.hex,
        }
        if event_in.event_type == EventType.page_view:
            obj_in_data = {
                **obj_in_data,
                **self._get_referrer_info(event_in.referrer, event_in.url),
                **(self._get_parsed_ua(event_in.ua_string)),
                **self._get_url_components(event_in.url),
                **self._get_geolocation_info(event_in.ip),
                "visitor_fingerprint": self._get_visitor_fingerprint(
                    event_in.ua_string, domain, event_in.ip
                ),
            }
        del obj_in_data["referrer"]
        del obj_in_data["ua_string"]
        del obj_in_data["url"]
        del obj_in_data["ip"]
        db_obj = self.model(**obj_in_data)
        return db_obj

    def create_with_domain(
        self,
        db: Session,
        *,
        obj_in: EventCreate,
        domain: Domain,
    ) -> Event:
        """
        Create an event
        """
        db_obj = self.build_db_obj(obj_in, domain=domain)
        db_obj.domain_id = domain.id
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
        country: str = None,
        page: str = None,
        browser: str = None,
        os: str = None,
        device: str = None,
        referrer_name: str = None,
    ) -> AnalyticsData:
        data = AnalyticsData(start=start, end=end)
        for field in fields:
            base_query = (
                db.query(Event)
                .filter(Event.domain_id == domain.id)
                .filter(
                    and_(
                        Event.timestamp >= start.datetime,
                        Event.timestamp <= end.datetime,
                    )
                )
            )
            if country is not None:
                base_query = base_query.filter(Event.ip_country_iso_code == country)
            if page is not None:
                base_query = base_query.filter(Event.path == page)
            if browser is not None:
                base_query = base_query.filter(Event.browser_family == browser)
            if os is not None:
                base_query = base_query.filter(Event.os_family == os)
            if device is not None:
                base_query = base_query.filter(Event.device_brand == device)
            if referrer_name is not None:
                base_query = base_query.filter(Event.referrer_name == referrer_name)
            page_view_base_query = base_query.filter(
                Event.event_type == EventType.page_view
            )
            metric_base_query = base_query.filter(Event.event_type == EventType.metric)
            if field == AnalyticsType.PAGEVIEWS:
                data.pageviews = PageViewStat.from_base_query(base_query)
            elif field == AnalyticsType.BROWSERS:
                data.browser_families = AggregateStat.from_base_query(
                    page_view_base_query, Event.browser_family
                )
            elif field == AnalyticsType.COUNTRIES:
                data.countries = AggregateStat.from_base_query(
                    page_view_base_query, Event.ip_country_iso_code, filter_none=True
                )
            elif field == AnalyticsType.OS:
                data.os_families = AggregateStat.from_base_query(
                    page_view_base_query, Event.os_family
                )
            elif field == AnalyticsType.DEVICES:
                data.device_families = AggregateStat.from_base_query(
                    page_view_base_query, Event.device_brand, filter_none=True
                )
            elif field == AnalyticsType.PAGES:
                data.pages = AggregateStat.from_base_query(
                    page_view_base_query, Event.path
                )
            elif field == AnalyticsType.REFERRER_MEDIUMS:
                data.referrer_mediums = AggregateStat.from_base_query(
                    page_view_base_query, Event.referrer_medium, filter_none=True
                )
            elif field == AnalyticsType.REFERRER_NAMES:
                data.referrer_names = AggregateStat.from_base_query(
                    page_view_base_query,
                    Event.referrer_name,
                    filter_none=True,
                )
            elif field == AnalyticsType.UTM_CAMPAIGNS:
                data.utm_campaigns = AggregateStat.from_base_query(
                    page_view_base_query,
                    Event.utm_campaign,
                    filter_none=True,
                )
            elif field == AnalyticsType.UTM_SOURCES:
                data.utm_sources = AggregateStat.from_base_query(
                    page_view_base_query,
                    Event.utm_source,
                    filter_none=True,
                )
            elif field == AnalyticsType.UTM_TERMS:
                data.utm_terms = AggregateStat.from_base_query(
                    page_view_base_query,
                    Event.utm_term,
                    filter_none=True,
                )
            elif field == AnalyticsType.UTM_CONTENTS:
                data.utm_contents = AggregateStat.from_base_query(
                    page_view_base_query,
                    Event.utm_content,
                    filter_none=True,
                )
            elif field == AnalyticsType.UTM_MEDIUMS:
                data.utm_mediums = AggregateStat.from_base_query(
                    page_view_base_query,
                    Event.utm_medium,
                    filter_none=True,
                )
            elif field == AnalyticsType.PAGEVIEWS_PER_DAY:
                data.pageviews_per_day = PageViewsPerDayStat.from_base_query(
                    base_query, start=start.datetime, end=end.datetime
                )
            elif field == AnalyticsType.LCP_PER_DAY:
                data.lcp_per_day = AvgMetricPerDayStat.from_base_query(
                    metric_base_query,
                    MetricType.LCP,
                    start=start.datetime,
                    end=end.datetime,
                )
            elif field == AnalyticsType.FID_PER_DAY:
                data.fid_per_day = AvgMetricPerDayStat.from_base_query(
                    metric_base_query,
                    MetricType.FID,
                    start=start.datetime,
                    end=end.datetime,
                )
            elif field == AnalyticsType.FP_PER_DAY:
                data.fp_per_day = AvgMetricPerDayStat.from_base_query(
                    metric_base_query,
                    MetricType.FP,
                    start=start.datetime,
                    end=end.datetime,
                )
            elif field == AnalyticsType.CLS_PER_DAY:
                data.cls_per_day = AvgMetricPerDayStat.from_base_query(
                    metric_base_query,
                    MetricType.CLS,
                    start=start.datetime,
                    end=end.datetime,
                )
            else:
                raise HTTPException(status_code=400)

        return data


event = CRUDEvent(Event)
