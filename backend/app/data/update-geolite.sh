#!/bin/bash -euo pipefail

if [ -z "$GEOIP_LICENSE_KEY" ]
then
    echo "Needs license key"
    exit 1
fi

# https://stackoverflow.com/a/246128
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

docker run --name geoip-updater \
    -e "EDITION_IDS=GeoLite2-ASN,GeoLite2-City,GeoLite2-Country" \
    -e "LICENSE_KEY=$GEOIP_LICENSE_KEY" \
    -e "DOWNLOAD_PATH=/data" \
    -e "LOG_LEVEL=info" \
    -e "LOG_JSON=false" \
    -v "${DIR}:/data" \
    crazymax/geoip-updater:latest

docker rm geoip-updater
