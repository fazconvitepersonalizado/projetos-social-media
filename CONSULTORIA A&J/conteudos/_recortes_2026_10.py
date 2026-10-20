# -*- coding: utf-8 -*-
"""Recorta objetos de fotos em fundo liso (Pexels, licença livre) para os carrosséis de outubro/2026.
Remove só o fundo ligado à borda (preenchimento a partir das bordas), para não apagar partes claras
de dentro do objeto (ex.: a folha branca da prancheta). Original em assets/raw, PNG em assets/edited."""
import urllib.request
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

BASE = Path(__file__).resolve().parent

# pasta, nome, id Pexels, recorte prévio (x0, y0, x1, y1 em fração), tolerância
RECORTES = [
    ("2026-10-21-cipa-no-papel", "slide4-prancheta", 12039583, (0.25, 0.05, 0.75, 0.98), 22),
    # megafone (8846034) trocado por traço em 2026-10-20: corpo branco igual à parede, recorte pela cor falha
    ("2026-10-30-precisa-de-consultoria-sst", "slide2-pastas", 16978372, (0.0, 0.0, 1.0, 1.0), 40),
]


def baixar(pid, dest):
    if not dest.exists():
        url = f"https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg?auto=compress&cs=tinysrgb&w=1600"
        dest.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        dest.write_bytes(urllib.request.urlopen(req, timeout=60).read())
    return dest


def recortar(src, dst, caixa, tol):
    img = Image.open(src).convert("RGB")
    w, h = img.size
    img = img.crop((int(caixa[0] * w), int(caixa[1] * h), int(caixa[2] * w), int(caixa[3] * h)))
    img.thumbnail((1000, 1000), Image.LANCZOS)
    a = np.asarray(img).astype(np.int16)
    H, W, _ = a.shape
    borda = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    fundo = np.median(borda, axis=0)
    parecido = np.abs(a - fundo).max(axis=2) <= tol
    if tol >= 40:  # objeto escuro em fundo claro: todo pixel claro e sem cor ligado à borda é fundo (inclui a sombra)
        parecido |= (a.min(axis=2) > 150) & ((a.max(axis=2) - a.min(axis=2)) < 28)
    ligado = np.zeros((H, W), bool)
    fila = deque()
    for x in range(W):
        for y in (0, H - 1):
            if parecido[y, x] and not ligado[y, x]:
                ligado[y, x] = True; fila.append((y, x))
    for y in range(H):
        for x in (0, W - 1):
            if parecido[y, x] and not ligado[y, x]:
                ligado[y, x] = True; fila.append((y, x))
    while fila:
        y, x = fila.popleft()
        for yy, xx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
            if 0 <= yy < H and 0 <= xx < W and parecido[yy, xx] and not ligado[yy, xx]:
                ligado[yy, xx] = True; fila.append((yy, xx))
    alfa = Image.fromarray(np.where(ligado, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    out = img.convert("RGBA"); out.putalpha(alfa)
    out = out.crop(alfa.point(lambda v: 255 if v > 30 else 0).getbbox())
    dst.parent.mkdir(parents=True, exist_ok=True)
    out.save(dst, "PNG", optimize=True)
    return out.size


if __name__ == "__main__":
    for pasta, nome, pid, caixa, tol in RECORTES:
        d = BASE / pasta / "assets"
        raw = baixar(pid, d / "raw" / f"{nome}-pexels-{pid}.jpg")
        print(pasta, nome, recortar(raw, d / "edited" / f"{nome}.png", caixa, tol))
