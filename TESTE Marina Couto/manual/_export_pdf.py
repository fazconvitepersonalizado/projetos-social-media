"""Exporta manual-marina-couto.html para PDF (1280x1810, fontes locais embutidas).
Uso: python _export_pdf.py <pasta node_modules/@fontsource>"""
import asyncio, sys
from pathlib import Path
from playwright.async_api import async_playwright

HERE = Path(__file__).resolve().parent
FS = Path(sys.argv[1])
FACES = [("Source Serif 4", "source-serif-4", [("400", "normal"), ("600", "normal"), ("400", "italic"), ("600", "italic")]),
         ("DM Sans", "dm-sans", [("400", "normal"), ("500", "normal"), ("700", "normal")]),
         ("DM Mono", "dm-mono", [("400", "normal"), ("500", "normal")])]
css = "".join(
    f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:{st};'
    f'src:url("{(FS / d / "files" / f"{d}-latin-{w}-{st}.woff2").as_uri()}") format("woff2");}}'
    for fam, d, fl in FACES for w, st in fl)
css += "section{padding-block:64px!important} .cover{padding-block:48px!important}"


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1280, "height": 1810})
        await pg.route("**/fonts.googleapis.com/**", lambda r: r.abort())
        await pg.goto((HERE / "manual-marina-couto.html").as_uri())
        await pg.add_style_tag(content=css)
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(500)
        out = HERE / "manual-marina-couto.pdf"
        await pg.pdf(path=str(out), width="1280px", height="1810px", print_background=True,
                     margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        await b.close()
        print("pdf", out.stat().st_size // 1024, "KB")

asyncio.run(main())
