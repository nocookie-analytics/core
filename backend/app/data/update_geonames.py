import asyncio
import csv
import zipfile
from io import StringIO, TextIOWrapper

import requests
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models import City, Country

city_field_names = [
    "geonameid",
    "name",
    "asciiname",
    "alternatenames",
    "latitude",
    "longitude",
    "feature class",
    "feature code",
    "country code",
    "cc2",
    "admin1 code",
    "admin2 code",
    "admin3 code",
    "admin4 code",
    "population",
    "elevation",
    "dem",
    "timezone",
    "modification date",
]

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


async def cities(db: Session):
    url = "http://localhost:8002/cities500.zip"
    filename = "./cities500.zip"
    download_file(url, filename)
    with zipfile.ZipFile(filename, mode="r") as zipped:
        files = zipped.namelist()
        assert len(files) == 1
        unzipped_byte_stream = zipped.open(files[0])
        unzipped_text_stream = TextIOWrapper(unzipped_byte_stream)
        for index, line in enumerate(
            csv.DictReader(
                unzipped_text_stream, delimiter="\t", fieldnames=city_field_names
            )
        ):
            assert None not in line, "File format has changed"
            city = db.query(City).get(line["geonameid"])
            if city:
                continue
            city = City(
                id=line["geonameid"],
                name=line["name"],
                asciiname=line["asciiname"],
                latitude=line["latitude"],
                longitude=line["longitude"],
                country_id=line["country code"],
            )
            db.add(city)
            if index % 1000 == 0:
                db.commit()


async def main():
    db = next(get_db())
    await countries(db)
    await cities(db)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
