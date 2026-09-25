# Brand Kit — Step 1: Collect & Persist

## Persistence rules (project-level)

The brand kit is stored at the project root in `brand-kit.json`.

**Before asking the user for brand details, ALWAYS check if `brand-kit.json` exists at the project root.**

- If it exists and is valid JSON: load it, summarize the saved brand back to the user in 1–2 lines, and ask: **"Uso esse brand kit ou quer atualizar algo?"**. Only proceed to collect details if the user asks to update.
- If it does not exist: run the collection flow below, then write the answers to `brand-kit.json` before continuing.

`brand-kit.json` schema:

```json
{
  "brand_name": "string",
  "instagram_handle": "@string",
  "primary_color": "#hex",
  "logo": {
    "type": "svg | image | initial | none",
    "path": "/abs/path/to/logo.svg | logo.png | null",
    "variants": {
      "primary": "/abs/path/to/logo-color.svg",
      "white":   "/abs/path/to/logo-white.svg",
      "dark":    "/abs/path/to/logo-dark.svg"
    },
    "initial_fallback": "P"
  },
  "heading_font": "Google Font name",
  "body_font": "Google Font name",
  "tone": "professional | casual | playful | bold | minimal | ...",
  "language": "pt-BR",
  "default_format": "standard | listicle | tutorial | comparacao",
  "derived": {
    "BRAND_PRIMARY": "#hex",
    "BRAND_LIGHT":   "#hex",
    "BRAND_DARK":    "#hex",
    "LIGHT_BG":      "#hex",
    "LIGHT_BORDER":  "#hex",
    "DARK_BG":       "#hex"
  },
  "saved_at": "ISO-8601 timestamp"
}
```

**Logo field rules:**
- `type: "svg"` — `path` is required; `variants` optional. Files are stored at their original absolute paths; the kit only stores references.
- `type: "image"` — same, but `path` points to PNG/JPG. Embedded as base64 data-URI at render time.
- `type: "initial"` — `initial_fallback` is the single letter used in the circle (default: first letter of `brand_name`).
- `type: "none"` — same fallback as `initial`, but no letter shown (empty circle in `BRAND_PRIMARY`).
- Before saving, verify each path with `Path(p).exists()`. If a path does not exist, ask the user to fix it instead of silently dropping the variant.

Always write the file via Python `Path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")` — never via shell heredoc.

---

## Step 1: Collect Brand Details

Before generating, ask the user for the following (if not already provided):

1. **Brand name** — displayed on first and last slides
2. **Instagram handle** — shown in the IG frame header
3. **Primary brand color** — hex code, or describe and Claude picks one
4. **Logo** — accept any of:
   - Caminho absoluto para um **SVG** (será embutido inline no HTML)
   - Caminho absoluto para um **PNG / JPG** (será embutido como base64 data-URI)
   - Múltiplos caminhos, um por variante de cor (`primary` / `white` / `dark`) — pergunte explicitamente: "Você tem versões da logo em cor / branca / preta?"
   - "Inicial" — uma única letra no círculo `BRAND_PRIMARY` (fallback)
   - "Sem logo" — círculo `BRAND_PRIMARY` vazio
   Valide com `Path(p).exists()` antes de salvar.
5. **Font preference** — see typography table below, or specific Google Fonts
6. **Tone** — professional, casual, playful, bold, minimal, etc.
7. **Images** — profile photo, screenshots, product images, etc.
8. **Idioma dos slides** — default: **Português (BR)** unless specified otherwise
9. **Carousel format** — standard (7 slides) or alternate sequence (see sequences section)

If the user provides a website URL or brand assets, derive colors and style from those.

If the user says "make me a carousel about X" without brand details, ask before generating. Don't assume defaults.

---

After collecting (or confirming reuse), proceed to [[design-system.md]] which contains color derivation, typography and slide architecture rules.
