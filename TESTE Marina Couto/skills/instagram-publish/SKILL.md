---
name: instagram-publish
description: >
  Publishes an exported Instagram carousel (PNG slides already on disk) to
  Instagram via the Meta Graph API. Handles image hosting on catbox.moe,
  carousel container creation, and final publication in one shot.
  Use this skill whenever the user says "publicar no Instagram", "postar o
  carrossel", "fazer upload pro Instagram", "publicar os slides", "post to
  Instagram", or any variant — even if the slides were just exported by the
  instagram-carousel skill. Also trigger when the user says "publicar",
  "postar", "upload Instagram", or "subir no insta".
---

# Instagram Publish — Workflow Orchestrator

This skill publishes an already-exported carousel (PNG slides in
`conteudos/<YYYY-MM-DD>-<slug>/slides/`) to Instagram using the Meta Graph API.

**Prerequisites** (check before starting):
- Slides exported: `conteudos/<slug>/slides/slide_1.png` … `slide_N.png`
- Credentials in `.env` at the project root (see below)

---

## Reference modules

- `references/meta-api.md` — Meta Graph API flow, endpoints, error codes
- `scripts/publish_carousel.py` — Ready-to-run publish script (call directly)

---

## Project layout expected

```
conteudos/
└── <YYYY-MM-DD>-<slug>/
    └── slides/
        ├── slide_1.png
        ├── slide_2.png
        └── …
.env                    # INSTAGRAM_ACCOUNT_ID + INSTAGRAM_ACCESS_TOKEN
```

---

## Workflow (run in order)

### Step 1 — Locate the carousel

Find the target carousel folder. In order of precedence:
1. The user specified a folder/slug explicitly.
2. The folder that was just exported in this session.
3. The most recently modified folder under `conteudos/` that has a `slides/`
   subdirectory with at least one `.png` file.

Show the user which folder you found and ask for confirmation before publishing.

### Step 2 — Check credentials

Look for `.env` at the project root. Required variables:

```
INSTAGRAM_ACCOUNT_ID=<id>
INSTAGRAM_ACCESS_TOKEN=<token>
```

If either is missing, **stop** and tell the user exactly what to add and where.
Do not guess or hard-code credentials. See `references/meta-api.md` for how to
obtain them.

### Step 3 — Dry-run (optional but recommended)

Before publishing for real, offer a dry-run:

> "Quer fazer um dry-run primeiro? Ele valida as credenciais e conta os slides
> sem publicar nada."

If the user agrees (or types "dry-run" / "sim"), run the script with `--dry-run`.

### Step 4 — Publish

Run the publish script:

```bash
python skills/instagram-publish/scripts/publish_carousel.py \
  --slides-dir conteudos/<YYYY-MM-DD>-<slug>/slides \
  --caption "<caption text>"
```

The script:
1. Uploads each PNG to catbox.moe (anonymous, no auth needed).
2. Creates one Instagram media container per image.
3. Creates the carousel container.
4. Publishes it and returns the post ID.

### Step 5 — Report

After a successful publish, report:
- Post ID
- Instagram profile URL: `https://www.instagram.com/<handle>/`
- Number of slides published

If the publish fails, read the error from the script output, check
`references/meta-api.md` for the error code, and tell the user what went wrong
and how to fix it.

---

## Caption handling

- If the user provided caption text: pass it verbatim as `--caption`.
- If not: read the first line of text in slide 1's HTML (the hook/headline) and
  suggest it as the caption. Ask the user to approve before publishing.
- Never publish with an empty caption — Instagram requires it.

---

## Non-negotiables

- Never hard-code or log credentials.
- Never publish without user confirmation (at minimum: confirm the target folder).
- Always report the post ID after a successful publish so the user can verify.
- If the token is expired (error code 190), tell the user to refresh it via
  Meta's token refresh flow — do not retry automatically.
