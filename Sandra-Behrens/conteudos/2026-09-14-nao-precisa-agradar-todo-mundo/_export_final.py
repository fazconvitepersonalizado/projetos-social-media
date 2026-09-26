import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent
INPUT_HTML = ROOT / "carousel.html"
OUTPUT_DIR = ROOT / "SETEMBRO" / "CARD3"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TOTAL_SLIDES = 4
VIEW_W = 420
VIEW_H = 525
SCALE = 1080 / 420

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": VIEW_W, "height": VIEW_H}, device_scale_factor=SCALE)
        html = INPUT_HTML.read_text(encoding="utf-8")
        await page.set_content(html, wait_until="networkidle")
        await page.wait_for_timeout(3000)
        await page.evaluate("""() => {
            document.querySelectorAll('.ig-header,.ig-dots,.ig-actions,.ig-caption,#carousel-editor,#carousel-editor-script')
                .forEach(el => el && (el.style.display='none'));
            const frame = document.querySelector('.ig-frame');
            frame.style.cssText = 'width:420px;height:525px;max-width:none;border-radius:0;box-shadow:none;overflow:hidden;margin:0;';
            const viewport = document.querySelector('.carousel-viewport');
            viewport.style.cssText = 'width:420px;height:525px;aspect-ratio:unset;overflow:hidden;cursor:default;';
            document.body.style.cssText = 'padding:0;margin:0;display:block;overflow:hidden;';
            document.querySelector('.carousel-track').style.transition = 'none';
        }""")
        await page.wait_for_timeout(500)
        for i in range(TOTAL_SLIDES):
            await page.evaluate("(idx) => { document.querySelector('.carousel-track').style.transform = 'translateX(' + (-idx * 420) + 'px)'; }", i)
            await page.wait_for_timeout(400)
            out = OUTPUT_DIR / f"slide_{i+1}.png"
            await page.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": VIEW_W, "height": VIEW_H})
            print(f"{out} ({out.stat().st_size // 1024} KB)")
        await browser.close()

asyncio.run(main())
