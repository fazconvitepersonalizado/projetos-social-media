"""Tratamento das fotos novas do TESTE anti-IA (escolha: fotos vívidas).

Card 3: Pexels 32577115, recorte 4:5 full-bleed (mulher ajoelhada na geladeira à noite).
Card 4: Pexels 19781592, recorte 420x270 para foto dividindo o slide (arroz, feijão, carne, salada).
Vívida = só ajuste leve de contraste e tinta de marca bem fraca, sem véu creme.
"""
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

HERE = Path(__file__).resolve().parent
RAW, OUT = HERE / "assets" / "raw", HERE / "assets" / "edited"
BRAND_DARK = "#2A4A5D"


def prep(src, dst, ratio, y_frac=0.5, tint=0.05):
    img = ImageOps.exif_transpose(Image.open(RAW / src).convert("RGB"))
    w, h = img.size
    if w / h > ratio:
        nw = int(h * ratio)
        x0 = (w - nw) // 2
        img = img.crop((x0, 0, x0 + nw, h))
    else:
        nh = int(w / ratio)
        y0 = int((h - nh) * y_frac)
        img = img.crop((0, y0, w, y0 + nh))
    img.thumbnail((1600, 1600), Image.LANCZOS)
    img = ImageEnhance.Contrast(img).enhance(1.05)
    img = Image.blend(img, Image.new("RGB", img.size, BRAND_DARK), tint)
    OUT.mkdir(parents=True, exist_ok=True)
    img.save(OUT / dst, "JPEG", quality=85, optimize=True)
    print(dst, img.size)


prep("card3-pexels-32577115.jpg", "card3.jpg", 1080 / 1350, y_frac=0.55)
prep("card4-pexels-19781592.jpg", "card4.jpg", 420 / 270)
