# Navegação da prévia (setas, pontos, contador, teclado)

Padrão desde 2026-10-19 (pedido do Thiago): toda prévia `carousel.html`
tem controles para navegar sem precisar arrastar. Eles ficam **na faixa dos
pontinhos, fora da área do slide** (`.ig-viewport`), então nunca entram no
export (`export.md` / `export_carousel.py` capturam só `.ig-viewport`) nem
na verificação visual (que esconde `.ig-dots`). Continuam no HTML limpo
baixado pelo painel de edição, o que é desejado.

O que tem:
- botões ‹ e › (cor da marca no hover, esmaecidos no primeiro/último slide);
- pontos clicáveis (o atual vira um tracinho na cor da marca);
- contador "n/total";
- setas ← → do teclado (ignoradas enquanto se digita no painel);
- arrastar continua funcionando.

## Como montar (Python, ao gerar o HTML)

No lugar de `<div class="ig-dots">…pontos…</div>` da moldura, use `NAV`;
coloque `NAV_CSS` depois do `<style>` principal e `NAV_JS` **no lugar** do
script de swipe antigo (ele já inclui o arrastar). Troque `{BRAND_PRIMARY}`
pelo hex real.

```python
TOTAL = 8  # número de slides
BRAND_PRIMARY = "#3D6A85"  # hex real do brand-kit

CHEV = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="{d}"/></svg>')
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
  .ig-nav .ig-dot.on {{ width:18px; background:{BRAND_PRIMARY}; }}
  .ig-nav-btn {{ width:34px; height:34px; border-radius:50%; border:1px solid rgba(0,0,0,0.12); background:#fff; color:#111;
    display:flex; align-items:center; justify-content:center; cursor:pointer; transition:background .15s, color .15s, opacity .15s; }}
  .ig-nav-btn:hover:not(:disabled) {{ background:{BRAND_PRIMARY}; color:#fff; border-color:{BRAND_PRIMARY}; }}
  .ig-nav-btn:disabled {{ opacity:.3; cursor:default; }}
  .ig-nav-btn:focus-visible, .ig-nav .ig-dot:focus-visible {{ outline:2px solid {BRAND_PRIMARY}; outline-offset:2px; }}
  .ig-nav-count {{ font:500 12px ui-monospace, monospace; color:#666; min-width:30px; text-align:center; }}
</style>'''
NAV_JS = """<script>
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
    if (/^(TEXTAREA|INPUT)$/.test(document.activeElement.tagName)) return;
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
"""
```

As classes `.ig-viewport` e `.ig-track` são as da moldura padrão; se a
moldura usar outros nomes (carrosséis antigos usavam `.carousel-viewport` /
`.carousel-track`), ajuste os seletores. Referência pronta e testada:
`TESTE Marina Couto/conteudos/2026-10-19-carboidrato-a-noite-engorda/_generate.py`.

## Conferência

Depois de gerar, abra a prévia (Playwright) e confira: clicar em › avança,
o último ponto leva ao último slide com › desativado, a seta do teclado
avança, e nenhum erro de JS.
