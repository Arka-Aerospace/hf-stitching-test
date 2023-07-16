from lightglue import LightGlue, SuperPoint, DISK, match_pair
from lightglue.utils import load_image
import cv2
import numpy as np
import imutils
from skimage.metrics import structural_similarity as compare_ssim
from pathlib import Path
from exif import Image
from typing import Tuple, Union


key_image = Path("with2.jpg")
query_dir = Path("/home/orin-arka/Downloads/Without_Fod-20230708T122532Z-001 (1)/Without_Fod")

def get_lat_lon(img_path: Path, in_float=False) -> Union[Tuple[int, int], Tuple[float, float]]:
    with open(img_path, "rb") as f:
        im = Image(f)
    lat = int(str(im.get("gps_latitude_ref")).replace(".", "").ljust(9, "0")) if not in_float else im.get("gps_latitude_ref") 
    lon = int(str(im.get("gps_longitude_ref")).replace(".", "").ljust(9, "0")) if not in_float else im.get("gps_longitude_ref")

    return lat, lon

def get_sqr_distance(lat_lon1: Union[Tuple[int, int], Tuple[float, float]], lat_lon2: Union[Tuple[int, int], Tuple[float, float]]) -> Union[int, float]:
    return (lat_lon1[0] - lat_lon2[0])**2 + (lat_lon1[1] - lat_lon2[1])**2

key_lat_lon = get_lat_lon(key_image)
query_images = sorted(query_dir.glob("*.jpg"), key= lambda n: get_sqr_distance(key_lat_lon, get_lat_lon(n)))[:25]

MATCHES_THRESHOLD = 110

# SuperPoint+LightGlue
extractor = SuperPoint(max_num_keypoints=1024).eval().cuda()  # load the extractor
matcher = LightGlue(features='superpoint', filter_confidence=0.5, depth_confidence=0.9, width_confidence=0.95).eval().cuda()  # load the matcher
image0 = load_image(Path(key_image)).cuda()

target_img = Path("without2.jpg")
print(get_lat_lon(key_image, in_float=True))
print(get_lat_lon(target_img, in_float=True))
# for query_image in query_images:
#     print("----------------")
#     print(get_lat_lon(key_image, in_float=True))
#     print(get_lat_lon(query_image, in_float=True))
#     try:
#         image1 = load_image(Path(query_image)).cuda()
#         feats0, feats1, matches01 = match_pair(extractor, matcher, image0, image1)
#     except KeyboardInterrupt:
#         exit() 
#     except:
#         continue
#     matches = matches01['matches']  # type: ignore
#     if matches.shape[0] > MATCHES_THRESHOLD:
#         img2_color = cv2.imread(str(query_image))
#         print(query_image, "- hit")
#         cv2.imshow("query matched", img2_color)
#         while cv2.waitKey(0) != 27:
#             pass
#     else:
#         print(query_image, "- miss")
        

# cv2.destroyAllWindows() 