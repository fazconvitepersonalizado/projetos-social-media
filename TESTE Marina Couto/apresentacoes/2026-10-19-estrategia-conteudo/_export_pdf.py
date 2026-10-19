"""Exporta a apresentação (project/slides/*.html) para PDF 1920x1080, uma página por slide.

Uso: python _export_pdf.py <pasta node_modules/@fontsource> [--png]
As imagens /_blob/<id> da versão online são trocadas pelos arquivos locais
da pasta da cliente; <aside> (notas) não aparece; <x-connector> vira seta.
"""
import asyncio
import json
import re
import sys
from pathlib import Path

from playwright.async_api import async_playwright

HERE = Path(__file__).resolve().parent
CLIENT = HERE.parents[1]
FS = Path(sys.argv[1])
PNG = "--png" in sys.argv

BLOBS = {
    "768dae270e9102c2aefa2506134ca3d6": CLIENT / "manual/img/01-jantar-caseiro.jpg",
    "dd9b7afe60cffa6760af96b90ce3e24a": CLIENT / "manual/img/07-feira.jpg",
    "bc04a8ee239104232082111bdb765e00": CLIENT / "manual/img/02-marmitas.jpg",
    "5daf2638a49c1b5f36bbde95320ff74c": CLIENT / "manual/img/06-bolo.jpg",
    "62b1c3e0d0f9050cc909d023c2c46904": CLIENT / "manual/img/08-cozinha-story.jpg",
    "819f239cea011c5aeb5684e899479083": CLIENT / "logo/logo-primary.svg",
    "81d2ca1213519b5729b0b37217d5e7c4": CLIENT / "logo/logo-white.svg",
}
FACES = [("Fraunces", "fraunces", [("400", "normal"), ("600", "normal"), ("400", "italic"), ("600", "italic")]),
         ("DM Sans", "dm-sans", [("400", "normal"), ("500", "normal"), ("700", "normal")]),
         ("DM Mono", "dm-mono", [("400", "normal"), ("500", "normal")])]
ARROW = ('<div style="flex:none;width:48px;display:flex;align-items:center;justify-content:center">'
         '<svg width="40" height="24" viewBox="0 0 40 24"><path d="M2 12h32M26 4l8 8-8 8" fill="none" '
         'stroke="#3D6A85" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></div>')

deck = json.loads((HERE / "project/deck.json").read_text(encoding="utf-8"))
sections = []
for sid in deck["order"]:
    s = (HERE / "project/slides" / f"{sid}.html").read_text(encoding="utf-8")
    s = re.sub(r"<aside>.*?</aside>", "", s, flags=re.S)
    s = re.sub(r"<x-connector[^>]*></x-connector>", ARROW, s)
    s = re.sub(r"/_blob/([0-9a-f]{32})", lambda m: BLOBS[m.group(1)].as_uri(), s)
    sections.append(s)

faces = "".join(
    f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:{st};'
    f'src:url("{(FS / d / "files" / f"{d}-latin-{w}-{st}.woff2").as_uri()}") format("woff2");}}'
    for fam, d, fl in FACES for w, st in fl)
css = faces + """
@page { size: 1920px 1080px; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
section { position: relative; width: 1920px; height: 1080px; overflow: hidden; break-after: page; }
section:last-child { break-after: auto; }
h1, h2, h3, p, ul, ol { margin: 0; }
ul { padding-left: 1.2em; }
table { width: 100%; border-collapse: collapse; padding: 0 !important; }
th, td { text-align: left; padding: 20px; border-bottom: 1px solid #D9CDB8; }
th { font-weight: 700; border-bottom: 2px solid #2E2A25; }
"""
html = f"<!doctype html><meta charset='utf-8'><style>{css}</style>" + "\n".join(sections)
tmp = HERE / "_print.html"
tmp.write_text(html, encoding="utf-8")


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1920, "height": 1080})
        await pg.goto(tmp.as_uri())
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(800)
        out = HERE / "apresentacao-estrategia-marina-couto.pdf"
        await pg.pdf(path=str(out), width="1920px", height="1080px", print_background=True,
                     margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        print("pdf", out.name, out.stat().st_size // 1024, "KB,", len(sections), "slides")
        if PNG:
            shots = Path(sys.argv[sys.argv.index("--png") + 1])
            shots.mkdir(parents=True, exist_ok=True)
            for i in range(len(sections)):
                await pg.screenshot(path=str(shots / f"p{i + 1:02d}.png"),
                                    clip={"x": 0, "y": i * 1080, "width": 1920, "height": 1080}, full_page=True)
        await b.close()
    tmp.unlink()

asyncio.run(main())
