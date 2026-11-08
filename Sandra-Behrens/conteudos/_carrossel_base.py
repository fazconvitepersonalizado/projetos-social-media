# -*- coding: utf-8 -*-
"""Base comum dos carrosséis da Sandra Behrens a partir de novembro/2026.

Adaptada da base da A&J (mesma moldura .ig-viewport/.ig-track do export_carousel.py, navegação de
references/preview-nav.md e painel de references/edit-panel.md), com a identidade da Sandra:
Cormorant Garamond nos títulos, Poppins no apoio, Parisienne só na assinatura ("Vamos conversar
sobre você?") e no monograma; fundos chapados creme, oliva, dourado e dourado escuro; destaque em
itálico; logo completa (texto do SVG da marca) na capa e no CTA, nos tamanhos fixados em 2026-09-14
(hero 160x70, cta 280x122); loguinho de canto de uma cor só no meio (padrão geral de 2026-10-20),
aqui o monograma "S" em Parisienne, porque a marca não tem ícone separado do nome.
Sem etiqueta acima do título, sem granulado, sem barra de progresso nem contador (regras anti-IA).
"""
import base64
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
brand = json.loads((ROOT / "brand-kit.json").read_text(encoding="utf-8"))
D = brand["derived"]
P, PL, PD = D["BRAND_PRIMARY"], D["BRAND_LIGHT"], D["BRAND_DARK"]
LBG, LBR, DBG = D["LIGHT_BG"], D["LIGHT_BORDER"], D["DARK_BG"]
HF, BF = brand["heading_font"], brand["body_font"]
SF = brand["brand_manual"].get("signature_font", "Parisienne")
NAME, HANDLE = brand["brand_name"], brand["instagram_handle"]
CAFE, SALVIA, TERRACOTA, ROSA_ANTIGO, AREIA = "#3A342C", "#6E7359", "#B5653F", "#C7A9A4", "#E7DBC5"
OLIVA_TXT = "#2E3127"   # texto sobre o dourado chapado (~4,6:1); branco sobre dourado não passa
OURO_CLARO = "#F1D9A6"  # destaque sobre dourado escuro e oliva (só em título grande)
W, H = 420, 525

TONS = {
    "creme": {"bg": LBG, "h": CAFE, "b": "rgba(58,52,44,0.86)", "acc": PD, "mute": "rgba(58,52,44,0.70)",
              "line": LBR, "canto": DBG, "logo": (P, CAFE, SALVIA), "claro": True},
    "oliva": {"bg": DBG, "h": "#fff", "b": "rgba(255,255,255,0.86)", "acc": PL, "mute": "rgba(255,255,255,0.72)",
              "line": "rgba(255,255,255,0.16)", "canto": "#fff", "logo": (P, "#fff", "rgba(255,255,255,0.75)")},
    "dourado": {"bg": P, "h": OLIVA_TXT, "b": OLIVA_TXT, "acc": DBG, "mute": "rgba(46,49,39,0.82)",
                "line": "rgba(46,49,39,0.25)", "canto": DBG, "canto_op": 0.9, "logo": (CAFE, CAFE, CAFE), "peso": 600},
    "ouro_escuro": {"bg": PD, "h": "#fff", "b": "#fff", "acc": OURO_CLARO, "mute": "rgba(255,255,255,0.78)",
                    "line": "rgba(255,255,255,0.2)", "canto": "#fff", "logo": (OURO_CLARO, "#fff", "rgba(255,255,255,0.8)")},
    # sobre foto: destaque em branco itálico (nunca a cor clara da marca sobre foto)
    "foto": {"bg": DBG, "h": "#fff", "b": "rgba(255,255,255,0.92)", "acc": "#fff", "mute": "rgba(255,255,255,0.85)",
             "line": "rgba(255,255,255,0.25)", "canto": "#fff", "logo": ("#fff", "#fff", "rgba(255,255,255,0.85)")},
}


def tom(nome):
    return TONS[nome]


def foto(path: Path) -> str:
    return "data:image/jpeg;base64," + base64.b64encode(Path(path).read_bytes()).decode()


# ---------------------------------------------------------------- texto
def h(n, html, t, size=40, role="headline", weight=600, lh=1.06, align=None, extra=""):
    a = f"text-align:{align};" if align else ""
    return (f'<h2 class="serif" data-edit-id="slide{n}-{role}" style="font-size:{size}px;font-weight:{weight};'
            f'line-height:{lh};letter-spacing:-0.01em;color:{t["h"]};margin:0;{a}{extra}">{html}</h2>')


def p(n, text, t, size=18, role="body", align=None, gap=16, weight=400, color=None, extra=""):
    a = f"text-align:{align};" if align else ""
    return (f'<p class="sans" data-edit-id="slide{n}-{role}" style="font-size:{size}px;line-height:1.45;'
            f'font-weight:{weight};color:{color or t["b"]};margin:{gap}px 0 0;{a}{extra}">{text}</p>')


def it(word, t, color=None):
    """Palavra-chave em itálico (peso misto; 1 ou 2 por carrossel)."""
    return f'<span style="font-style:italic;font-weight:600;color:{color or t["acc"]};">{word}</span>'


def assinatura(n, t, texto="Vamos conversar sobre você?", size=30, gap=22, align=None, cor=None):
    """Assinatura da marca em Parisienne (substitui o botão de app)."""
    a = f"text-align:{align};" if align else ""
    return (f'<p data-edit-id="slide{n}-assinatura" style="font-family:\'{SF}\',cursive;font-size:{size}px;line-height:1.15;'
            f'color:{cor or t["acc"]};margin:{gap}px 0 0;{a}">{texto}</p>')


# ---------------------------------------------------------------- blocos
def bloco(inner, align="left", anchor="center", pad="64px 36px 76px", maxw=360):
    jc = {"center": "center", "top": "flex-start", "bottom": "flex-end"}[anchor]
    ta = "center" if align == "center" else "left"
    return (f'<div style="position:relative;z-index:2;height:100%;display:flex;flex-direction:column;'
            f'justify-content:{jc};padding:{pad};box-sizing:border-box;text-align:{ta};">'
            f'<div style="max-width:{maxw}px;width:100%;margin:0 auto;">{inner}</div></div>')


def slide(t, inner, layers=""):
    return (f'<div class="slide" style="position:relative;width:{W}px;height:{H}px;flex:none;overflow:hidden;'
            f'background:{t["bg"]};">{layers}{inner}</div>')


# ---------------------------------------------------------------- logo
def logo_svg(t, w=160, cores=None):
    """Logo da marca (mesmo desenho de logo/logo-*.svg), nas cores do fundo: script, nome, subtítulo."""
    c1, c2, c3 = cores or t["logo"]
    hh = round(w * 210 / 480)
    return (f'<svg width="{w}" height="{hh}" viewBox="0 30 480 150" style="display:block;" role="img" aria-label="{NAME}">'
            f'<text x="240" y="90" text-anchor="middle" font-size="72" fill="{c1}" style="font-family:\'{SF}\',cursive;">Sandra</text>'
            f'<text x="240" y="136" text-anchor="middle" font-size="32" font-weight="600" letter-spacing="7" fill="{c2}" '
            f'style="font-family:\'{HF}\',serif;">BEHRENS</text>'
            f'<text x="240" y="162" text-anchor="middle" font-size="12" font-weight="500" letter-spacing="4" fill="{c3}" '
            f'style="font-family:\'{BF}\',sans-serif;">PSICÓLOGA</text></svg>')


def logo_lockup(t, w=160, align="center", gap_below=18, chip=None, cores=None):
    jc = {"center": "center", "left": "flex-start", "right": "flex-end"}[align]
    fundo = f"background:{chip};padding:6px 10px;border-radius:8px;" if chip else ""
    return (f'<div data-ap-fixo style="display:flex;justify-content:{jc};margin-bottom:{gap_below}px;">'
            f'<div style="display:inline-block;{fundo}">{logo_svg(t, w, cores)}</div></div>')


def marca_canto(i, total, t, foto_no_canto=False, canto="tl"):
    """Loguinho de canto: monograma 'S' de uma cor só pelo fundo; chip só sobre foto."""
    if not 0 < i < total - 1:
        return ""
    cor, op = t["canto"], t.get("canto_op", 0.72 if t["canto"] != "#fff" else 0.82)
    fundo = ""
    if foto_no_canto:
        cor, op = "#fff", 0.95
        fundo = "background:rgba(62,66,52,0.55);padding:2px 9px 0;border-radius:7px;"
    pos = {"tl": "top:16px;left:22px;", "tr": "top:16px;right:22px;", "bl": "bottom:16px;left:22px;"}[canto]
    return (f'<div data-ap-fixo data-ap-logo style="position:absolute;{pos}z-index:4;{fundo}">'
            f'<span style="font-family:\'{SF}\',cursive;font-size:30px;line-height:1.1;color:{cor};opacity:{op};">S</span></div>')


# ---------------------------------------------------------------- componentes
def lista(n, t, itens, size=19, gap_top=20):
    out = ""
    for k, txt in enumerate(itens, 1):
        out += (f'<div style="display:flex;gap:12px;align-items:flex-start;padding:11px 0;border-top:1px solid {t["line"]};">'
                f'<span style="flex:none;width:14px;height:2px;margin-top:13px;background:{t["acc"]};"></span>'
                f'<span class="sans" data-edit-id="slide{n}-item-{k}" style="font-size:{size}px;line-height:1.35;'
                f'color:{t["h"]};font-weight:{t.get("peso", 500)};">{txt}</span></div>')
    return f'<div style="margin-top:{gap_top}px;text-align:left;">{out}</div>'


def foto_full(src, ate=0.68, pos="50% 50%", nota="", de="baixo", rgb="62,66,52"):
    """Foto no slide inteiro + véu oliva dimensionado pelo texto + camada uniforme de reforço."""
    a = int(ate * 100)
    ang = "0deg" if de == "baixo" else "180deg"
    return (f'<!-- foto: {nota} -->'
            f'<img src="{src}" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{pos};">'
            f'<div style="position:absolute;inset:0;z-index:1;background:linear-gradient({ang},rgba({rgb},0.94) 0%,'
            f'rgba({rgb},0.86) {int(a*0.45)}%,rgba({rgb},0.6) {int(a*0.7)}%,rgba({rgb},0.22) {int(a*0.88)}%,rgba({rgb},0) {a}%);"></div>'
            f'<div style="position:absolute;inset:0;z-index:1;background:rgba({rgb},0.16);"></div>')


def foto_card(src, w, hgt, pos="50% 50%", nota="", r=10, sombra=True, extra=""):
    sh = "box-shadow:0 14px 30px rgba(0,0,0,0.18);" if sombra else ""
    return (f'<!-- foto: {nota} --><img src="{src}" alt="" data-ap-fixo style="display:block;width:{w}px;height:{hgt}px;'
            f'object-fit:cover;object-position:{pos};border-radius:{r}px;{sh}{extra}">')


# ---------------------------------------------------------------- traços (regra "nenhum slide só com fundo e texto")
def _mandala(petalas=12, aneis=True, pontos=True):
    s = '<circle cx="100" cy="100" r="92"/><circle cx="100" cy="100" r="16"/><circle cx="100" cy="100" r="6"/>'
    if aneis:
        s += '<circle cx="100" cy="100" r="40"/><circle cx="100" cy="100" r="66"/>'
    for k in range(petalas):
        a = 360 * k / petalas
        s += f'<ellipse cx="100" cy="72" rx="9" ry="22" transform="rotate({a:.1f} 100 100)"/>'
        s += f'<path d="M100 34 Q112 18 100 8 Q88 18 100 34Z" transform="rotate({a + 180 / petalas:.1f} 100 100)"/>'
        if pontos:
            x = 100 + 79 * math.cos(math.radians(a - 90))
            y = 100 + 79 * math.sin(math.radians(a - 90))
            s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3"/>'
    return s


TRACOS = {
    "mandala": _mandala(),
    "mandala8": _mandala(8, pontos=False),
    "mandala16": _mandala(16),
    "lapis": ('<path d="M40 170L150 60l20 20L60 190z"/><path d="M40 170l-8 28 28-8"/><path d="M138 72l20 20"/>'
              '<path d="M70 120l10 10"/>'),
    "espelho": ('<ellipse cx="100" cy="86" rx="56" ry="72"/><ellipse cx="100" cy="86" rx="44" ry="60"/>'
                '<path d="M100 158v26M70 190h60"/><path d="M76 60q10-16 26-20"/>'),
    "livro": ('<path d="M100 52C78 38 46 36 20 42v116c26-6 58-4 80 10 22-14 54-16 80-10V42c-26-6-58-4-80 10z"/>'
              '<path d="M100 52v116"/><path d="M38 70c16-2 34 0 46 6M38 94c16-2 34 0 46 6M116 76c12-6 30-8 46-6M116 100c12-6 30-8 46-6"/>'),
    "lua": '<path d="M130 30a74 74 0 1 0 40 120A60 60 0 0 1 130 30z"/>',
    "termometro": ('<path d="M88 30a12 12 0 0 1 24 0v94a28 28 0 1 1-24 0z"/><path d="M100 70v74"/>'
                   '<path d="M124 50h14M124 72h14M124 94h14"/>'),
    "xicara": ('<path d="M36 80h108v40a54 54 0 0 1-108 0z"/><path d="M144 92h12a20 20 0 0 1 0 40h-16"/>'
               '<path d="M24 182h140"/><path d="M70 60c-8-12 8-18 0-30M100 60c-8-12 8-18 0-30M130 60c-8-12 8-18 0-30"/>'),
    "agenda": ('<rect x="30" y="24" width="140" height="160" rx="10"/><path d="M30 60h140M66 12v26M134 12v26"/>'
               '<path d="M50 84l6 6 10-12M78 84h70M50 110l6 6 10-12M78 110h70M50 136l6 6 10-12M78 136h70M50 162l6 6 10-12M78 162h50"/>'),
    "folha": ('<path d="M40 170C40 90 90 30 170 30c0 80-50 140-130 140z"/><path d="M40 170L140 64"/>'
              '<path d="M80 128l-6-30M104 102l-4-34M80 128l30 2M104 102l30 0"/>'),
    "mao": ('<path d="M70 190v-60c0-10-18-40-18-62 0-10 14-12 18 0l12 34V40c0-12 18-12 18 0v54V30c0-12 18-12 18 0v64V44'
            'c0-12 18-12 18 0v70l10-18c6-10 22-4 16 8l-20 44c-6 14-12 22-12 42"/>'),
    "bussola": ('<circle cx="100" cy="100" r="80"/><circle cx="100" cy="100" r="66"/><path d="M100 50l18 50-18 50-18-50z"/>'
                '<path d="M100 20v12M100 168v12M20 100h12M168 100h12"/>'),
    "pincel": ('<path d="M150 20l30 30-80 80-30-30z"/><path d="M70 100c-26 0-40 20-40 40 0 14-6 22-16 30 40 6 76-6 76-40"/>'
               '<path d="M136 34l30 30"/>'),
    "mala": ('<rect x="30" y="64" width="140" height="110" rx="12"/><path d="M78 64V42a8 8 0 0 1 8-8h28a8 8 0 0 1 8 8v22"/>'
             '<path d="M30 104h140M64 64v110M136 64v110"/><circle cx="56" cy="186" r="6"/><circle cx="144" cy="186" r="6"/>'),
    "flor": ('<path d="M100 196V110"/><path d="M100 150c-30 0-44-20-46-40 26 0 46 16 46 40zM100 170c24-2 40-18 42-38-24 0-42 14-42 38z"/>'
             '<circle cx="100" cy="74" r="16"/><path d="M100 58c-10-30 20-30 0 0M116 74c30-10 30 20 0 0M100 90c10 30-20 30 0 0'
             'M84 74c-30 10-30-20 0 0M111 63c22-22 36 4 0 0M111 85c22 22-4 36 0 0M89 85c-22 22-36-4 0 0M89 63c-22-22 4-36 0 0"/>'),
    "onda": '<path d="M-10 100c30-50 60-50 90 0s60 50 90 0 60-50 90 0"/><path d="M-10 130c30-50 60-50 90 0s60 50 90 0 60-50 90 0"/>',
}


def traco(nome, cor, x, y, w, op=1.0, sw=4, rot=0):
    """Ilustração em traço (viewBox 200x200), atrás do texto, podendo sair pela borda."""
    return (f'<div data-ap-fixo style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{w}px;z-index:1;'
            f'opacity:{op};transform:rotate({rot}deg);pointer-events:none;">'
            f'<svg viewBox="0 0 200 200" width="{w}" height="{w}" fill="none" stroke="{cor}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" overflow="visible">{TRACOS[nome]}</svg></div>')


def circulo(cor, cx, cy, r, op=1.0, contorno=0):
    estilo = f"border:{contorno}px solid {cor};" if contorno else f"background:{cor};"
    return (f'<div style="position:absolute;left:{cx - r}px;top:{cy - r}px;width:{2 * r}px;height:{2 * r}px;'
            f'border-radius:50%;{estilo}opacity:{op};z-index:1;pointer-events:none;"></div>')


def bloco_cor(cor, x, y, w, hgt, r=0, op=1.0, rot=0):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{hgt}px;border-radius:{r}px;'
            f'background:{cor};opacity:{op};transform:rotate({rot}deg);z-index:1;pointer-events:none;"></div>')


# ---------------------------------------------------------------- moldura + navegação + painel
CHEV = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
        'stroke-linecap="round" stroke-linejoin="round"><path d="{d}"/></svg>')
FONTES = ("https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600&"
          "family=Poppins:wght@400;500;600&family=Parisienne&display=swap")


def pagina(titulo, subtitulo, legenda, slides, labels, pasta_rel):
    # legenda final do post: <pasta>/legenda.txt (lida também pela página de aprovação)
    arq = ROOT / pasta_rel / "legenda.txt"
    if arq.exists():
        legenda = arq.read_text(encoding="utf-8").strip()
    legenda = legenda.replace("\n", "<br>")
    total = len(slides)
    dots = "".join(f'<button class="ig-dot" type="button" aria-label="Ir para o slide {i + 1}" data-go="{i}"></button>'
                   for i in range(total))
    nav = (f'<div class="ig-dots ig-nav"><button class="ig-nav-btn" id="ig-prev" type="button" aria-label="Slide anterior">'
           f'{CHEV.format(d="M15 6l-6 6 6 6")}</button><div class="ig-nav-dots">{dots}</div>'
           f'<span class="ig-nav-count" id="ig-count">1/{total}</span><button class="ig-nav-btn" id="ig-next" type="button" '
           f'aria-label="Próximo slide">{CHEV.format(d="M9 6l6 6-6 6")}</button></div>')
    avatar = logo_svg(TONS["creme"], 30)
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo} | {NAME}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTES}" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin:0; background:#efeee9; display:flex; gap:24px; align-items:flex-start; padding:24px; font-family:'{BF}', sans-serif; }}
  .serif {{ font-family:'{HF}', serif; }}
  .sans {{ font-family:'{BF}', sans-serif; }}
  .ig-frame {{ width:420px; flex:none; background:#fff; border-radius:16px; overflow:hidden; box-shadow:0 8px 40px rgba(0,0,0,0.12); border:1px solid #efefef; }}
  .ig-header {{ display:flex; align-items:center; gap:10px; padding:12px 14px; }}
  .ig-avatar {{ width:36px; height:36px; border-radius:50%; background:{LBG}; flex:none; display:flex; align-items:center; justify-content:center; overflow:hidden; border:1px solid {LBR}; }}
  .ig-header-text {{ display:flex; flex-direction:column; line-height:1.2; }}
  .ig-header-handle {{ font-size:13px; font-weight:600; color:#262626; }}
  .ig-header-sub {{ font-size:11px; color:#8e8e8e; }}
  .ig-viewport {{ width:420px; height:525px; overflow:hidden; position:relative; cursor:grab; touch-action:pan-y; }}
  .ig-track {{ display:flex; width:{420 * total}px; height:525px; }}
  .ig-actions {{ display:flex; align-items:center; gap:14px; padding:6px 14px; }}
  .ig-caption {{ padding:2px 14px 16px; font-size:13px; color:#262626; line-height:1.4; }}
  .ig-caption .ts {{ display:block; margin-top:6px; font-size:10px; color:#8e8e8e; letter-spacing:0.5px; text-transform:uppercase; }}
  .ig-nav {{ display:flex; align-items:center; justify-content:center; gap:12px; padding:10px 14px; }}
  .ig-nav-dots {{ display:flex; gap:6px; align-items:center; }}
  .ig-nav .ig-dot {{ width:7px; height:7px; padding:0; border:0; border-radius:4px; background:rgba(0,0,0,0.2); cursor:pointer; transition:width .2s, background .2s; }}
  .ig-nav .ig-dot.on {{ width:18px; background:{P}; }}
  .ig-nav-btn {{ width:34px; height:34px; border-radius:50%; border:1px solid rgba(0,0,0,0.12); background:#fff; color:#111; display:flex; align-items:center; justify-content:center; cursor:pointer; transition:background .15s, color .15s, opacity .15s; }}
  .ig-nav-btn:hover:not(:disabled) {{ background:{P}; color:#fff; border-color:{P}; }}
  .ig-nav-btn:disabled {{ opacity:.3; cursor:default; }}
  .ig-nav-btn:focus-visible, .ig-nav .ig-dot:focus-visible {{ outline:2px solid {P}; outline-offset:2px; }}
  .ig-nav-count {{ font:500 12px ui-monospace, monospace; color:#666; min-width:30px; text-align:center; }}
</style>
</head>
<body>
<div class="ig-frame">
  <div class="ig-header">
    <div class="ig-avatar">{avatar}</div>
    <div class="ig-header-text"><span class="ig-header-handle">{HANDLE.lstrip('@')}</span><span class="ig-header-sub">{subtitulo}</span></div>
  </div>
  <div class="ig-viewport"><div class="ig-track">{''.join(slides)}</div></div>
  {nav if total > 1 else ''}
  <div class="ig-actions">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M12 21s-7.5-4.9-10-9.2C.3 8.6 1.7 5 5.2 4.2 7.4 3.7 9.6 4.7 12 7.3c2.4-2.6 4.6-3.6 6.8-3.1 3.5.8 4.9 4.4 3.2 7.6C19.5 16.1 12 21 12 21z" stroke="#262626" stroke-width="1.5"/></svg>
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v10z" stroke="#262626" stroke-width="1.5"/></svg>
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M22 2 11 13M22 2l-7 20-4-9-9-4 20-7z" stroke="#262626" stroke-width="1.5" stroke-linejoin="round"/></svg>
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style="margin-left:auto;"><path d="M6 3h12v18l-6-4-6 4V3z" stroke="#262626" stroke-width="1.5" stroke-linejoin="round"/></svg>
  </div>
  <div class="ig-caption"><p style="margin:0;"><strong>{HANDLE}</strong> {legenda}</p><span class="ts">2 HORAS ATRÁS</span></div>
</div>

<aside id="carousel-editor" style="width:360px;max-height:90vh;overflow:auto;background:#fff;border:1px solid #e5e5e5;border-radius:14px;padding:18px;font-family:system-ui,sans-serif;font-size:13px;box-shadow:0 4px 24px rgba(0,0,0,0.06);position:sticky;top:24px;">
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;">
    <strong style="font-size:14px;">Editar carrossel</strong>
    <button id="ce-download" style="background:#111;color:#fff;border:0;border-radius:8px;padding:8px 14px;font-weight:600;cursor:pointer;font-size:12px;">Baixar HTML</button>
  </div>
  <div id="ce-groups"></div>
  <p style="margin-top:14px;color:#888;font-size:11px;line-height:1.4;">O download remove o painel e gera um <code>carousel.html</code> limpo, pronto para exportar. Substitua o arquivo em <code>{pasta_rel}/carousel.html</code>.</p>
</aside>

<script>
(function(){{
  const track = document.querySelector('.ig-track');
  const viewport = document.querySelector('.ig-viewport');
  const dots = Array.from(document.querySelectorAll('.ig-nav .ig-dot'));
  const prev = document.getElementById('ig-prev'), next = document.getElementById('ig-next');
  const count = document.getElementById('ig-count');
  const total = track.children.length, slideW = 420;
  if (!prev) return;
  let index = 0, startX = 0, dragging = false, currentX = 0;
  function goTo(i){{
    index = Math.max(0, Math.min(total - 1, i));
    track.style.transition = 'transform .35s ease';
    track.style.transform = 'translateX(' + (-index * slideW) + 'px)';
    dots.forEach((d, di) => d.classList.toggle('on', di === index));
    prev.disabled = index === 0; next.disabled = index === total - 1;
    count.textContent = (index + 1) + '/' + total;
  }}
  prev.addEventListener('click', () => goTo(index - 1));
  next.addEventListener('click', () => goTo(index + 1));
  dots.forEach(d => d.addEventListener('click', () => goTo(+d.dataset.go)));
  document.addEventListener('keydown', (e) => {{
    if (/^(TEXTAREA|INPUT)$/.test(document.activeElement.tagName)) return;
    if (e.key === 'ArrowRight') goTo(index + 1);
    if (e.key === 'ArrowLeft') goTo(index - 1);
  }});
  viewport.addEventListener('pointerdown', (e) => {{ dragging = true; startX = e.clientX; currentX = -index * slideW; track.style.transition = 'none'; viewport.setPointerCapture(e.pointerId); }});
  viewport.addEventListener('pointermove', (e) => {{ if(!dragging) return; track.style.transform = 'translateX(' + (currentX + e.clientX - startX) + 'px)'; }});
  viewport.addEventListener('pointerup', (e) => {{ if(!dragging) return; dragging = false; const dx = e.clientX - startX; if (dx < -60) goTo(index + 1); else if (dx > 60) goTo(index - 1); else goTo(index); }});
  viewport.addEventListener('pointerleave', () => {{ if(dragging){{ dragging = false; goTo(index); }} }});
  goTo(0);
}})();
</script>

<script id="carousel-editor-script">
(function(){{
  const SLIDE_LABELS = {json.dumps(labels, ensure_ascii=False)};
  const groups = document.getElementById('ce-groups');
  const slides = {{}};
  document.querySelectorAll('[data-edit-id]').forEach(el => {{
    const id = el.getAttribute('data-edit-id');
    const m = id.match(/^slide(\\d+)-(.+)$/);
    if(!m) return;
    (slides[+m[1]] = slides[+m[1]] || []).push({{id, role:m[2], el}});
  }});
  Object.keys(slides).sort((a,b)=>+a-+b).forEach(n => {{
    const det = document.createElement('details');
    det.open = (+n <= 2);
    det.style.cssText = 'margin-bottom:8px;border:1px solid #eee;border-radius:8px;padding:8px 10px;';
    det.innerHTML = `<summary style="cursor:pointer;font-weight:600;">Slide ${{n}} · ${{SLIDE_LABELS[n]||''}}</summary>`;
    slides[n].forEach(({{role, el}}) => {{
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
