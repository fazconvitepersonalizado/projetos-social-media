"""Baixa e prepara as fotos do carrossel 'Não precisa agradar todo mundo' (v2).
Slide 1: full-bleed (hero). Slide 2: framed card (pequena)."""
import urllib.request
from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "assets" / "raw"
EDITED = ROOT / "assets" / "edited"
BRAND_DARK = "#8B6C31"

PHOTOS = {
    "slide1-mulher-sorrindo.jpg": (
        "https://images.pexels.com/photos/7984828/pexels-photo-7984828.jpeg?cs=srgb&w=1600&q=80",
        "fullbleed",
    ),
    "slide2-mulher-pensativa.jpg": (
        "https://images.pexels.com/photos/8560801/pexels-photo-8560801.jpeg?cs=srgb&w=1600&q=80",
        "card",
    ),
}


def download_photo(url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    dest.write_bytes(urllib.request.urlopen(req).read())
    return dest


def prep_photo(src_path: Path, dst_path: Path, brand_dark_hex: str, mode: str = "fullbleed", tint_strength: float = 0.16) -> Path:
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


for fname, (url, mode) in PHOTOS.items():
    raw_path = download_photo(url, RAW / fname)
    print(f"baixado: {raw_path} ({raw_path.stat().st_size // 1024} KB)")
    tint = 0.14 if mode == "fullbleed" else 0.12
    dst = prep_photo(raw_path, EDITED / fname, BRAND_DARK, mode=mode, tint_strength=tint)
    print(f"editado ({mode}): {dst}")
