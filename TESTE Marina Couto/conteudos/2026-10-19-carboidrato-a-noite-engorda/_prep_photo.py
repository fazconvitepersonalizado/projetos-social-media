"""Tratamento das fotos do carrossel (receita de references/photo-sourcing.md).

Capa:   Pexels 34134206 (th2city), recorte 4:5, full-bleed.
Card 6: Unsplash jUPOXXRNdcA (Brooke Lark), recorte 4:3, foto emoldurada.
Escolha da cliente: fotos suaves/esmaecidas -> tinta de marca leve + véu creme.
"""
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

HERE = Path(__file__).resolve().parent
RAW = HERE / "assets" / "raw"
OUT = HERE / "assets" / "edited"
BRAND_DARK = "#2A4A5D"
LIGHT_BG = "#F4EEE3"


def prep(src, dst, mode, tint=0.10, veil=0.16):
    img = ImageOps.exif_transpose(Image.open(src).convert("RGB"))
    ratio = (1080 / 1350) if mode == "fullbleed" else (4 / 3)
    w, h = img.size
    if w / h > ratio:
        nw = int(h * ratio)
        x0 = (w - nw) // 2
        img = img.crop((x0, 0, x0 + nw, h))
    else:
        nh = int(w / ratio)
        y0 = (h - nh) // 3
        img = img.crop((0, y0, w, y0 + nh))
    img.thumbnail((1600, 1600), Image.LANCZOS)
    img = ImageEnhance.Contrast(img).enhance(1.04)
    img = ImageEnhance.Color(img).enhance(0.92)
    img = Image.blend(img, Image.new("RGB", img.size, BRAND_DARK), tint)
    img = Image.blend(img, Image.new("RGB", img.size, LIGHT_BG), veil)  # esmaecido
    OUT.mkdir(parents=True, exist_ok=True)
    img.save(OUT / dst, "JPEG", quality=85, optimize=True)
    print(dst, img.size)


prep(RAW / "capa-pexels-34134206.jpg", "capa.jpg", "fullbleed")
prep(RAW / "card6-unsplash-jUPOXXRNdcA.jpg", "card6.jpg", "card")
