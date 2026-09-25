# Visual QA — Reading Every Slide Before Showing It to the User

This step runs **every time** `carousel.html` is generated or edited (Phase 3,
and again after any fix), **before** telling the user it's ready to review.
Skipping it defeats the purpose: catching problems before the user has to.

Rendering an HTML preview is not the same as looking at it. A slide can have
perfectly valid CSS and still fail once rendered: text that lands on a
bright/busy part of a photo, or a photo cropped so tight the subject that
matches the slide's text is no longer in frame. Both are invisible from the
HTML source; both are obvious from a screenshot.

## Step 1 — Render every slide as a PNG

Reuse the same viewport/scale approach as `export.md`, but this can run at a
lower `device_scale_factor` (e.g. 2x instead of 2.5714x) since this is for
Claude's own inspection, not the final deliverable:

```python
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

CAROUSEL_DIR = Path("conteudos/<YYYY-MM-DD>-<slug>")
INPUT_HTML = CAROUSEL_DIR / "carousel.html"
OUT_DIR = Path("<scratchpad>/visual-qa/<slug>")  # never write throwaway QA shots into conteudos/
OUT_DIR.mkdir(parents=True, exist_ok=True)

VIEW_W, VIEW_H, SCALE, TOTAL_SLIDES = 420, 525, 2, 7  # adjust TOTAL_SLIDES

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": VIEW_W, "height": VIEW_H}, device_scale_factor=SCALE)
        await page.set_content(INPUT_HTML.read_text(encoding="utf-8"), wait_until="networkidle")
        await page.wait_for_timeout(1500)
        await page.evaluate("""() => {
            const vp = document.querySelector('.ig-viewport');
            document.body.innerHTML = '';
            document.body.appendChild(vp);
            document.body.style.cssText = 'padding:0;margin:0;display:block;overflow:hidden;background:#000;';
            vp.style.cssText = 'position:relative;width:420px;height:525px;overflow:hidden;background:#000;';
            document.querySelector('.ig-track').style.transition = 'none';
        }""")
        await page.wait_for_timeout(300)
        for i in range(TOTAL_SLIDES):
            await page.evaluate("(idx) => { document.querySelector('.ig-track').style.transform = 'translateX(' + (-idx * 420) + 'px)'; }", i)
            await page.wait_for_timeout(200)
            await page.screenshot(path=str(OUT_DIR / f"slide_{i+1}.png"), clip={"x": 0, "y": 0, "width": VIEW_W, "height": VIEW_H})
        await browser.close()

asyncio.run(main())
```

## Step 2 — Read every screenshot, slide by slide

Use the `Read` tool on each `slide_N.png`. For **every slide that has a
photo** (full-bleed or framed card) and for the **hero/CTA slides
regardless**, check both of these explicitly — don't eyeball the whole batch
at once, look at each slide on its own:

1. **Is the text easy to read at a glance?**
   Check contrast against what is *actually* behind each text block in the
   rendered image, not the theoretical `LIGHT_BG`/`DARK_BG` token. A gradient
   scrim that looks fine in CSS can still leave a headline sitting on a
   bright sky, a light patch of concrete, or a low-contrast part of the
   photo. If any line is hard to read at normal viewing size, that's a fail.

2. **Does the visible part of the photo still match what the text is about?**
   After `object-fit:cover` crops the source image down to the card/frame
   size, check the subject the photo was chosen for (the person, the object,
   the action) is actually still in frame and recognizable, not cropped out
   or reduced to an unrelated background detail (e.g. a wide shot where the
   worker becomes a speck and the frame is dominated by an empty wall).
   Also re-confirm no logo/watermark lands on a face (see
   `logo-protection-chip` rule already required by `design-system.md`).

## Step 3 — Report, don't silently fix

For every slide that fails either check: **stop and tell the user** exactly
what's wrong (which slide, which of the two checks failed, why) and what you
propose to change (e.g. "mover object-position pra 50% 80%", "escurecer o
scrim de 0.5 pra 0.7 nessa faixa", "trocar a foto por outra opção"). Wait for
approval before touching the file — this applies even to a small technical
tweak like `object-position` or overlay opacity, not just a full photo swap.
If nothing fails, say so explicitly ("conferi os N slides, texto e foto
batem em todos") instead of staying silent about the check having happened.

## Fixing text-over-photo legibility (recipe)

When Step 2 finds a text-over-photo slide that fails the legibility check,
this is the recipe that actually fixed it in practice (A&J, "5 motivos de
acidentes de trabalho", 2026-09-25) — use it as the starting point instead
of re-deriving a fix from scratch each time:

1. **Size the scrim to the real content height, not a guessed percentage.**
   A single-stop gradient that fades out at, say, 55% of the slide looks
   fine in isolation but fails the moment the actual text block (headline +
   subhead + any small label/badge) extends further down than that — the
   tail of the text lands directly on the bare photo. Look at where the
   text block *actually* ends in the rendered screenshot and make sure the
   gradient stays at a legible opacity at least that far down, e.g.:
   ```html
   <div style="position:absolute;inset:0;background:linear-gradient(180deg,
     rgba(18,63,60,0.92) 0%, rgba(18,63,60,0.82) 20%, rgba(18,63,60,0.68) 40%,
     rgba(18,63,60,0.52) 58%, rgba(18,63,60,0.34) 72%, rgba(18,63,60,0.14) 90%
   );z-index:1;"></div>
   ```
   (hex values are `{DARK_BG}` as rgba — interpolate the brand's actual dark
   token, this is the A&J example).

2. **Add a low, uniform flat wash as a safety net**, on top of the
   directional gradient, so no point on the slide — including the very tail
   of the fade — ever drops below a baseline contrast floor:
   ```html
   <div style="position:absolute;inset:0;background:rgba({DARK_BG_rgb},0.16);z-index:1;"></div>
   ```
   This is cheap insurance: it catches whatever the directional gradient's
   math doesn't quite cover, without visibly changing the design.

3. **A secondary opposite-edge gradient is fine for vignette consistency**,
   but keep it genuinely subtle and don't let it re-darken an area you
   deliberately kept clear for another reason (e.g. a face) — cap its reach
   (a `to top, ... transparent 38%` style stop that only touches the very
   bottom edge) rather than letting it grow to meet the main scrim.

4. **Never use a brand's pale/light accent token (e.g. `BRAND_LIGHT`) for
   emphasized text sitting directly on a photo.** It reads fine over a flat
   brand-gradient CTA slide (fully controlled background) but loses contrast
   fast over a real photo, especially in a scrim's fade zone where the
   underlying image can be bright (sky, light concrete, etc). Use white or
   cream instead, and get the "mixed weight" emphasis effect from
   weight+italic alone (e.g. `font-weight:700;font-style:italic;color:#fff`)
   rather than from color, whenever the text sits over a photo.

5. **Low-opacity microcopy (a small swipe hint, a secondary label) needs a
   higher floor over a photo than over a flat/solid slide background.**
   Something styled at `opacity:0.5-0.6` reads as an intentional, quiet
   detail over `LIGHT_BG`/`DARK_BG`/the brand gradient, but the same opacity
   over a busy photo — especially past the point where the scrim has faded —
   can become genuinely unreadable. Push it toward `0.75-0.85` and bump the
   font-weight when it sits over a photo.

Re-render after applying and re-check per Step 2 above — don't assume the
recipe worked without looking at the result.

## When to re-run

Any time `carousel.html`'s slides change: after first generation, after any
fix (including a fix suggested by this very check), and after the user
downloads an edited version from the in-page editor and it's swapped back in
before export. Never export straight from Phase 3 without this step running
at least once on the final content.
