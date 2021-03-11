import sys
import json


# Usage: python backend/app/data/update-geojson.py custom.json frontend/src/components/data/world.geo.json
# Input file from https://geojson-maps.ash.ms/

# TODO: Use topojson/world-atlas: https://github.com/topojson/world-atlas/ for smaller JSON files


def main():
    input_file, output_file = sys.argv[1], sys.argv[2]

    # keys_to_keep = set("admin,name,formal_en,iso_a2,continent".split())
    keys_to_keep = set("name,iso_a2".split(","))
    with open(input_file) as f:
        data = json.load(f)
        for feature in data["features"]:
            feature["properties"] = {
                k: v for k, v in feature["properties"].items() if k in keys_to_keep
            }
    with open(output_file, "w") as of:
        json.dump(data, of)


if __name__ == "__main__":
    main()
