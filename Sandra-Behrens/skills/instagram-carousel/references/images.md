# Handling User-Provided Images

**This section applies from the very first HTML generation — not only during export.**

When the user provides an image file path (e.g., `/home/user/gestante.png`, `/mnt/user-data/uploads/foto.jpg`):

### ⚠️ Critical Rules

1. **NEVER use relative paths** (`gestante.png`) — they break in every browser context except the exact folder the HTML lives in.
2. **NEVER use `background: url(filepath)`** — leads to 1.5MB+ base64 inline strings that crash the browser parser.
3. **ALWAYS embed as base64 `data:` URI** — works in preview, export, and any environment.
4. **ALWAYS generate the HTML via Python** (`Path.write_text()`) — shell heredocs interpolate `$` and backticks, corrupting base64 strings.

### Step-by-step: embed an image

```bash
# 1. Check the actual file format (extension may lie)
file /path/to/image.png
```

```python
import base64
from pathlib import Path

# 2. Read and encode
img_path = Path("/path/to/image.png")
# Use "image/jpeg" if `file` command says JPEG, else "image/png"
mime = "image/jpeg"  # or "image/png"
b64 = base64.b64encode(img_path.read_bytes()).decode()
data_uri = f"data:{mime};base64,{b64}"

# 3. Inject into HTML template as a Python variable — never via shell
html = f"""
<div style="position:relative;width:100%;height:100%;">
  <img src="{data_uri}"
       style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;">
  <div style="position:absolute;inset:0;background:rgba(255,255,255,0.35);z-index:1;"></div>
  <!-- slide content goes here, z-index:2 -->
</div>
"""

Path("/home/claude/carousel.html").write_text(html, encoding="utf-8")
```

### Image as slide background (most common use)

```html
<!-- Inside the slide div, before any content -->
<img src="{data_uri}"
     style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;">
<!-- Semi-transparent overlay so text stays readable -->
<div style="position:absolute;inset:0;background:rgba(255,255,255,0.35);z-index:1;"></div>
<!-- All slide content must have z-index:2 or higher -->
```

For dark slides, use `rgba(0,0,0,0.45)` as the overlay instead.

### Common image mistakes to avoid

| Mistake | What goes wrong | Fix |
|---------|----------------|-----|
| `<img src="gestante.png">` | Broken image — relative path only works if HTML and image share the same folder | Always use base64 `data:` URI |
| `background: url('data:...')` inline with 1.5MB base64 | Browser parser crash, 1.3M token context | Use `<img>` tag with `object-fit:cover` |
| Generating HTML via shell `echo` or heredoc | `$` and backtick characters in base64 get interpolated and corrupt the string | Always use Python `Path.write_text()` |
| Assuming `.png` extension = PNG format | File may actually be JPEG; wrong MIME type breaks rendering | Run `file` command to detect actual format |
