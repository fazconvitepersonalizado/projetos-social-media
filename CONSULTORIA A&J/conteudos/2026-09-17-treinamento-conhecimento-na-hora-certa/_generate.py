# -*- coding: utf-8 -*-
import base64
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]

brand = json.loads((ROOT / "brand-kit.json").read_text(encoding="utf-8"))
D = brand["derived"]
BRAND_PRIMARY = D["BRAND_PRIMARY"]
BRAND_LIGHT = D["BRAND_LIGHT"]
BRAND_DARK = D["BRAND_DARK"]
LIGHT_BG = D["LIGHT_BG"]
LIGHT_BORDER = D["LIGHT_BORDER"]
DARK_BG = D["DARK_BG"]
HEADING_FONT = brand["heading_font"]
BODY_FONT = brand["body_font"]
BRAND_NAME = brand["brand_name"]
HANDLE = brand["instagram_handle"]

TOTAL = 4

logo_bytes = (ROOT / "logo" / "icon.png").read_bytes()
LOGO_URI = "data:image/png;base64," + base64.b64encode(logo_bytes).decode()

photo2_bytes = (BASE / "assets" / "edited" / "slide2-photo.jpg").read_bytes()
PHOTO2_URI = "data:image/jpeg;base64," + base64.b64encode(photo2_bytes).decode()

photo3_bytes = (BASE / "assets" / "edited" / "slide3-photo.jpg").read_bytes()
PHOTO3_URI = "data:image/jpeg;base64," + base64.b64encode(photo3_bytes).decode()

SECONDARY = "#8A8580"


def swipe_arrow(kind, is_last):
    if is_last:
        return ""
    is_light = kind == "light"
    bg = "rgba(0,0,0,0.06)" if is_light else "rgba(255,255,255,0.08)"
    stroke = "rgba(0,0,0,0.25)" if is_light else "rgba(255,255,255,0.35)"
    return (
        '<div style="position:absolute;right:0;top:0;bottom:0;width:48px;z-index:9;'
        f'display:flex;align-items:center;justify-content:center;background:linear-gradient(to right,transparent,{bg});">'
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none">'
        f'<path d="M9 6l6 6-6 6" stroke="{stroke}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
        "</svg></div>"
    )


def corner_mark(kind):
    accent = {"light": BRAND_PRIMARY, "dark": BRAND_LIGHT}.get(kind, "rgba(255,255,255,0.6)")
    return (
        '<svg width="12" height="12" viewBox="0 0 12 12" style="position:absolute;top:24px;right:24px;z-index:5;">'
        f'<path d="M6 0v12M0 6h12" stroke="{accent}" stroke-width="1.2"/></svg>'
    )


def grain():
    return (
        '<svg class="grain" aria-hidden="true" style="position:absolute;inset:0;width:100%;height:100%;'
        'pointer-events:none;opacity:0.05;mix-blend-mode:overlay;z-index:1;">'
        '<filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/></filter>'
        '<rect width="100%" height="100%" filter="url(#g)"/></svg>'
    )


def gradient_scrim():
    return (
        '<div style="position:absolute;inset:0;z-index:1;pointer-events:none;background:'
        "radial-gradient(circle at 15% 20%, rgba(0,0,0,0.48) 0%, transparent 60%),"
        'rgba(0,0,0,0.12);"></div>'
    )


def logo_watermark():
    return (
        '<div style="position:absolute;top:20px;left:28px;opacity:0.5;z-index:5;">'
        f'<img src="{LOGO_URI}" style="width:20px;height:20px;object-fit:contain;display:block;">'
        "</div>"
    )


def logo_watermark_chip(chip_bg):
    return (
        '<div style="position:absolute;top:16px;left:24px;z-index:5;'
        f'background:{chip_bg};border-radius:8px;padding:7px;display:inline-flex;">'
        f'<img src="{LOGO_URI}" style="width:20px;height:20px;object-fit:contain;display:block;">'
        "</div>"
    )


def logo_lockup(size, font_size, text_color):
    return (
        '<div style="display:flex;align-items:center;justify-content:center;gap:10px;margin-bottom:20px;">'
        f'<img src="{LOGO_URI}" style="width:{size}px;height:{size}px;object-fit:contain;">'
        f'<span class="sans" style="font-size:{font_size}px;font-weight:600;letter-spacing:0.5px;color:{text_color};">{BRAND_NAME}</span>'
        "</div>"
    )


def bg_style(kind):
    if kind == "light":
        return (
            f"background:radial-gradient(circle at 20% 0%, {BRAND_PRIMARY}1F 0%, transparent 45%),"
            f"radial-gradient(circle at 100% 100%, {BRAND_LIGHT}24 0%, transparent 50%),{LIGHT_BG};"
        )
    if kind == "dark":
        return (
            f"background:radial-gradient(circle at 80% 10%, {BRAND_PRIMARY}3D 0%, transparent 40%),"
            f"radial-gradient(circle at 0% 90%, {BRAND_DARK}66 0%, transparent 55%),{DARK_BG};"
        )
    if kind == "gradient":
        return (
            f"background:radial-gradient(circle at 15% 20%, {BRAND_LIGHT} 0%, transparent 55%),"
            f"radial-gradient(circle at 90% 10%, {BRAND_PRIMARY} 0%, transparent 50%),"
            f"radial-gradient(circle at 60% 100%, {BRAND_DARK} 0%, transparent 65%),{BRAND_PRIMARY};"
        )
    return f"background:{DARK_BG};"


def tag_color(kind):
    return {"light": BRAND_PRIMARY, "dark": BRAND_LIGHT}.get(kind, "rgba(255,255,255,0.6)")


def headline_color(kind):
    return BRAND_DARK if kind == "light" else "#fff"


def body_color(kind):
    return SECONDARY if kind == "light" else "rgba(255,255,255,0.75)"


def tag_html(n, text, kind):
    return (
        f'<span class="sans" data-edit-id="slide{n}-tag" style="display:inline-block;font-size:10px;'
        f'font-weight:600;letter-spacing:2px;color:{tag_color(kind)};margin-bottom:16px;">{text}</span>'
    )


def hairline(kind):
    return f'<div style="width:40px;height:1px;background:{tag_color(kind)};opacity:0.6;margin:6px 0 18px;"></div>'


def headline_html(n, html, kind, size="36px", line_height="1.12"):
    return (
        f'<h1 class="serif" data-edit-id="slide{n}-headline" style="font-size:{size};font-weight:600;'
        f'letter-spacing:-0.5px;line-height:{line_height};color:{headline_color(kind)};margin:0 0 16px;">{html}</h1>'
    )


def body_html(n, text, kind, role="body", size="17px"):
    return (
        f'<p class="sans" data-edit-id="slide{n}-{role}" style="font-size:{size};line-height:1.5;'
        f'color:{body_color(kind)};margin:0;">{text}</p>'
    )


def content_wrapper(inner):
    return (
        '<div style="position:relative;z-index:2;height:100%;display:flex;flex-direction:column;'
        'justify-content:center;padding:64px 36px 56px;box-sizing:border-box;">'
        f'<div style="max-width:360px;margin:0 auto;width:100%;">{inner}</div></div>'
    )


def slide_wrapper(n, kind, extra_bg_layers, decorative, content, is_last=False):
    style = bg_style(kind)
    return (
        f'<div class="slide" style="position:relative;width:420px;height:525px;flex:none;overflow:hidden;{style}">'
        f"{extra_bg_layers}{grain()}{decorative}{content}"
        f"{swipe_arrow(kind, is_last)}"
        "</div>"
    )


# ---------------------------------------------------------------------------
# Slide 1 - Hero (brand gradient)
# ---------------------------------------------------------------------------
slide1_content = content_wrapper(
    logo_lockup(32, 13, "#fff")
    + tag_html(1, "TREINAMENTO COM PROPÓSITO", "gradient")
    + hairline("gradient")
    + headline_html(
        1,
        '<span style="font-weight:300;">Treinamento não é só</span> '
        f'<span style="font-weight:600;font-style:italic;color:{BRAND_LIGHT};">certificado.</span>',
        "gradient",
        size="32px",
    )
    + body_html(
        1,
        "É conhecimento que pode fazer diferença na hora certa.",
        "gradient",
        role="subhead",
    )
)
slide1 = slide_wrapper(1, "gradient", "", gradient_scrim() + corner_mark("gradient"), slide1_content)

# ---------------------------------------------------------------------------
# Slide 2 - Context (full-bleed photo, soft/faded) + pull-quote
# ---------------------------------------------------------------------------
slide2_photo_layer = (
    f'<img src="{PHOTO2_URI}" style="position:absolute;inset:0;width:100%;height:100%;'
    'object-fit:cover;opacity:0.85;z-index:0;">'
    '<!-- foto: pexels.com/photo/team-of-engineers-reviewing-construction-plans-indoors-37198881 (Harrun Muhammad) -->'
    '<div style="position:absolute;inset:0;z-index:1;pointer-events:none;background:'
    f"linear-gradient(to top, {DARK_BG}F2 0%, {DARK_BG}D9 34%, {DARK_BG}66 64%, {DARK_BG}26 100%);"
    '"></div>'
)
slide2_quote = (
    f'<blockquote style="border-left:2px solid {BRAND_LIGHT};padding:8px 0 8px 20px;margin:20px 0 0;">'
    '<p class="serif" data-edit-id="slide2-quote" style="font-size:24px;font-style:italic;font-weight:400;'
    'line-height:1.35;color:#fff;margin:0;">"Um trabalhador bem orientado entende melhor os riscos da sua '
    'atividade e sabe como agir diante deles."</p>'
    "</blockquote>"
)
slide2_content = content_wrapper(
    tag_html(2, "POR QUE ISSO IMPORTA", "dark")
    + hairline("dark")
    + slide2_quote
)
slide2 = slide_wrapper(
    2, "photo", slide2_photo_layer,
    corner_mark("dark") + logo_watermark_chip(f"{DARK_BG}CC"),
    slide2_content,
)

# ---------------------------------------------------------------------------
# Slide 3 - Checklist (light)
# ---------------------------------------------------------------------------
def checklist_item(n, i, label):
    return (
        '<div style="display:flex;align-items:center;gap:14px;padding:6px 0;">'
        f'<span style="flex:none;width:28px;height:28px;border-radius:9px;background:{BRAND_PRIMARY}1A;'
        f'color:{BRAND_PRIMARY};display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;">✓</span>'
        f'<span class="sans" data-edit-id="slide{n}-item-{i}" style="font-size:17px;font-weight:600;color:{BRAND_DARK};">{label}</span>'
        "</div>"
    )


slide3_photo_card = (
    '<div style="width:100%;border-radius:16px;overflow:hidden;box-shadow:0 12px 32px rgba(0,0,0,0.18);margin-bottom:14px;">'
    f'<img src="{PHOTO3_URI}" style="display:block;width:100%;height:130px;object-fit:cover;">'
    "</div>"
    '<!-- foto: pexels.com/photo/person-pointing-on-documents-8487392 (Kindel Media) -->'
)
checklist = ["Claro", "Prático", "Adequado à atividade", "Aplicável à rotina"]
slide3_list = '<div style="display:flex;flex-direction:column;gap:2px;margin-top:2px;">' + "".join(
    checklist_item(3, i + 1, label) for i, label in enumerate(checklist)
) + "</div>"
slide3_content = content_wrapper(
    tag_html(3, "TREINAMENTO PRECISA SER", "light").replace("margin-bottom:16px;", "margin-bottom:10px;")
    + slide3_photo_card
    + headline_html(3, "Por isso, treinamento precisa ser:", "light", size="22px", line_height="1.3").replace(
        "margin:0 0 16px;", "margin:0 0 10px;"
    )
    + slide3_list
)
slide3 = slide_wrapper(3, "light", "", corner_mark("light") + logo_watermark(), slide3_content)

# ---------------------------------------------------------------------------
# Slide 4 - CTA (gradient)
# ---------------------------------------------------------------------------
slide4_content = content_wrapper(
    logo_lockup(48, 15, "#fff")
    + '<div style="text-align:center;">'
    + headline_html(4, "Porque segurança começa com conhecimento.", "dark", size="32px").replace(
        "margin:0 0 16px;", "margin:0 0 16px;text-align:center;"
    )
    + body_html(
        4,
        "E conhecimento precisa sair da sala de treinamento e chegar à rotina.",
        "dark",
        role="subhead",
    ).replace("margin:0;", "margin:0 0 26px;text-align:center;")
    + f'<p class="sans" style="font-size:13.5px;color:rgba(255,255,255,0.85);letter-spacing:1px;text-align:center;margin:0;">{HANDLE}</p>'
    + "</div>"
)
slide4 = slide_wrapper(4, "gradient", "", gradient_scrim() + corner_mark("gradient"), slide4_content, is_last=True)

SLIDES_HTML = slide1 + slide2 + slide3 + slide4

SLIDE_LABELS = {1: "Hero", 2: "Contexto", 3: "Checklist", 4: "CTA"}

FONT_LINK = (
    "https://fonts.googleapis.com/css2?"
    "family=Lora:ital,wght@0,300;0,400;0,600;0,700;1,400;1,600&"
    "family=Poppins:wght@400;500;600&display=swap"
)

DOTS = "".join(
    f'<span class="ig-dot{" active" if i == 0 else ""}" data-dot="{i}" '
    f'style="width:{6 if i==0 else 5}px;height:{6 if i==0 else 5}px;border-radius:50%;'
    f'background:{"#262626" if i==0 else "#c7c7c7"};display:inline-block;margin:0 3px;"></span>'
    for i in range(TOTAL)
)

HTML = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Treinamento não é só certificado | {BRAND_NAME}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONT_LINK}" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; background: #efeee9; display: flex; gap: 24px; align-items: flex-start;
    padding: 24px; font-family: 'Poppins', sans-serif;
  }}
  .serif {{ font-family: '{HEADING_FONT}', serif; }}
  .sans {{ font-family: '{BODY_FONT}', sans-serif; }}
  .ig-frame {{
    width: 420px; flex: none; background: #fff; border-radius: 16px; overflow: hidden;
    box-shadow: 0 8px 40px rgba(0,0,0,0.12); border: 1px solid #efefef;
  }}
  .ig-header {{ display:flex; align-items:center; gap:10px; padding:12px 14px; }}
  .ig-avatar {{
    width:36px; height:36px; border-radius:50%; background:{BRAND_PRIMARY}; flex:none;
    display:flex; align-items:center; justify-content:center; padding:5px; overflow:hidden;
  }}
  .ig-avatar img {{ width:100%; height:100%; object-fit:contain; }}
  .ig-header-text {{ display:flex; flex-direction:column; line-height:1.2; }}
  .ig-header-handle {{ font-size:13px; font-weight:600; color:#262626; }}
  .ig-header-sub {{ font-size:11px; color:#8e8e8e; }}
  .carousel-viewport {{ width:420px; height:525px; overflow:hidden; position:relative; cursor:grab; }}
  .carousel-track {{ display:flex; width:{420 * TOTAL}px; height:525px; transition: transform 0.35s ease; }}
  .ig-dots {{ display:flex; align-items:center; justify-content:center; padding:10px 0; }}
  .ig-actions {{ display:flex; align-items:center; gap:14px; padding:6px 14px; }}
  .ig-actions svg {{ display:block; }}
  .ig-caption {{ padding:2px 14px 16px; font-size:13px; color:#262626; line-height:1.4; }}
  .ig-caption b {{ font-weight:600; }}
  .ig-caption .ts {{ display:block; margin-top:6px; font-size:10px; color:#8e8e8e; letter-spacing:0.5px; text-transform:uppercase; }}
</style>
</head>
<body>

<div class="ig-frame">
  <div class="ig-header">
    <div class="ig-avatar"><img src="{LOGO_URI}"></div>
    <div class="ig-header-text">
      <span class="ig-header-handle">{HANDLE.lstrip('@')}</span>
      <span class="ig-header-sub">Treinamento & Segurança do Trabalho</span>
    </div>
  </div>
  <div class="carousel-viewport">
    <div class="carousel-track">
      {SLIDES_HTML}
    </div>
  </div>
  <div class="ig-dots">{DOTS}</div>
  <div class="ig-actions">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M12 21s-7.5-4.9-10-9.2C.3 8.6 1.7 5 5.2 4.2 7.4 3.7 9.6 4.7 12 7.3c2.4-2.6 4.6-3.6 6.8-3.1 3.5.8 4.9 4.4 3.2 7.6C19.5 16.1 12 21 12 21z" stroke="#262626" stroke-width="1.5"/></svg>
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v10z" stroke="#262626" stroke-width="1.5"/></svg>
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M22 2 11 13M22 2l-7 20-4-9-9-4 20-7z" stroke="#262626" stroke-width="1.5" stroke-linejoin="round"/></svg>
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style="margin-left:auto;"><path d="M6 3h12v18l-6-4-6 4V3z" stroke="#262626" stroke-width="1.5" stroke-linejoin="round"/></svg>
  </div>
  <div class="ig-caption">
    <b>{HANDLE.lstrip('@')}</b> Treinamento não é só certificado, é conhecimento aplicado na hora certa. Arraste para ver. 👉
    <span class="ts">2 HORAS ATRÁS</span>
  </div>
</div>

<aside id="carousel-editor" style="
  width:360px;max-height:90vh;overflow:auto;
  background:#fff;border:1px solid #e5e5e5;border-radius:14px;
  padding:18px;font-family:system-ui,sans-serif;font-size:13px;
  box-shadow:0 4px 24px rgba(0,0,0,0.06);position:sticky;top:24px;
">
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;">
    <strong style="font-size:14px;">Editar carrossel - Treinamento</strong>
    <button id="ce-download" style="
      background:#111;color:#fff;border:0;border-radius:8px;
      padding:8px 14px;font-weight:600;cursor:pointer;font-size:12px;">
      Baixar HTML
    </button>
  </div>
  <div id="ce-groups"></div>
  <p style="margin-top:14px;color:#888;font-size:11px;line-height:1.4;">
    O download remove o painel e gera um <code>carousel.html</code> limpo,
    pronto para exportar. Substitua o arquivo em
    <code>conteudos/2026-09-17-treinamento-conhecimento-na-hora-certa/carousel.html</code>.
  </p>
</aside>

<script>
(function(){{
  const track = document.querySelector('.carousel-track');
  const viewport = document.querySelector('.carousel-viewport');
  const dots = Array.from(document.querySelectorAll('.ig-dot'));
  const total = {TOTAL};
  const width = 420;
  let index = 0;
  let startX = 0, currentX = 0, dragging = false;

  function goTo(i) {{
    index = Math.max(0, Math.min(total - 1, i));
    track.style.transform = 'translateX(' + (-index * width) + 'px)';
    dots.forEach((d, di) => {{
      d.style.background = di === index ? '#262626' : '#c7c7c7';
      d.style.width = di === index ? '6px' : '5px';
      d.style.height = di === index ? '6px' : '5px';
    }});
  }}

  viewport.addEventListener('pointerdown', (e) => {{
    dragging = true; startX = e.clientX; currentX = 0;
    track.style.transition = 'none';
    viewport.style.cursor = 'grabbing';
    viewport.setPointerCapture(e.pointerId);
  }});
  viewport.addEventListener('pointermove', (e) => {{
    if (!dragging) return;
    currentX = e.clientX - startX;
    track.style.transform = 'translateX(' + (-index * width + currentX) + 'px)';
  }});
  function endDrag() {{
    if (!dragging) return;
    dragging = false;
    track.style.transition = 'transform 0.35s ease';
    viewport.style.cursor = 'grab';
    if (currentX < -60) goTo(index + 1);
    else if (currentX > 60) goTo(index - 1);
    else goTo(index);
    currentX = 0;
  }}
  viewport.addEventListener('pointerup', endDrag);
  viewport.addEventListener('pointerleave', endDrag);
  dots.forEach((d, di) => d.addEventListener('click', () => goTo(di)));
}})();
</script>

<script id="carousel-editor-script">
(function(){{
  const SLIDE_LABELS = {json.dumps(SLIDE_LABELS)};
  const groups = document.getElementById('ce-groups');
  const slides = {{}};
  document.querySelectorAll('[data-edit-id]').forEach(el => {{
    const id = el.getAttribute('data-edit-id');
    const m = id.match(/^slide(\\d+)-(.+)$/);
    if(!m) return;
    const n = +m[1];
    (slides[n] = slides[n] || []).push({{id, role:m[2], el}});
  }});
  Object.keys(slides).sort((a,b)=>+a-+b).forEach(n => {{
    const det = document.createElement('details');
    det.open = true;
    det.style.cssText = 'margin-bottom:8px;border:1px solid #eee;border-radius:8px;padding:8px 10px;';
    det.innerHTML = `<summary style="cursor:pointer;font-weight:600;">Slide ${{n}} - ${{SLIDE_LABELS[n]||''}}</summary>`;
    slides[n].forEach(({{id, role, el}}) => {{
      const wrap = document.createElement('div');
      wrap.style.cssText = 'margin:8px 0;';
      const label = document.createElement('label');
      label.textContent = role;
      label.style.cssText = 'display:block;color:#666;font-size:11px;margin-bottom:4px;text-transform:uppercase;letter-spacing:1px;';
      const ta = document.createElement('textarea');
      ta.value = el.textContent.trim();
      ta.style.cssText = 'width:100%;min-height:48px;border:1px solid #ddd;border-radius:6px;padding:8px;font:inherit;resize:vertical;';
      ta.addEventListener('input', () => {{ el.textContent = ta.value; }});
      wrap.append(label, ta);
      det.append(wrap);
    }});
    groups.append(det);
  }});
  document.getElementById('ce-download').addEventListener('click', () => {{
    const clone = document.documentElement.cloneNode(true);
    clone.querySelector('#carousel-editor')?.remove();
    clone.querySelector('#carousel-editor-script')?.remove();
    const body = clone.querySelector('body');
    if (body) body.removeAttribute('style');
    const html = '<!doctype html>\\n' + clone.outerHTML;
    const blob = new Blob([html], {{type:'text/html'}});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'carousel.html';
    document.body.appendChild(a); a.click(); a.remove();
  }});
}})();
</script>

</body>
</html>
"""

out_path = BASE / "carousel.html"
out_path.write_text(HTML, encoding="utf-8")
print("written:", out_path, len(HTML), "chars")
