from geoip2.database import Reader
from app.core.config import settings
from typing import Optional
from geoip2.errors import AddressNotFoundError
from geoip2.models import City


def get_ip_gelocation(ip_address: str) -> Optional[City]:
    try:
        city = GEOLITE_INSTANCE.city(ip_address)
        return city
    except AddressNotFoundError:
        return None


GEOLITE_INSTANCE = Reader(settings.GEOLITE_PATH)
