"""Baixa e prepara as fotos do carrossel 'Nem todo silêncio é vazio' (Sandra Behrens)."""
import json
import urllib.request
from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent.parent

brand = json.loads((PROJECT_ROOT / "brand-kit.json").read_text(encoding="utf-8"))
BRAND_DARK = brand["derived"]["BRAND_DARK"]

PHOTOS = [
    {
        "url": "https://images.pexels.com/photos/6874398/pexels-photo-6874398.jpeg?cs=srgb&dl=pexels-teona-swift-6874398.jpg&fm=jpg",
        "raw": "slide3-mulher-janela.jpg",
        "edited": "slide3-mulher-janela.jpg",
        "mode": "card",
        "credit": "pexels.com/photo/wistful-mature-woman-looking-out-window-6874398 (Teona Swift)",
    },
    {
        "url": "https://images.pexels.com/photos/11284054/pexels-photo-11284054.jpeg?cs=srgb&dl=pexels-centre-for-ageing-better-55954677-11284054.jpg&fm=jpg",
        "raw": "slide5-mulher-parque.jpg",
        "edited": "slide5-mulher-parque.jpg",
        "mode": "fullbleed",
        "credit": "pexels.com/photo/happy-woman-walking-through-park-11284054 (Centre for Ageing Better)",
    },
]


def download_photo(url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    dest.write_bytes(urllib.request.urlopen(req).read())
    return dest


def prep_photo(src_path: Path, dst_path: Path, brand_dark_hex: str, mode: str, tint_strength: float = 0.16) -> Path:
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


for p in PHOTOS:
    raw_path = ROOT / "assets" / "raw" / p["raw"]
    edited_path = ROOT / "assets" / "edited" / p["edited"]
    download_photo(p["url"], raw_path)
    prep_photo(raw_path, edited_path, BRAND_DARK, p["mode"])
    print(f"ok: {p['edited']}  <-  {p['credit']}")
