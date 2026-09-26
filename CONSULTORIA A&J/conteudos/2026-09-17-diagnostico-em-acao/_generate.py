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
DARK_BG = D["DARK_BG"]
HEADING_FONT = brand["heading_font"]
BODY_FONT = brand["body_font"]
BRAND_NAME = brand["brand_name"]
HANDLE = brand["instagram_handle"]

TOTAL = 5
SECONDARY = "#8A8580"

logo_bytes = (ROOT / "logo" / "icon.png").read_bytes()
LOGO_URI = "data:image/png;base64," + base64.b64encode(logo_bytes).decode()

photo1_bytes = (BASE / "assets" / "edited" / "slide1-photo.jpg").read_bytes()
PHOTO1_URI = "data:image/jpeg;base64," + base64.b64encode(photo1_bytes).decode()

photo4_bytes = (BASE / "assets" / "edited" / "slide4-photo.jpg").read_bytes()
PHOTO4_URI = "data:image/jpeg;base64," + base64.b64encode(photo4_bytes).decode()


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


def logo_chip(inner_img_html, kind):
    # Small tight background chip behind every logo instance (hero/watermark/CTA),
    # using A&J's own derived tokens so the logo reads on any slide background.
    bg = f"{LIGHT_BG}E6" if kind == "light" else f"{DARK_BG}59"
    return f'<div style="display:inline-flex;background:{bg};border-radius:7px;padding:6px;">{inner_img_html}</div>'


def logo_watermark(kind):
    img = f'<img src="{LOGO_URI}" style="width:20px;height:20px;object-fit:contain;display:block;">'
    return f'<div style="position:absolute;top:18px;left:22px;z-index:5;">{logo_chip(img, kind)}</div>'


def logo_lockup(size, font_size, text_color, kind):
    img = f'<img src="{LOGO_URI}" style="width:{size}px;height:{size}px;object-fit:contain;display:block;">'
    return (
        '<div style="display:flex;align-items:center;justify-content:center;gap:10px;margin-bottom:20px;">'
        f'{logo_chip(img, kind)}'
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
    return SECONDARY if kind == "light" else "rgba(255,255,255,0.78)"


def tag_html(n, text, kind):
    return (
        f'<span class="sans" data-edit-id="slide{n}-tag" style="display:inline-block;font-size:10px;'
        f'font-weight:600;letter-spacing:2px;color:{tag_color(kind)};margin-bottom:16px;">{text}</span>'
    )


def hairline(kind, margin="6px 0 18px"):
    return f'<div style="width:40px;height:1px;background:{tag_color(kind)};opacity:0.6;margin:{margin};"></div>'


def headline_html(n, html, kind, size="32px", extra=""):
    return (
        f'<h1 class="serif" data-edit-id="slide{n}-headline" style="font-size:{size};font-weight:600;'
        f'letter-spacing:-0.5px;line-height:1.2;color:{headline_color(kind)};margin:0 0 14px;{extra}">{html}</h1>'
    )


def body_html(n, text, kind, role="body", size="15px", extra=""):
    return (
        f'<p class="sans" data-edit-id="slide{n}-{role}" style="font-size:{size};line-height:1.5;'
        f'color:{body_color(kind)};margin:0;{extra}">{text}</p>'
    )


def content_wrapper(inner):
    return (
        '<div style="position:relative;z-index:2;height:100%;display:flex;flex-direction:column;'
        'justify-content:center;padding:64px 36px 76px;box-sizing:border-box;">'
        f'<div style="max-width:360px;margin:0 auto;width:100%;">{inner}</div></div>'
    )


def slide_wrapper(n, kind, extra_bg_layers, decorative, content, is_last=False):
    style = bg_style(kind) if kind != "photo" else f"background:{DARK_BG};"
    pb_kind = "dark" if kind == "photo" else kind
    return (
        f'<div class="slide" style="position:relative;width:420px;height:525px;flex:none;overflow:hidden;{style}">'
        f"{extra_bg_layers}{grain()}{decorative}{content}"
        f"{swipe_arrow(pb_kind, is_last)}"
        "</div>"
    )


# ---------------------------------------------------------------------------
# Slide 1 — Hero (photo full-bleed): "Documento pronto não significa problema resolvido."
# ---------------------------------------------------------------------------
slide1_photo_layer = (
    f'<img src="{PHOTO1_URI}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;">'
    '<!-- foto: pexels.com/photo/colleagues-looking-at-a-document-5918192 (Jack Sparrow) -->'
    '<div style="position:absolute;inset:0;z-index:1;pointer-events:none;background:'
    f"linear-gradient(to top, {DARK_BG}F2 0%, {DARK_BG}D9 42%, {DARK_BG}00 80%);"
    '"></div>'
)
slide1_content = content_wrapper(
    logo_lockup(32, 13, "#fff", "dark")
    + tag_html(1, "DO DIAGNÓSTICO À AÇÃO", "gradient")
    + hairline("gradient")
    + headline_html(
        1,
        '<span style="font-weight:300;">Documento pronto não significa</span> '
        f'<span style="font-weight:600;font-style:italic;color:{BRAND_LIGHT};">problema resolvido.</span>',
        "dark",
        size="34px",
    )
)
slide1 = slide_wrapper(1, "photo", slide1_photo_layer, corner_mark("gradient"), slide1_content)

# ---------------------------------------------------------------------------
# Slide 2 — Light: "Nosso trabalho é transformar diagnóstico em ação."
# ---------------------------------------------------------------------------
slide2_content = content_wrapper(
    tag_html(2, "NOSSO JEITO DE TRABALHAR", "light")
    + hairline("light")
    + body_html(
        2,
        "Na A&J, não acreditamos em soluções que ficam apenas no papel.",
        "light",
        role="subhead",
        size="17px",
        extra="margin-bottom:18px;",
    )
    + headline_html(
        2,
        '<span style="font-weight:300;">Nosso trabalho é transformar diagnóstico em </span>'
        f'<span style="font-weight:600;font-style:italic;color:{BRAND_PRIMARY};">ação.</span>',
        "light",
        size="30px",
    )
)
slide2 = slide_wrapper(2, "light", "", corner_mark("light") + logo_watermark("light"), slide2_content)

# ---------------------------------------------------------------------------
# Slide 3 — Gradient: "melhorias viáveis, aplicáveis e possíveis de acompanhar"
# ---------------------------------------------------------------------------
def quality_row(n, i, word):
    return (
        '<div style="display:flex;align-items:center;gap:12px;padding:9px 0;">'
        f'<span style="flex:none;width:24px;height:24px;border-radius:50%;background:rgba(255,255,255,0.16);'
        'display:flex;align-items:center;justify-content:center;">'
        '<svg width="12" height="10" viewBox="0 0 12 10" fill="none"><path d="M1 5l3.2 3.2L11 1" stroke="#fff" '
        'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></span>'
        f'<span class="serif" data-edit-id="slide3-item-{i}" style="font-size:19px;font-weight:600;'
        f'font-style:italic;color:#fff;">{word}</span></div>'
    )

slide3_qualities = (
    '<div style="background:rgba(255,255,255,0.08);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);'
    'border:1px solid rgba(255,255,255,0.14);border-radius:16px;padding:6px 20px;margin-top:20px;">'
    + quality_row(3, 1, "Viáveis")
    + '<div style="height:1px;background:rgba(255,255,255,0.14);"></div>'
    + quality_row(3, 2, "Aplicáveis")
    + '<div style="height:1px;background:rgba(255,255,255,0.14);"></div>'
    + quality_row(3, 3, "Possíveis de acompanhar")
    + "</div>"
)
slide3_content = content_wrapper(
    tag_html(3, "COMO TRABALHAMOS", "gradient")
    + hairline("gradient")
    + headline_html(
        3,
        "Entendemos a realidade de cada empresa e propomos melhorias que sejam:",
        "dark",
        size="26px",
        extra="font-weight:500;",
    )
    + slide3_qualities
)
slide3 = slide_wrapper(3, "gradient", "", gradient_scrim() + corner_mark("gradient"), slide3_content)

# ---------------------------------------------------------------------------
# Slide 4 — Dark + framed photo card: "Continuamos junto."
# ---------------------------------------------------------------------------
slide4_card = (
    '<div style="width:100%;border-radius:16px;overflow:hidden;box-shadow:0 12px 32px rgba(0,0,0,0.28);margin:6px 0 20px;">'
    f'<img src="{PHOTO4_URI}" style="display:block;width:100%;height:196px;object-fit:cover;">'
    '<!-- foto: pexels.com/photo/couple-love-people-office-7979605 (Kindel Media) -->'
    "</div>"
)
slide4_content = content_wrapper(
    tag_html(4, "E DEPOIS DA ENTREGA?", "dark")
    + hairline("dark")
    + slide4_card
    + f'<p class="serif" data-edit-id="slide4-highlight" style="font-size:25px;font-weight:600;font-style:italic;'
    f'line-height:1.25;color:{BRAND_LIGHT};margin:0 0 12px;">Continuamos junto.</p>'
    + body_html(
        4,
        "Orientamos, esclarecemos dúvidas e acompanhamos a implementação das ações.",
        "dark",
        size="15.5px",
    )
)
slide4 = slide_wrapper(4, "dark", "", corner_mark("dark") + logo_watermark("dark"), slide4_content)

# ---------------------------------------------------------------------------
# Slide 5 — Gradient CTA
# ---------------------------------------------------------------------------
slide5_content = content_wrapper(
    logo_lockup(48, 15, "#fff", "gradient")
    + f'<div style="text-align:center;">'
    + body_html(
        5,
        "Nosso objetivo não é apenas entregar um documento.",
        "dark",
        role="subhead",
        size="17px",
        extra="text-align:center;margin-bottom:16px;",
    )
    + f'<p class="serif" data-edit-id="slide5-highlight" style="font-size:24px;font-weight:600;font-style:italic;'
    f'line-height:1.3;color:#fff;margin:0 0 22px;text-align:center;">É ajudar sua empresa a colocar as melhorias em prática.</p>'
    + hairline("gradient", margin="0 auto 20px").replace("width:40px", "width:40px")
    + f'<p class="serif" data-edit-id="slide5-tagline" style="font-size:20px;font-weight:500;font-style:italic;'
    f'color:#fff;margin:0 0 22px;text-align:center;">A&amp;J, soluções que saem do papel.</p>'
    + f'<span class="sans" data-edit-id="slide5-cta" style="display:inline-block;font-size:12px;font-weight:600;'
    f'letter-spacing:1.5px;color:rgba(255,255,255,0.65);">{HANDLE}</span>'
    + "</div>"
)
slide5 = slide_wrapper(5, "gradient", "", gradient_scrim() + corner_mark("gradient"), slide5_content, is_last=True)

SLIDES_HTML = slide1 + slide2 + slide3 + slide4 + slide5

SLIDE_LABELS = {1: "Capa", 2: "Nosso jeito", 3: "Como trabalhamos", 4: "Acompanhamento", 5: "CTA"}

FONT_LINK = (
    "https://fonts.googleapis.com/css2?"
    "family=Lora:ital,wght@0,300;0,400;0,500;0,600;1,400;1,500;1,600&"
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
<title>Diagnóstico em ação | {BRAND_NAME}</title>
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
      <span class="ig-header-sub">Diagnóstico em ação</span>
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
    <b>{HANDLE.lstrip('@')}</b> Documento pronto não é problema resolvido. A gente continua junto até virar prática. 🌱
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
    <strong style="font-size:14px;">Editar carrossel — Diagnóstico em ação</strong>
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
    <code>conteudos/2026-09-17-diagnostico-em-acao/carousel.html</code>.
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
    det.open = (+n <= 2);
    det.style.cssText = 'margin-bottom:8px;border:1px solid #eee;border-radius:8px;padding:8px 10px;';
    det.innerHTML = `<summary style="cursor:pointer;font-weight:600;">Slide ${{n}} — ${{SLIDE_LABELS[n]||''}}</summary>`;
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
