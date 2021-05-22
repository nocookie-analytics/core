import asyncio
import csv
import zipfile
from io import StringIO, TextIOWrapper

import requests
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models import Country

country_field_names = [
    "iso",
    "iso3",
    "iso-numeric",
    "fips",
    "country",
    "capital",
    "area(in sq km)",
    "population",
    "continent",
    "tld",
    "currencycode",
    "currencyname",
    "phone",
    "postal code format",
    "postal code regex",
    "languages",
    "geonameid",
    "neighbours",
    "equivalentfipscode",
]

import requests
import shutil


def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        with open(local_filename, "wb") as f:
            shutil.copyfileobj(r.raw, f)

    return local_filename


async def countries(db: Session):
    r = requests.get("https://download.geonames.org/export/dump/countryInfo.txt")
    data = r.text
    lines = data.split("\n")
    only_country_data = "\n".join(line for line in lines if line and line[0] != "#")
    for line in csv.DictReader(
        StringIO(only_country_data), delimiter="\t", fieldnames=country_field_names
    ):
        assert None not in line, "File format has changed"
        country = db.query(Country).get(line["iso"])
        if country:
            continue
        country = Country(id=line["iso"], name=line["country"])
        db.add(country)
        db.commit()


async def main():
    db = next(get_db())
    await countries(db)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
