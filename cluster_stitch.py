from pathlib import Path
from typing import Tuple, Dict, List
from exif import Image

GRID_LAT_COUNT = 20
GRID_LON_COUNT = 20

image_dir = Path("with")

def get_lat_lon(img_path: Path) -> Tuple[int, int]:
    with open(img_path, "rb") as f:
        im = Image(f)
    lat = int(str(im.get("gps_latitude_ref")).replace(".", "").ljust(9, "0"))
    lon = int(str(im.get("gps_longitude_ref")).replace(".", "").ljust(9, "0"))

    return lat, lon

bins: Dict[Tuple[int, int], List[Path]] = {}


imgs: Dict[Path, Tuple[int, int]] = {}

for img_path in image_dir.glob("*.jpg"):
    lat, lon = get_lat_lon(img_path)
    if lat == 0 or lon == 0:
        continue
    imgs[img_path] = lat, lon

min_lat = imgs[min(imgs, key=lambda k: imgs[k][0])][0]
max_lat = imgs[max(imgs, key=lambda k: imgs[k][0])][0]

min_lon = imgs[min(imgs, key=lambda k: imgs[k][1])][1]
max_lon= imgs[max(imgs, key=lambda k: imgs[k][1])][1]


cell_lat_length = (max_lat - min_lat) / GRID_LAT_COUNT
cell_lon_length = (max_lon - min_lon) / GRID_LON_COUNT 

def get_bin(lat: int, lon: int) -> Tuple[int, int]:
    return round((lat - min_lat) / cell_lat_length), round((lon - min_lon) / cell_lon_length)

for img, (lat, lon) in imgs.items():
    bins.setdefault(get_bin(lat, lon), []).append(img)
