# Sourcing, Editing and Placing Real Photos in Slides

This module covers the parts `references/images.md` does not: **finding** a
photo when the user doesn't already have one, **preparing** it (crop, focal
point, brand tint) so it doesn't look like a random stock photo dropped on
top of the design, and **placing** it with one of the approved layouts.

`references/images.md` still owns the final embedding step (base64
`data:` URI, no relative paths, no `background: url()`). Never skip it —
this module hands its output straight into that one.

---

## Step 1 — Decide the source

Ask (don't assume): **"Você tem a foto ou quer que eu busque uma opção livre de direitos?"**

- User has a file/path → skip to Step 3 (Edit).
- User wants Claude to search → Step 2.
- User has no strong preference → search, but always show candidates before
  downloading (Step 2) — never pick silently and commit it straight to a slide.

## Step 2 — Search (only when Claude is sourcing the photo)

**Only use sources that are free for commercial use without permission
chasing:** Unsplash, Pexels, Pixabay. Never scrape a brand's site, a news
outlet, or a random image-search result — those are usually copyrighted and
the user has no license to post them.

### Relevance and brand-fit come first — never search generically

A photo that is technically "free to use" but unrelated to the slide's
actual message, or that clashes with the brand kit's tone, is a rejected
candidate even before checking its license. Before searching:

1. **Derive the query from the specific slide content**, not the carousel's
   general topic. "5 dicas de segurança no trabalho" → the slide about EPI
   (safety gear) searches `"trabalhador EPI capacete construção"`, not
   `"segurança"` or `"trabalho"` alone. A generic query returns generic,
   swappable-with-any-brand stock photos — the opposite of what makes a
   carousel look intentional.
2. **Read `tone` and the derived palette from `brand-kit.json` first** and
   filter candidates against them:
   - `tone: professional/corporate` → real workplaces, natural light, no
     exaggerated stock-photo smiling-at-camera poses.
   - `tone: casual/playful` → candid, warmer, less posed.
   - `tone: bold/minimal` → strong single-subject compositions, negative
     space (a photo needs breathing room if text/gradient will sit over it
     in the full-bleed component).
   - Color: prefer photos whose dominant tones don't fight `BRAND_PRIMARY`
     (e.g. don't pick a heavily red-toned photo for a brand built on green —
     the Step 3 tint blend softens this but can't fully rescue a clashing
     photo).
3. When multiple candidates pass the relevance filter, THEN apply the
   license/source filter below.

1. Use `WebSearch` to find candidates, e.g. `site:unsplash.com <slide-specific
   subject> photo` or `<slide-specific subject> free stock photo pexels`.
2. Resolve each candidate to a **direct image URL** (not the gallery/page
   URL) — `WebFetch` the page if needed to find the real `<img>`/CDN link.
3. Show the user 2–3 candidate links/thumbnails **before downloading**,
   stating in one line why each fits the slide's message and the brand tone,
   and ask which one to use. Don't guess — a wrong or off-brand photo is
   wasted download + edit work, and looks worse than no photo at all.
4. Download the chosen one with the standard library (no new dependency):

```python
import urllib.request
from pathlib import Path

def download_photo(url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    dest.write_bytes(urllib.request.urlopen(req).read())
    return dest

download_photo(
    "https://images.unsplash.com/photo-XXXX?w=1600&q=80",
    Path("conteudos/<slug>/assets/raw/slide3-photo.jpg"),
)
```

Keep the source URL as a one-line comment above the `<img>` in the HTML
(`<!-- foto: unsplash.com/photos/... -->`) so it's traceable later.
Unsplash/Pexels/Pixabay don't legally require attribution, but keeping the
link costs nothing and helps if the user wants to credit the photographer.

## Step 3 — Edit for the slide

Never embed a raw photo straight from disk/download. Always run it through
this pass first — it fixes the two most common "looks bad" causes (wrong
crop, and a stock photo that clashes with the brand palette) and keeps the
base64 payload sane (see `images.md` mistake #2 — huge inline strings crash
the parser).

```python
from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps

def prep_photo(
    src_path: Path,
    dst_path: Path,
    brand_dark_hex: str,        # BRAND_DARK from brand-kit.json, e.g. "#1A1918"
    mode: str = "fullbleed",    # "fullbleed" (4:5) or "card" (4:3, for the framed card component)
    tint_strength: float = 0.16 # 0 = no tint, ~0.15-0.22 reads as "on-brand" without muddying the photo
) -> Path:
    img = ImageOps.exif_transpose(Image.open(src_path).convert("RGB"))

    target_ratio = (1080 / 1350) if mode == "fullbleed" else (4 / 3)
    w, h = img.size
    if w / h > target_ratio:
        new_w = int(h * target_ratio)
        x0 = (w - new_w) // 2
        img = img.crop((x0, 0, x0 + new_w, h))
    else:
        new_h = int(w / target_ratio)
        y0 = (h - new_h) // 3  # bias toward the top third — keeps faces/heads in frame
        img = img.crop((0, y0, w, y0 + new_h))

    max_dim = 1600
    if max(img.size) > max_dim:
        img.thumbnail((max_dim, max_dim), Image.LANCZOS)

    img = ImageEnhance.Contrast(img).enhance(1.05)
    img = ImageEnhance.Color(img).enhance(0.95)

    # Brand-tint blend: pulls the photo's colors toward BRAND_DARK so it feels
    # designed, not pasted. Keep it subtle — this is not a duotone filter.
    tint = Image.new("RGB", img.size, brand_dark_hex)
    img = Image.blend(img, tint, tint_strength)

    dst_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(dst_path, "JPEG", quality=85, optimize=True)
    return dst_path
```

Requires `Pillow` (see `requirements.txt`). Run `pip install -r
requirements.txt` if `PIL` import fails.

Save edited output to `conteudos/<slug>/assets/edited/` — keep raw downloads
in `conteudos/<slug>/assets/raw/` so a bad crop can be redone without
re-downloading.

## Step 4 — Embed

Feed `dst_path` from Step 3 into `references/images.md` exactly as written
there (base64 `data:` URI, Python `Path.write_text()`, verify MIME with
`file`). Do not shortcut this step even for a photo Claude just generated —
the same crash/relative-path risks apply.

## Step 5 — Place it beautifully

Pick one of the **Photo Components** in `references/design-system.md`
("Photo slide — full-bleed" or "Framed photo card") — don't invent a new
layout ad hoc. Both already account for the grain overlay, corner mark,
watermark, progress bar and swipe arrow that every slide requires per
`design-system.md`'s Decorative Layer — a photo slide is not exempt from
those.

Rule of thumb for which component:
- **Full-bleed** — Hero or a single strong "proof" slide (e.g. a
  screenshot-style result, a portrait for an about/CTA slide). Photo *is*
  the slide.
- **Framed card** — Feature/Detail/How-to slides where the photo supports a
  headline/body rather than replacing it. Keeps the editorial rhythm with
  the rest of the carousel.

## Common mistakes

| Mistake | What goes wrong | Fix |
|---|---|---|
| Searching the carousel's general topic instead of the slide's specific content | Generic, could-be-any-brand stock photo that doesn't reinforce the slide's point | Derive the query from that slide's actual message (Step 2) |
| Ignoring `brand-kit.json`'s `tone`/palette when picking a candidate | Photo feels bolted-on instead of part of the same design | Filter candidates against tone + color fit before license (Step 2) |
| Downloading straight from a Google Images result | Usually copyrighted, no license to post | Only Unsplash/Pexels/Pixabay, or the user's own file |
| Skipping Step 3 and embedding the raw download | Wrong aspect ratio stretches/crops badly at export; photo clashes with brand colors | Always run `prep_photo()` first |
| Picking one candidate photo without asking | Wastes a full edit+embed cycle if the user doesn't like it | Show 2–3 links, get a pick, then download |
| Applying a heavy filter/duotone | Photo looks over-processed, fights the editorial look | `tint_strength` ~0.15–0.22, never a full duotone unless asked |
