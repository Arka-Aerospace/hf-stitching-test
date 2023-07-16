from pathlib import Path
from exif import Image
from math import inf

inp = Path("without/2023-06-28 12_16_44.096.jpg")
with open(inp, "rb") as f:
    my_image = Image(f)


lat = float(my_image.get("gps_latitude_ref"))
lon = float(my_image.get("gps_longitude_ref"))

min_dist = inf
min_path = None
for path in Path("with").glob("*.jpg"):
    with open(path, "rb") as f:
        im = Image(f)
    new_lat = float(im.get("gps_latitude_ref"))
    new_lon = float(im.get("gps_longitude_ref"))
    print(new_lat, lat)

    dist = (new_lat - lat)**2 + (new_lon - lon)**2
    print(dist)
    if dist < min_dist:
        min_dist = dist
        min_path = path

print(min_path)
print(min_dist)