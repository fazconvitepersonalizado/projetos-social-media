"""Gera carousel.html: "Carboidrato à noite engorda?" (Marina Couto, TESTE fictício).

Versão 2 (oficial, 2026-10-19), a versão 1 ficou em carousel-v1.html
(_generate_v1.py). Feita como teste das regras anti-IA e aprovada pelo Thiago:
- copy revisada por humanizer / stop-slop / no-ai-slop (nota 25 → 38 de 50);
- design pelo Impeccable: sem etiqueta acima do título, sem brilho radial nem
  granulado, sem pílulas/cards de app, composições variadas, fundos chapados;
- fotos: capa (Pexels 34134206), card 3 full-bleed (Pexels 32577115) e card 4
  dividindo o slide (Pexels 19781592), vívidas (_prep_photo_v2.py);
- título em Source Serif 4 (Fraunces parecia tremida), título e apoio no mesmo
  bloco, elementos desenhados com função (linha do dia, prato dividido).
"""
import re

import _generate_v1 as base  # tokens, capa, logo, moldura do IG, painel e swipe

INK, CREAM = base.DARK_BG, base.LIGHT_BG
PRIMARY, LIGHT = base.BRAND_PRIMARY, base.BRAND_LIGHT
INK_SOFT = "#4F4941"
TOTAL = 8
CARD3 = base.data_uri(base.HERE / "assets/edited/card3.jpg")
CARD4 = base.data_uri(base.HERE / "assets/edited/card4.jpg")
SLIDE = ('position:relative;width:420px;height:525px;flex:none;overflow:hidden;display:flex;'
         'flex-direction:column;padding:44px 36px 52px;')
GAP = 16  # distância título → apoio: bloco único, sem vácuo entre eles


def counter(n, color):
    return (f'<span class="mono" style="position:absolute;bottom:22px;left:36px;font-size:12px;'
            f'letter-spacing:1px;color:{color};z-index:3;">{n}/{TOTAL}</span>')


def h(size, color, text, eid, extra=""):
    return (f'<h2 class="serif" data-edit-id="{eid}" style="font-size:{size}px;font-weight:500;line-height:1.08;'
            f'letter-spacing:-0.02em;color:{color};margin:0;text-wrap:balance;{extra}">{text}</h2>')


def p(color, text, eid, size=18, extra=""):
    return (f'<p class="sans" data-edit-id="{eid}" style="font-size:{size}px;line-height:1.45;color:{color};'
            f'margin:{GAP}px 0 0;{extra}">{text}</p>')


# 1 · Capa: foto full-bleed, título e apoio juntos no espaço livre de cima
s1 = f'''<section class="ig-slide" style="{SLIDE}">
  <!-- foto: pexels.com/photo/grilled-chicken-with-rice-and-beans-meal-close-up-34134206 (th2city) -->
  <img src="{base.CAPA}" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 70%;">
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,
    rgba(244,238,227,0.97) 0%, rgba(244,238,227,0.94) 40%, rgba(244,238,227,0.78) 56%,
    rgba(244,238,227,0.35) 68%, rgba(244,238,227,0) 80%);"></div>
  <div style="position:relative;">
    <div style="display:inline-flex;background:rgba(244,238,227,0.85);border:1px solid {base.LIGHT_BORDER};border-radius:7px;padding:6px 8px;margin-bottom:30px;">{base.svg("logo-primary.svg", 28)}</div>
    <h1 class="serif" data-edit-id="slide1-headline" style="font-size:54px;font-weight:500;line-height:1.0;letter-spacing:-0.03em;color:{INK};margin:0;">Carboidrato à noite <i style="font-weight:600;color:{PRIMARY};">engorda?</i></h1>
    {p(INK, "Seu corpo usa o arroz das 20h do mesmo jeito que usa o do meio-dia.", "slide1-subhead", 18, "max-width:330px;")}
  </div>
  <span class="sans" style="position:absolute;bottom:22px;right:22px;display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:600;color:{INK};background:rgba(244,238,227,0.92);border-radius:6px;padding:7px 10px;">Arraste para o lado
    <svg width="14" height="10" viewBox="0 0 14 10" fill="none" stroke="{INK}" stroke-width="1.6"><path d="M0 5h12M8 1l4 4-4 4"/></svg></span>
</section>'''


# 2 · Grafite: texto e linha do dia num bloco só, centralizado (o jantar é um ponto do dia)
def dia():
    pts = [("café", "7h", 0.0), ("almoço", "12h", 0.36), ("lanche", "16h", 0.64), ("jantar", "20h", 0.93)]
    w = 330
    marks = ""
    for nome, hora, x in pts:
        cx = 8 + x * (w - 16)
        cor = LIGHT if nome == "jantar" else "rgba(244,238,227,0.75)"
        marks += (f'<circle cx="{cx:.0f}" cy="14" r="{7 if nome == "jantar" else 5}" fill="{cor}"/>'
                  f'<text x="{cx:.0f}" y="44" text-anchor="middle" style="font-family:DM Sans;font-size:14px;font-weight:600;fill:{cor};">{nome}</text>'
                  f'<text x="{cx:.0f}" y="62" text-anchor="middle" style="font-family:DM Mono;font-size:12px;fill:rgba(244,238,227,0.7);">{hora}</text>')
    return (f'<svg width="{w}" height="66" viewBox="0 0 {w} 66" aria-hidden="true" style="display:block;overflow:visible;">'
            f'<line x1="8" y1="14" x2="{w - 8}" y2="14" stroke="rgba(244,238,227,0.35)" stroke-width="2"/>{marks}</svg>')


s2 = f'''<section class="ig-slide" style="background:{INK};{SLIDE}justify-content:center;">
  {h(40, CREAM, "O que pesa na balança é o que você come no dia inteiro e quanto se mexe.", "slide2-headline")}
  {p("rgba(244,238,227,0.88)", "Se o total do dia fecha, o horário do arroz muda pouco.", "slide2-body")}
  <div style="margin-top:40px;">{dia()}</div>
  {counter(2, "rgba(244,238,227,0.75)")}
</section>'''

# 3 · Foto full-bleed (geladeira à noite), rosto livre no alto, texto embaixo sobre degradê
s3 = f'''<section class="ig-slide" style="{SLIDE}justify-content:flex-end;">
  <!-- foto: pexels.com/photo/woman-exploring-fridge-late-at-night-32577115 -->
  <img src="{CARD3}" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 30%;">
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,
    rgba(30,27,24,0) 30%, rgba(30,27,24,0.55) 48%, rgba(30,27,24,0.86) 64%, rgba(30,27,24,0.94) 100%);"></div>
  <div style="position:absolute;inset:0;background:rgba(30,27,24,0.12);"></div>
  <div style="position:relative;">
    <span class="mono" data-edit-id="slide3-hora" style="display:block;font-size:15px;color:{LIGHT};margin-bottom:10px;">23h10</span>
    {h(36, "#fff", "Quem corta o arroz do jantar costuma ir dormir com fome.", "slide3-headline")}
    {p("rgba(255,255,255,0.92)", "Aí aparece a torrada, depois o biscoito. Somados, passam fácil da concha de arroz que você evitou.", "slide3-body", 17)}
  </div>
  {counter(3, "rgba(255,255,255,0.8)")}
</section>'''

# 4 · Foto dividindo o slide (o jantar de que o texto fala) + texto no creme
s4 = f'''<section class="ig-slide" style="background:{CREAM};{SLIDE}padding:0;">
  <!-- foto: pexels.com/photo/meals-in-frying-pans-on-wooden-table-19781592 -->
  <img src="{CARD4}" alt="" style="display:block;width:420px;height:262px;object-fit:cover;">
  <div style="padding:26px 36px 0;">
    {h(29, INK, "Um jantar com arroz, feijão, proteína e salada segura a fome até o café da manhã.", "slide4-headline")}
    {p(INK_SOFT, "Batata e pão também entram, se for o que tem na sua casa.", "slide4-body", 17, "margin-top:12px;")}
  </div>
  {counter(4, "rgba(46,42,37,0.75)")}
</section>'''

# 5 · Creme: frase grande e apoio colados, bloco no centro
s5 = f'''<section class="ig-slide" style="background:{CREAM};{SLIDE}justify-content:center;">
  <div>
    {h(52, INK, "O resultado depende do tamanho do prato.", "slide5-headline", "line-height:1.0;letter-spacing:-0.03em;")}
    {p(INK_SOFT, "Quem pula o almoço chega no jantar com fome de dois. Se você comeu direito durante o dia, uma concha de arroz com feijão basta.", "slide5-body", 18, "margin-top:20px;")}
  </div>
  {counter(5, "rgba(46,42,37,0.75)")}
</section>'''

# 6 · Grafite: título colado no prato desenhado (geometria exata, não ilustração)
plate = f'''<svg width="190" height="190" viewBox="0 0 196 196" aria-hidden="true">
  <circle cx="98" cy="98" r="96" fill="none" stroke="rgba(244,238,227,0.35)" stroke-width="2"/>
  <path d="M98 14 A84 84 0 0 0 98 182 Z" fill="{LIGHT}"/>
  <path d="M98 14 A84 84 0 0 1 182 98 L98 98 Z" fill="{CREAM}"/>
  <path d="M182 98 A84 84 0 0 1 98 182 L98 98 Z" fill="{PRIMARY}"/>
  <path d="M98 14V182M98 98H182" stroke="{INK}" stroke-width="3"/>
</svg>'''


def legend(color, frac, label, n):
    return (f'<div style="display:flex;align-items:baseline;gap:10px;">'
            f'<span style="width:10px;height:10px;border-radius:50%;background:{color};flex:none;transform:translateY(-1px);"></span>'
            f'<span class="sans" data-edit-id="slide6-parte-{n}" style="font-size:17px;line-height:1.3;color:{CREAM};">'
            f'<b style="font-weight:600;">{frac}</b> {label}</span></div>')


s6 = f'''<section class="ig-slide" style="background:{INK};{SLIDE}justify-content:center;">
  {h(40, CREAM, "Dá pra montar o prato de olho, sem balança.", "slide6-headline")}
  <div style="display:flex;align-items:center;gap:22px;margin-top:30px;">
    {plate}
    <div style="display:flex;flex-direction:column;gap:12px;">
      {legend(LIGHT, "metade", "legumes", 1)}
      {legend(CREAM, "um quarto", "proteína", 2)}
      {legend(PRIMARY, "um quarto", "arroz ou outro carboidrato", 3)}
    </div>
  </div>
  {counter(6, "rgba(244,238,227,0.75)")}
</section>'''

# 7 · Azul claro: pergunta grande com o convite colado nela
icon_c = f'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="{INK}" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>'
icon_s = f'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="{INK}" stroke-width="2"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>'
s7 = f'''<section class="ig-slide" style="background:{LIGHT};{SLIDE}justify-content:center;">
  <div>
    {h(56, INK, "Você corta o carboidrato à noite?", "slide7-headline", "line-height:1.0;letter-spacing:-0.03em;")}
    {p(INK, "Me conta nos comentários. E salva o post pra consultar na hora de montar o prato.", "slide7-body", 18, "margin-top:20px;")}
    <div style="display:flex;gap:20px;margin-top:18px;">
      <span class="sans" style="display:flex;align-items:center;gap:6px;font-size:14px;font-weight:600;color:{INK};">{icon_c}comente</span>
      <span class="sans" style="display:flex;align-items:center;gap:6px;font-size:14px;font-weight:600;color:{INK};">{icon_s}salve</span>
    </div>
  </div>
  {counter(7, "rgba(46,42,37,0.8)")}
</section>'''

# 8 · Azul profundo chapado: um bloco só (logo, convite, botão, assinatura em 2 linhas)
s8 = f'''<section class="ig-slide" style="background:{PRIMARY};{SLIDE}justify-content:center;">
  <div style="display:inline-flex;align-self:flex-start;background:rgba(0,0,0,0.22);border-radius:8px;padding:8px 10px;margin-bottom:28px;">{base.svg("logo-white.svg", 36)}</div>
  {p("#fff", "No Comer em Paz, a gente monta o seu jantar em cima da rotina que você tem, com arroz e feijão.", "slide8-body", 21, "margin:0 0 22px;")}
  <div class="sans" data-edit-id="slide8-cta" style="display:inline-flex;align-self:flex-start;padding:13px 22px;background:{CREAM};color:{INK};font-weight:700;font-size:15px;border-radius:10px;">Agende sua consulta pelo link da bio</div>
  <p class="serif" data-edit-id="slide8-signoff" style="font-size:28px;font-weight:500;line-height:1.15;color:#fff;margin:34px 0 0;">Comida de verdade,<br><i style="white-space:nowrap;">sem neura.</i></p>
  <span class="mono" style="position:absolute;bottom:22px;left:36px;font-size:12px;color:rgba(255,255,255,0.92);">{base.HANDLE}</span>
</section>'''

SLIDES = [s1, s2, s3, s4, s5, s6, s7, s8]
HEAD = base.HEAD.replace(
    "family=Fraunces:ital,wght@0,300;0,400;0,600;1,400;1,600",
    "family=Source+Serif+4:ital,opsz,wght@0,8..60,400..700;1,8..60,400..700",
).replace("font-family:'Fraunces', Georgia, serif;", "font-family:'Source Serif 4', Georgia, serif; font-optical-sizing:auto;")
assert "Source+Serif+4" in HEAD and "'Source Serif 4'" in HEAD
EDITOR = base.EDITOR.replace(
    '{1:"Capa (foto)",2:"Total do dia",3:"Fome mais tarde",4:"Jantar equilibrado",5:"Quantidade",6:"Prato em 3 partes (foto)",7:"CTA",8:"Encerramento"}',
    '{1:"Capa (foto)",2:"Dia inteiro",3:"Geladeira 23h (foto)",4:"Jantar (foto)",5:"Tamanho do prato",6:"Prato de olho",7:"Pergunta",8:"Encerramento"}')
assert EDITOR != base.EDITOR
# Navegação da prévia: fica na faixa dos pontinhos, fora da área do slide,
# então nunca entra no export (export_carousel.py só captura .ig-viewport).
CHEV = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="{d}"/></svg>'
NAV_DOTS = "".join(f'<button class="ig-dot" type="button" aria-label="Ir para o slide {i + 1}" data-go="{i}"></button>'
                   for i in range(TOTAL))
NAV = f'''<div class="ig-dots ig-nav">
  <button class="ig-nav-btn" id="ig-prev" type="button" aria-label="Slide anterior">{CHEV.format(d="M15 6l-6 6 6 6")}</button>
  <div class="ig-nav-dots">{NAV_DOTS}</div>
  <span class="ig-nav-count" id="ig-count">1/{TOTAL}</span>
  <button class="ig-nav-btn" id="ig-next" type="button" aria-label="Próximo slide">{CHEV.format(d="M9 6l6 6-6 6")}</button>
</div>'''
NAV_CSS = f'''<style>
  .ig-nav {{ display:flex; align-items:center; justify-content:center; gap:12px; padding:10px 14px; }}
  .ig-nav-dots {{ display:flex; gap:6px; align-items:center; }}
  .ig-nav .ig-dot {{ width:7px; height:7px; padding:0; border:0; border-radius:4px; background:rgba(0,0,0,0.2); cursor:pointer; transition:width .2s, background .2s; }}
  .ig-nav .ig-dot.on {{ width:18px; background:{PRIMARY}; }}
  .ig-nav-btn {{ width:34px; height:34px; border-radius:50%; border:1px solid rgba(0,0,0,0.12); background:#fff; color:#111;
    display:flex; align-items:center; justify-content:center; cursor:pointer; transition:background .15s, color .15s, opacity .15s; }}
  .ig-nav-btn:hover:not(:disabled) {{ background:{PRIMARY}; color:#fff; border-color:{PRIMARY}; }}
  .ig-nav-btn:disabled {{ opacity:.3; cursor:default; }}
  .ig-nav-btn:focus-visible, .ig-nav .ig-dot:focus-visible {{ outline:2px solid {PRIMARY}; outline-offset:2px; }}
  .ig-nav-count {{ font:500 12px 'DM Mono', monospace; color:#666; min-width:30px; text-align:center; }}
</style>'''
NAV_JS = '''<script>
(function(){
  const track = document.querySelector('.ig-track');
  const viewport = document.querySelector('.ig-viewport');
  const dots = Array.from(document.querySelectorAll('.ig-nav .ig-dot'));
  const prev = document.getElementById('ig-prev'), next = document.getElementById('ig-next');
  const count = document.getElementById('ig-count');
  const total = track.children.length, slideW = 420;
  let index = 0, startX = 0, dragging = false, currentX = 0;
  function goTo(i){
    index = Math.max(0, Math.min(total - 1, i));
    track.style.transition = 'transform .35s ease';
    track.style.transform = 'translateX(' + (-index * slideW) + 'px)';
    dots.forEach((d, di) => d.classList.toggle('on', di === index));
    prev.disabled = index === 0; next.disabled = index === total - 1;
    count.textContent = (index + 1) + '/' + total;
  }
  prev.addEventListener('click', () => goTo(index - 1));
  next.addEventListener('click', () => goTo(index + 1));
  dots.forEach(d => d.addEventListener('click', () => goTo(+d.dataset.go)));
  document.addEventListener('keydown', (e) => {
    if (/^(TEXTAREA|INPUT)$/.test(document.activeElement.tagName)) return;  // não atrapalha o painel de edição
    if (e.key === 'ArrowRight') goTo(index + 1);
    if (e.key === 'ArrowLeft') goTo(index - 1);
  });
  viewport.addEventListener('pointerdown', (e) => { dragging = true; startX = e.clientX; currentX = -index * slideW; track.style.transition = 'none'; viewport.setPointerCapture(e.pointerId); });
  viewport.addEventListener('pointermove', (e) => { if(!dragging) return; track.style.transform = 'translateX(' + (currentX + e.clientX - startX) + 'px)'; });
  viewport.addEventListener('pointerup', (e) => { if(!dragging) return; dragging = false; const dx = e.clientX - startX; if (dx < -60) goTo(index + 1); else if (dx > 60) goTo(index - 1); else goTo(index); });
  viewport.addEventListener('pointerleave', () => { if(dragging){ dragging = false; goTo(index); } });
  goTo(0);
})();
</script>
'''
FRAME = base.FRAME.replace("".join(base.SLIDES), "".join(SLIDES)).replace(f'<div class="ig-dots">{base.DOTS}</div>', NAV)
assert NAV in FRAME
html = HEAD + NAV_CSS + FRAME + EDITOR + NAV_JS
html = html.replace("Arrasta pro lado que eu te explico.", "Arrasta que eu explico.")
assert "".join(SLIDES) in html
assert not re.search(r"[—–]", re.sub(r"<[^>]+>", "", "".join(SLIDES))), "travessão na copy"
(base.HERE / "carousel.html").write_text(html, encoding="utf-8")
print("carousel.html", len(html) // 1024, "KB")
