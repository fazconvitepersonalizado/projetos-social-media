"""VERSÃO 1 (substituída em 2026-10-19 pela versão anti-IA em _generate.py). Gera carousel-v1.html: "Carboidrato à noite engorda?" (Marina Couto, TESTE fictício).

Escolhas da rodada (2026-10-19): fotos na capa (full-bleed) e no card 6
(emoldurada); texto da capa no espaço livre (topo); fotos suaves; selo
"ARRASTE" só na capa, sem barra de progresso; fotos de banco gratuito.
"""
import base64
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
KIT = json.loads((ROOT / "brand-kit.json").read_text(encoding="utf-8"))
D = KIT["derived"]
BRAND_PRIMARY, BRAND_LIGHT, BRAND_DARK = D["BRAND_PRIMARY"], D["BRAND_LIGHT"], D["BRAND_DARK"]
LIGHT_BG, LIGHT_BORDER, DARK_BG = D["LIGHT_BG"], D["LIGHT_BORDER"], D["DARK_BG"]
HANDLE = KIT["instagram_handle"]
TOTAL = 8


def data_uri(p, mime="image/jpeg"):
    return f"data:{mime};base64,{base64.b64encode(Path(p).read_bytes()).decode()}"


CAPA = data_uri(HERE / "assets/edited/capa.jpg")
CARD6 = data_uri(HERE / "assets/edited/card6.jpg")


def svg(name, height):
    s = (ROOT / "logo" / name).read_text(encoding="utf-8")
    w, h = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s).groups())
    width = height * w / h
    s = re.sub(r'width="[\d.]+" height="[\d.]+"', f'width="{width:.1f}" height="{height}"', s, count=1)
    return s.replace("<svg ", '<svg style="display:block" aria-hidden="true" ', 1)


def grain():
    return ('<svg class="grain" aria-hidden="true" style="position:absolute;inset:0;width:100%;height:100%;'
            'pointer-events:none;opacity:0.05;mix-blend-mode:overlay;z-index:1;">'
            '<filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/></filter>'
            '<rect width="100%" height="100%" filter="url(#g)"/></svg>')


def corner(accent):
    return (f'<svg width="12" height="12" viewBox="0 0 12 12" style="position:absolute;top:24px;right:24px;z-index:5;">'
            f'<path d="M6 0v12M0 6h12" stroke="{accent}" stroke-width="1.2"/></svg>')


def mono_mark(light):
    """Monograma MC como marca d'água (slides 2..N-1), substitui o 0n/0N."""
    v = "monograma-primary.svg" if light else "monograma-white.svg"
    return f'<div style="position:absolute;top:16px;left:24px;opacity:0.5;z-index:5;">{svg(v, 30)}</div>'


def counter(n, light):
    c = "rgba(46,42,37,0.55)" if light else "rgba(244,238,227,0.6)"
    return (f'<span class="mono" style="position:absolute;bottom:24px;left:0;right:0;text-align:center;font-size:11px;'
            f'letter-spacing:2px;color:{c};z-index:5;">{n}/{TOTAL}</span>')


def light_bg():
    return (f"radial-gradient(circle at 20% 0%, {BRAND_PRIMARY}1F 0%, transparent 45%),"
            f"radial-gradient(circle at 100% 100%, {BRAND_LIGHT}24 0%, transparent 50%),{LIGHT_BG}")


def dark_bg():
    return (f"radial-gradient(circle at 80% 10%, {BRAND_PRIMARY}3D 0%, transparent 40%),"
            f"radial-gradient(circle at 0% 90%, {BRAND_DARK}66 0%, transparent 55%),{DARK_BG}")


def tag(text, color, n, role="tag"):
    return (f'<span class="sans" data-edit-id="slide{n}-{role}" style="display:block;font-size:11px;font-weight:700;'
            f'letter-spacing:2px;color:{color};text-transform:uppercase;">{text}</span>'
            f'<div style="width:40px;height:1px;background:{color};opacity:0.6;margin:8px 0 18px;"></div>')


SLIDE = ('position:relative;width:420px;height:525px;flex:none;overflow:hidden;display:flex;'
         'flex-direction:column;justify-content:center;padding:64px 36px 76px;')
BLOCK = 'max-width:360px;width:100%;margin:0 auto;position:relative;z-index:2;'
INK, INK_SOFT = DARK_BG, "#5E574E"
CREAM, CREAM_SOFT = LIGHT_BG, "rgba(244,238,227,0.82)"

# ---------- 1 · Capa (foto full-bleed, texto no topo, onde o véu creme dá espaço) ----------
s1 = f'''<section class="ig-slide" style="{SLIDE}justify-content:flex-start;padding:52px 36px 76px;">
  <!-- foto: pexels.com/photo/grilled-chicken-with-rice-and-beans-meal-close-up-34134206 (th2city) -->
  <img src="{CAPA}" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 70%;z-index:0;">
  <div style="position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,
    rgba(244,238,227,0.96) 0%, rgba(244,238,227,0.93) 34%, rgba(244,238,227,0.82) 50%,
    rgba(244,238,227,0.50) 62%, rgba(244,238,227,0.12) 76%, rgba(244,238,227,0) 86%);"></div>
  <div style="position:absolute;inset:0;z-index:1;background:rgba(244,238,227,0.12);"></div>
  {grain()}
  {corner(BRAND_PRIMARY)}
  <div style="{BLOCK}">
    <div style="display:inline-flex;background:rgba(244,238,227,0.85);border:1px solid {LIGHT_BORDER};border-radius:7px;padding:6px 8px;margin-bottom:22px;">{svg("logo-primary.svg", 30)}</div>
    {tag("Sem neura", BRAND_PRIMARY, 1)}
    <h1 class="serif" data-edit-id="slide1-headline" style="font-size:42px;line-height:1.04;letter-spacing:-1px;color:{INK};margin:0 0 14px;">
      <span style="font-weight:400;">Carboidrato à noite </span><span style="font-weight:600;font-style:italic;color:{BRAND_PRIMARY};">engorda?</span></h1>
    <p class="sans" data-edit-id="slide1-subhead" style="font-size:16px;line-height:1.45;color:{INK};margin:0;">Spoiler: o relógio pesa bem menos do que você imagina.</p>
  </div>
  <span class="mono" data-edit-id="slide1-swipe" style="position:absolute;bottom:22px;right:22px;z-index:5;font-size:10px;font-weight:500;letter-spacing:2px;color:{INK};background:rgba(244,238,227,0.9);border-radius:6px;padding:7px 10px;">ARRASTE PARA O LADO →</span>
</section>'''

# ---------- 2 · Total do dia (escuro, Big Stat) ----------
s2 = f'''<section class="ig-slide" style="background:{dark_bg()};{SLIDE}">
  {grain()}{corner(BRAND_LIGHT)}{mono_mark(False)}
  <div style="{BLOCK}">
    {tag("O que conta", BRAND_LIGHT, 2)}
    <span class="serif" style="display:block;font-size:96px;font-weight:300;line-height:0.9;letter-spacing:-3px;color:{CREAM};">24<span style="font-style:italic;color:{BRAND_LIGHT};">h</span></span>
    <p class="sans" style="font-size:12px;letter-spacing:2px;text-transform:uppercase;color:{CREAM_SOFT};margin:10px 0 22px;">o dia inteiro, não o relógio</p>
    <p class="sans" data-edit-id="slide2-body" style="font-size:17px;line-height:1.5;color:{CREAM};margin:0;">O que define ganho de peso é o total do dia: quanto você come, o que come e como se movimenta. O horário, sozinho, não muda essa conta.</p>
  </div>
  {counter(2, False)}
</section>'''

# ---------- 3 · Fome mais tarde (claro) ----------
s3 = f'''<section class="ig-slide" style="background:{light_bg()};{SLIDE}">
  {grain()}{corner(BRAND_PRIMARY)}{mono_mark(True)}
  <div style="{BLOCK}">
    {tag("O efeito rebote", BRAND_PRIMARY, 3)}
    <h2 class="serif" data-edit-id="slide3-headline" style="font-size:30px;font-weight:400;line-height:1.12;letter-spacing:-0.5px;color:{INK};margin:0 0 18px;">Cortar o carboidrato do jantar pode deixar você com <i>fome mais tarde.</i></h2>
    <p class="sans" data-edit-id="slide3-body" style="font-size:17px;line-height:1.5;color:{INK_SOFT};margin:0;">E fome à noite vira beliscada no armário, quase sempre maior do que o arroz que você evitou.</p>
  </div>
  {counter(3, True)}
</section>'''

# ---------- 4 · Jantar equilibrado (escuro, lista) ----------
def item(lbl):
    return (f'<span class="sans" style="font-size:14px;font-weight:500;padding:7px 14px;border-radius:20px;'
            f'background:rgba(158,195,218,0.16);color:{CREAM};border:1px solid rgba(158,195,218,0.35);">{lbl}</span>')


s4 = f'''<section class="ig-slide" style="background:{dark_bg()};{SLIDE}">
  {grain()}{corner(BRAND_LIGHT)}{mono_mark(False)}
  <div style="{BLOCK}">
    {tag("No prato", BRAND_LIGHT, 4)}
    <h2 class="serif" data-edit-id="slide4-headline" style="font-size:30px;font-weight:400;line-height:1.12;letter-spacing:-0.5px;color:{CREAM};margin:0 0 18px;">Um jantar equilibrado tem carboidrato, <i>sim.</i></h2>
    <div style="display:flex;flex-wrap:wrap;gap:8px;margin:0 0 20px;">{item("arroz")}{item("feijão")}{item("batata")}{item("pão")}{item("legumes")}{item("proteína")}</div>
    <p class="sans" data-edit-id="slide4-body" style="font-size:17px;line-height:1.5;color:{CREAM};margin:0;">É essa mistura que segura a fome até de manhã.</p>
  </div>
  {counter(4, False)}
</section>'''

# ---------- 5 · Quantidade (claro, pull-quote) ----------
s5 = f'''<section class="ig-slide" style="background:{light_bg()};{SLIDE}">
  {grain()}{corner(BRAND_PRIMARY)}{mono_mark(True)}
  <div style="{BLOCK}">
    {tag("O ponto", BRAND_PRIMARY, 5)}
    <h2 class="serif" data-edit-id="slide5-headline" style="font-size:34px;font-weight:600;line-height:1.08;letter-spacing:-0.5px;color:{INK};margin:0 0 22px;">O ponto é a <i style="color:{BRAND_PRIMARY};">quantidade.</i></h2>
    <blockquote style="border-left:2px solid {BRAND_PRIMARY};padding:6px 0 6px 18px;margin:0;">
      <p class="serif" data-edit-id="slide5-quote" style="font-size:20px;font-style:italic;font-weight:400;line-height:1.35;color:{INK};margin:0;">Uma concha de arroz com feijão não é o problema; o prato que vira montanha porque você passou o dia sem comer, sim.</p>
    </blockquote>
  </div>
  {counter(5, True)}
</section>'''

# ---------- 6 · Prato em 3 partes (claro, foto emoldurada + passos) ----------
def part(frac, lbl, n):
    return (f'<div style="flex:1;display:flex;flex-direction:column;gap:4px;">'
            f'<span class="sans" style="font-size:34px;font-weight:500;line-height:1;color:{BRAND_PRIMARY};">{frac}</span>'
            f'<span class="sans" data-edit-id="slide6-step-{n}" style="font-size:13px;font-weight:600;line-height:1.3;color:{INK};">{lbl}</span></div>')


s6 = f'''<section class="ig-slide" style="background:{light_bg()};{SLIDE}padding:56px 36px 64px;">
  {grain()}{corner(BRAND_PRIMARY)}{mono_mark(True)}
  <div style="{BLOCK}">
    <!-- foto: unsplash.com/photos/jUPOXXRNdcA (Brooke Lark) -->
    <div style="width:100%;border-radius:14px;overflow:hidden;box-shadow:0 12px 32px rgba(46,42,37,0.18);margin-bottom:16px;">
      <img src="{CARD6}" alt="" style="display:block;width:100%;height:150px;object-fit:cover;object-position:45% 45%;"></div>
    {tag("Dica prática", BRAND_PRIMARY, 6)}
    <h2 class="serif" data-edit-id="slide6-headline" style="font-size:26px;font-weight:400;line-height:1.12;color:{INK};margin:-6px 0 14px;">Monte o prato em <i>3 partes.</i></h2>
    <div style="display:flex;gap:12px;margin:0 0 14px;">{part("½", "de legumes", 1)}{part("¼", "de proteína", 2)}{part("¼", "de carboidrato", 3)}</div>
    <p class="sans" data-edit-id="slide6-body" style="font-size:15px;font-weight:500;line-height:1.4;color:{INK_SOFT};margin:0;">Sem balança, sem contar, sem neura.</p>
  </div>
  {counter(6, True)}
</section>'''

# ---------- 7 · CTA de interação (claro com bloco azul) ----------
s7 = f'''<section class="ig-slide" style="background:{light_bg()};{SLIDE}">
  {grain()}{corner(BRAND_PRIMARY)}{mono_mark(True)}
  <div style="{BLOCK}">
    <div style="background:{BRAND_LIGHT};border-radius:16px;padding:30px 26px;">
      <span class="mono" style="display:block;font-size:11px;letter-spacing:2px;color:{INK};margin-bottom:14px;">ENQUETE RÁPIDA</span>
      <h2 class="serif" data-edit-id="slide7-headline" style="font-size:32px;font-weight:400;line-height:1.1;color:{INK};margin:0 0 16px;">Você evita carboidrato <i>à noite?</i></h2>
      <p class="sans" data-edit-id="slide7-body" style="font-size:16px;line-height:1.5;color:{INK};margin:0;">Me conta nos comentários e salva este post pra lembrar na hora do jantar.</p>
    </div>
    <div style="display:flex;gap:18px;margin-top:18px;padding-left:4px;">
      <span class="sans" style="font-size:13px;font-weight:600;color:{INK_SOFT};display:flex;align-items:center;gap:6px;"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="{INK_SOFT}" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>comente</span>
      <span class="sans" style="font-size:13px;font-weight:600;color:{INK_SOFT};display:flex;align-items:center;gap:6px;"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="{INK_SOFT}" stroke-width="2"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>salve</span>
    </div>
  </div>
  {counter(7, True)}
</section>'''

# ---------- 8 · Encerramento (degradê da marca) ----------
grad = (f"radial-gradient(circle at 15% 20%, {BRAND_LIGHT} 0%, transparent 55%),"
        f"radial-gradient(circle at 90% 10%, {BRAND_PRIMARY} 0%, transparent 50%),"
        f"radial-gradient(circle at 60% 100%, {BRAND_DARK} 0%, transparent 65%),{BRAND_PRIMARY}")
s8 = f'''<section class="ig-slide" style="background:{grad};{SLIDE}">
  {grain()}
  <div style="position:absolute;inset:0;z-index:1;pointer-events:none;background:
    radial-gradient(circle at 15% 20%, rgba(0,0,0,0.48) 0%, transparent 60%), rgba(0,0,0,0.12);"></div>
  {corner("rgba(255,255,255,0.6)")}
  <div style="{BLOCK}text-align:center;">
    <div style="display:inline-flex;background:rgba(0,0,0,0.22);border-radius:8px;padding:8px 10px;margin-bottom:24px;">{svg("logo-white.svg", 44)}</div>
    <p class="sans" data-edit-id="slide8-body" style="font-size:18px;line-height:1.5;color:#fff;margin:0 0 22px;">No <b>Comer em Paz</b>, a gente monta o jantar que cabe na sua rotina, com arroz e feijão inclusos.</p>
    <div data-edit-id="slide8-cta" class="sans" style="display:inline-flex;padding:12px 26px;background:{LIGHT_BG};color:{BRAND_DARK};font-weight:700;font-size:14px;border-radius:28px;margin-bottom:22px;">Agende sua consulta pelo link da bio</div>
    <p class="serif" data-edit-id="slide8-signoff" style="font-size:24px;font-weight:400;line-height:1.2;color:#fff;margin:0;text-wrap:balance;">Comida de verdade,<br><i style="font-weight:600;">sem neura.</i></p>
  </div>
  <span class="mono" style="position:absolute;bottom:24px;left:0;right:0;text-align:center;font-size:11px;letter-spacing:2px;color:rgba(255,255,255,0.7);z-index:5;">{HANDLE}</span>
</section>'''

SLIDES = [s1, s2, s3, s4, s5, s6, s7, s8]
DOTS = "".join(
    f'<span class="ig-dot" style="width:6px;height:6px;border-radius:50%;background:{"#111" if i == 0 else "rgba(0,0,0,0.2)"};'
    f'display:inline-block;margin:0 3px;"></span>' for i in range(TOTAL))

HEAD = f'''<meta charset="UTF-8">
<title>Carboidrato à noite engorda? · Marina Couto</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,300;0,400;0,600;1,400;1,600&family=DM+Sans:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin:0; padding:24px; display:flex; gap:24px; align-items:flex-start; background:#ecebe8; font-family:'DM Sans',sans-serif; }}
  .serif {{ font-family:'Fraunces', Georgia, serif; }}
  .sans {{ font-family:'DM Sans', sans-serif; }}
  .mono {{ font-family:'DM Mono', monospace; }}
  .ig-frame {{ width:420px; background:#fff; border-radius:16px; overflow:hidden; box-shadow:0 8px 40px rgba(0,0,0,0.12); }}
  .ig-viewport {{ position:relative; width:420px; aspect-ratio:4/5; overflow:hidden; cursor:grab; touch-action:pan-y; }}
  .ig-track {{ display:flex; height:100%; }}
  .ig-dots {{ text-align:center; padding:10px 0; }}
</style>
'''

FRAME = f'''<div class="ig-frame">
<div class="ig-header" style="display:flex;align-items:center;gap:10px;padding:12px 14px;">
  <div style="width:32px;height:32px;border-radius:50%;background:{BRAND_LIGHT};display:flex;align-items:center;justify-content:center;">{svg("monograma-dark.svg", 22)}</div>
  <div style="display:flex;flex-direction:column;line-height:1.2;">
    <span class="sans" style="font-size:13px;font-weight:600;color:#111;">{HANDLE.lstrip("@")}</span>
    <span class="sans" style="font-size:11px;color:#888;">Marina Couto | Nutricionista</span>
  </div>
</div>
<div class="ig-viewport"><div class="ig-track">
{"".join(SLIDES)}
</div></div>
<div class="ig-dots">{DOTS}</div>
<div class="ig-actions" style="display:flex;align-items:center;gap:14px;padding:12px 14px 4px;">
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#111" stroke-width="1.8"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.6l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21l7.8-7.6 1-1a5.5 5.5 0 0 0 0-7.8z"/></svg>
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#111" stroke-width="1.8"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#111" stroke-width="1.8"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4z"/></svg>
  <span style="flex:1;"></span>
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#111" stroke-width="1.8"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
</div>
<div class="ig-caption" style="padding:2px 14px 16px;">
  <p class="sans" style="font-size:13px;color:#111;line-height:1.4;margin:0;"><strong>{HANDLE.lstrip("@")}</strong> Você também já ouviu que carboidrato à noite engorda? Arrasta pro lado que eu te explico.</p>
  <p class="sans" style="font-size:11px;color:#999;margin:6px 0 0;letter-spacing:0.3px;">2 HORAS ATRÁS</p>
</div>
</div>
'''

EDITOR = '''<aside id="carousel-editor" style="width:360px;max-height:90vh;overflow:auto;background:#fff;border:1px solid #e5e5e5;border-radius:14px;padding:18px;font-family:system-ui,sans-serif;font-size:13px;box-shadow:0 4px 24px rgba(0,0,0,0.06);position:sticky;top:24px;">
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;">
    <strong style="font-size:14px;">Editar carrossel</strong>
    <button id="ce-download" style="background:#111;color:#fff;border:0;border-radius:8px;padding:8px 14px;font-weight:600;cursor:pointer;font-size:12px;">Baixar HTML</button>
  </div>
  <div id="ce-groups"></div>
  <p style="margin-top:14px;color:#888;font-size:11px;line-height:1.4;">O download remove o painel e gera um <code>carousel.html</code> limpo, pronto para exportar. Substitua o arquivo em <code>conteudos/2026-10-19-carboidrato-a-noite-engorda/carousel.html</code>.</p>
</aside>
<script id="carousel-editor-script">
(function(){
  const SLIDE_LABELS = {1:"Capa (foto)",2:"Total do dia",3:"Fome mais tarde",4:"Jantar equilibrado",5:"Quantidade",6:"Prato em 3 partes (foto)",7:"CTA",8:"Encerramento"};
  const groups = document.getElementById('ce-groups');
  const slides = {};
  document.querySelectorAll('[data-edit-id]').forEach(el => {
    const id = el.getAttribute('data-edit-id');
    const m = id.match(/^slide(\\d+)-(.+)$/);
    if(!m) return;
    const n = +m[1];
    (slides[n] = slides[n] || []).push({id, role:m[2], el});
  });
  Object.keys(slides).sort((a,b)=>+a-+b).forEach(n => {
    const det = document.createElement('details');
    det.open = (+n <= 2);
    det.style.cssText = 'margin-bottom:8px;border:1px solid #eee;border-radius:8px;padding:8px 10px;';
    det.innerHTML = `<summary style="cursor:pointer;font-weight:600;">Slide ${n} · ${SLIDE_LABELS[n]||''}</summary>`;
    slides[n].forEach(({id, role, el}) => {
      const wrap = document.createElement('div');
      wrap.style.cssText = 'margin:8px 0;';
      const label = document.createElement('label');
      label.textContent = role;
      label.style.cssText = 'display:block;color:#666;font-size:11px;margin-bottom:4px;text-transform:uppercase;letter-spacing:1px;';
      const ta = document.createElement('textarea');
      ta.value = el.textContent.trim();
      ta.style.cssText = 'width:100%;min-height:48px;border:1px solid #ddd;border-radius:6px;padding:8px;font:inherit;resize:vertical;';
      ta.addEventListener('input', () => { el.textContent = ta.value; });
      wrap.append(label, ta);
      det.append(wrap);
    });
    groups.append(det);
  });
  document.getElementById('ce-download').addEventListener('click', () => {
    const clone = document.documentElement.cloneNode(true);
    clone.querySelector('#carousel-editor')?.remove();
    clone.querySelector('#carousel-editor-script')?.remove();
    const body = clone.querySelector('body');
    if (body) body.removeAttribute('style');
    const html = '<!doctype html>\\n' + clone.outerHTML;
    const blob = new Blob([html], {type:'text/html'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'carousel.html';
    document.body.appendChild(a); a.click(); a.remove();
  });
})();
</script>
'''

SWIPE = '''<script>
(function(){
  const track = document.querySelector('.ig-track');
  const viewport = document.querySelector('.ig-viewport');
  const dots = Array.from(document.querySelectorAll('.ig-dot'));
  const total = track.children.length, slideW = 420;
  let index = 0, startX = 0, dragging = false, currentX = 0;
  function goTo(i){
    index = Math.max(0, Math.min(total - 1, i));
    track.style.transition = 'transform .35s ease';
    track.style.transform = 'translateX(' + (-index * slideW) + 'px)';
    dots.forEach((d, di) => { d.style.background = di === index ? '#111' : 'rgba(0,0,0,0.2)'; });
  }
  viewport.addEventListener('pointerdown', (e) => { dragging = true; startX = e.clientX; currentX = -index * slideW; track.style.transition = 'none'; viewport.setPointerCapture(e.pointerId); });
  viewport.addEventListener('pointermove', (e) => { if(!dragging) return; track.style.transform = 'translateX(' + (currentX + e.clientX - startX) + 'px)'; });
  viewport.addEventListener('pointerup', (e) => { if(!dragging) return; dragging = false; const dx = e.clientX - startX; if (dx < -60) goTo(index + 1); else if (dx > 60) goTo(index - 1); else goTo(index); });
  viewport.addEventListener('pointerleave', () => { if(dragging){ dragging = false; goTo(index); } });
  goTo(0);
})();
</script>
'''

html = HEAD + FRAME + EDITOR + SWIPE
assert "—" not in re.sub(r"<[^>]+>", "", "".join(SLIDES)), "travessão na copy"
(HERE / "carousel-v1.html").write_text(html, encoding="utf-8")
print("carousel-v1.html", len(html) // 1024, "KB")
