import base64
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LOGO_PATH = ROOT / "logo" / "icon.png"
PHOTO_PATH = HERE / "assets" / "edited" / "slide1-photo.jpg"
OUT_HTML = HERE / "carousel.html"

logo_b64 = base64.b64encode(LOGO_PATH.read_bytes()).decode()
LOGO_URI = f"data:image/png;base64,{logo_b64}"

photo_b64 = base64.b64encode(PHOTO_PATH.read_bytes()).decode()
PHOTO_URI = f"data:image/jpeg;base64,{photo_b64}"

BRAND_PRIMARY = "#5FA23B"
BRAND_LIGHT = "#D9E8D6"
BRAND_DARK = "#1C5B57"
LIGHT_BG = "#F4F0E7"
DARK_BG = "#123F3C"

TOTAL = 2

def grain():
    return ('<svg class="grain" aria-hidden="true" style="position:absolute;inset:0;width:100%;height:100%;'
            'pointer-events:none;opacity:0.05;mix-blend-mode:overlay;z-index:1;">'
            '<filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/></filter>'
            '<rect width="100%" height="100%" filter="url(#g)"/></svg>')

def corner_mark(accent):
    return (f'<svg width="12" height="12" viewBox="0 0 12 12" style="position:absolute;top:24px;right:24px;z-index:5;">'
            f'<path d="M6 0v12M0 6h12" stroke="{accent}" stroke-width="1.2"/></svg>')

def swipe_arrow(is_light):
    bg = "rgba(0,0,0,0.06)" if is_light else "rgba(255,255,255,0.08)"
    stroke = "rgba(0,0,0,0.25)" if is_light else "rgba(255,255,255,0.35)"
    return (f'<div style="position:absolute;right:0;top:0;bottom:0;width:48px;z-index:9;display:flex;'
            f'align-items:center;justify-content:center;background:linear-gradient(to right,transparent,{bg});">'
            f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M9 6l6 6-6 6" stroke="{stroke}" '
            f'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>')

# ---------- Slide 1 — Hero (full-bleed photo, text at the bottom) ----------
slide1 = f'''<section class="ig-slide" style="position:relative;width:420px;height:525px;flex:none;
  overflow:hidden;display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 48px;">
  <img src="{PHOTO_URI}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;">
  <div style="position:absolute;inset:0;background:linear-gradient(to top,{DARK_BG}F5 0%,{DARK_BG}D9 38%,{DARK_BG}4D 68%,{DARK_BG}00 88%);z-index:1;"></div>
  {grain()}
  {corner_mark(BRAND_LIGHT)}
  <div style="position:absolute;top:20px;left:28px;z-index:5;background:rgba(0,0,0,0.32);border-radius:8px;padding:6px 8px;">
    <img src="{LOGO_URI}" style="display:block;width:20px;height:20px;object-fit:contain;">
  </div>
  <div style="max-width:360px;margin:0 auto;position:relative;z-index:2;">
    <span class="sans" data-edit-id="slide1-tag" style="display:block;font-size:10px;font-weight:600;
      letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:14px;">SST &amp; GESTÃO</span>
    <div style="width:40px;height:1px;background:{BRAND_LIGHT};opacity:0.6;margin:0 0 16px;"></div>
    <h1 class="serif" data-edit-id="slide1-headline" style="font-size:32px;line-height:1.15;
      letter-spacing:-0.5px;color:#fff;margin:0 0 14px;">
      <span style="font-weight:300;">SST também faz parte de um </span><span style="font-weight:600;font-style:italic;color:{BRAND_PRIMARY};">negócio saudável.</span>
    </h1>
    <p class="sans" data-edit-id="slide1-subhead" style="font-size:17px;line-height:1.5;
      color:rgba(255,255,255,0.85);margin:0 0 16px;">Cuidar da segurança e da saúde dos trabalhadores não é apenas cumprir uma obrigação.</p>
    <div style="width:40px;height:1px;background:rgba(255,255,255,0.4);margin:0 0 16px;"></div>
    <p class="serif" data-edit-id="slide1-highlight" style="font-size:24px;font-weight:600;font-style:italic;
      line-height:1.3;color:#fff;margin:0;">É prevenir, melhorar e fortalecer a empresa.</p>
  </div>
  {swipe_arrow(False)}
</section>'''

# ---------- Slide 2 — CTA discreto (Brand gradient) ----------
slide2_bg = (f"radial-gradient(circle at 15% 20%, {BRAND_LIGHT} 0%, transparent 55%),"
             f"radial-gradient(circle at 90% 10%, {BRAND_PRIMARY} 0%, transparent 50%),"
             f"radial-gradient(circle at 60% 100%, {BRAND_DARK} 0%, transparent 65%),{BRAND_PRIMARY}")

slide2 = f'''<section class="ig-slide" style="background:{slide2_bg};position:relative;width:420px;height:525px;flex:none;
  overflow:hidden;display:flex;flex-direction:column;justify-content:center;padding:64px 36px 56px;">
  {grain()}
  <div style="position:absolute;inset:0;z-index:1;pointer-events:none;background:
    radial-gradient(circle at 15% 20%, rgba(0,0,0,0.48) 0%, transparent 60%),
    rgba(0,0,0,0.12);"></div>
  {corner_mark("rgba(255,255,255,0.6)")}
  <div style="max-width:360px;margin:0 auto;position:relative;z-index:2;text-align:center;">
    <div style="display:flex;align-items:center;justify-content:center;gap:10px;margin-bottom:22px;">
      <img src="{LOGO_URI}" style="width:44px;height:44px;object-fit:contain;">
      <span class="sans" style="font-size:15px;font-weight:600;letter-spacing:0.5px;color:#fff;">A&amp;J Soluções em SSTMA</span>
    </div>
    <h2 class="serif" data-edit-id="slide2-headline" style="font-size:34px;font-weight:600;letter-spacing:-0.5px;
      line-height:1.15;color:#fff;margin:0 0 20px;">
      <span style="font-weight:300;">Prevenção também é </span><span style="font-weight:600;font-style:italic;">investimento.</span>
    </h2>
    <p class="sans" data-edit-id="slide2-body" style="font-size:17px;line-height:1.55;color:rgba(255,255,255,0.85);margin:0 0 22px;">
      Mais segurança para quem trabalha.<br>Mais tranquilidade para quem empreende.</p>
    <div style="width:40px;height:1px;background:rgba(255,255,255,0.5);opacity:0.8;margin:0 auto 20px;"></div>
    <p class="serif" data-edit-id="slide2-highlight" style="font-size:24px;font-weight:600;font-style:italic;
      line-height:1.3;color:#fff;margin:0 0 26px;">SST é cuidado que gera resultados.</p>
    <span class="sans" data-edit-id="slide2-cta" style="display:inline-block;font-size:11px;font-weight:600;
      letter-spacing:2px;color:rgba(255,255,255,0.65);text-transform:uppercase;">@aejsolucoesemsstma</span>
  </div>
</section>'''

DOTS = "".join(
    f'<span class="ig-dot" data-dot="{i}" style="width:6px;height:6px;border-radius:50%;'
    f'background:{"#111" if i == 0 else "rgba(0,0,0,0.2)"};display:inline-block;margin:0 3px;transition:background .2s;"></span>'
    for i in range(TOTAL)
)

HTML = f'''<meta charset="UTF-8">
<title>SST também faz parte de um negócio saudável. A&amp;J Soluções em SSTMA</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,300;0,400;0,600;1,400;1,600&family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin:0; padding:24px; display:flex; gap:24px; align-items:flex-start; background:#f0f0f0; font-family:'Poppins',sans-serif; }}
  .serif {{ font-family:'Lora', serif; }}
  .sans {{ font-family:'Poppins', sans-serif; }}
  .ig-frame {{ width:420px; background:#fff; border-radius:16px; overflow:hidden; box-shadow:0 8px 40px rgba(0,0,0,0.12); }}
  .ig-viewport {{ position:relative; width:420px; aspect-ratio:4/5; overflow:hidden; cursor:grab; touch-action:pan-y; }}
  .ig-track {{ display:flex; height:100%; }}
  .ig-dots {{ text-align:center; padding:10px 0; }}
</style>

<div class="ig-frame">

<div class="ig-header" style="display:flex;align-items:center;gap:10px;padding:12px 14px;">
  <img src="{LOGO_URI}" style="width:32px;height:32px;border-radius:50%;object-fit:cover;">
  <div style="display:flex;flex-direction:column;line-height:1.2;">
    <span class="sans" style="font-size:13px;font-weight:600;color:#111;">@aejsolucoesemsstma</span>
    <span class="sans" style="font-size:11px;color:#888;">A&amp;J Soluções em SSTMA</span>
  </div>
</div>
  <div class="ig-viewport">
    <div class="ig-track">
{slide1}
{slide2}
</div>
  </div>
  <div class="ig-dots">{DOTS}</div>

<div class="ig-actions" style="display:flex;align-items:center;gap:14px;padding:12px 14px 4px;">
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#111" stroke-width="1.8"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.6l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21l7.8-7.6 1-1a5.5 5.5 0 0 0 0-7.8z"/></svg>
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#111" stroke-width="1.8"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#111" stroke-width="1.8"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4z"/></svg>
  <span style="flex:1;"></span>
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#111" stroke-width="1.8"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
</div>

<div class="ig-caption" style="padding:2px 14px 16px;">
  <p class="sans" style="font-size:13px;color:#111;line-height:1.4;margin:0;">
    <strong>@aejsolucoesemsstma</strong> SST também faz parte de um negócio saudável. Prevenção é investimento. 🌱
  </p>
  <p class="sans" style="font-size:11px;color:#999;margin:6px 0 0;letter-spacing:0.3px;">2 HORAS ATRÁS</p>
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
    <code>conteudos/2026-09-17-sst-negocio-saudavel/carousel.html</code>.
  </p>
</aside>

<script id="carousel-editor-script">
(function(){{
  const SLIDE_LABELS = {{
    1:"Hero (foto)",2:"CTA"
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
    det.open = true;
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


<script>
(function(){{
  const track = document.querySelector('.ig-track');
  const viewport = document.querySelector('.ig-viewport');
  const dots = Array.from(document.querySelectorAll('.ig-dot'));
  const total = track.children.length;
  const slideW = 420;
  let index = 0, startX = 0, dragging = false, currentX = 0;

  function goTo(i){{
    index = Math.max(0, Math.min(total - 1, i));
    track.style.transition = 'transform .35s ease';
    track.style.transform = 'translateX(' + (-index * slideW) + 'px)';
    dots.forEach((d, di) => {{ d.style.background = di === index ? '#111' : 'rgba(0,0,0,0.2)'; }});
  }}

  viewport.addEventListener('pointerdown', (e) => {{
    dragging = true; startX = e.clientX; currentX = -index * slideW;
    track.style.transition = 'none';
    viewport.setPointerCapture(e.pointerId);
  }});
  viewport.addEventListener('pointermove', (e) => {{
    if(!dragging) return;
    const dx = e.clientX - startX;
    track.style.transform = 'translateX(' + (currentX + dx) + 'px)';
  }});
  viewport.addEventListener('pointerup', (e) => {{
    if(!dragging) return;
    dragging = false;
    const dx = e.clientX - startX;
    if (dx < -60) goTo(index + 1);
    else if (dx > 60) goTo(index - 1);
    else goTo(index);
  }});
  viewport.addEventListener('pointerleave', () => {{ if(dragging){{ dragging = false; goTo(index); }} }});

  goTo(0);
}})();
</script>
'''

OUT_HTML.write_text(HTML, encoding="utf-8")
print(f"Wrote {OUT_HTML} ({OUT_HTML.stat().st_size} bytes)")
