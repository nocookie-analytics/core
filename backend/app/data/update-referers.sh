#!/bin/bash -euo pipefail

# The data source of this script is here:
# https://github.com/snowplow-referer-parser/referer-parser

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

curl -s https://s3-eu-west-1.amazonaws.com/snowplow-hosted-assets/third-party/referer-parser/referers-latest.json -o referers.json
