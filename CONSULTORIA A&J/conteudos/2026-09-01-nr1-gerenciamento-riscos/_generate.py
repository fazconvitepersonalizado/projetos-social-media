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

TOTAL = 7

logo_bytes = (ROOT / "logo" / "icon.png").read_bytes()
LOGO_URI = "data:image/png;base64," + base64.b64encode(logo_bytes).decode()

photo_bytes = (BASE / "assets" / "edited" / "slide1-photo.jpg").read_bytes()
PHOTO_URI = "data:image/jpeg;base64," + base64.b64encode(photo_bytes).decode()

SECONDARY = "#8A8580"


def progress_bar(index, kind):
    is_light = kind == "light"
    fill = BRAND_PRIMARY if is_light else "#fff"
    track = "rgba(0,0,0,0.10)" if is_light else "rgba(255,255,255,0.18)"
    label = "rgba(0,0,0,0.35)" if is_light else "rgba(255,255,255,0.45)"
    segs = "".join(
        f'<div style="flex:1;height:3px;background:{fill if i <= index else track};border-radius:2px;"></div>'
        for i in range(TOTAL)
    )
    return (
        '<div style="position:absolute;bottom:0;left:0;right:0;padding:16px 28px 20px;'
        'z-index:10;display:flex;align-items:center;gap:10px;">'
        f'<div style="flex:1;display:flex;gap:4px;">{segs}</div>'
        f'<span style="font-size:11px;color:{label};font-weight:500;">{index + 1}/{TOTAL}</span>'
        "</div>"
    )


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


def headline_html(n, html, kind, size="36px"):
    return (
        f'<h1 class="serif" data-edit-id="slide{n}-headline" style="font-size:{size};font-weight:600;'
        f'letter-spacing:-0.5px;line-height:1.1;color:{headline_color(kind)};margin:0 0 14px;">{html}</h1>'
    )


def body_html(n, text, kind, role="body"):
    return (
        f'<p class="sans" data-edit-id="slide{n}-{role}" style="font-size:15px;line-height:1.5;'
        f'color:{body_color(kind)};margin:0;">{text}</p>'
    )


def content_wrapper(inner):
    return (
        '<div style="position:relative;z-index:2;height:100%;display:flex;flex-direction:column;'
        'justify-content:center;padding:64px 36px 76px;box-sizing:border-box;">'
        f'<div style="max-width:360px;margin:0 auto;width:100%;">{inner}</div></div>'
    )


def slide_wrapper(n, kind, extra_bg_layers, decorative, content, is_last=False):
    style = bg_style(kind) if kind != "photo" else f"background:{DARK_BG};"
    return (
        f'<div class="slide" style="position:relative;width:420px;height:525px;flex:none;overflow:hidden;{style}">'
        f"{extra_bg_layers}{grain()}{decorative}{content}"
        f"{progress_bar(n - 1, kind if kind != 'photo' else 'dark')}"
        f"{swipe_arrow(kind if kind != 'photo' else 'dark', is_last)}"
        "</div>"
    )


# ---------------------------------------------------------------------------
# Slide 1 — Hero (photo full-bleed)
# ---------------------------------------------------------------------------
slide1_photo_layer = (
    f'<img src="{PHOTO_URI}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;">'
    '<!-- foto: pexels.com/photo/trabalhador-da-construcao-civil-em-andaime-com-equipamento-de-seguranca-33914927 (Shivang Kushwaha) -->'
    '<div style="position:absolute;inset:0;z-index:1;pointer-events:none;background:'
    f"linear-gradient(to top, {DARK_BG}F2 0%, {DARK_BG}D9 40%, {DARK_BG}00 78%);"
    '"></div>'
)
slide1_content = content_wrapper(
    logo_lockup(32, 13, "#fff")
    + tag_html(1, "NR-1 · ATUALIZAÇÃO 2026", "gradient")
    + hairline("gradient")
    + headline_html(
        1,
        '<span style="font-weight:300;">Sua empresa já está</span> '
        f'<span style="font-weight:600;font-style:italic;color:{BRAND_LIGHT};">fora do prazo?</span>',
        "dark",
        size="44px",
    )
    + body_html(
        1,
        "Desde 26 de maio, o PGR precisa cobrir também os riscos psicossociais — não só os físicos.",
        "dark",
        role="subhead",
    )
)
slide1 = slide_wrapper(1, "photo", slide1_photo_layer, corner_mark("gradient"), slide1_content)

# ---------------------------------------------------------------------------
# Slide 2 — Problem (dark) + Big Stat
# ---------------------------------------------------------------------------
slide2_stat = (
    '<div style="text-align:center;margin-top:22px;">'
    '<span class="serif" data-edit-id="slide2-stat-number" style="font-size:72px;font-weight:300;'
    f'color:{BRAND_LIGHT};line-height:1;letter-spacing:-3px;display:block;">546 mil</span>'
    '<p class="sans" data-edit-id="slide2-stat-caption" style="font-size:13px;color:rgba(255,255,255,0.65);'
    'margin-top:8px;letter-spacing:0.3px;">afastamentos por transtorno mental em 2025 (+15,6%)</p>'
    '<p class="sans" data-edit-id="slide2-stat-source" style="font-size:10px;color:rgba(255,255,255,0.35);'
    'margin-top:6px;letter-spacing:1px;text-transform:uppercase;">Fonte: INSS / ANAMT</p>'
    "</div>"
)
slide2_content = content_wrapper(
    logo_watermark_placeholder := (
        tag_html(2, "O QUE MUDOU NA NORMA", "dark")
        + hairline("dark")
        + headline_html(2, "Segurança não é só capacete", "dark")
        + body_html(
            2,
            "Por décadas, a NR-1 tratava risco como algo físico, químico ou biológico. Sobrecarga, "
            "metas abusivas e assédio ficavam de fora — até agora.",
            "dark",
        )
        + slide2_stat
    )
)
slide2 = slide_wrapper(2, "dark", "", corner_mark("dark") + logo_watermark(), slide2_content)

# ---------------------------------------------------------------------------
# Slide 3 — Solution (gradient) + quote box
# ---------------------------------------------------------------------------
slide3_quote = (
    '<div style="padding:16px;background:rgba(0,0,0,0.15);border-radius:12px;border:1px solid rgba(255,255,255,0.08);margin-top:8px;">'
    '<p class="sans" data-edit-id="slide3-quote-label" style="font-size:13px;color:rgba(255,255,255,0.5);margin-bottom:6px;">O que muda no PGR</p>'
    '<p class="serif" data-edit-id="slide3-quote" style="font-size:15px;color:#fff;font-style:italic;line-height:1.4;margin:0;">'
    "\"Perigo físico, químico, biológico, ergonômico e psicossocial — tudo mapeado, documentado e revisado.\"</p>"
    "</div>"
)
slide3_content = content_wrapper(
    tag_html(3, "A RESPOSTA: GRO + PGR", "gradient")
    + hairline("gradient")
    + headline_html(3, "Gerenciar riscos, não improvisar segurança", "dark", size="34px")
    + body_html(3, "O Gerenciamento de Riscos Ocupacionais (GRO) e o PGR deixam de olhar só para o corpo — e passam a olhar para a rotina de trabalho como um todo.", "dark")
    + slide3_quote
)
# override headline color to white (gradient slide, "dark" kind text color would be white already since kind!="light")
slide3 = slide_wrapper(3, "gradient", "", gradient_scrim() + corner_mark("gradient"), slide3_content)

# ---------------------------------------------------------------------------
# Slide 4 — Features (light)
# ---------------------------------------------------------------------------
def feature_item(n, i, icon, title, desc):
    return (
        '<div style="display:flex;align-items:flex-start;gap:12px;padding:3px 0;">'
        f'<span style="flex:none;width:26px;height:26px;border-radius:8px;background:{BRAND_PRIMARY}1A;'
        f'color:{BRAND_PRIMARY};display:flex;align-items:center;justify-content:center;font-size:13px;">{icon}</span>'
        '<div style="display:flex;flex-direction:column;gap:1px;">'
        f'<span class="sans" data-edit-id="slide{n}-item-{i}-title" style="font-size:13px;font-weight:600;color:{BRAND_DARK};">{title}</span>'
        f'<span class="sans" data-edit-id="slide{n}-item-{i}-desc" style="font-size:11px;color:{SECONDARY};line-height:1.35;">{desc}</span>'
        "</div></div>"
    )

features = [
    ("🔍", "Identificação de perigos", "Físico, químico, biológico e psicossocial."),
    ("📋", "Inventário de riscos", "Documento vivo, sempre atualizado."),
    ("🛠", "Plano de ação", "Medidas de controle com prazo definido."),
    ("🔁", "Monitoramento contínuo", "Revisão periódica, não só na fiscalização."),
    ("📁", "Evidências para fiscalização", "Registros prontos para auditoria."),
]
slide4_list = '<div style="display:flex;flex-direction:column;gap:3px;margin-top:4px;">' + "".join(
    feature_item(4, i + 1, icon, title, desc) for i, (icon, title, desc) in enumerate(features)
) + "</div>"
slide4_content = content_wrapper(
    tag_html(4, "O QUE A NORMA EXIGE", "light").replace("margin-bottom:16px;", "margin-bottom:8px;")
    + hairline("light").replace("margin:6px 0 18px;", "margin:4px 0 10px;")
    + headline_html(4, "5 frentes que sua empresa precisa cobrir", "light", size="27px").replace(
        "margin:0 0 14px;", "margin:0 0 8px;"
    )
    + slide4_list
)
slide4 = slide_wrapper(4, "light", "", corner_mark("light") + logo_watermark(), slide4_content)

# ---------------------------------------------------------------------------
# Slide 5 — Details (dark) + pull-quote
# ---------------------------------------------------------------------------
slide5_quote = (
    f'<blockquote style="border-left:2px solid {BRAND_LIGHT};padding:6px 0 6px 18px;margin:18px 0 0;">'
    '<p class="serif" data-edit-id="slide5-quote" style="font-size:20px;font-style:italic;font-weight:400;'
    'line-height:1.35;color:#fff;margin:0;">"A partir de 26/05/2026, a NR-1 passa a exigir a identificação de '
    'perigos e riscos, incluindo os psicossociais, no PGR de toda empresa."</p>'
    '<p class="sans" data-edit-id="slide5-quote-attribution" style="font-size:11px;color:rgba(255,255,255,0.5);'
    'letter-spacing:2px;text-transform:uppercase;margin-top:10px;">NR-1 · Ministério do Trabalho e Emprego</p>'
    "</blockquote>"
)
slide5_content = content_wrapper(
    tag_html(5, "O CUSTO DE IGNORAR", "dark")
    + hairline("dark")
    + headline_html(5, "Não é mais uma opção segura", "dark")
    + body_html(5, "Sem isso: autuação, passivo trabalhista e aumento do custo do seguro acidente (FAP).", "dark")
    + slide5_quote
)
slide5 = slide_wrapper(5, "dark", "", corner_mark("dark") + logo_watermark(), slide5_content)

# ---------------------------------------------------------------------------
# Slide 6 — How-to (light)
# ---------------------------------------------------------------------------
def step_item(n, i, title, desc):
    return (
        '<div style="display:flex;flex-direction:column;gap:1px;padding:4px 0;">'
        f'<span class="serif" style="font-size:30px;font-weight:300;color:{BRAND_PRIMARY};line-height:1;letter-spacing:-1px;">0{i}</span>'
        f'<span class="sans" data-edit-id="slide{n}-step-{i}-title" style="font-size:14px;font-weight:600;color:{BRAND_DARK};">{title}</span>'
        f'<span class="sans" data-edit-id="slide{n}-step-{i}-desc" style="font-size:11px;color:{SECONDARY};line-height:1.35;">{desc}</span>'
        "</div>"
    )

steps = [
    ("Diagnóstico", "Mapeie os riscos, incluindo os psicossociais."),
    ("Atualize o PGR", "Documente perigos, riscos e medidas de controle."),
    ("Implemente", "Treine lideranças e aplique as medidas."),
    ("Monitore", "Revise e mantenha registros para auditoria."),
]
slide6_list = '<div style="display:flex;flex-direction:column;margin-top:2px;">' + "".join(
    step_item(6, i + 1, title, desc) for i, (title, desc) in enumerate(steps)
) + "</div>"
slide6_content = content_wrapper(
    tag_html(6, "COMO SE ADEQUAR", "light").replace("margin-bottom:16px;", "margin-bottom:8px;")
    + hairline("light").replace("margin:6px 0 18px;", "margin:4px 0 8px;")
    + headline_html(6, "4 passos para colocar sua empresa em dia", "light", size="26px").replace(
        "margin:0 0 14px;", "margin:0 0 6px;"
    )
    + slide6_list
)
slide6 = slide_wrapper(6, "light", "", corner_mark("light") + logo_watermark(), slide6_content)

# ---------------------------------------------------------------------------
# Slide 7 — CTA (gradient)
# ---------------------------------------------------------------------------
slide7_button = (
    f'<div style="display:inline-flex;align-items:center;gap:8px;padding:12px 28px;background:{LIGHT_BG};'
    f'color:{BRAND_DARK};font-family:\'{BODY_FONT}\',sans-serif;font-weight:600;font-size:14px;border-radius:28px;">'
    '<span data-edit-id="slide7-cta">Fale com a gente</span></div>'
)
slide7_content = content_wrapper(
    logo_lockup(48, 15, "#fff")
    + f'<div style="text-align:center;">'
    + headline_html(7, "Não espere a fiscalização bater na porta", "dark", size="32px").replace(
        'margin:0 0 14px;', 'margin:0 0 14px;text-align:center;'
    )
    + body_html(7, "A A&J Soluções em SSTMA cuida do seu PGR do diagnóstico à conformidade.", "dark", role="subhead").replace(
        'margin:0;', 'margin:0 0 24px;text-align:center;'
    )
    + '<div style="display:flex;justify-content:center;">' + slide7_button + "</div>"
    + f'<p class="sans" style="font-size:12px;color:rgba(255,255,255,0.6);text-align:center;margin-top:16px;">{HANDLE}</p>'
    + "</div>"
)
slide7 = slide_wrapper(7, "gradient", "", gradient_scrim() + corner_mark("gradient"), slide7_content, is_last=True)

SLIDES_HTML = slide1 + slide2 + slide3 + slide4 + slide5 + slide6 + slide7

SLIDE_LABELS = {1: "Hero", 2: "Problem", 3: "Solution", 4: "Features", 5: "Details", 6: "How-to", 7: "CTA"}

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
<title>NR-1 — Gerenciamento de Riscos | {BRAND_NAME}</title>
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
      <span class="ig-header-sub">NR-1 · Gerenciamento de Riscos</span>
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
    <b>{HANDLE.lstrip('@')}</b> A NR-1 mudou — e sua empresa precisa estar em dia. Arraste para ver como se adequar. 👉
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
    <strong style="font-size:14px;">Editar carrossel — NR-1</strong>
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
    <code>conteudos/2026-09-01-nr1-gerenciamento-riscos/carousel.html</code>.
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
