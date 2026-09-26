# -*- coding: utf-8 -*-
from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps

HERE = Path(__file__).resolve().parent
RAW = HERE / "assets" / "raw"
EDITED = HERE / "assets" / "edited"

BRAND_DARK = "#1C5B57"


def prep_photo(
    src_path: Path,
    dst_path: Path,
    brand_dark_hex: str,
    mode: str = "fullbleed",
    tint_strength: float = 0.16,
) -> Path:
    img = ImageOps.exif_transpose(Image.open(src_path).convert("RGB"))

    target_ratio = (1080 / 1350) if mode == "fullbleed" else (4 / 3)
    w, h = img.size
    if w / h > target_ratio:
        new_w = int(h * target_ratio)
        x0 = (w - new_w) // 2
        img = img.crop((x0, 0, x0 + new_w, h))
    else:
        new_h = int(w / target_ratio)
        y0 = (h - new_h) // 3
        img = img.crop((0, y0, w, y0 + new_h))

    max_dim = 1600
    if max(img.size) > max_dim:
        img.thumbnail((max_dim, max_dim), Image.LANCZOS)

    img = ImageEnhance.Contrast(img).enhance(1.05)
    img = ImageEnhance.Color(img).enhance(0.95)

    tint = Image.new("RGB", img.size, brand_dark_hex)
    img = Image.blend(img, tint, tint_strength)

    dst_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(dst_path, "JPEG", quality=85, optimize=True)
    return dst_path


prep_photo(RAW / "slide2-photo.jpg", EDITED / "slide2-photo.jpg", BRAND_DARK, mode="fullbleed", tint_strength=0.16)
prep_photo(RAW / "slide3-photo.jpg", EDITED / "slide3-photo.jpg", BRAND_DARK, mode="card", tint_strength=0.16)
print("prepped slide2-photo.jpg (fullbleed) and slide3-photo.jpg (card)")
