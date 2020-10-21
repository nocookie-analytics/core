from psycopg2.extensions import register_adapter, AsIs
from pydantic.networks import IPv4Address, IPv6Address
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def adapt_pydantic_ip_address(ip):
    return AsIs(repr(ip.exploded))


register_adapter(IPv4Address, adapt_pydantic_ip_address)
register_adapter(IPv6Address, adapt_pydantic_ip_address)
