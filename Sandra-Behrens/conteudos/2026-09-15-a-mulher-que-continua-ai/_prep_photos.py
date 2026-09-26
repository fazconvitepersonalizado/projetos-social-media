"""Prepara as fotos (crop, ajuste, tint de marca) para o carrossel 'A mulher que continua aí'."""
from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parent
BRAND_DARK = "#8B6C31"

def prep_photo(src_path: Path, dst_path: Path, mode: str = "fullbleed", tint_strength: float = 0.16) -> Path:
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

    tint = Image.new("RGB", img.size, BRAND_DARK)
    img = Image.blend(img, tint, tint_strength)

    dst_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(dst_path, "JPEG", quality=85, optimize=True)
    return dst_path

prep_photo(
    ROOT / "assets" / "raw" / "slide3-mulher-reencontro.jpg",
    ROOT / "assets" / "edited" / "slide3-mulher-reencontro.jpg",
    mode="fullbleed",
    tint_strength=0.14,
)
prep_photo(
    ROOT / "assets" / "raw" / "slide4-mao-caderno.jpg",
    ROOT / "assets" / "edited" / "slide4-mao-caderno.jpg",
    mode="card",
    tint_strength=0.12,
)
print("ok")
