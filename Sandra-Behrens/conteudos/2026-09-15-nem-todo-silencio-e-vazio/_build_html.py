"""Gera carousel.html para 'Nem todo silêncio é vazio' (Sandra Behrens)."""
import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent.parent

brand = json.loads((PROJECT_ROOT / "brand-kit.json").read_text(encoding="utf-8"))
d = brand["derived"]
BRAND_PRIMARY = d["BRAND_PRIMARY"]   # #C69A46
BRAND_LIGHT   = d["BRAND_LIGHT"]     # #D1AE6B
BRAND_DARK    = d["BRAND_DARK"]      # #8B6C31
LIGHT_BG      = d["LIGHT_BG"]        # #F5EDDF
LIGHT_BORDER  = d["LIGHT_BORDER"]    # #E7DBC5
DARK_BG       = d["DARK_BG"]         # #3E4234

LOGO_PRIMARY = Path(brand["logo"]["variants"]["primary"]).read_text(encoding="utf-8").strip()
LOGO_WHITE   = Path(brand["logo"]["variants"]["white"]).read_text(encoding="utf-8").strip()

def sized_logo(svg: str, w: int, h: int) -> str:
    return svg.replace('width="480" height="210"', f'width="{w}" height="{h}"', 1)

LOGO_HERO_LIGHT      = sized_logo(LOGO_PRIMARY, 160, 70)
LOGO_WATERMARK_LIGHT = sized_logo(LOGO_PRIMARY, 136, 60)
LOGO_WATERMARK_DARK  = sized_logo(LOGO_WHITE, 136, 60)
LOGO_GRADIENT        = sized_logo(LOGO_WHITE, 150, 66)
LOGO_CTA_WHITE       = sized_logo(LOGO_WHITE, 190, 83)
LOGO_CORNER_ON_PHOTO = sized_logo(LOGO_PRIMARY, 118, 52)

def photo_uri(name: str) -> str:
    b = (ROOT / "assets" / "edited" / name).read_bytes()
    return f"data:image/jpeg;base64,{base64.b64encode(b).decode()}"

PHOTO3_URI = photo_uri("slide3-mulher-janela.jpg")
PHOTO5_URI = photo_uri("slide5-mulher-parque.jpg")

def grain():
    return ('<svg class="grain" aria-hidden="true" style="position:absolute;inset:0;width:100%;height:100%;'
            'pointer-events:none;opacity:0.05;mix-blend-mode:overlay;z-index:1;">'
            '<filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/></filter>'
            '<rect width="100%" height="100%" filter="url(#g)"/></svg>')

def corner_mark(accent):
    return (f'<svg width="12" height="12" viewBox="0 0 12 12" style="position:absolute;top:24px;right:24px;z-index:5;">'
            f'<path d="M6 0v12M0 6h12" stroke="{accent}" stroke-width="1.2"/></svg>')

def swipe_arrow(is_light):
    bg = 'rgba(0,0,0,0.06)' if is_light else 'rgba(255,255,255,0.08)'
    stroke = 'rgba(0,0,0,0.25)' if is_light else 'rgba(255,255,255,0.35)'
    return (f'<div style="position:absolute;right:0;top:0;bottom:0;width:48px;z-index:9;display:flex;'
            f'align-items:center;justify-content:center;background:linear-gradient(to right,transparent,{bg});">'
            f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none">'
            f'<path d="M9 6l6 6-6 6" stroke="{stroke}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>')

def logo_chip(sized_svg, bg, radius=6, pad="6px"):
    return (f'<div style="display:inline-flex;padding:{pad};background:{bg};border-radius:{radius}px;'
            f'box-shadow:0 3px 10px rgba(0,0,0,0.14);">{sized_svg}</div>')

def watermark_topright(sized_svg, bg):
    return f'<div style="position:absolute;top:56px;right:24px;z-index:6;">{logo_chip(sized_svg, bg)}</div>'

def logo_centered(sized_svg, bg, margin_bottom=18):
    return f'<div style="display:flex;justify-content:center;margin-bottom:{margin_bottom}px;">{logo_chip(sized_svg, bg, radius=8, pad="8px")}</div>'

def hairline(accent, margin="6px auto 16px"):
    return f'<div style="width:40px;height:1px;background:{accent};opacity:0.6;margin:{margin};"></div>'

CONTENT_OPEN = ('<div style="position:relative;z-index:2;display:flex;flex-direction:column;justify-content:center;'
                 'height:100%;padding:64px 36px 76px;box-sizing:border-box;">'
                 '<div style="max-width:360px;margin:0 auto;width:100%;text-align:center;">')
CONTENT_CLOSE = '</div></div>'

# ---------------------------------------------------------------------------
# SLIDE 1 — Capa (LIGHT_BG, tipográfico)
# ---------------------------------------------------------------------------
slide1_bg = (f'background:radial-gradient(circle at 20% 0%, {BRAND_PRIMARY}1F 0%, transparent 45%),'
             f'radial-gradient(circle at 100% 100%, {BRAND_LIGHT}24 0%, transparent 50%),{LIGHT_BG};')

slide1 = f'''<div style="width:420px;height:525px;flex:none;position:relative;overflow:hidden;{slide1_bg}">{grain()}{corner_mark(BRAND_PRIMARY)}{CONTENT_OPEN}
{logo_centered(LOGO_HERO_LIGHT, f"{LIGHT_BORDER}CC", margin_bottom=22)}
<h1 class="serif" data-edit-id="slide1-headline" style="font-size:32px;line-height:1.28;margin:0 0 18px;color:#3A342C;"><span style="font-weight:300;">Nem todo silêncio é </span><span style="font-weight:600;font-style:italic;color:{BRAND_PRIMARY};">vazio.</span></h1>
<p class="serif" data-edit-id="slide1-subhead" style="font-size:17.5px;font-style:italic;font-weight:400;line-height:1.5;color:#3A342C;opacity:0.8;margin:0 0 16px;">Há momentos em que a mulher simplesmente precisa parar de ouvir tantas vozes externas para conseguir escutar a própria.</p>
<p class="serif" data-edit-id="slide1-closing" style="font-size:16.5px;font-style:italic;font-weight:400;line-height:1.5;color:#3A342C;opacity:0.75;margin:0 0 26px;">Na maturidade, talvez o silêncio deixe de ser ausência e passe a ser encontro.</p>
<span class="sans" style="display:inline-flex;align-items:center;gap:6px;font-size:10px;font-weight:600;letter-spacing:1.5px;color:#3A342C;opacity:0.45;text-transform:uppercase;">ARRASTE PARA O LADO <svg width="11" height="11" viewBox="0 0 24 24" fill="none"><path d="M9 6l6 6-6 6" stroke="#3A342C" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
{CONTENT_CLOSE}{swipe_arrow(True)}</div>'''

# ---------------------------------------------------------------------------
# SLIDE 2 — Um encontro (DARK_BG, tipográfico)
# ---------------------------------------------------------------------------
slide2_bg = (f'background:radial-gradient(circle at 80% 10%, {BRAND_PRIMARY}3D 0%, transparent 40%),'
             f'radial-gradient(circle at 0% 90%, {BRAND_DARK}66 0%, transparent 55%),{DARK_BG};')

slide2 = f'''<div style="width:420px;height:525px;flex:none;position:relative;overflow:hidden;{slide2_bg}">{grain()}{corner_mark(BRAND_LIGHT)}{CONTENT_OPEN}
{logo_centered(LOGO_WATERMARK_DARK, "rgba(0,0,0,0.24)")}
<span class="sans" data-edit-id="slide2-tag" style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:2px;">UM ENCONTRO</span>
{hairline(BRAND_LIGHT)}
<p class="serif" data-edit-id="slide2-line1" style="font-size:21px;font-style:italic;font-weight:400;line-height:1.4;color:#fff;margin:0 0 10px;">Com aquilo que você sente.</p>
<p class="serif" data-edit-id="slide2-line2" style="font-size:21px;font-style:italic;font-weight:400;line-height:1.4;color:#fff;margin:0 0 10px;">Com aquilo que você deseja.</p>
<p class="serif" data-edit-id="slide2-line3" style="font-size:21px;font-style:italic;font-weight:600;line-height:1.4;color:{BRAND_LIGHT};margin:0 0 24px;">Com aquilo que você já não aceita.</p>
<p class="sans" data-edit-id="slide2-attribution" style="font-size:13.5px;font-style:italic;color:rgba(255,255,255,0.85);line-height:1.4;margin:0;">Uma reflexão inspirada no universo de Clarice Lispector.</p>
{CONTENT_CLOSE}{swipe_arrow(False)}</div>'''

# ---------------------------------------------------------------------------
# SLIDE 3 — O ruído de fora (LIGHT_BG, foto pequena em card)
# ---------------------------------------------------------------------------
slide3_bg = (f'background:radial-gradient(circle at 20% 0%, {BRAND_PRIMARY}1F 0%, transparent 45%),'
             f'radial-gradient(circle at 100% 100%, {BRAND_LIGHT}24 0%, transparent 50%),{LIGHT_BG};')

photo3_card = (f'<div style="width:100%;border-radius:14px;overflow:hidden;box-shadow:0 12px 32px rgba(0,0,0,0.18);margin-bottom:16px;">'
               f'<!-- foto: pexels.com/photo/wistful-mature-woman-looking-out-window-6874398 (Teona Swift) -->'
               f'<img src="{PHOTO3_URI}" style="display:block;width:100%;height:200px;object-fit:cover;object-position:50% 30%;"></div>')

slide3 = f'''<div style="width:420px;height:525px;flex:none;position:relative;overflow:hidden;{slide3_bg}">{grain()}{corner_mark(BRAND_PRIMARY)}{CONTENT_OPEN}
{logo_centered(LOGO_WATERMARK_LIGHT, f"{LIGHT_BORDER}CC", margin_bottom=14)}
{photo3_card}
<span class="sans" data-edit-id="slide3-tag" style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_PRIMARY};margin-bottom:2px;">O RUÍDO DE FORA</span>
{hairline(BRAND_PRIMARY, margin="6px auto 14px")}
<h2 class="serif" data-edit-id="slide3-headline" style="font-size:22px;line-height:1.32;margin:0 0 10px;color:#3A342C;font-weight:500;">Passamos anos aprendendo a escutar todo mundo.</h2>
<p class="serif" data-edit-id="slide3-body" style="font-size:17px;font-style:italic;font-weight:400;line-height:1.5;color:#3A342C;opacity:0.78;margin:0;">Os pais, os filhos, o parceiro, o trabalho, as expectativas — vozes que ensinam, cobram, esperam. E que, aos poucos, abafam a que mais importa: a sua.</p>
{CONTENT_CLOSE}{swipe_arrow(True)}</div>'''

# ---------------------------------------------------------------------------
# SLIDE 4 — O silêncio possível (Brand gradient, pull-quote tipográfico)
# ---------------------------------------------------------------------------
slide4_bg = (f'background:radial-gradient(circle at 15% 20%, {BRAND_LIGHT} 0%, transparent 55%),'
             f'radial-gradient(circle at 90% 10%, {BRAND_PRIMARY} 0%, transparent 50%),'
             f'radial-gradient(circle at 60% 100%, {BRAND_DARK} 0%, transparent 65%),{BRAND_PRIMARY};')
slide4_legibility_scrim = ('<div style="position:absolute;inset:0;z-index:1;pointer-events:none;background:'
                            'radial-gradient(circle at 15% 20%, rgba(0,0,0,0.48) 0%, transparent 60%),'
                            'rgba(0,0,0,0.12);"></div>')

slide4 = f'''<div style="width:420px;height:525px;flex:none;position:relative;overflow:hidden;{slide4_bg}">{grain()}{slide4_legibility_scrim}{corner_mark("rgba(255,255,255,0.6)")}{CONTENT_OPEN}
{logo_centered(LOGO_GRADIENT, "rgba(0,0,0,0.22)", margin_bottom=18)}
<span class="sans" data-edit-id="slide4-tag" style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:rgba(255,255,255,0.65);margin-bottom:2px;">O SILÊNCIO POSSÍVEL</span>
{hairline("rgba(255,255,255,0.5)")}
<blockquote style="border-left:2px solid #fff;padding:4px 0 4px 18px;margin:0 0 16px;text-align:left;">
<p class="serif" data-edit-id="slide4-quote" style="font-size:24px;font-style:italic;font-weight:400;line-height:1.32;color:#fff;margin:0;">"Existe um silêncio que não é solidão. É espaço."</p>
</blockquote>
<p class="serif" data-edit-id="slide4-body" style="font-size:17.5px;font-style:italic;font-weight:400;line-height:1.5;color:#fff;opacity:0.9;margin:0;">Espaço para ouvir, sem pressa, o que você mesma tem para dizer.</p>
{CONTENT_CLOSE}{swipe_arrow(False)}</div>'''

# ---------------------------------------------------------------------------
# SLIDE 5 — Para você (CTA, foto full-bleed suave, texto embaixo)
# ---------------------------------------------------------------------------
slide5_scrim = (f'background:linear-gradient(to top, {DARK_BG}F7 0%, {DARK_BG}E8 24%, '
                 f'{DARK_BG}A0 46%, {DARK_BG}00 70%);')

SLIDE5_CONTENT_OPEN = ('<div style="position:relative;z-index:2;display:flex;flex-direction:column;justify-content:flex-end;'
                       'height:100%;padding:64px 36px 76px;box-sizing:border-box;">'
                       '<div style="max-width:360px;margin:0 auto;width:100%;text-align:center;">')

slide5 = f'''<div style="width:420px;height:525px;flex:none;position:relative;overflow:hidden;background:{DARK_BG};">
<!-- foto: pexels.com/photo/happy-woman-walking-through-park-11284054 (Centre for Ageing Better) -->
<img src="{PHOTO5_URI}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 30%;opacity:0.85;z-index:0;">
<div style="position:absolute;inset:0;z-index:1;pointer-events:none;{slide5_scrim}"></div>
{grain()}{corner_mark("rgba(255,255,255,0.6)")}{watermark_topright(LOGO_CORNER_ON_PHOTO, f"{LIGHT_BG}F2")}{SLIDE5_CONTENT_OPEN}
<span class="sans" data-edit-id="slide5-tag" style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:2px;">PARA VOCÊ</span>
{hairline(BRAND_LIGHT, margin="6px auto 14px")}
<h2 class="serif" data-edit-id="slide5-headline" style="font-size:21px;line-height:1.34;margin:0 0 10px;color:#fff;font-weight:400;">Se esse silêncio tem te dito algo, talvez valha a pena escutá-lo com companhia.</h2>
<p class="sans" data-edit-id="slide5-caption" style="font-size:13.5px;font-style:italic;color:rgba(255,255,255,0.85);line-height:1.4;margin:0 0 18px;">Um espaço de escuta, com Sandra Behrens.</p>
<div style="display:flex;justify-content:center;margin-bottom:12px;"><div class="sans" data-edit-id="slide5-cta" style="display:inline-flex;align-items:center;gap:8px;padding:13px 28px;background:{LIGHT_BG};color:{BRAND_DARK};font-weight:600;font-size:14.5px;border-radius:28px;">Agende uma conversa.</div></div>
<p class="sans" data-edit-id="slide5-handle" style="text-align:center;font-size:12px;color:rgba(255,255,255,0.7);letter-spacing:0.5px;margin:0;">@psicologasandrabehrens</p>
{CONTENT_CLOSE}</div>'''

SLIDES = [slide1, slide2, slide3, slide4, slide5]
TOTAL = len(SLIDES)

dots_html = "".join(
    f'<span class="dot{" active" if i == 0 else ""}" data-i="{i}" style="width:6px;height:6px;border-radius:50%;'
    f'background:{"#C69A46" if i == 0 else "#ddd"};cursor:pointer;transition:background .2s;"></span>'
    for i in range(TOTAL)
)

AVATAR_SVG = sized_logo(LOGO_PRIMARY, 22, 10)

html = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Sandra Behrens. Nem todo silêncio é vazio</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,600&family=Poppins:wght@400;500;600&family=Parisienne&display=swap');
* {{ box-sizing: border-box; }}
body {{
  margin:0; padding:24px; display:flex; gap:24px; align-items:flex-start;
  background:#EFE9DE; font-family:'Poppins',sans-serif;
}}
.serif {{ font-family:'Cormorant Garamond', Georgia, serif; }}
.sans  {{ font-family:'Poppins', Arial, sans-serif; }}
.signature {{ font-family:'Parisienne', cursive; }}
.ig-frame {{
  width:420px; background:#fff; border-radius:16px; overflow:hidden;
  box-shadow:0 20px 60px rgba(0,0,0,0.15); flex:none;
}}
.ig-header {{ display:flex; align-items:center; gap:10px; padding:12px 14px; border-bottom:1px solid #f0f0f0; }}
.ig-header-text {{ line-height:1.3; }}
.ig-header-text b {{ font-size:13px; color:#111; }}
.ig-header-text span {{ display:block; font-size:11px; color:#8a8580; }}
.carousel-viewport {{ width:420px; height:525px; overflow:hidden; position:relative; cursor:grab; touch-action:pan-y; }}
.carousel-track {{ display:flex; width:{420*TOTAL}px; height:525px; transition:transform .35s ease; }}
.ig-dots {{ display:flex; justify-content:center; gap:6px; padding:10px 0; }}
.ig-actions {{ display:flex; align-items:center; gap:14px; padding:8px 14px; }}
.ig-actions .spacer {{ flex:1; }}
.ig-caption {{ padding:0 14px 16px; font-size:13px; color:#333; line-height:1.4; }}
.ig-caption .time {{ display:block; margin-top:4px; font-size:10px; letter-spacing:1px; color:#aaa; text-transform:uppercase; }}
</style>
</head>
<body>
<div class="ig-frame">
  <div class="ig-header">
    <div class="ig-avatar">{AVATAR_SVG}</div>
    <div class="ig-header-text">
      <b>psicologasandrabehrens</b>
      <span>Sandra Behrens · Psicóloga</span>
    </div>
  </div>
  <div class="carousel-viewport">
    <div class="carousel-track">
      {''.join(SLIDES)}
    </div>
  </div>
  <div class="ig-dots">{dots_html}</div>
  <div class="ig-actions">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#262626" stroke-width="1.8"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.6l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21l7.8-7.6 1-1a5.5 5.5 0 0 0 0-7.8Z"/></svg><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#262626" stroke-width="1.8"><path d="M21 11.5a8.38 8.38 0 0 1-8.5 8.5 8.5 8.5 0 0 1-4-1L3 20l1-4.5a8.5 8.5 0 1 1 17-4Z"/></svg><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#262626" stroke-width="1.8"><path d="M22 2 11 13M22 2l-7 20-4-9-9-4 20-7Z"/></svg><div class="spacer"></div><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#262626" stroke-width="1.8"><path d="M19 21 12 16l-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16Z"/></svg>
  </div>
  <div class="ig-caption">
    <b>@psicologasandrabehrens</b> Nem todo silêncio é vazio.
    <span class="time">2 HORAS ATRÁS</span>
  </div>
</div>

<aside id="carousel-editor" style="
  width:360px;max-height:90vh;overflow:auto;
  background:#fff;border:1px solid #e5e5e5;border-radius:14px;
  padding:18px;font-family:system-ui,sans-serif;font-size:13px;
  box-shadow:0 4px 24px rgba(0,0,0,0.06);position:sticky;top:24px;
">
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;">
    <strong style="font-size:14px;">Editar carrossel</strong>
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
    <code>conteudos/2026-09-15-nem-todo-silencio-e-vazio/carousel.html</code>.
  </p>
</aside>

<script id="carousel-editor-script">
(function(){{
  const SLIDE_LABELS = {{
    1:"Capa",2:"Um encontro",3:"O ruído de fora",4:"O silêncio possível",5:"CTA"
  }};
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

<script id="carousel-drag-script">
(function(){{
  var track = document.querySelector('.carousel-track');
  var viewport = document.querySelector('.carousel-viewport');
  var dots = document.querySelectorAll('.ig-dots .dot');
  var total = dots.length, index = 0, startX = 0, currentX = 0, dragging = false;
  function goTo(i){{
    index = Math.max(0, Math.min(total - 1, i));
    track.style.transform = 'translateX(' + (-index * 420) + 'px)';
    dots.forEach(function(d, j){{ d.style.background = (j === index) ? '#C69A46' : '#ddd'; }});
  }}
  viewport.addEventListener('pointerdown', function(e){{
    dragging = true; startX = e.clientX; currentX = 0;
    viewport.setPointerCapture(e.pointerId);
    track.style.transition = 'none';
  }});
  viewport.addEventListener('pointermove', function(e){{
    if(!dragging) return;
    currentX = e.clientX - startX;
    track.style.transform = 'translateX(' + (-index * 420 + currentX) + 'px)';
  }});
  function endDrag(){{
    if(!dragging) return;
    dragging = false;
    track.style.transition = 'transform .35s ease';
    if (currentX < -60) goTo(index + 1);
    else if (currentX > 60) goTo(index - 1);
    else goTo(index);
    currentX = 0;
  }}
  viewport.addEventListener('pointerup', endDrag);
  viewport.addEventListener('pointerleave', function(){{ if(dragging) endDrag(); }});
  dots.forEach(function(d, j){{ d.addEventListener('click', function(){{ goTo(j); }}); }});
  goTo(0);
}})();
</script>

</body>
</html>
'''

out_path = ROOT / "carousel.html"
out_path.write_text(html, encoding="utf-8")
print(f"gerado: {out_path} ({out_path.stat().st_size // 1024} KB)")
