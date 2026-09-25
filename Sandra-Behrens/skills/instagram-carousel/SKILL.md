---
name: instagram-carousel
description: >
  Creates high-quality Instagram carousels as swipeable HTML previews with
  export-ready slides (1080×1350px PNG). Handles the full workflow: brand
  setup, slide copy, visual design system (colors, fonts, components), HTML
  generation, and Playwright-based export. Use this skill whenever the user
  asks to create, design, or generate an Instagram carousel, carrossel,
  slides para Instagram, or any Instagram multi-image post — even if they
  don't explicitly say "carousel" or "skill". Also trigger for requests to
  "create a post with multiple slides", "fazer carrossel", or "exportar slides
  para o Instagram".
---

# Instagram Carousel Generator — Workflow Orchestrator

This skill is split into a thin orchestrator (this file) plus reference modules
that contain the **verbatim** design and export rules. Never paraphrase, edit
or skip rules in the references — they are required for the export pipeline to
work.

## Reference modules (load on demand)

- `references/brand-kit.md` — Brand kit collection + persistence to `brand-kit.json`
- `references/images.md` — Handling user-provided images (base64, Python only)
- `references/photo-sourcing.md` — Sourcing photos (search + license), cropping/tinting them to fit the brand, and picking a placement — use whenever no ready-made image file was given
- `references/design-system.md` — Colors, typography, slide sequences, components, layout, IG frame
- `references/edit-panel.md` — Side-panel editor + "Baixar HTML" button injected into the preview
- `references/export.md` — Playwright export to 1080×1350 PNGs + project path conventions

Read a reference fully before doing work that depends on it. If a reference
contradicts something you remember, the reference wins.

---

## Project layout

```
carrossel-instagram/
├── brand-kit.json                            # created on first run (Phase 1)
├── conteudos/
│   └── <YYYY-MM-DD>-<slug>/                 # one folder per carousel
│       ├── carousel.html                     # editable HTML (with edit panel)
│       └── slides/
│           ├── slide_1.png
│           └── …
└── skills/instagram-carousel/                # this skill
```

`<slug>` = kebab-case, ASCII, no accents, derived from the carousel topic.
`<YYYY-MM-DD>` = current date.

---

## The workflow (run in order, do not skip phases)

### Phase 0 — Detect state

At the start of every session, before doing anything else:

1. Check whether `brand-kit.json` exists at the project root.
2. Tell the user one line: either "Brand kit encontrado: <brand_name> (<primary_color>). Uso esse ou quer atualizar?" or "Nenhum brand kit encontrado — vou rodar a configuração inicial."

Do not move to Phase 2 without a valid brand kit loaded in context.

### Phase 1 — Brand kit (only if missing or update requested)

Follow `references/brand-kit.md` end-to-end. Save the answers to
`brand-kit.json` at the project root via Python (`Path.write_text` + JSON
serialization). Compute and store the derived 6-token palette per
`references/design-system.md` "Step 2".

### Phase 2 — Carousel planning

Ask the user for **the carousel theme/topic** and confirm:
- The sequence to use (default: standard 7 slides — see `references/design-system.md`).
- The slug for the folder (suggest one derived from the theme; let the user override).
- Any images they want to embed: do they have the file(s), or should Claude
  search for free-to-use photos? Either way, name **which slide(s)** get a
  photo and what each photo should show — a photo must reinforce that
  specific slide's message and the brand kit's tone/palette, never a
  generic stock image (see `references/photo-sourcing.md`).

Draft the slide-by-slide copy plan (hook, problem, solution, …) and **show it
in chat** for approval before generating any HTML. Keep it short.

### Phase 3 — Generate HTML

Once the plan is approved:

1. Create `conteudos/<YYYY-MM-DD>-<slug>/` (and the `slides/` subfolder).
2. If any slide needs a photo Claude is sourcing (not a file the user
   already gave), run `references/photo-sourcing.md` first — search, get
   the user's pick, crop/tint — so the prepared file exists before HTML
   generation.
3. Generate `conteudos/<YYYY-MM-DD>-<slug>/carousel.html` via Python
   (`Path.write_text`). Follow every rule in:
   - `references/images.md`
   - `references/photo-sourcing.md` (if photos are involved)
   - `references/design-system.md`
4. **Inject the edit panel** per `references/edit-panel.md`. Every text element
   that the user is likely to tweak gets a `data-edit-id="slideN-role"`
   attribute.
5. Tell the user the file path and instruct them to open it in a browser to
   review and edit.

### Phase 4 — Review & edit

The user opens the HTML, tweaks copy in the side panel, and clicks **"Baixar
HTML"** to download a clean `carousel.html`. They place that file at
`conteudos/<YYYY-MM-DD>-<slug>/carousel.html` (overwrite).

You may still iterate via chat per the original review rule:

> Generate the HTML preview first — never jump directly to export. Show the
> preview and ask: **"Quais slides precisam de ajuste antes de exportar?"**
> Fix only the mentioned slides — never regenerate the entire carousel unless
> the direction fundamentally changes. Only proceed to export when the user
> explicitly confirms approval (e.g., "pode exportar", "aprovado", "ok").

### Phase 5 — Export

Only after explicit approval ("pode exportar" / "aprovado" / "ok"):

1. Verify the clean HTML at `conteudos/<YYYY-MM-DD>-<slug>/carousel.html` has
   no `#carousel-editor` element. If it does, ask the user to download via the
   panel first (see `references/edit-panel.md` safety check).
2. Run the Playwright export per `references/export.md`. Write PNGs to
   `conteudos/<YYYY-MM-DD>-<slug>/slides/`.
3. Report the output folder back to the user.

---

## Non-negotiables

- Never edit or paraphrase the contents of `references/images.md`,
  `references/photo-sourcing.md`, or `references/export.md`.
  `references/design-system.md` is the editable design source — its rules
  are authoritative as currently written.
- Never source a photo generically. Every photo must be picked for that
  specific slide's message and checked against `brand-kit.json`'s tone and
  palette before it's downloaded — see `references/photo-sourcing.md`.
- Always generate HTML via Python (`Path.write_text`), never shell.
- Always embed user images as base64 `data:` URIs.
- Always keep `.ig-frame` at exactly 420px.
- Never skip the review step. Never export without explicit approval.
- **Universal centralization:** every slide uses `justify-content: center`
  with the content block at `max-width: 360px; margin: 0 auto` and slide
  padding `64px 36px 76px`. Never align content to `flex-end`, regardless of
  density. Hero/CTA are not special-cased — they share the same layout.
- **Real logo:** if `brand-kit.json` has `logo.type` in `["svg", "image"]`,
  render the actual logo (SVG inline or `<img>` base64) in the Hero and CTA
  slides and as a small watermark (20px, opacity 0.5, top-left) on every
  intermediate slide. The initial-in-circle is a fallback only — never use
  it when a real logo file is available.
- **Logo legibility:** when more than one color variant exists, always use
  the one that reads best against that slide's actual background, and
  double-check before rendering that a light/white variant is never placed
  over a light area and a dark/colored variant is never placed over a dark
  area — see the legibility check in `references/design-system.md`.
- **Editorial baseline:** every carousel must include (a) layered radial
  backgrounds (never flat `LIGHT_BG`/`DARK_BG`), (b) the grain SVG overlay,
  (c) corner mark + slide watermark on every slide, (d) at least one
  Big-Stat or Pull-quote component somewhere, (e) one mixed-weight
  headline. These are visual minimums, not options.
