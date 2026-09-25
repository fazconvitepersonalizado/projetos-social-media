# Exporting Slides as Instagram-Ready PNGs

> All technical rules below are **verbatim** from the original skill. The only
> additions are project-level path conventions (input/output locations).

## Project path conventions

- Input HTML: `conteudos/<YYYY-MM-DD>-<slug>/carousel.html` (clean — without edit panel)
- Output PNGs: `conteudos/<YYYY-MM-DD>-<slug>/slides/slide_1.png` … `slide_N.png`
- `<slug>` is a kebab-case slug derived from the carousel topic, lowercase, ASCII, no accents.

Use absolute paths in the Python script. Build them from the project root:

```python
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # adjust as needed
CAROUSEL_DIR = PROJECT_ROOT / "conteudos" / "<YYYY-MM-DD>-<slug>"
INPUT_HTML   = CAROUSEL_DIR / "carousel.html"
OUTPUT_DIR   = CAROUSEL_DIR / "slides"
```

---

After the user approves the carousel preview, export each slide as an individual **1080×1350px PNG**.

### Critical Export Rules

1. **Use Python for HTML generation** — never use shell scripts with variable interpolation. Always use `Path.write_text()` or `open().write()`.

2. **Embed images as base64** — all user-uploaded images must be base64-encoded as `data:image/jpeg;base64,...` URIs. Check actual file format with the `file` command — a `.png` extension may contain a JPEG.

3. **Keep the 420px layout width** — use Playwright's `device_scale_factor` to scale up to 1080px output WITHOUT changing the layout viewport.

### Install Playwright (only if needed)

Before running the export script, check and install only if missing:

```bash
python3 -c "import playwright" 2>/dev/null || pip3 install playwright
python3 -c "from playwright.sync_api import sync_playwright; sync_playwright().__enter__().chromium" 2>/dev/null || python3 -m playwright install chromium
```

### Export Script

```python
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

INPUT_HTML = Path("/path/to/carousel.html")
OUTPUT_DIR = Path("/path/to/output/slides")
OUTPUT_DIR.mkdir(exist_ok=True)

TOTAL_SLIDES = 7  # Update to match your carousel

VIEW_W = 420
VIEW_H = 525
SCALE = 1080 / 420  # = 2.5714...

async def export_slides():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": VIEW_W, "height": VIEW_H},
            device_scale_factor=SCALE,
        )

        html_content = INPUT_HTML.read_text(encoding="utf-8")
        await page.set_content(html_content, wait_until="networkidle")
        await page.wait_for_timeout(3000)  # Wait for Google Fonts to load

        # Hide IG frame chrome, show only the slide viewport
        await page.evaluate("""() => {
            document.querySelectorAll('.ig-header,.ig-dots,.ig-actions,.ig-caption')
                .forEach(el => el.style.display='none');

            const frame = document.querySelector('.ig-frame');
            frame.style.cssText = 'width:420px;height:525px;max-width:none;border-radius:0;box-shadow:none;overflow:hidden;margin:0;';

            const viewport = document.querySelector('.carousel-viewport');
            viewport.style.cssText = 'width:420px;height:525px;aspect-ratio:unset;overflow:hidden;cursor:default;';

            document.body.style.cssText = 'padding:0;margin:0;display:block;overflow:hidden;';
        }""")
        await page.wait_for_timeout(500)

        for i in range(TOTAL_SLIDES):
            await page.evaluate("""(idx) => {
                const track = document.querySelector('.carousel-track');
                track.style.transition = 'none';
                track.style.transform = 'translateX(' + (-idx * 420) + 'px)';
            }""", i)
            await page.wait_for_timeout(400)

            await page.screenshot(
                path=str(OUTPUT_DIR / f"slide_{i+1}.png"),
                clip={"x": 0, "y": 0, "width": VIEW_W, "height": VIEW_H}
            )
            print(f"Exported slide {i+1}/{TOTAL_SLIDES}")

        await browser.close()

asyncio.run(export_slides())
```

### Why This Works

- **`device_scale_factor=2.5714`** renders at high DPI — a 420px element becomes 1080px in the output. Layout stays at 420px.
- **`clip`** captures only the carousel viewport, not browser chrome.
- **`wait_for_timeout(3000)`** gives Google Fonts time to load.
- **`track.style.transition = 'none'`** disables swipe animation so slides snap instantly.

### Common Export Mistakes to Avoid

| Mistake | What goes wrong | Fix |
|---------|----------------|-----|
| Setting viewport to 1080×1350 | Layout reflows — fonts tiny, spacing breaks | Keep viewport at 420×525, use `device_scale_factor` |
| Using shell scripts to generate HTML | `$` signs and backticks get interpolated | Always use Python for HTML generation |
| Not waiting for fonts | Headings render in fallback system fonts | `wait_for_timeout(3000)` after page load |
| Not hiding IG frame chrome | Export includes header, dots, caption | Hide `.ig-header,.ig-dots,.ig-actions,.ig-caption` |
| Changing `.ig-frame` width | Entire layout shifts | Always keep at exactly 420px |
| Leaving `BRAND_PRIMARY` as variable name in CSS | Color renders as invalid / invisible | Always interpolate actual hex values into HTML |
