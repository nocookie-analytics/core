from geoip2.database import Reader
from pydantic.networks import IPvAnyAddress
from app.core.config import settings
from typing import Optional, Union
from geoip2.errors import AddressNotFoundError
from geoip2.models import City


def get_ip_gelocation(
    ip_address: Optional[Union[IPvAnyAddress, str]]
) -> Optional[City]:
    if not ip_address:
        return None
    if isinstance(ip_address, IPvAnyAddress):
        ip_address = str(ip_address)
    try:
        city = GEOLITE_INSTANCE.city(str(ip_address))
        return city
    except AddressNotFoundError:
        return None


GEOLITE_INSTANCE = Reader(settings.GEOLITE_PATH)
