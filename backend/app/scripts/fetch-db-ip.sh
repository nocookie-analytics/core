#!/bin/bash -eou pipefail

curl https://download.db-ip.com/free/dbip-country-lite-2021-06.mmdb.gz -o /tmp/db-ip.mmdb.gz
gzip -d /tmp/db-ip.mmdb.gz
mkdir -p /app/backend/app/data/
mv /tmp/db-ip.mmdb /app/backend/app/data/db-ip-country.mmdb 
