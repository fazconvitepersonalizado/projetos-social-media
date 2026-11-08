# -*- coding: utf-8 -*-
"""Baixa e trata as fotos de novembro/2026 da Sandra (Pexels, licença livre, escolhidas pelo Thiago em 2026-11-08).
Opacidade "suave": saturação e contraste um pouco abaixo, leve tinta no dourado escuro da marca.
Original em <pasta>/assets/raw, editado em <pasta>/assets/edited."""
import json
import urllib.request
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

BASE = Path(__file__).resolve().parent
BRAND_DARK = json.loads((BASE.parent / "brand-kit.json").read_text(encoding="utf-8"))["derived"]["BRAND_DARK"]

# pasta, arquivo, id Pexels, proporção final (w/h), foco vertical, foco horizontal, tinta
FOTOS = [
    ("2026-11-12-mandalaterapia", "slide1-dividida", 7181612, 420 / 300, 0.42, 0.5, 0.10),
    ("2026-11-14-menopausa-nao-se-reconhecem", "slide1-full", 6874398, 1080 / 1350, 0.30, 0.30, 0.12),
    ("2026-11-14-menopausa-nao-se-reconhecem", "slide7-full", 5473066, 1080 / 1350, 0.25, 0.45, 0.12),
    ("2026-11-17-voce-cuida-de-todos", "post-card", 6874522, 4 / 3, 0.5, 0.5, 0.08),
    ("2026-11-19-cores-da-mandala", "slide3-card", 7181600, 1.0, 0.5, 0.5, 0.0),
    ("2026-11-24-menopausa-e-autoestima", "slide1-recortada", 6874412, 4 / 5, 0.30, 0.92, 0.10),
    ("2026-11-24-menopausa-e-autoestima", "slide3-card", 10221832, 4 / 3, 0.35, 0.5, 0.10),
    ("2026-11-26-nao-precisa-dar-conta-de-tudo", "slide1-recortada", 6874521, 4 / 5, 0.40, 0.5, 0.10),
    ("2026-11-26-nao-precisa-dar-conta-de-tudo", "slide5-card", 1115692, 4 / 3, 0.5, 0.5, 0.10),
    ("2026-11-28-envelhecer-novas-versoes", "slide1-full", 8417222, 1080 / 1350, 0.5, 0.62, 0.12),
    ("2026-11-28-envelhecer-novas-versoes", "slide6-full", 8829200, 1080 / 1350, 0.3, 0.5, 0.12),
]


def baixar(pid: int, dest: Path) -> Path:
    if dest.exists():
        return dest
    url = f"https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg?auto=compress&cs=tinysrgb&w=1800"
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    dest.write_bytes(urllib.request.urlopen(req, timeout=60).read())
    return dest


def tratar(src: Path, dst: Path, ratio: float, fy: float, fx: float, tint: float) -> Path:
    img = ImageOps.exif_transpose(Image.open(src).convert("RGB"))
    w, h = img.size
    if w / h > ratio:
        nw = int(h * ratio)
        x0 = int((w - nw) * fx)
        img = img.crop((x0, 0, x0 + nw, h))
    else:
        nh = int(w / ratio)
        y0 = int((h - nh) * fy)
        img = img.crop((0, y0, w, y0 + nh))
    if max(img.size) > 1600:
        img.thumbnail((1600, 1600), Image.LANCZOS)
    img = ImageEnhance.Contrast(img).enhance(0.97)
    img = ImageEnhance.Color(img).enhance(0.86)
    img = ImageEnhance.Brightness(img).enhance(1.03)
    if tint:
        img = Image.blend(img, Image.new("RGB", img.size, BRAND_DARK), tint)
    dst.parent.mkdir(parents=True, exist_ok=True)
    img.save(dst, "JPEG", quality=85, optimize=True)
    return dst


if __name__ == "__main__":
    for pasta, nome, pid, ratio, fy, fx, tint in FOTOS:
        d = BASE / pasta / "assets"
        raw = baixar(pid, d / "raw" / f"{nome}-pexels-{pid}.jpg")
        out = tratar(raw, d / "edited" / f"{nome}.jpg", ratio, fy, fx, tint)
        print(pasta, nome, Image.open(raw).size, "->", Image.open(out).size)
