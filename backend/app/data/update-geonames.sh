#!/bin/bash

set -euo pipefail

# curl -s "https://download.geonames.org/export/dump/cities500.zip" -o /tmp/cities500.zip
zcat /tmp/cities500.zip
