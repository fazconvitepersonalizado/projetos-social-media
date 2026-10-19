# Design System — Colors, Typography, Slides, Components, Layout

> All rules in this file are **verbatim** from the original skill. Do not edit
> any value, table or code block here — exporters and previewers depend on
> them being exact.

---

## Step 2: Derive the Full Color System

From the user's **single primary brand color**, generate the full 6-token palette:

```
BRAND_PRIMARY   = {user's color}                    // Main accent — progress bar, icons, tags
BRAND_LIGHT     = {primary lightened ~20%}           // Secondary accent — tags on dark, pills
BRAND_DARK      = {primary darkened ~30%}            // CTA text, gradient anchor
LIGHT_BG        = {warm or cool off-white}           // Light slide background (never pure #fff)
LIGHT_BORDER    = {slightly darker than LIGHT_BG}    // Dividers on light slides
DARK_BG         = {near-black with brand tint}       // Dark slide background
```

**Rules for deriving colors:**
- LIGHT_BG: tinted off-white complementing the primary (warm → warm cream, cool → cool gray-white)
- DARK_BG: near-black with subtle brand tint (warm → #1A1918, cool → #0F172A)
- LIGHT_BORDER: always ~1 shade darker than LIGHT_BG
- Brand gradient (mesh): three overlapping `radial-gradient`s anchored at different corners over `BRAND_PRIMARY`. Never a flat linear gradient.

```css
/* Brand gradient — used on Solution and CTA slides */
background:
  radial-gradient(circle at 15% 20%, {BRAND_LIGHT} 0%, transparent 55%),
  radial-gradient(circle at 90% 10%, {BRAND_PRIMARY} 0%, transparent 50%),
  radial-gradient(circle at 60% 100%, {BRAND_DARK} 0%, transparent 65%),
  {BRAND_PRIMARY};
```

**Legibility scrim (mandatory on every brand-gradient slide):** the `{BRAND_LIGHT}`
stop at 15%/20% is often close to white, which makes `#fff` headline/quote text
unreadable wherever it sits over that hotspot. A vignette centered on the
content block is NOT enough — the hotspot is in the top-left corner, not the
center, so a center-anchored fade misses it entirely. The scrim must instead be
anchored at the **same position as the light stop** so it directly cancels it,
plus a light uniform wash for baseline contrast everywhere else. Placed
immediately after the grain `<svg>` (so it sits above the gradient, below the
content at `z-index: 2`):

```html
<div style="position:absolute;inset:0;z-index:1;pointer-events:none;background:
  radial-gradient(circle at 15% 20%, rgba(0,0,0,0.48) 0%, transparent 60%),
  rgba(0,0,0,0.12);"></div>
```

This is not optional and not a substitute for the grain overlay — both layers
are present on every brand-gradient slide. Never anchor this scrim at the
slide's center — always match the light stop's own position (15% 20%).

### Background composition — NEVER use flat colors

`LIGHT_BG` and `DARK_BG` are tokens but they are **never** used as a single flat fill. Every slide background is a layered composition:

**Light slides:**
```css
background:
  radial-gradient(circle at 20% 0%, {BRAND_PRIMARY}1F 0%, transparent 45%),
  radial-gradient(circle at 100% 100%, {BRAND_LIGHT}24 0%, transparent 50%),
  {LIGHT_BG};
```

**Dark slides:**
```css
background:
  radial-gradient(circle at 80% 10%, {BRAND_PRIMARY}3D 0%, transparent 40%),
  radial-gradient(circle at 0% 90%, {BRAND_DARK}66 0%, transparent 55%),
  {DARK_BG};
```

The `{COLOR}NN` suffix is a hex alpha (e.g. `1F` ≈ 12% opacity). Always interpolate the actual hex into the suffix — do NOT leave token names in the CSS.

### Grain overlay (every slide)

Every slide includes a fractal-noise SVG overlay at low opacity. This kills the "AI-rendered" feel and gives a paper/film texture:

```html
<svg class="grain" aria-hidden="true" style="position:absolute;inset:0;width:100%;height:100%;pointer-events:none;opacity:0.05;mix-blend-mode:overlay;z-index:1;">
  <filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/></filter>
  <rect width="100%" height="100%" filter="url(#g)"/>
</svg>
```

All slide content sits at `z-index: 2` or higher. The grain `<svg>` is the very first child inside the slide container.

---

## Step 3: Set Up Typography

Based on the user's font preference, pick a **heading font** and **body font** from Google Fonts.

| Style | Heading Font | Body Font |
|-------|-------------|-----------|
| Editorial / premium | Playfair Display | DM Sans |
| Modern / clean | Plus Jakarta Sans (700) | Plus Jakarta Sans (400) |
| Warm / approachable | Lora | Nunito Sans |
| Technical / sharp | Space Grotesk | Space Grotesk |
| Bold / expressive | Fraunces | Outfit |
| Classic / trustworthy | Libre Baskerville | Work Sans |
| Rounded / friendly | Bricolage Grotesque | Bricolage Grotesque |

**Editorial font size scale (fixed across all brands):**
- Hero headline (Slide 1): **44–56px**, weight 600, letter-spacing -1px, line-height 1.05
- Slide headline (problem/solution/features/etc): **32–40px**, weight 600, letter-spacing -0.5px, line-height 1.1
- Subhead / lead paragraph: 16–17px, weight 400, line-height 1.45, opacity 0.75
- Body: 14px, weight 400, line-height 1.5–1.55
- Tags/labels: 10px, weight 600, letter-spacing 2px, uppercase
- Step numbers: heading font, 44px, weight 300 (used *above* the step title, not inline)
- Big-stat number: heading font, 72–96px, weight 300, letter-spacing -3px (see Big Stat component)
- Small text: 11–12px

Apply via CSS classes `.serif` (heading font) and `.sans` (body font) throughout all slides.

**Mandatory mixed-weight headline:** In every carousel, at least ONE headline must mix weights/styles inside the same title to break monotony. Example:

```html
<h1 class="serif" style="font-size:48px;line-height:1.05;">
  <span style="font-weight:300;">Você está usando IA</span>
  <span style="font-weight:600;font-style:italic;color:{BRAND_PRIMARY};">errado</span>
</h1>
```

---

## Slide 1 — Hook Rules

The first slide must stop the scroll in under 1 second. Prioritize these formats:

| Hook format | Example |
|---|---|
| Afirmação polêmica | "Você está usando IA errado" |
| Número + benefício | "7 ferramentas que substituem seu designer" |
| Pergunta que dói | "Por que seus carrosséis têm 0 salvamentos?" |
| Resultado concreto | "Esse post gerou 4.200 seguidores em 3 dias" |
| Inversão de expectativa | "Mais esforço no design = menos alcance" |

**Rules:**
- Never start with the brand name as headline
- Visual proof on Slide 1 whenever possible (screenshot, result, real number)
- Hook must promise value that the following slides deliver

---

## Slide Sequences

### Standard (7 slides — default)

| # | Type | Background | Purpose |
|---|------|------------|---------|
| 1 | Hero | LIGHT_BG | Hook — bold statement, logo lockup, optional watermark |
| 2 | Problem | DARK_BG | Pain point — what's broken, frustrating, or outdated |
| 3 | Solution | Brand gradient | The answer — what solves it, optional quote/prompt box |
| 4 | Features | LIGHT_BG | What you get — feature list with icons |
| 5 | Details | DARK_BG | Depth — customization, specs, differentiators |
| 6 | How-to | LIGHT_BG | Steps — numbered workflow or process |
| 7 | CTA | Brand gradient | Call to action — logo, tagline, CTA button. **No arrow. Full progress bar.** |

### Listicle (5–10 slides)

| # | Type | Background |
|---|------|------------|
| 1 | Hero | LIGHT_BG |
| 2–N | Item N | Alternating LIGHT/DARK |
| Last | CTA | Brand gradient |

Use for: "X ferramentas", "X erros", "X dicas"

### Tutorial (7 slides)

| # | Type | Background |
|---|------|------------|
| 1 | Hero | LIGHT_BG |
| 2 | Contexto / Por quê | DARK_BG |
| 3–5 | Passo 1, 2, 3 | Alternating |
| 6 | Resultado esperado | DARK_BG |
| 7 | CTA | Brand gradient |

### Comparação (5 slides)

| # | Type | Background |
|---|------|------------|
| 1 | Hero (o que será comparado) | LIGHT_BG |
| 2 | Opção A | LIGHT_BG |
| 3 | Opção B | DARK_BG |
| 4 | Veredicto | Brand gradient |
| 5 | CTA | DARK_BG |

**General rules for all sequences:**
- Start with a hook — first slide must stop the scroll
- End CTA on brand gradient — no swipe arrow, progress bar at 100%
- Alternate light and dark backgrounds for visual rhythm
- Adapt sequence to topic — not every carousel needs all slides

---

## Slide Architecture

### Format
- Aspect ratio: **4:5** (Instagram carousel standard)
- Each slide is self-contained — all UI elements baked into the image
- Alternate LIGHT_BG and DARK_BG backgrounds for visual rhythm

### Required Elements on Every Slide

#### 1. Progress Bar (segmented, "stories" style — bottom of every slide)

Shows position in the carousel as N discrete segments (one per slide), filled up to and including the current slide.

- Position: absolute bottom, full width, 28px horizontal padding, 20px bottom padding
- Each segment: `flex:1; height:3px; border-radius:2px`
- Gap between segments: `4px`
- Fill color (current slide and all previous): `BRAND_PRIMARY` (light slides) or `#fff` (dark slides)
- Track color (future segments): `rgba(0,0,0,0.10)` (light) or `rgba(255,255,255,0.18)` (dark)
- Counter label at the end: "1/7" format, 11px, weight 500, opacity 0.4

```javascript
function progressBar(index, total, isLightSlide) {
  const fillColor   = isLightSlide ? BRAND_PRIMARY : '#fff'; // actual hex
  const trackColor  = isLightSlide ? 'rgba(0,0,0,0.10)' : 'rgba(255,255,255,0.18)';
  const labelColor  = isLightSlide ? 'rgba(0,0,0,0.35)' : 'rgba(255,255,255,0.45)';
  const segments = Array.from({length: total}, (_, i) => {
    const color = i <= index ? fillColor : trackColor;
    return `<div style="flex:1;height:3px;background:${color};border-radius:2px;"></div>`;
  }).join('');
  return `<div style="position:absolute;bottom:0;left:0;right:0;padding:16px 28px 20px;z-index:10;display:flex;align-items:center;gap:10px;">
    <div style="flex:1;display:flex;gap:4px;">${segments}</div>
    <span style="font-size:11px;color:${labelColor};font-weight:500;">${index + 1}/${total}</span>
  </div>`;
}
```

⚠️ **Important:** Always replace `BRAND_PRIMARY` with the actual hex value before rendering. Never leave it as a variable name in the HTML output.

#### 2. Swipe Arrow (right edge — every slide EXCEPT the last)

Subtle chevron guiding the user to keep swiping. Removed on the last slide.

- Position: absolute right, full height, 48px wide
- Background: gradient fade transparent → subtle tint
- Chevron: 24×24 SVG, rounded strokes
- Light slides: `rgba(0,0,0,0.06)` bg, `rgba(0,0,0,0.25)` stroke
- Dark slides: `rgba(255,255,255,0.08)` bg, `rgba(255,255,255,0.35)` stroke

```javascript
function swipeArrow(isLightSlide) {
  const bg = isLightSlide ? 'rgba(0,0,0,0.06)' : 'rgba(255,255,255,0.08)';
  const stroke = isLightSlide ? 'rgba(0,0,0,0.25)' : 'rgba(255,255,255,0.35)';
  return `<div style="position:absolute;right:0;top:0;bottom:0;width:48px;z-index:9;display:flex;align-items:center;justify-content:center;background:linear-gradient(to right,transparent,${bg});">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
      <path d="M9 6l6 6-6 6" stroke="${stroke}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </div>`;
}
```

---

#### 3. Decorative layer (every slide)

A minimal "visual language" used across all slides for cohesion. All three appear on every slide.

**Corner mark** — small SVG (cross/plus) anchored top-right:
```html
<svg width="12" height="12" viewBox="0 0 12 12" style="position:absolute;top:24px;right:24px;z-index:5;">
  <path d="M6 0v12M0 6h12" stroke="{accent}" stroke-width="1.2"/>
</svg>
```
- `{accent}` = `BRAND_PRIMARY` on light slides, `BRAND_LIGHT` on dark slides, `rgba(255,255,255,0.6)` on gradient slides.

**Slide watermark** — slide number top-left, `01 / 07` format, heading font, weight 300, 11px, opacity 0.35:
```html
<span class="serif" style="position:absolute;top:22px;left:28px;font-size:11px;font-weight:300;letter-spacing:1px;opacity:0.35;z-index:5;color:{textColor};">
  0{n} / 0{total}
</span>
```

**Hair-line divider** — 1px horizontal line, 40px wide, placed directly under the tag/label inside the content block:
```html
<div style="width:40px;height:1px;background:{accent};opacity:0.6;margin:6px 0 18px;"></div>
```

**Logo watermark** (slides 2..N-1, only when a real logo is provided in the brand kit) — see "Logo Lockup" section below. Placed top-left, 20px tall, opacity 0.5, **replaces** the textual slide watermark `0n / 0total` on those slides. On slides 1 and N (which carry the full logo lockup), no watermark is added.

---

## Reusable Components

### Strikethrough pills
```html
<span style="font-size:11px;padding:5px 12px;border:1px solid rgba(255,255,255,0.1);border-radius:20px;color:#6B6560;text-decoration:line-through;">{Old tool}</span>
```

### Tag pills
```html
<span style="font-size:11px;padding:5px 12px;background:rgba(255,255,255,0.06);border-radius:20px;color:{BRAND_LIGHT};">{Label}</span>
```

### Prompt / quote box
```html
<div style="padding:16px;background:rgba(0,0,0,0.15);border-radius:12px;border:1px solid rgba(255,255,255,0.08);">
  <p class="sans" style="font-size:13px;color:rgba(255,255,255,0.5);margin-bottom:6px;">{Label}</p>
  <p class="serif" style="font-size:15px;color:#fff;font-style:italic;line-height:1.4;">"{Quote text}"</p>
</div>
```

### Feature list (icon tile, no borders)
```html
<div style="display:flex;align-items:flex-start;gap:14px;padding:6px 0;">
  <span style="
    flex:none;width:28px;height:28px;border-radius:8px;
    background:{BRAND_PRIMARY}1A;color:{BRAND_PRIMARY};
    display:flex;align-items:center;justify-content:center;font-size:14px;
  ">{icon}</span>
  <div style="display:flex;flex-direction:column;gap:2px;">
    <span class="sans" style="font-size:14px;font-weight:600;color:{DARK_BG};">{Label}</span>
    <span class="sans" style="font-size:12px;color:#8A8580;line-height:1.4;">{Description}</span>
  </div>
</div>
```

### Numbered steps (number-above, editorial)
```html
<div style="display:flex;flex-direction:column;gap:4px;padding:10px 0;">
  <span class="serif" style="font-size:44px;font-weight:300;color:{BRAND_PRIMARY};line-height:1;letter-spacing:-1px;">01</span>
  <span class="sans" style="font-size:15px;font-weight:600;color:{DARK_BG};">{Step title}</span>
  <span class="sans" style="font-size:12px;color:#8A8580;line-height:1.4;">{Step description}</span>
</div>
```

### Big Stat (impact number)
Use at least once per carousel (typically Slide 2 or 5) — provides editorial weight.
```html
<div style="text-align:center;">
  <span class="serif" style="font-size:88px;font-weight:300;color:{BRAND_PRIMARY};line-height:1;letter-spacing:-3px;display:block;">4.200</span>
  <p class="sans" style="font-size:13px;color:#8A8580;margin-top:8px;letter-spacing:0.5px;">seguidores em 3 dias</p>
</div>
```

### Pull-quote (vertical bar)
```html
<blockquote style="border-left:2px solid {BRAND_PRIMARY};padding:6px 0 6px 18px;margin:0;">
  <p class="serif" style="font-size:22px;font-style:italic;font-weight:400;line-height:1.3;color:{DARK_BG};margin:0;">"{Quote text}"</p>
  <p class="sans" style="font-size:11px;color:#8A8580;letter-spacing:2px;text-transform:uppercase;margin-top:8px;">{Attribution}</p>
</blockquote>
```

### Glass card (gradient slides only)
For containing quotes / stats / CTA blocks on top of the brand gradient.
```html
<div style="
  background:rgba(255,255,255,0.08);
  backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);
  border:1px solid rgba(255,255,255,0.14);
  border-radius:16px;padding:22px;color:#fff;
">{content}</div>
```

### Color swatches
```html
<div style="width:32px;height:32px;border-radius:8px;background:{color};border:1px solid rgba(255,255,255,0.08);"></div>
```

### CTA button (final slide only)
```html
<div style="display:inline-flex;align-items:center;gap:8px;padding:12px 28px;background:{LIGHT_BG};color:{BRAND_DARK};font-family:'{BODY_FONT}',sans-serif;font-weight:600;font-size:14px;border-radius:28px;">
  {CTA text}
</div>
```

### Tag / Category Label
```html
<span class="sans" style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{color};margin-bottom:16px;">{TAG TEXT}</span>
```
- Light slides: `BRAND_PRIMARY`
- Dark slides: `BRAND_LIGHT`
- Brand gradient slides: `rgba(255,255,255,0.6)`

### Photo Components

Use these when a slide includes a real photo. **Before reaching for either
component, source and prepare the photo per `references/photo-sourcing.md`**
— it owns relevance-to-theme, brand-tone fit, cropping and the base64
embedding step. Neither component below is complete without that: a
correctly-placed but off-topic or off-brand photo still fails the "visually
beautiful" bar this design system exists for.

Both components still require the full Decorative Layer (grain overlay,
corner mark, watermark, progress bar, swipe arrow) — a photo slide is not a
special case.

**Photo slide — full-bleed** (Hero or a single "proof" slide):
```html
<img src="{data_uri}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;">
<div style="position:absolute;inset:0;background:linear-gradient(to top,{DARK_BG}F2 0%,{DARK_BG}00 55%);z-index:1;"></div>
<!-- content block sits in the lower portion, z-index:2, text in #fff -->
```
Use the photo's own composition to decide top vs. bottom scrim direction —
keep text over the visually calmest part of the photo (usually where the
subject leaves negative space). The single-stop example above is a starting
point only — size the scrim to the actual rendered content, and layer extra
protection when the photo has bright/busy areas. See the legibility recipe
in `references/visual-qa.md` ("Fixing text-over-photo legibility") for the
concrete layering pattern (multi-stop gradient sized to content height +
flat uniform wash + white/cream text instead of a brand's pale accent
color) — this is required whenever a single directional gradient leaves any
part of the text sitting on a light/busy patch of the photo.

**Framed photo card** (Feature/Detail/How-to — photo supports the copy, doesn't replace it):
```html
<div style="width:100%;border-radius:16px;overflow:hidden;box-shadow:0 12px 32px rgba(0,0,0,0.18);margin-bottom:18px;">
  <img src="{data_uri}" style="display:block;width:100%;height:220px;object-fit:cover;">
</div>
<!-- tag / headline / body follow below, inside the same centered content block -->
```

### Logo Lockup — real logo rendering

Read `logo` from `brand-kit.json`. Behavior depends on `logo.type`:

| `logo.type` | How to render |
|---|---|
| `svg`     | Read the SVG file with `Path(path).read_text()`, inline the full `<svg>` element directly into the HTML (do **not** wrap in `<img>`). Force `width` / `height` attributes per the size table below. If the SVG uses `currentColor`, set `color:` on the inline style; otherwise pick the variant matching the slide background. |
| `image`   | Read bytes, base64-encode, embed as `<img src="data:image/{ext};base64,..." style="width:..;height:..;object-fit:contain">` (same rules as `references/images.md`). |
| `initial` / `none` | Fallback: 40px circle (`BRAND_PRIMARY` bg) with the first letter of `brand_name` centered in white. |

**Variant selection** (when `logo.variants` exists):
- Light slide → `variants.primary` (or `variants.dark` if `primary` missing)
- Dark slide → `variants.white`
- Brand-gradient slide → `variants.white`
- If only `logo.path` is set (no variants): use it on all slides.

**Legibility check (mandatory, every slide with a logo):** before placing the
logo, confirm the chosen variant actually reads against that slide's real
background, not just against the LIGHT_BG/DARK_BG label. Never place a
`white` variant on a light or near-white area (this includes the light stop
on brand-gradient slides, around 15%/20%, where a white logo can vanish the
same way white text does). Never place a `dark`/`primary` (colored) variant
on a dark or busy area. If multiple color variants exist, pick whichever one
has the best contrast against the actual pixels behind it on that slide, even
if that means deviating from the table above.

**Where the logo appears:**

| Slide | Treatment | Size |
|---|---|---|
| Slide 1 (Hero) | Lockup centered above the headline: logo + brand name side by side | 32×32 logo, 13px brand name |
| Last slide (CTA) | Lockup centered above the CTA: logo + brand name | 48×48 logo, 15px brand name |
| Slides 2..N-1 | Watermark, top-left corner, opacity 0.5. **Replaces** the `01/07` slide watermark on those slides. | 20×20 logo, no brand name |

**Lockup markup (Hero / CTA):**
```html
<div style="display:flex;align-items:center;justify-content:center;gap:10px;margin-bottom:20px;">
  <!-- inline <svg>… here, OR <img src="data:..."> -->
  <span class="sans" style="font-size:13px;font-weight:600;letter-spacing:0.5px;color:{textColor};">
    {brand_name}
  </span>
</div>
```

**Watermark markup (slides 2..N-1):**
```html
<div style="position:absolute;top:20px;left:28px;opacity:0.5;z-index:5;">
  <!-- inline <svg width="20" height="20"…> OR <img …> -->
</div>
```

If `logo.type` is `initial` / `none`, fall back to the 40px circle described above on Hero and CTA, and use the textual `0n / 0total` watermark on slides 2..N-1 (see Decorative Layer).

---

## Layout Rules

**Universal centralization — all slides:**

- Every slide is a flex column with `justify-content: center` on the vertical axis. **Never use `flex-end`**, regardless of content density.
- Slide padding (fixed): `64px 36px 76px` (top / sides / bottom-clears-progress-bar).
- The content block inside the slide uses `max-width: 360px; margin: 0 auto` so wrapping is consistent across slides.
- Slides with lists (Features, How-to, Listicle items): center the **list block** as a whole, with `display:flex; flex-direction:column; gap:14px;`. Each list item still left-aligns its text inside the centered block.
- Content must never overlap the progress bar — the `padding-bottom: 76px` (slide) already clears it; do not reduce.
- Hero/CTA slides keep the same layout as the others — the difference is only the background (gradient) and the presence of the logo lockup; vertical alignment is identical.

---

## Instagram Frame (Preview Wrapper)

When displaying in chat, wrap in an Instagram-style frame:

- **Header:** Avatar (BRAND_PRIMARY circle + logo) + handle + subtitle
- **Viewport:** 4:5 aspect ratio, swipeable/draggable track with all slides
- **Dots:** Small dot indicators below the viewport
- **Actions:** Heart, comment, share, bookmark SVG icons
- **Caption:** Handle + short description + "2 HOURS AGO" timestamp

Include pointer-based swipe/drag interaction for preview. Slides are still standalone export-ready images.

**Important:** `.ig-frame` must be exactly **420px wide**. The carousel viewport is 420×525px. Do NOT change this width — export depends on it.

---

## Design Principles

1. **Every slide is export-ready** — arrow and progress bar are part of the slide image
2. **Light/dark alternation** — creates visual rhythm across swipes
3. **Heading + body font pairing** — display font for impact, body for readability
4. **Brand-derived palette** — all colors stem from one primary, keeping everything cohesive
5. **Progressive disclosure** — progress bar fills and arrow guides forward
6. **Last slide is special** — no arrow, full progress bar, clear CTA
7. **Consistent components** — same tag style, list style, spacing across all slides
8. **Content padding clears UI** — body text never overlaps progress bar or arrow
9. **Hook-first copy** — Slide 1 exists to stop the scroll, not to introduce the brand
10. **Iterate fast** — show preview, fix specific slides, don't rebuild from scratch
