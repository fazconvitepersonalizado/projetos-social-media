"""Gera assinatura (wordmark) e monograma da Marina Couto em SVG, com o texto
convertido em contorno (não depende da fonte instalada).

Uso: python _build_logos.py <pasta-node_modules/@fontsource>
Saída: ../logo/ (variantes por cor)
"""
import sys
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FS = Path(sys.argv[1])
OUT = Path(__file__).resolve().parent.parent / "logo"
OUT.mkdir(exist_ok=True)

FRAUNCES = TTFont(FS / "fraunces/files/fraunces-latin-400-normal.woff2")
FRAUNCES_IT = TTFont(FS / "fraunces/files/fraunces-latin-400-italic.woff2")
MONO = TTFont(FS / "dm-mono/files/dm-mono-latin-500-normal.woff2")

COLORS = {
    "grafite": "#2E2A25",
    "creme": "#F4EEE3",
    "azul-claro": "#9EC3DA",     # cor principal (fundos/blocos; texto grafite por cima)
    "azul-profundo": "#3D6A85",  # azul como texto/traço sobre creme (contraste 5:1)
}
# 2026-10-19: cliente escolheu Azul Claro (fora das opções oliva/terracota do
# briefing). Azul claro não tem contraste como texto sobre creme, então a
# parte colorida da assinatura usa o Azul Profundo.


def text_path(font, text, size, x, y, tracking=0.0):
    """Path SVG do texto com baseline em y. Retorna (d, largura)."""
    upm = font["head"].unitsPerEm
    scale = size / upm
    cmap = font.getBestCmap()
    gs = font.getGlyphSet()
    hmtx = font["hmtx"]
    pen = SVGPathPen(gs)
    cx = x
    for ch in text:
        name = cmap.get(ord(ch))
        if name is None:
            cx += size * 0.3
            continue
        tpen = TransformPen(pen, (scale, 0, 0, -scale, cx, y))
        gs[name].draw(tpen)
        cx += hmtx[name][0] * scale + tracking * size
    width = cx - x - (tracking * size if text else 0)
    return pen.getCommands(), width


def measure(font, text, size, tracking=0.0):
    return text_path(font, text, size, 0, 0, tracking)[1]


def wordmark(color_main, color_accent):
    size = 96
    w1 = measure(FRAUNCES, "Marina ", size)
    w2 = measure(FRAUNCES_IT, "Couto", size)
    total = w1 + w2
    sub_size, sub_track = 22, 0.32
    wsub = measure(MONO, "NUTRICIONISTA", sub_size, sub_track)
    W = max(total, wsub) + 40
    x0 = (W - total) / 2
    d1, _ = text_path(FRAUNCES, "Marina ", size, x0, 100)
    d2, _ = text_path(FRAUNCES_IT, "Couto", size, x0 + w1, 100)
    d3, _ = text_path(MONO, "NUTRICIONISTA", sub_size, (W - wsub) / 2, 158, sub_track)
    H = 180
    return W, H, (
        f'<path d="{d1}" fill="{color_main}"/>'
        f'<path d="{d2}" fill="{color_accent}"/>'
        f'<path d="{d3}" fill="{color_main}"/>'
    )


def monogram(color_main, color_accent):
    size = 230
    wm = measure(FRAUNCES, "M", size)
    wc = measure(FRAUNCES_IT, "C", size)
    overlap = size * 0.04
    total = wm + wc - overlap
    W = H = 400
    x0 = (W - total) / 2
    base = 282
    dm, _ = text_path(FRAUNCES, "M", size, x0, base)
    dc, _ = text_path(FRAUNCES_IT, "C", size, x0 + wm - overlap, base)
    return W, H, f'<path d="{dm}" fill="{color_main}"/><path d="{dc}" fill="{color_accent}"/>'


def write(name, W, H, body):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" '
           f'width="{W:.0f}" height="{H:.0f}">{body}</svg>')
    (OUT / name).write_text(svg, encoding="utf-8")


write("logo-primary.svg", *wordmark(COLORS["grafite"], COLORS["azul-profundo"]))
write("monograma-primary.svg", *monogram(COLORS["grafite"], COLORS["azul-profundo"]))
# Variantes de cor única (não dependem da cor escolhida)
write("logo-dark.svg", *wordmark(COLORS["grafite"], COLORS["grafite"]))
write("logo-white.svg", *wordmark(COLORS["creme"], COLORS["creme"]))
write("monograma-dark.svg", *monogram(COLORS["grafite"], COLORS["grafite"]))
write("monograma-white.svg", *monogram(COLORS["creme"], COLORS["creme"]))
print("ok:", sorted(p.name for p in OUT.glob("*.svg")))
