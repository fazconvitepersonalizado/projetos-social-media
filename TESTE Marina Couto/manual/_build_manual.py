"""Gera manual/manual-marina-couto.html (+ manual/img/ em tamanho web).

Uso: python _build_manual.py
Lê brand-kit.json, logo/*.svg e assets/*.jpg da pasta do cliente.
"""
import json
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
KIT = json.loads((ROOT / "brand-kit.json").read_text(encoding="utf-8"))
IMG = HERE / "img"
IMG.mkdir(exist_ok=True)

# Fotos em tamanho web (o tratado fica em assets/, o original em assets/raw/)
for f in sorted((ROOT / "assets").glob("*.jpg")):
    im = Image.open(f)
    im.thumbnail((900, 1600))
    im.save(IMG / f.name, quality=82)


def svg(name, cls=""):
    s = (ROOT / "logo" / name).read_text(encoding="utf-8")
    return s.replace("<svg ", f'<svg class="{cls}" role="img" aria-label="{name}" ', 1)


BIO = KIT["brand_manual"]["bio"]
BIO_LEN = len(BIO)

# Grade de 12 posts da prévia: (tipo, conteúdo, título)
GRID = [
    ("photo", "01-jantar-caseiro.jpg", "Carboidrato à noite engorda?"),
    ("type-blue", None, "Comida de verdade, sem neura."),
    ("photo", "02-marmitas.jpg", "Marmitas da semana em 1 hora"),
    ("type-dark", None, "Prazer, Marina Couto"),
    ("photo", "04-lanches.jpg", "5 lanches pra levar ao trabalho"),
    ("type-cream", None, "Fruta engorda?"),
    ("photo", "05-mulher-xicara.jpg", "Fome emocional: como reconhecer"),
    ("type-blue", None, "A dieta da moda passa. A rotina fica."),
    ("photo", "06-bolo.jpg", "Comi o doce. E agora?"),
    ("type-dark", None, "Como ler o rótulo em 30 segundos"),
    ("photo", "07-feira.jpg", "Comer em Paz começa na feira"),
    ("photo", "03-maos-legumes.jpg", "Como funciona o Comer em Paz"),
]


def tile(kind, img, title):
    if kind == "photo":
        return (f'<div class="tile photo"><img src="img/{img}" alt="">'
                f'<span>{title}</span></div>')
    return f'<div class="tile {kind}"><span>{title}</span></div>'


grid_html = "\n".join(tile(*g) for g in GRID)

HTML = """<title>Manual Marina Couto</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400;1,8..60,600&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,700&family=DM+Mono:wght@400;500&display=swap">
<style>
/* Layout: caderno de cozinha; cada seção é uma página com etiqueta em mono à esquerda e conteúdo à direita.
   Tema único (as cores do manual são as cores reais da marca; não invertem no modo escuro). */
:root {
  --creme: #F4EEE3; --areia: #E6DCCB; --pedra: #8A8174; --grafite: #2E2A25;
  --azul: #9EC3DA; --azul-fundo: #3D6A85; --branco: #FFFDF9;
  --f-display: "Source Serif 4", Georgia, "Times New Roman", serif;
  --f-body: "DM Sans", "Segoe UI", system-ui, sans-serif;
  --f-mono: "DM Mono", ui-monospace, Consolas, monospace;
  --step--1: 0.8125rem; --step-0: 1rem; --step-1: 1.25rem; --step-2: 1.75rem; --step-3: 2.5rem; --step-4: clamp(2.75rem, 7vw, 5rem);
  color-scheme: light;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--creme); color: var(--grafite); font: 400 var(--step-0)/1.6 var(--f-body); }
.wrap { max-width: 1120px; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
h1, h2, h3 { font-family: var(--f-display); font-weight: 400; text-wrap: balance; margin: 0; line-height: 1.1; }
h2 { font-size: var(--step-3); }
h2 em, h1 em { font-style: italic; color: var(--azul-fundo); }
h3 { font-size: var(--step-1); font-weight: 600; }
p { margin: 0; max-width: 62ch; }
.label { font: 500 var(--step--1)/1.3 var(--f-mono); letter-spacing: 0.14em; text-transform: uppercase; color: var(--pedra); }
.test-flag { display: inline-block; font: 500 0.75rem/1 var(--f-mono); letter-spacing: 0.12em; text-transform: uppercase; background: var(--grafite); color: var(--creme); padding: 7px 10px; border-radius: 4px; }

/* Seções */
section { border-top: 1px solid var(--areia); padding-block: 72px; }
.sec { display: grid; grid-template-columns: 200px minmax(0, 1fr); gap: 32px; }
.sec > .label { padding-top: 10px; }
.sec-body { display: grid; gap: 28px; min-width: 0; }
@media (max-width: 760px) { .sec { grid-template-columns: minmax(0, 1fr); gap: 16px; } section { padding-block: 48px; } }

/* Capa */
.cover { border-top: 0; padding-block: 56px 80px; }
.cover-top { display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; }
.cover-mark { margin-block: 72px 40px; }
.cover-mark svg { width: min(640px, 100%); height: auto; display: block; }
.cover-meta { display: flex; gap: 32px; flex-wrap: wrap; }
.cover-meta div { display: grid; gap: 4px; }
.cover-meta b { font: 500 var(--step-0) var(--f-body); }
.cover-photo { margin-top: 56px; border-radius: 6px; overflow: hidden; aspect-ratio: 16 / 7; max-width: 100%; }
.cover-photo img { width: 100%; height: 100%; object-fit: cover; object-position: 50% 62%; display: block; }

/* Essência */
.thesis { font: 400 var(--step-2)/1.3 var(--f-display); max-width: 30ch; }
.trio { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }
.trio div { border-top: 2px solid var(--grafite); padding-top: 12px; display: grid; gap: 6px; }
@media (max-width: 640px) { .trio { grid-template-columns: minmax(0, 1fr); } }

/* Nome e perfil */
.handles { display: grid; gap: 0; border: 1px solid var(--areia); border-radius: 6px; background: var(--branco); }
.handles div { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 12px; padding: 14px 18px; border-bottom: 1px solid var(--areia); align-items: baseline; }
.handles div:last-child { border-bottom: 0; }
.handles code { font: 500 var(--step-1) var(--f-mono); overflow-wrap: anywhere; }
.handles .rec { background: var(--azul); }
.handles small { font: 400 var(--step--1) var(--f-body); color: var(--grafite); }
.bio { white-space: pre-line; font-size: var(--step-1); line-height: 1.5; border-left: 3px solid var(--azul); padding-left: 16px; }

/* Assinatura */
.marks { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }
.mark { aspect-ratio: 4 / 3; max-width: 100%; border-radius: 6px; display: grid; place-items: center; padding: 24px; }
.mark svg { width: 100%; height: auto; max-height: 100%; }
.mark.on-creme { background: var(--branco); border: 1px solid var(--areia); }
.mark.on-dark { background: var(--grafite); }
.mark.on-blue { background: var(--azul); }
.mark.mono svg { width: 55%; }
.mark-cap { font: 400 var(--step--1) var(--f-mono); color: var(--pedra); margin-top: 6px; }
@media (max-width: 640px) { .marks { grid-template-columns: minmax(0, 1fr); } }
.rules { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 24px; }
.rules ul { margin: 8px 0 0; padding-left: 18px; display: grid; gap: 6px; }
@media (max-width: 640px) { .rules { grid-template-columns: minmax(0, 1fr); } }

/* Cores */
.swatches { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }
.sw { border-radius: 6px; overflow: hidden; border: 1px solid var(--areia); background: var(--branco); }
.sw .chip { height: 110px; }
.sw .info { padding: 12px 14px; display: grid; gap: 2px; }
.sw .info b { font-weight: 500; }
.sw .info code { font: 400 var(--step--1) var(--f-mono); color: var(--pedra); }
.sw.main { grid-column: span 2; }
.sw.main .chip { height: 180px; }
@media (max-width: 640px) { .swatches { grid-template-columns: repeat(2, minmax(0, 1fr)); } .sw.main { grid-column: span 2; } }
.ratio { display: flex; height: 36px; border-radius: 4px; overflow: hidden; border: 1px solid var(--areia); }
.ratio span { display: grid; place-items: center; font: 500 0.7rem var(--f-mono); }
.contrast { width: 100%; border-collapse: collapse; font-size: var(--step--1); }
.contrast th, .contrast td { text-align: left; padding: 10px 8px; border-bottom: 1px solid var(--areia); }
.contrast td.num { font-variant-numeric: tabular-nums; font-family: var(--f-mono); }
.pill { display: inline-block; padding: 4px 10px; border-radius: 3px; font-weight: 500; }
.table-scroll { overflow-x: auto; }

/* Tipografia */
.type-rows { display: grid; gap: 0; }
.type-row { display: grid; grid-template-columns: 180px minmax(0, 1fr); gap: 24px; padding-block: 24px; border-bottom: 1px solid var(--areia); align-items: baseline; }
.type-row .spec { display: grid; gap: 4px; }
.type-row .spec b { font-weight: 500; overflow-wrap: anywhere; }
.sample-display { font: 400 var(--step-4)/1 var(--f-display); }
.sample-display em { color: var(--azul-fundo); }
.sample-body { font: 400 var(--step-1)/1.5 var(--f-body); max-width: 46ch; }
.sample-body b { font-weight: 700; display: block; font-size: var(--step-2); line-height: 1.15; margin-bottom: 8px; }
.sample-mono { font: 500 var(--step-0) var(--f-mono); letter-spacing: 0.16em; text-transform: uppercase; }
@media (max-width: 640px) { .type-row { grid-template-columns: minmax(0, 1fr); gap: 8px; } }

/* Imagem */
.photos { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; }
.photos img { width: 100%; aspect-ratio: 4 / 5; object-fit: cover; border-radius: 4px; display: block; }
@media (max-width: 640px) { .photos { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
.prompt { font: 400 var(--step--1)/1.6 var(--f-mono); background: var(--grafite); color: var(--creme); padding: 18px 20px; border-radius: 6px; overflow-wrap: anywhere; }

/* Tom */
.voice { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }
.voice > div { padding: 20px; border-radius: 6px; display: grid; gap: 10px; align-content: start; }
.voice .yes { background: var(--azul); }
.voice .no { background: var(--branco); border: 1px solid var(--areia); }
.voice ul { margin: 0; padding-left: 18px; display: grid; gap: 6px; }
.voice .no li { text-decoration: line-through; text-decoration-color: var(--pedra); }
@media (max-width: 640px) { .voice { grid-template-columns: minmax(0, 1fr); } }
.caption { background: var(--branco); border: 1px solid var(--areia); border-radius: 6px; padding: 20px; white-space: pre-line; max-width: 60ch; }

/* Conteúdo */
.pillars { display: grid; gap: 14px; }
.pillar { display: grid; grid-template-columns: minmax(0, 1fr) 3.5rem; gap: 6px 16px; align-items: center; }
.pillar .bar { grid-column: 1 / -1; height: 10px; background: var(--areia); border-radius: 5px; overflow: hidden; }
.pillar .bar i { display: block; height: 100%; background: var(--azul-fundo); }
.pillar .pct { font: 500 var(--step-0) var(--f-mono); text-align: right; font-variant-numeric: tabular-nums; }
.freq { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; }
.freq div { border-top: 2px solid var(--grafite); padding-top: 10px; }
.freq b { font: 400 var(--step-3)/1 var(--f-display); display: block; }
@media (max-width: 640px) { .freq { grid-template-columns: repeat(2, minmax(0, 1fr)); } }

/* Prévia do Instagram */
.ig-wrap { display: grid; grid-template-columns: minmax(0, 400px) minmax(0, 1fr); gap: 40px; align-items: start; }
@media (max-width: 860px) { .ig-wrap { grid-template-columns: minmax(0, 1fr); } }
.phone { background: var(--branco); border: 1px solid var(--areia); border-radius: 28px; padding: 22px 0 0; overflow: hidden; max-width: 400px; width: 100%; }
.ig-head { padding: 0 16px; display: grid; gap: 12px; }
.ig-handle { font: 700 1rem var(--f-body); }
.ig-row { display: grid; grid-template-columns: 84px minmax(0, 1fr); gap: 18px; align-items: center; }
.avatar { width: 84px; height: 84px; border-radius: 50%; background: var(--azul); display: grid; place-items: center; }
.avatar svg { width: 64%; height: auto; }
.stats { display: grid; grid-template-columns: repeat(3, 1fr); text-align: center; font-size: 0.8rem; }
.stats b { display: block; font-size: 1rem; font-variant-numeric: tabular-nums; }
.ig-name { font-weight: 700; font-size: 0.875rem; }
.ig-cat { color: var(--pedra); font-size: 0.8rem; }
.ig-bio { white-space: pre-line; font-size: 0.875rem; line-height: 1.4; }
.ig-btns { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 6px; }
.ig-btns span { background: var(--areia); border-radius: 8px; text-align: center; font: 500 0.8rem/1 var(--f-body); padding: 9px 4px; }
.ig-btns span:first-child { background: var(--azul-fundo); color: var(--branco); }
.hl { display: flex; gap: 14px; overflow-x: auto; padding-bottom: 4px; }
.hl div { display: grid; justify-items: center; gap: 4px; font-size: 0.7rem; flex: none; }
.hl i { width: 58px; height: 58px; border-radius: 50%; border: 2px solid var(--azul); display: grid; place-items: center; font: italic 400 1.35rem var(--f-display); color: var(--azul-fundo); background: var(--creme); }
.grid12 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2px; margin-top: 14px; }
.tile { aspect-ratio: 4 / 5; position: relative; overflow: hidden; display: grid; padding: 7%; align-content: end; container-type: inline-size; }
.tile span { position: relative; font: 400 10cqi/1.15 var(--f-display); }
.tile.photo img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.tile.photo::after { content: ""; position: absolute; inset: 0; background: linear-gradient(to top, rgba(46,42,37,0.78) 0%, rgba(46,42,37,0.35) 45%, rgba(46,42,37,0) 70%); }
.tile.photo span { z-index: 1; color: var(--branco); }
.tile.type-blue { background: var(--azul); align-content: center; }
.tile.type-dark { background: var(--grafite); color: var(--creme); align-content: center; }
.tile.type-cream { background: var(--creme); align-content: center; border: 1px solid var(--areia); }
.tile.type-blue span, .tile.type-dark span, .tile.type-cream span { font-size: 11.5cqi; font-style: italic; }

/* Posts em tamanho real e story */
.posts { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; }
@media (max-width: 960px) { .posts { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 640px) { .posts { grid-template-columns: minmax(0, 1fr); } }
.post { aspect-ratio: 4 / 5; max-width: 100%; border-radius: 4px; overflow: hidden; position: relative; display: grid; padding: 9%; container-type: inline-size; }
.post .n { font: 500 3.2cqi var(--f-mono); letter-spacing: 0.14em; }
.post h4 { margin: 0; font: 400 10.5cqi/1.05 var(--f-display); text-wrap: balance; }
.post h4 em { font-style: italic; }
.post p { font-size: 4.6cqi; }
.post .sig { font: 500 3cqi var(--f-mono); letter-spacing: 0.14em; text-transform: uppercase; }
.post.cover-post { color: var(--branco); align-content: space-between; }
.post.cover-post img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: 50% 70%; }
.post.cover-post::before { content: ""; position: absolute; inset: 0; background: linear-gradient(to bottom, rgba(46,42,37,0.72) 0%, rgba(46,42,37,0.45) 42%, rgba(46,42,37,0) 64%), rgba(46,42,37,0.15); }
.post.cover-post > * { position: relative; }
.chip-logo { justify-self: start; background: rgba(0,0,0,0.24); padding: 6px 8px; border-radius: 7px; display: inline-flex; }
.chip-logo svg { width: 32cqi; height: auto; }
.post.tip { background: var(--creme); border: 1px solid var(--areia); align-content: space-between; }
.post.tip ol { margin: 0; padding-left: 1.2em; display: grid; gap: 2cqi; font-size: 4.8cqi; }
.post.quote { background: var(--azul); align-content: center; gap: 18px; }
.post.invite { background: var(--grafite); color: var(--creme); align-content: space-between; }
.post.invite .btn { justify-self: start; background: var(--azul); color: var(--grafite); font: 500 4.2cqi var(--f-body); padding: 2.6cqi 4cqi; border-radius: 4px; }
.post.invite em { color: var(--azul); }
.story { aspect-ratio: 9 / 16; max-width: 300px; width: 100%; border-radius: 16px; overflow: hidden; position: relative; display: grid; align-content: start; padding: 22% 9% 0; gap: 16px; }
.story img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.story::before { content: ""; position: absolute; inset: 0; background: linear-gradient(to bottom, rgba(244,238,227,0.55), rgba(244,238,227,0) 55%); }
.story > *:not(img) { position: relative; }
.story h4 { margin: 0; font: 400 1.6rem/1.1 var(--f-display); text-align: center; }
.poll { background: var(--branco); border-radius: 12px; padding: 12px; display: grid; gap: 8px; box-shadow: 0 6px 20px rgba(46,42,37,0.18); }
.poll span { border: 1px solid var(--areia); border-radius: 8px; padding: 9px; text-align: center; font: 500 0.85rem var(--f-body); }
.poll span:first-child { background: var(--azul); border-color: var(--azul); }
.story-col { display: grid; gap: 16px; justify-items: start; }

/* Pendências */
.todo { display: grid; gap: 0; border: 1px solid var(--areia); border-radius: 6px; background: var(--branco); }
.todo div { padding: 14px 18px; border-bottom: 1px solid var(--areia); display: grid; gap: 2px; }
.todo div:last-child { border-bottom: 0; }
.todo small { color: var(--pedra); }
footer { padding-block: 40px 64px; border-top: 1px solid var(--areia); display: flex; gap: 16px; justify-content: space-between; flex-wrap: wrap; }

:focus-visible { outline: 2px solid var(--azul-fundo); outline-offset: 3px; }
@media print { section { break-before: page; } .cover { break-before: auto; } }
</style>

<div class="wrap">

<section class="cover">
  <div class="cover-top"><span class="label">Manual da marca · v1 · outubro 2026</span><span class="test-flag">Cliente fictício de teste</span></div>
  <div class="cover-mark">{{LOGO_PRIMARY}}</div>
  <div class="cover-meta">
    <div><span class="label">Conceito</span><b>Comer em Paz</b></div>
    <div><span class="label">Perfil</span><b>@marinacouto</b></div>
    <div><span class="label">Atendimento</span><b>Online e Campinas (SP)</b></div>
  </div>
  <div class="cover-photo"><img src="img/01-jantar-caseiro.jpg" alt="Jantar caseiro com arroz, feijão, legumes e frango num prato azul claro"></div>
</section>

<section id="essencia"><div class="sec">
  <span class="label">01 · Essência</span>
  <div class="sec-body">
    <h2>Comer em <em>Paz</em></h2>
    <p class="thesis">Marina Couto ajuda mulheres com rotina corrida a comer bem sem culpa e sem dieta da moda, com um plano feito em cima da rotina real delas.</p>
    <p>O nome do programa principal da Marina vira o conceito da marca: a paz com a comida no lugar da guerra das dietas. A mesa posta simples, a cozinha de casa e a comida de verdade são o universo visual e verbal. Metáforas de mesa e cozinha aparecem com moderação.</p>
    <div class="trio">
      <div><h3>Acolhedora</h3><p>Fala com quem já tentou de tudo, sem bronca e sem culpa.</p></div>
      <div><h3>Prática</h3><p>Toda dica cabe numa semana corrida, com o que tem em casa.</p></div>
      <div><h3>Leve</h3><p>Sem terrorismo nutricional; ciência dita em linguagem de conversa.</p></div>
    </div>
    <p><b>Para quem:</b> mulheres de 28 a 45 anos, que trabalham fora, vivem o efeito sanfona e sentem culpa depois de comer. Querem energia, praticidade e emagrecer sem sofrimento.</p>
  </div>
</div></section>

<section id="perfil"><div class="sec">
  <span class="label">02 · Nome e perfil</span>
  <div class="sec-body">
    <h2>Marina Couto, <em>pelo nome</em></h2>
    <p>Marca pessoal: o nome é a marca. Sem título antes do nome, a pedido da Marina. As opções abaixo estão em ordem de preferência; a disponibilidade de cada @ ainda precisa ser conferida.</p>
    <div class="handles">
      <div class="rec"><code>@marinacouto</code><small>Recomendado: curto, fácil de ditar</small></div>
      <div><code>@marina.couto</code><small>2ª opção</small></div>
      <div><code>@marinacouto.nutri</code><small>Se as duas primeiras estiverem ocupadas</small></div>
      <div><code>@nutri.couto</code><small>Última alternativa</small></div>
    </div>
    <div><span class="label">Nome de exibição</span><p style="font-size:var(--step-1)">Marina Couto | Nutricionista</p></div>
    <div><span class="label">Bio · {{BIO_LEN}} de 150 caracteres</span><p class="bio">{{BIO}}</p></div>
    <div><span class="label">Destaques</span><p>Comece aqui · Consulta · Comer em Paz · Receitas · Dúvidas</p></div>
  </div>
</div></section>

<section id="assinatura"><div class="sec">
  <span class="label">03 · Assinatura</span>
  <div class="sec-body">
    <h2>Assinatura e <em>monograma</em></h2>
    <p>"Marina" em Fraunces regular e "Couto" em Fraunces itálico, com NUTRICIONISTA em DM Mono espaçado. O monograma MC usa a mesma lógica e vai na foto de perfil e nas capas de destaque.</p>
    <div class="marks">
      <div><div class="mark on-creme">{{LOGO_PRIMARY}}</div><div class="mark-cap">Principal · sobre claro</div></div>
      <div><div class="mark on-dark">{{LOGO_WHITE}}</div><div class="mark-cap">Branca · sobre escuro e foto</div></div>
      <div><div class="mark on-blue">{{LOGO_DARK}}</div><div class="mark-cap">Grafite · sobre azul claro</div></div>
      <div><div class="mark on-creme mono">{{MONO_PRIMARY}}</div><div class="mark-cap">Monograma principal</div></div>
      <div><div class="mark on-dark mono">{{MONO_WHITE}}</div><div class="mark-cap">Monograma branco</div></div>
      <div><div class="mark on-blue mono">{{MONO_DARK}}</div><div class="mark-cap">Monograma na foto de perfil</div></div>
    </div>
    <div class="rules">
      <div><h3>Área de respiro</h3><p>Em volta da assinatura, deixar livre no mínimo a altura do "M" de Marina. Tamanho mínimo: 120 px de largura no digital.</p></div>
      <div><h3>Não fazer</h3><ul>
        <li>Distorcer, inclinar ou trocar as fontes.</li>
        <li>Usar o azul claro como cor do texto sobre fundo creme ou branco.</li>
        <li>Colocar sobre rosto em foto ou sobre área poluída sem o fundo de proteção.</li>
        <li>Separar "Marina" e "Couto" em linhas com cores trocadas.</li>
      </ul></div>
    </div>
  </div>
</div></section>

<section id="cores"><div class="sec">
  <span class="label">04 · Cores</span>
  <div class="sec-body">
    <h2>Creme, grafite e <em>azul claro</em></h2>
    <p>A Marina escolheu o azul claro como cor principal. Como ele é claro demais para texto, ganha um par: o Azul Profundo, usado sempre que o azul precisa ser lido.</p>
    <div class="swatches">
      <div class="sw main"><div class="chip" style="background:var(--azul)"></div><div class="info"><b>Azul Claro · cor principal</b><code>#9EC3DA · fundos, blocos, destaques; texto grafite por cima</code></div></div>
      <div class="sw"><div class="chip" style="background:var(--azul-fundo)"></div><div class="info"><b>Azul Profundo</b><code>#3D6A85 · azul como texto e botão</code></div></div>
      <div class="sw"><div class="chip" style="background:var(--creme)"></div><div class="info"><b>Creme Linho</b><code>#F4EEE3 · fundo principal</code></div></div>
      <div class="sw"><div class="chip" style="background:var(--areia)"></div><div class="info"><b>Areia</b><code>#E6DCCB · bordas, apoio</code></div></div>
      <div class="sw"><div class="chip" style="background:var(--grafite)"></div><div class="info"><b>Grafite Café</b><code>#2E2A25 · texto, fundo escuro</code></div></div>
    </div>
    <div><span class="label">Proporção numa peça</span>
      <div class="ratio" aria-label="Proporção de cores">
        <span style="flex:55;background:var(--creme)">Creme 55%</span>
        <span style="flex:20;background:var(--grafite);color:var(--creme)">Grafite 20%</span>
        <span style="flex:15;background:var(--azul)">Azul 15%</span>
        <span style="flex:10;background:var(--areia)">10%</span>
      </div>
    </div>
    <div class="table-scroll"><table class="contrast">
      <thead><tr><th>Combinação</th><th>Contraste</th><th>Uso</th></tr></thead>
      <tbody>
        <tr><td><span class="pill" style="background:var(--azul);color:var(--grafite)">Grafite sobre Azul Claro</span></td><td class="num">7,6 : 1</td><td>Liberado para qualquer texto</td></tr>
        <tr><td><span class="pill" style="background:var(--creme);color:var(--azul-fundo);border:1px solid var(--areia)">Azul Profundo sobre Creme</span></td><td class="num">5,0 : 1</td><td>Títulos e destaques</td></tr>
        <tr><td><span class="pill" style="background:var(--azul-fundo);color:var(--branco)">Branco sobre Azul Profundo</span></td><td class="num">5,8 : 1</td><td>Botões e faixas</td></tr>
        <tr><td><span class="pill" style="background:var(--azul);color:var(--branco)">Branco sobre Azul Claro</span></td><td class="num">1,9 : 1</td><td>Proibido</td></tr>
      </tbody>
    </table></div>
  </div>
</div></section>

<section id="tipografia"><div class="sec">
  <span class="label">05 · Tipografia</span>
  <div class="sec-body">
    <h2>Três fontes, <em>três papéis</em></h2>
    <p>Todas do Google Fonts e disponíveis no Canva.</p>
    <div class="type-rows">
      <div class="type-row"><div class="spec"><span class="label">Destaque</span><b>Source Serif 4</b><small>Regular e itálico. Títulos e poucas palavras. A Fraunces fica só no desenho do logo.</small></div><div class="sample-display">Comer em <em>Paz</em></div></div>
      <div class="type-row"><div class="spec"><span class="label">Títulos e texto</span><b>DM Sans</b><small>Bold nos subtítulos, regular no texto.</small></div><div class="sample-body"><b>Marmita da semana em 1 hora</b>Escolha 2 proteínas, 3 legumes e 1 carboidrato. Cozinhe tudo junto no domingo e monte os potes em 15 minutos.</div></div>
      <div class="type-row"><div class="spec"><span class="label">Utilitária</span><b>DM Mono</b><small>Caixa alta espaçada. Numeração, etiquetas, rodapés.</small></div><div class="sample-mono">2/8 · Rotina prática · @marinacouto</div></div>
    </div>
  </div>
</div></section>

<section id="imagem"><div class="sec">
  <span class="label">06 · Estilo de imagem</span>
  <div class="sec-body">
    <h2>Revista de <em>cozinha de casa</em></h2>
    <p>Luz natural de janela, linho creme, madeira e louça azul clara. Comida de verdade, sem montagem de estúdio. Pessoas aparecem sem o rosto de frente. As fotos abaixo foram geradas com IA e mostram modelos, não a Marina.</p>
    <div class="photos">
      <img src="img/02-marmitas.jpg" alt="Marmitas de vidro alinhadas na bancada">
      <img src="img/03-maos-legumes.jpg" alt="Mãos cortando legumes na tábua">
      <img src="img/04-lanches.jpg" alt="Lanches para levar ao trabalho">
      <img src="img/05-mulher-xicara.jpg" alt="Mulher segurando xícara azul à mesa">
      <img src="img/06-bolo.jpg" alt="Fatia de bolo caseiro em prato azul claro">
      <img src="img/07-feira.jpg" alt="Cesta de feira com frutas e verduras">
      <img src="img/01-jantar-caseiro.jpg" alt="Jantar caseiro">
      <img src="img/08-cozinha-story.jpg" alt="Bancada de cozinha com ingredientes">
    </div>
    <div class="rules">
      <div><h3>Sempre</h3><ul><li>Luz natural, sombras suaves.</li><li>Um toque de azul claro na cena (louça, guardanapo).</li><li>Ajuste leve: contraste +4%, saturação −4%.</li></ul></div>
      <div><h3>Nunca</h3><ul><li>Comida de dieta "fitness" com balança e fita métrica.</li><li>Foto de antes e depois (aguardando regra do CFN).</li><li>IA simulando a própria Marina.</li></ul></div>
    </div>
    <div><span class="label">Prompt base para gerar com IA</span>
    <p class="prompt">Editorial food magazine photograph, natural window light, soft shadows, warm cream linen, pale light-blue ceramic. [cena]. Real, honest home cooking, calm mood. No text, no logos.</p></div>
  </div>
</div></section>

<section id="tom"><div class="sec">
  <span class="label">07 · Tom de voz</span>
  <div class="sec-body">
    <h2>Como a Marina <em>fala</em></h2>
    <p>Frases curtas, exemplos do dia a dia, termo técnico só com explicação. Nunca culpa, nunca promessa de quilos ou prazos.</p>
    <div class="voice">
      <div class="yes"><h3>Usar</h3><ul><li>"Comida de verdade, sem neura."</li><li>"Dá pra ajustar à sua rotina."</li><li>"Comeu o doce? Segue o dia normal."</li></ul></div>
      <div class="no"><h3>Evitar</h3><ul><li>"Dieta para secar em 7 dias"</li><li>"Carboidrato proibido à noite"</li><li>"Detox" e "barriga negativa"</li></ul></div>
    </div>
    <div><span class="label">Legenda modelo</span>
    <p class="caption">Você também já ouviu que carboidrato à noite engorda?
Engorda o excesso no dia todo; o horário pesa bem menos do que a quantidade e a qualidade do prato.
No Comer em Paz a gente monta o jantar que cabe na sua rotina, com arroz e feijão inclusos.
Me conta nos comentários: você evita carboidrato à noite?
Pra montar o seu plano, agende sua consulta pelo link da bio.</p></div>
  </div>
</div></section>

<section id="conteudo"><div class="sec">
  <span class="label">08 · Conteúdo</span>
  <div class="sec-body">
    <h2>Pilares e <em>frequência</em></h2>
    <div class="pillars">
      <div class="pillar"><span><b>Comer sem culpa</b> · identificação, quebra de objeção</span><span class="pct">30%</span><span class="bar"><i style="width:30%"></i></span></div>
      <div class="pillar"><span><b>Rotina prática</b> · educar, mostrar o método</span><span class="pct">30%</span><span class="bar"><i style="width:30%"></i></span></div>
      <div class="pillar"><span><b>Sem neura</b> · mitos, autoridade</span><span class="pct">25%</span><span class="bar"><i style="width:25%"></i></span></div>
      <div class="pillar"><span><b>Comer em Paz</b> · convite, bastidores, venda</span><span class="pct">15%</span><span class="bar"><i style="width:15%"></i></span></div>
    </div>
    <div class="freq">
      <div><b>2</b>carrosséis por semana</div>
      <div><b>1</b>post único por semana</div>
      <div><b>3</b>dias de stories por semana</div>
      <div><b>0</b>Reels; a Marina não grava vídeo por enquanto</div>
    </div>
  </div>
</div></section>

<section id="previa"><div class="sec">
  <span class="label">09 · Prévia do Instagram</span>
  <div class="sec-body">
    <h2>O perfil <em>no dia da estreia</em></h2>
    <p>Grade de estreia com os 12 primeiros posts, alternando foto e post tipográfico para a grade respirar.</p>
    <div class="ig-wrap">
      <div class="phone">
        <div class="ig-head">
          <div class="ig-handle">marinacouto</div>
          <div class="ig-row"><div class="avatar">{{MONO_DARK}}</div>
            <div class="stats"><div><b>12</b>posts</div><div><b>0</b>seguidores</div><div><b>0</b>seguindo</div></div></div>
          <div><div class="ig-name">Marina Couto | Nutricionista</div><div class="ig-cat">Nutricionista</div><div class="ig-bio">{{BIO}}</div></div>
          <div class="ig-btns"><span>Seguir</span><span>Mensagem</span><span>WhatsApp</span></div>
          <div class="hl"><div><i>MC</i>Comece aqui</div><div><i>C</i>Consulta</div><div><i>P</i>Comer em Paz</div><div><i>R</i>Receitas</div><div><i>?</i>Dúvidas</div></div>
        </div>
        <div class="grid12">{{GRID}}</div>
      </div>
      <div class="sec-body">
        <div class="story-col">
          <div><span class="label">Story com enquete</span><p style="margin-top:8px">Stories sem vídeo: enquete e caixinha de perguntas sobre foto do dia a dia. A resposta vira tema de carrossel.</p></div>
          <div class="story"><img src="img/08-cozinha-story.jpg" alt=""><h4>Você come <em>carboidrato</em> à noite?</h4><div class="poll"><span>Sim, sem culpa</span><span>Evito</span></div></div>
        </div>
      </div>
    </div>
    <span class="label">4 posts em tamanho real</span>
    <div class="posts">
          <div class="post cover-post"><img src="img/01-jantar-caseiro.jpg" alt=""><div style="display:grid;gap:3.5cqi"><span class="chip-logo">{{LOGO_WHITE}}</span><h4>Carboidrato à noite <em>engorda?</em></h4></div><span class="sig">Arraste para o lado →</span></div>
          <div class="post tip"><span class="n">ROTINA PRÁTICA · 3/8</span><div style="display:grid;gap:3.5cqi"><h4>Marmita em <em>1 hora</em></h4><ol><li>2 proteínas</li><li>3 legumes</li><li>1 carboidrato</li><li>Monte os potes em 15 minutos</li></ol></div><span class="sig">@marinacouto</span></div>
          <div class="post quote"><span class="n">SEM NEURA</span><h4>A dieta da moda passa. <em>A rotina fica.</em></h4><span class="sig">Marina Couto · Nutricionista</span></div>
          <div class="post invite"><span class="n">COMER EM PAZ</span><div style="display:grid;gap:3cqi"><h4>Comer bem <em>sem culpa</em> cabe na sua semana.</h4><p>Acompanhamento de 3 meses, online ou em Campinas.</p></div><span class="btn">Agende pelo link da bio</span></div>
        </div>
  </div>
</div></section>

<section id="pendencias"><div class="sec">
  <span class="label">10 · Pendências</span>
  <div class="sec-body">
    <h2>A confirmar com <em>a Marina</em></h2>
    <div class="todo">
      <div><b>Disponibilidade do @marinacouto</b><small>Conferir ao criar a conta; se ocupado, seguir a ordem das alternativas.</small></div>
      <div><b>Aprovação da bio e do nome de exibição</b><small>"Posso usar essa bio no perfil?"</small></div>
      <div><b>CRN na bio ou nas peças</b><small>Conferir a regra atual do CFN antes da estreia.</small></div>
      <div><b>Regras sobre antes e depois</b><small>Enquanto não confirmar, não usar.</small></div>
      <div><b>Ensaio de fotos profissionais</b><small>Previsão de data; até lá, imagens geradas com IA (modelos).</small></div>
      <div><b>Concorrentes e referências do nicho</b><small>Pergunta 11 do briefing, sem resposta.</small></div>
    </div>
  </div>
</div></section>

<footer><span class="label">Marina Couto · Manual da marca v1</span><span class="label">Cliente fictício de teste · outubro 2026</span></footer>
</div>
"""

out = (HTML
       .replace("{{LOGO_PRIMARY}}", svg("logo-primary.svg"))
       .replace("{{LOGO_WHITE}}", svg("logo-white.svg"))
       .replace("{{LOGO_DARK}}", svg("logo-dark.svg"))
       .replace("{{MONO_PRIMARY}}", svg("monograma-primary.svg"))
       .replace("{{MONO_WHITE}}", svg("monograma-white.svg"))
       .replace("{{MONO_DARK}}", svg("monograma-dark.svg"))
       .replace("{{BIO_LEN}}", str(BIO_LEN))
       .replace("{{BIO}}", BIO)
       .replace("{{GRID}}", grid_html))
assert "{{" not in out
(HERE / "manual-marina-couto.html").write_text(out, encoding="utf-8")
print("ok", len(out) // 1024, "KB; bio", BIO_LEN, "chars")
