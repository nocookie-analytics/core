#!/bin/bash -eou pipefail

# Filename has "year-month" format, parse the latest one first
version=$(curl -s https://db-ip.com/db/download/ip-to-country-lite | grep free_download_link | grep csv | grep -Eo '20..-..')
echo "Parsed version ${version}"
curl -s https://download.db-ip.com/free/dbip-country-lite-"${version}".mmdb.gz -o /tmp/db-ip.mmdb.gz
gzip -d /tmp/db-ip.mmdb.gz
mv /tmp/db-ip.mmdb backend/app/data/db-ip-country.mmdb
