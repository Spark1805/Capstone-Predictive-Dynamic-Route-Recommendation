
from pathlib import Path
import geopandas as gpd
import re

data_dir = Path("data")

zones = {
    "south": "southern-zone-261002-free.gpkg",
    "central": "central-zone-261002-free.gpkg",
    "north": "northern-zone-261002-free.gpkg",
    "east": "eastern-zone-261002-free.gpkg",
    "west": "western-zone-261002-free.gpkg",
    "north-east": "north-eastern-zone-261002-free.gpkg",
}

def notebook_zone_match(filename):
    stem = Path(filename).stem.lower()
    for zone, expected in zones.items():
        normalized = re.sub(r"[^a-z]", "", stem)
        if Path(expected).stem.lower() in stem or zone.replace("-", "") in normalized:
            return zone
    return None

for path in sorted(data_dir.glob("*.gpkg")):
    print("\n" + "=" * 65)
    print("FILE:", path.name)
    print("NOTEBOOK ZONE MATCH:", notebook_zone_match(path.name))

    try:
        layers = gpd.list_layers(path)
        road_layers = layers[
            layers["name"].str.contains("roads", case=False, na=False)
        ]

        if road_layers.empty:
            print("ROAD LAYER: NOT FOUND")
            continue

        for layer_name in road_layers["name"]:
            # Read only zero rows to inspect the schema.
            schema = gpd.read_file(
                path, layer=layer_name, rows=0
            )
            columns = list(schema.columns)
            normalized = {
                re.sub(r"[^a-z0-9]+", "_", c.lower()).strip("_"): c
                for c in columns
            }

            timestamp_candidates = [
                "timestamp", "datetime", "date_time", "date", "time"
            ]
            speed_candidates = [
                "speed", "traffic_speed", "observed_speed", "measurement"
            ]
            road_id_candidates = [
                "osm_id", "osmid", "road_id", "edge_id", "id", "fid"
            ]

            def find(candidates):
                return next(
                    (normalized[c] for c in candidates if c in normalized),
                    None
                )

            print("ROAD LAYER:", layer_name)
            print("COLUMNS:", columns)
            print("ROAD ID FIELD:", find(road_id_candidates))
            print("TIMESTAMP FIELD:", find(timestamp_candidates))
            print("SPEED FIELD:", find(speed_candidates))

    except Exception as exc:
        print("AUDIT ERROR:", repr(exc))
