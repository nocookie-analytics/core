from typing import Optional, Union

from geoip2.database import Reader
from geoip2.errors import AddressNotFoundError
from geoip2.models import Country
from pydantic.networks import IPvAnyAddress
from starlette.requests import Request

from app.core.config import settings
from app.logger import logger


def get_ip_gelocation(
    ip_address: Optional[Union[IPvAnyAddress, str]]
) -> Optional[Country]:
    if not ip_address:
        return None
    if isinstance(ip_address, IPvAnyAddress):
        ip_address = str(ip_address)
    try:
        country = MMDB_INSTANCE.country(str(ip_address))
        return country
    except AddressNotFoundError:
        return None


def get_ip_from_request(request: Request) -> str:
    if "x-real-ip" in request.headers:
        # Using this header blindly might be a security issue normally but it seems
        # that traefik will overwrite this header if an end user passes it
        return request.headers["x-real-ip"]
    elif "x-forwarded-for" in request.headers:
        forwarded_for = request.headers["x-forwarded-for"].split(",")
        return forwarded_for[-1]
    else:
        # This is a fallback, and most likely never accurate unless we're interacting
        # with the app directly without an intermediate proxy
        return request.client.host


try:
    MMDB_INSTANCE = Reader(settings.MMDB_PATH)
except FileNotFoundError:
    logger.error(
        "MMDB file not found in %s, you should run %s first",
        settings.MMDB_PATH,
        "scripts/fetch-db-ip.sh",
    )
