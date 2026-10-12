
from pathlib import Path
import geopandas as gpd
import json

DATA_DIR = Path("data")

for path in sorted(DATA_DIR.glob("*.gpkg")):
    print("\n" + "=" * 80)
    print("FILE:", path.name)
    print("SIZE_GB:", round(path.stat().st_size / (1024**3), 3))

    try:
        layers = gpd.list_layers(path)
        print("LAYERS:")
        print(layers.to_string(index=False))

        for layer_name in layers["name"]:
            print("\nLAYER:", layer_name)
            try:
                # Read a small sample, not the entire multi-GB layer.
                sample = gpd.read_file(
                    path,
                    layer=layer_name,
                    rows=5
                )
                print("SAMPLE_COLUMNS:", list(sample.columns))
                print("DTYPES:", {
                    str(k): str(v)
                    for k, v in sample.dtypes.items()
                })
                print("CRS:", sample.crs)
                print("SAMPLE_GEOMETRY_TYPES:",
                      sample.geometry.geom_type.value_counts().to_dict()
                      if sample.geometry.name in sample.columns else {})
                print("SAMPLE_ROWS:")
                print(sample.drop(
                    columns="geometry", errors="ignore"
                ).head(3).to_string(index=False))

            except Exception as exc:
                print("LAYER_SAMPLE_ERROR:", repr(exc))

    except Exception as exc:
        print("FILE_ERROR:", repr(exc))
