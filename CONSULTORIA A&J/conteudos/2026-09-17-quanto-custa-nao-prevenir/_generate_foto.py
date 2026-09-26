# -*- coding: utf-8 -*-
import base64
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT_HTML = HERE / "carousel-foto.html"

brand = json.loads((ROOT / "brand-kit.json").read_text(encoding="utf-8"))
D = brand["derived"]
BRAND_PRIMARY = D["BRAND_PRIMARY"]
BRAND_LIGHT = D["BRAND_LIGHT"]
BRAND_DARK = D["BRAND_DARK"]
DARK_BG = D["DARK_BG"]
BRAND_NAME = brand["brand_name"]
HANDLE = brand["instagram_handle"]

logo_bytes = (ROOT / "logo" / "icon.png").read_bytes()
LOGO_URI = "data:image/png;base64," + base64.b64encode(logo_bytes).decode()

photo_bytes = (HERE / "assets" / "edited" / "slide-photo.jpg").read_bytes()
PHOTO_URI = "data:image/jpeg;base64," + base64.b64encode(photo_bytes).decode()


def grain():
    return (
        '<svg class="grain" aria-hidden="true" style="position:absolute;inset:0;width:100%;height:100%;'
        'pointer-events:none;opacity:0.05;mix-blend-mode:overlay;z-index:1;">'
        '<filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/></filter>'
        '<rect width="100%" height="100%" filter="url(#g)"/></svg>'
    )


def corner_mark():
    return (
        f'<svg width="12" height="12" viewBox="0 0 12 12" style="position:absolute;top:24px;right:24px;z-index:5;">'
        f'<path d="M6 0v12M0 6h12" stroke="{BRAND_LIGHT}" stroke-width="1.2"/></svg>'
    )


# Single-page post — same technique as the "SST negócio saudável" hero slide:
# full-bleed photo, dark gradient rising from the bottom, text anchored low so
# it never overlaps the subject's face.
content = f'''<div style="max-width:360px;margin:0 auto;position:relative;z-index:2;">
  <span class="sans" data-edit-id="post-tag" style="display:block;font-size:10px;font-weight:600;
    letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:14px;">SST &amp; GESTÃO</span>
  <div style="width:40px;height:1px;background:{BRAND_LIGHT};opacity:0.6;margin:0 0 16px;"></div>
  <h1 class="serif" data-edit-id="post-headline" style="font-size:36px;line-height:1.15;
    letter-spacing:-0.5px;color:#fff;margin:0 0 16px;">
    <span style="font-weight:300;">Quanto custa </span><span style="font-weight:600;font-style:italic;color:{BRAND_PRIMARY};">não prevenir?</span>
  </h1>
  <p class="sans" data-edit-id="post-body" style="font-size:17px;line-height:1.5;
    color:rgba(255,255,255,0.85);margin:0 0 18px;">Um acidente, um afastamento, uma perda de produtividade ou um problema que poderia ter sido evitado.</p>
  <div style="width:40px;height:1px;background:rgba(255,255,255,0.4);margin:0 0 18px;"></div>
  <blockquote style="border-left:2px solid {BRAND_PRIMARY};padding:4px 0 4px 18px;margin:0 0 24px;">
    <p class="serif" data-edit-id="post-highlight" style="font-size:23px;font-style:italic;font-weight:600;
      line-height:1.3;color:#fff;margin:0;">Investir em SST é também cuidar da continuidade do negócio.</p>
  </blockquote>
  <div style="display:flex;align-items:center;gap:8px;opacity:0.85;">
    <img src="{LOGO_URI}" style="width:20px;height:20px;object-fit:contain;display:block;">
    <span class="sans" data-edit-id="post-cta" style="font-size:12.5px;font-weight:600;letter-spacing:0.5px;color:#fff;">{HANDLE}</span>
  </div>
</div>'''

slide = f'''<section class="ig-slide slide" style="position:relative;width:420px;height:525px;flex:none;
  overflow:hidden;display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 48px;">
  <img src="{PHOTO_URI}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;">
  <div style="position:absolute;inset:0;background:linear-gradient(to top,{DARK_BG}F5 0%,{DARK_BG}D9 38%,{DARK_BG}4D 68%,{DARK_BG}00 88%);z-index:1;"></div>
  {grain()}
  {corner_mark()}
  {content}
</section>'''

HTML = f'''<meta charset="UTF-8">
<title>Quanto custa não prevenir? A&amp;J Soluções em SSTMA</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,300;0,400;0,600;1,400;1,600&family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin:0; padding:24px; display:flex; gap:24px; align-items:flex-start; background:#f0f0f0; font-family:'Poppins',sans-serif; }}
  .serif {{ font-family:'Lora', serif; }}
  .sans {{ font-family:'Poppins', sans-serif; }}
  .ig-frame {{ width:420px; background:#fff; border-radius:16px; overflow:hidden; box-shadow:0 8px 40px rgba(0,0,0,0.12); }}
  .ig-viewport {{ position:relative; width:420px; aspect-ratio:4/5; overflow:hidden; }}
  .ig-track {{ display:flex; height:100%; }}
</style>

<div class="ig-frame">

<div class="ig-header" style="display:flex;align-items:center;gap:10px;padding:12px 14px;">
  <img src="{LOGO_URI}" style="width:32px;height:32px;border-radius:50%;object-fit:cover;">
  <div style="display:flex;flex-direction:column;line-height:1.2;">
    <span class="sans" style="font-size:13px;font-weight:600;color:#111;">{HANDLE}</span>
    <span class="sans" style="font-size:11px;color:#888;">{BRAND_NAME}</span>
  </div>
</div>
  <div class="ig-viewport">
    <div class="ig-track">
{slide}
</div>
  </div>

<div class="ig-actions" style="display:flex;align-items:center;gap:14px;padding:12px 14px 4px;">
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#111" stroke-width="1.8"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.6l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21l7.8-7.6 1-1a5.5 5.5 0 0 0 0-7.8z"/></svg>
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#111" stroke-width="1.8"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#111" stroke-width="1.8"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4z"/></svg>
  <span style="flex:1;"></span>
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#111" stroke-width="1.8"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
</div>

<div class="ig-caption" style="padding:2px 14px 16px;">
  <p class="sans" style="font-size:13px;color:#111;line-height:1.4;margin:0;">
    <strong>{HANDLE}</strong> Quanto custa não prevenir? Investir em SST é cuidar da continuidade do negócio. 🌱
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
    <strong style="font-size:14px;">Editar post</strong>
    <button id="ce-download" style="
      background:#111;color:#fff;border:0;border-radius:8px;
      padding:8px 14px;font-weight:600;cursor:pointer;font-size:12px;">
      Baixar HTML
    </button>
  </div>
  <div id="ce-groups"></div>
  <p style="margin-top:14px;color:#888;font-size:11px;line-height:1.4;">
    O download remove o painel e gera um <code>carousel-foto.html</code> limpo,
    pronto para exportar. Substitua o arquivo em
    <code>conteudos/2026-09-17-quanto-custa-nao-prevenir/carousel-foto.html</code>.
  </p>
</aside>

<script id="carousel-editor-script">
(function(){{
  const groups = document.getElementById('ce-groups');
  const det = document.createElement('details');
  det.open = true;
  det.style.cssText = 'margin-bottom:8px;border:1px solid #eee;border-radius:8px;padding:8px 10px;';
  det.innerHTML = '<summary style="cursor:pointer;font-weight:600;">Post</summary>';
  document.querySelectorAll('[data-edit-id]').forEach(el => {{
    const id = el.getAttribute('data-edit-id');
    const role = id.replace(/^post-/, '');
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
    a.download = 'carousel-foto.html';
    document.body.appendChild(a); a.click(); a.remove();
  }});
}})();
</script>
'''

OUT_HTML.write_text(HTML, encoding="utf-8")
print(f"Wrote {OUT_HTML} ({OUT_HTML.stat().st_size} bytes)")
