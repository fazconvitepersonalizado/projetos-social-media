# -*- coding: utf-8 -*-
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "assets" / "raw"
RAW.mkdir(parents=True, exist_ok=True)


def download_photo(url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    dest.write_bytes(urllib.request.urlopen(req).read())
    return dest


download_photo(
    "https://images.pexels.com/photos/37198881/pexels-photo-37198881.jpeg?cs=srgb&dl=pexels-harrun-muhammad-116282236-37198881.jpg&fm=jpg",
    RAW / "slide2-photo.jpg",
)
download_photo(
    "https://images.pexels.com/photos/8487392/pexels-photo-8487392.jpeg?cs=srgb&dl=pexels-kindelmedia-8487392.jpg&fm=jpg",
    RAW / "slide3-photo.jpg",
)
print("downloaded slide2-photo.jpg and slide3-photo.jpg")
