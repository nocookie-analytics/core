#!/bin/bash -eou pipefail

curl -s https://download.db-ip.com/free/dbip-country-lite-2022-02.mmdb.gz -o /tmp/db-ip.mmdb.gz
gzip -d /tmp/db-ip.mmdb.gz
mv /tmp/db-ip.mmdb backend/app/data/db-ip-country.mmdb
