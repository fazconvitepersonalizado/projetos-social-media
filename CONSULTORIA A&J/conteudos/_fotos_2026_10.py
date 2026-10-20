# -*- coding: utf-8 -*-
"""Baixa e trata as fotos dos carrosséis de outubro/2026 (Pexels, licença livre)."""
import urllib.request
from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps

BASE = Path(__file__).resolve().parent
BRAND_DARK = "#1C5B57"

# pasta, arquivo, id Pexels, proporção final (w/h), foco vertical (0 topo .. 1 base), foco horizontal, tinta
FOTOS = [
    ("2026-10-21-cipa-no-papel", "slide7-photo", 8961064, 420 / 250, 0.30, 0.55, 0.12),
    ("2026-10-23-quase-acidente", "slide1-photo", 5498025, 4 / 3, 0.45, 0.50, 0.12),
    ("2026-10-26-dds-que-a-equipe-escuta", "slide1-photo", 35082106, 420 / 255, 0.25, 0.65, 0.12),
    ("2026-10-26-dds-que-a-equipe-escuta", "slide2-photo", 30179842, 1080 / 1350, 0.20, 0.55, 0.12),
    ("2026-10-26-dds-que-a-equipe-escuta", "slide8-photo", 8961259, 1080 / 1350, 0.45, 0.45, 0.12),
    ("2026-10-28-outubro-rosa-na-empresa", "slide1-photo", 8385421, 4 / 3, 0.50, 0.45, 0.06),
    ("2026-10-28-outubro-rosa-na-empresa", "slide3-photo", 8487402, 210 / 525, 0.30, 0.50, 0.12),
    ("2026-10-30-precisa-de-consultoria-sst", "slide3-photo", 8293680, 4 / 3, 0.45, 0.55, 0.12),
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
    img = ImageEnhance.Contrast(img).enhance(1.05)
    img = ImageEnhance.Color(img).enhance(0.95)
    img = Image.blend(img, Image.new("RGB", img.size, BRAND_DARK), tint)
    dst.parent.mkdir(parents=True, exist_ok=True)
    img.save(dst, "JPEG", quality=85, optimize=True)
    return dst


if __name__ == "__main__":
    for pasta, nome, pid, ratio, fy, fx, tint in FOTOS:
        d = BASE / pasta / "assets"
        raw = baixar(pid, d / "raw" / f"{nome}-pexels-{pid}.jpg")
        out = tratar(raw, d / "edited" / f"{nome}.jpg", ratio, fy, fx, tint)
        print(pasta, nome, Image.open(out).size)
