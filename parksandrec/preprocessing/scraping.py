import json
import httpx
from pathlib import Path
import time

DATA_DIR = Path(__file__).parent.parent.parent
CACHE_DIR = Path(__file__).parent / "_cache"
START_URL = "https://services5.arcgis.com/LcMXE3TFhi1BSaCY/arcgis/rest/services/Land_Use_Inventory_for_Northeast_Illinois_2013_v2/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"
ALLOWED_CHARS = "abcdefghijklmnopqrstuvwxyz1234567890%+,^=._"


def get_lui_data(page_url):
    """
    Deprecated

    Query geojson records of land use inventoried parcels for 2013

    Inputs:
        page_url

    Returns:
        response(string): string element containing 2000 land use records

    """
    cache_directory = CACHE_DIR
    cache_directory.mkdir(exist_ok=True)

    lower_url = page_url.lower()
    short_url = lower_url.replace("https://", "")
    cache_key = "".join(char if char in ALLOWED_CHARS else "_" for char in short_url)

    page_path = Path(CACHE_DIR / cache_key)

    if page_path.exists():
        with open(page_path, "r") as cached_file:
            cached_response = cached_file.read()
            return cached_response

    response = httpx.get(page_url, follow_redirects=True, timeout=None)

    if response.status_code == 200:
        page_path.write_text(response.text)
        return response.text


def write_geojson(filename, record_count=0, max_records=100000):
    """
    Build geojson data base via page iteration of API queries containing
    records of land use parcels for 2013.

    Input:
        filename: Desired file name for geojson output
        record_count: initial parameter for pagination
        max_records: record limit to prevent memory issues


    Returns:
        None. Creates geojson file in local directory.

    """
    assert record_count < max_records

    features = []
    if record_count == 0:
        page_url = START_URL
    else:
        page_url = f"{START_URL}&resultOffset={record_count}"

    geojson_file = DATA_DIR / f"{filename}.geojson"

    while record_count < max_records:
        time.sleep(0.5)
        page = json.loads(get_lui_data(page_url))

        features.extend(page["features"])

        record_count += len(page["features"])
        page_url = f"{START_URL}&resultOffset={record_count}"

        if record_count == 509803:
            break

    with open(geojson_file, "w") as file:
        lui_geojson = {
            "type": "FeatureCollection",
            "name": "2013_Land_Use_Inventory_for_Northeastern_Illinois",
            "features": features,
            "crs": {
                "type": "name",
                "properties": {"name": "urn:ogc:def:crs:EPSG::3435"},
            },
        }

        json.dump(lui_geojson, file, indent=4)

    return None
