"""Exporta um carrossel HTML para PNGs 1080x1350.

Uso:
    python export_carousel.py <pasta-do-carrossel> [--slides N]

Exemplo:
    python export_carousel.py conteudos/2026-05-14-5-dicas-claude-code
    python export_carousel.py conteudos/2026-05-14-5-dicas-claude-code --slides 7

A pasta deve conter `slides/carousel.html` (ou `carousel.html` na raiz da pasta).
Os PNGs são gravados em `<pasta>/slides/slide_N.png`.
"""
import argparse
import asyncio
import sys
from pathlib import Path

from playwright.async_api import async_playwright

VIEW_W = 420
VIEW_H = 525
SCALE = 1080 / 420  # -> 1080x1350


def resolve_html(carousel_dir: Path) -> Path:
    candidates = [
        carousel_dir / "slides" / "carousel.html",
        carousel_dir / "carousel.html",
    ]
    for c in candidates:
        if c.exists():
            return c
    raise FileNotFoundError(
        f"carousel.html não encontrado em {carousel_dir} "
        f"(procurei em slides/carousel.html e carousel.html)"
    )


async def export_slides(carousel_dir: Path, total_slides: int) -> None:
    input_html = resolve_html(carousel_dir)
    output_dir = carousel_dir / "slides"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Exportando de {input_html}")
    print(f"Saída: {output_dir}")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": VIEW_W, "height": VIEW_H},
            device_scale_factor=SCALE,
        )

        html = input_html.read_text(encoding="utf-8")
        await page.set_content(html, wait_until="networkidle")
        await page.wait_for_timeout(3000)  # Google Fonts

        await page.evaluate("""
        () => {
          const vp = document.querySelector('.ig-viewport');
          document.body.innerHTML = '';
          document.body.appendChild(vp);
          document.body.style.cssText = 'padding:0;margin:0;display:block;overflow:hidden;background:#000;';
          vp.style.cssText = 'position:relative;width:420px;height:525px;overflow:hidden;background:#000;';
          const track = document.querySelector('.ig-track');
          track.style.transition = 'none';
        }
        """)
        await page.wait_for_timeout(500)

        for i in range(total_slides):
            await page.evaluate(
                "(idx) => { document.querySelector('.ig-track').style.transform = "
                "'translateX(' + (-idx * 420) + 'px)'; }",
                i,
            )
            await page.wait_for_timeout(300)
            out = output_dir / f"slide_{i + 1}.png"
            await page.screenshot(
                path=str(out),
                clip={"x": 0, "y": 0, "width": VIEW_W, "height": VIEW_H},
            )
            print(f"  {out.name}  ({out.stat().st_size // 1024} KB)")

        await browser.close()

    print("Pronto.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Exporta carrossel HTML para PNGs 1080x1350.")
    parser.add_argument("carousel_dir", type=Path, help="Pasta do carrossel (ex: conteudos/2026-05-14-tema)")
    parser.add_argument("--slides", type=int, default=7, help="Quantidade de slides (default: 7)")
    args = parser.parse_args()

    if not args.carousel_dir.exists():
        print(f"Erro: pasta não existe: {args.carousel_dir}", file=sys.stderr)
        return 1

    asyncio.run(export_slides(args.carousel_dir, args.slides))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
