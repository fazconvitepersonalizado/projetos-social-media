# -*- coding: utf-8 -*-
"""Base comum dos carrosséis da A&J a partir de outubro/2026.

Segue a decisão de design registrada em brand-kit.json ("design_assinatura",
2026-10-19): fundos chapados (creme, petróleo, verde), degradê verde só no
CTA, Lora + Poppins, 1 ou 2 itálicos por carrossel, logo com chip só na capa
e no CTA, sem etiqueta acima do título, sem enfeite de canto, sem granulado.
Moldura com .ig-viewport/.ig-track (export_carousel.py), navegação de
references/preview-nav.md e painel de references/edit-panel.md.
"""
import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
brand = json.loads((ROOT / "brand-kit.json").read_text(encoding="utf-8"))
D = brand["derived"]
P, PL, PD = D["BRAND_PRIMARY"], D["BRAND_LIGHT"], D["BRAND_DARK"]
LBG, LBR, DBG = D["LIGHT_BG"], D["LIGHT_BORDER"], D["DARK_BG"]
HF, BF = brand["heading_font"], brand["body_font"]
NAME, HANDLE = brand["brand_name"], brand["instagram_handle"]
INK = "#2F3B38"          # texto de apoio em fundo claro (contraste alto sobre o creme)
# Verde da marca como TEXTO sobre o creme: #5FA23B dá 2,7:1; este tom fechado dá 3,7:1 (aprovado em 2026-10-19).
# Fios, pontos e barras continuam no BRAND_PRIMARY.
P_TEXTO = "#4A8A2C"
W, H = 420, 525

LOGO = "data:image/png;base64," + base64.b64encode((ROOT / "logo" / "icon.png").read_bytes()).decode()


def foto(path: Path) -> str:
    return "data:image/jpeg;base64," + base64.b64encode(Path(path).read_bytes()).decode()


# ---------------------------------------------------------------- tons
TONS = {
    "claro": {"bg": LBG, "h": DBG, "b": INK, "acc": P_TEXTO, "mute": "rgba(18,63,60,0.72)", "line": LBR},
    "escuro": {"bg": DBG, "h": "#fff", "b": "rgba(255,255,255,0.84)", "acc": PL, "mute": "rgba(255,255,255,0.55)", "line": "rgba(255,255,255,0.16)"},
    "petroleo": {"bg": PD, "h": "#fff", "b": "rgba(255,255,255,0.86)", "acc": PL, "mute": "rgba(255,255,255,0.6)", "line": "rgba(255,255,255,0.18)"},
    "verde": {"bg": P, "h": DBG, "b": DBG, "acc": "#fff", "mute": "rgba(18,63,60,0.7)", "line": "rgba(18,63,60,0.25)"},
    # assinatura da A&J: degradê petróleo → verde, só no CTA (com scrim de legibilidade)
    "cta": {"bg": None, "h": "#fff", "b": "rgba(255,255,255,0.9)", "acc": DBG, "mute": "rgba(255,255,255,0.7)", "line": "rgba(255,255,255,0.2)"},
    "foto": {"bg": DBG, "h": "#fff", "b": "rgba(255,255,255,0.9)", "acc": "#fff", "mute": "rgba(255,255,255,0.8)", "line": "rgba(255,255,255,0.25)"},
}
# Cores de campanha temática (regra geral de 2026-10-19: a cor da campanha domina; a marca fica no logo e nas fontes)
ROSA_CLARO, ROSA, VINHO, ROSA_SUAVE = "#FBE4EC", "#E5679A", "#8C2453", "#F7B8CF"
TONS.update({
    "rosa": {"bg": ROSA_CLARO, "h": VINHO, "b": "#4A1A30", "acc": VINHO, "mute": "rgba(140,36,83,0.78)",
             "line": "#F1C3D3", "fill": ROSA, "rule": ROSA, "chip": "rgba(255,255,255,0.75)", "chip_border": "#F1C3D3"},
    "vinho": {"bg": VINHO, "h": "#fff", "b": "rgba(255,255,255,0.88)", "acc": ROSA_SUAVE, "mute": "rgba(255,255,255,0.7)",
              "line": "rgba(255,255,255,0.2)", "fill": "#fff", "rule": ROSA_SUAVE},
    "cta_rosa": {"bg": None, "h": "#fff", "b": "rgba(255,255,255,0.92)", "acc": "#fff", "mute": "rgba(255,255,255,0.78)",
                 "line": "rgba(255,255,255,0.2)", "fill": "#fff"},
})
CTA_ROSA_BG = (f"background:radial-gradient(circle at 15% 20%, {ROSA_SUAVE} 0%, transparent 55%),"
               f"radial-gradient(circle at 90% 10%, {ROSA} 0%, transparent 50%),"
               f"radial-gradient(circle at 60% 100%, {VINHO} 0%, transparent 65%),{ROSA};")

CTA_BG = (f"background:radial-gradient(circle at 15% 20%, {PL} 0%, transparent 55%),"
          f"radial-gradient(circle at 90% 10%, {P} 0%, transparent 50%),"
          f"radial-gradient(circle at 60% 100%, {PD} 0%, transparent 65%),{P};")
CTA_SCRIM = ('<div style="position:absolute;inset:0;z-index:1;pointer-events:none;background:'
             'radial-gradient(circle at 15% 20%, rgba(0,0,0,0.48) 0%, transparent 60%),rgba(0,0,0,0.12);"></div>')


def tom(nome):
    return TONS[nome]


# ---------------------------------------------------------------- texto
def h(n, html, t, size=40, role="headline", weight=600, lh=1.06, align=None, extra=""):
    a = f"text-align:{align};" if align else ""
    return (f'<h2 class="serif" data-edit-id="slide{n}-{role}" style="font-size:{size}px;font-weight:{weight};'
            f'line-height:{lh};letter-spacing:-0.02em;color:{t["h"]};margin:0;{a}{extra}">{html}</h2>')


def p(n, text, t, size=17, role="body", align=None, gap=18, weight=400, color=None, extra=""):
    a = f"text-align:{align};" if align else ""
    return (f'<p class="sans" data-edit-id="slide{n}-{role}" style="font-size:{size}px;line-height:1.45;'
            f'font-weight:{weight};color:{color or t["b"]};margin:{gap}px 0 0;{a}{extra}">{text}</p>')


def it(word, t, color=None):
    """Palavra-chave em Lora itálico (assinatura; no máximo 1 ou 2 por carrossel)."""
    return f'<span style="font-style:italic;font-weight:600;color:{color or t["acc"]};">{word}</span>'


# ---------------------------------------------------------------- blocos
def bloco(inner, align="left", anchor="center", pad="64px 36px 76px"):
    jc = {"center": "center", "top": "flex-start", "bottom": "flex-end"}[anchor]
    ta = "center" if align == "center" else "left"
    return (f'<div style="position:relative;z-index:2;height:100%;display:flex;flex-direction:column;'
            f'justify-content:{jc};padding:{pad};box-sizing:border-box;text-align:{ta};">'
            f'<div style="max-width:360px;width:100%;margin:0 auto;">{inner}</div></div>')


def slide(t, inner, layers=""):
    if t is TONS["cta"]:
        bg, scrim = CTA_BG, CTA_SCRIM
    elif t is TONS["cta_rosa"]:
        bg, scrim = CTA_ROSA_BG, CTA_SCRIM
    else:
        bg, scrim = f"background:{t['bg']};", ""
    return (f'<div class="slide" style="position:relative;width:{W}px;height:{H}px;flex:none;overflow:hidden;{bg}">'
            f"{layers}{scrim}{inner}</div>")


def chip_bg(t):
    if "chip" in t:
        return t["chip"]
    return f"{LBG}D9" if t is TONS["claro"] else "rgba(0,0,0,0.22)"


def logo_lockup(t, size=30, fs=13, align="center", gap_below=22, chip=None):
    jc = "center" if align == "center" else "flex-start"
    border = (f"border:1px solid {LBR};" if t is TONS["claro"]
              else f"border:1px solid {t['chip_border']};" if "chip_border" in t else "")
    return (f'<div style="display:flex;justify-content:{jc};margin-bottom:{gap_below}px;">'
            f'<div style="display:inline-flex;align-items:center;gap:9px;padding:7px 11px 7px 7px;border-radius:8px;'
            f'background:{chip or chip_bg(t)};{border}">'
            f'<img src="{LOGO}" style="width:{size}px;height:{size}px;object-fit:contain;display:block;">'
            f'<span class="sans" style="font-size:{fs}px;font-weight:600;letter-spacing:0.3px;color:{t["h"]};">{NAME}</span>'
            "</div></div>")


def botao(n, text, role="cta", bg=None, fg=None):
    return (f'<div style="margin-top:26px;"><span class="sans" data-edit-id="slide{n}-{role}" style="display:inline-block;'
            f'padding:13px 26px;background:{bg or LBG};color:{fg or PD};font-weight:600;font-size:16px;border-radius:28px;">'
            f'{text}</span></div>')


# ---------------------------------------------------------------- indicadores (sorteados)
def indicador(tipo, i, total, t):
    if tipo == "selo" and i == 0:
        return (f'<div class="sans" style="position:absolute;right:28px;bottom:26px;z-index:4;font-size:12px;'
                f'font-weight:600;letter-spacing:1.2px;color:{t["mute"]};">ARRASTE PARA O LADO →</div>')
    if tipo == "selo" and 0 < i < total - 1:
        # do slide 2 ao penúltimo, só uma setinha (Thiago, 2026-10-20); o último fica sem
        return (f'<div class="sans" style="position:absolute;right:28px;bottom:20px;z-index:4;font-size:20px;'
                f'font-weight:600;line-height:1;color:{t["mute"]};">→</div>')
    if tipo == "contador":
        return (f'<div class="sans" style="position:absolute;right:28px;bottom:24px;z-index:4;font-size:12px;'
                f'font-weight:500;color:{t["mute"]};">{i + 1}/{total}</div>')
    if tipo == "barra":
        claro = t["bg"] in (LBG, ROSA_CLARO)
        fill = t.get("fill") or (P if claro else "#fff")
        track = "rgba(0,0,0,0.10)" if claro else "rgba(255,255,255,0.22)"
        segs = "".join(f'<div style="flex:1;height:3px;border-radius:2px;background:{fill if k <= i else track};"></div>'
                       for k in range(total))
        return (f'<div style="position:absolute;left:0;right:0;bottom:0;padding:16px 28px 20px;z-index:4;'
                f'display:flex;align-items:center;gap:10px;"><div style="flex:1;display:flex;gap:4px;">{segs}</div>'
                f'<span class="sans" style="font-size:12px;font-weight:500;color:{t["mute"]};">{i + 1}/{total}</span></div>')
    return ""


# ---------------------------------------------------------------- componentes desenhados
def comparacao(n, t, cab_esq, cab_dir, linhas, size=16, gap_top=22, cab_serif=False, cab_size=None):
    """Duas colunas: a da esquerda esmaecida, a da direita com o fio da marca no topo."""
    cel = f"font-size:{size}px;line-height:1.35;padding:14px 0;border-top:1px solid {t['line']};"
    rows = ""
    for k, (a, b) in enumerate(linhas, 1):
        rows += (f'<div class="sans" data-edit-id="slide{n}-row-{k}-a" style="{cel}color:{t["mute"]};">{a}</div>'
                 f'<div class="sans" data-edit-id="slide{n}-row-{k}-b" style="{cel}color:{t["h"]};font-weight:500;">{b}</div>')
    cab = (f"class=\"serif\" style=\"font-size:{cab_size or 22}px;line-height:1.1;font-weight:600;" if cab_serif
           else f"class=\"sans\" style=\"font-size:{cab_size or 13}px;font-weight:600;letter-spacing:0.3px;")
    head = (f'<div {cab}color:{t["mute"]};padding-bottom:10px;" data-edit-id="slide{n}-col-a">{cab_esq}</div>'
            f'<div {cab}color:{t["h"]};padding-bottom:10px;box-shadow:inset 0 -3px 0 '
            f'{t.get("rule") or (P if t is TONS["claro"] else PL)};" '
            f'data-edit-id="slide{n}-col-b">{cab_dir}</div>')
    return (f'<div style="display:grid;grid-template-columns:1fr 1fr;column-gap:18px;margin-top:{gap_top}px;text-align:left;">'
            f"{head}{rows}</div>")


def lista(n, t, itens, size=17, numerada=False, gap_top=20):
    out = ""
    for k, txt in enumerate(itens, 1):
        marca = (f'<span class="serif" style="flex:none;width:26px;font-size:20px;font-weight:700;color:{t["acc"]};">{k}</span>'
                 if numerada else
                 f'<span style="flex:none;width:14px;height:2px;margin-top:12px;background:{t["acc"]};"></span>')
        out += (f'<div style="display:flex;gap:12px;align-items:flex-start;padding:11px 0;border-top:1px solid {t["line"]};">'
                f'{marca}<span class="sans" data-edit-id="slide{n}-item-{k}" style="font-size:{size}px;line-height:1.35;'
                f'color:{t["h"]};font-weight:500;">{txt}</span></div>')
    return f'<div style="margin-top:{gap_top}px;text-align:left;">{out}</div>'


def passos_verticais(n, t, etapas, retorno=None, size=17, gap_top=22, seta=False):
    """Linha vertical com nós; o último pode apontar de volta ao primeiro (ciclo)."""
    out = ""
    for k, txt in enumerate(etapas, 1):
        ultimo = k == len(etapas)
        linha = "" if ultimo else f'<span style="position:absolute;left:10px;top:24px;bottom:-6px;width:2px;background:{t["line"]};"></span>'
        ponta = ("" if (ultimo or not seta) else
                 f'<span style="position:absolute;left:5px;bottom:-8px;width:0;height:0;border-left:6px solid transparent;'
                 f'border-right:6px solid transparent;border-top:7px solid {t["acc"]};"></span>')
        out += (f'<div style="position:relative;display:flex;gap:14px;align-items:flex-start;padding-bottom:16px;">{linha}{ponta}'
                f'<span class="sans" style="position:relative;flex:none;width:22px;height:22px;border-radius:50%;'
                f'background:{t["acc"]};color:{t["bg"] or DBG};font-size:12px;font-weight:700;display:flex;'
                f'align-items:center;justify-content:center;">{k}</span>'
                f'<span class="sans" data-edit-id="slide{n}-step-{k}" style="font-size:{size}px;line-height:1.3;'
                f'color:{t["h"]};font-weight:500;padding-top:1px;">{txt}</span></div>')
    volta = ""
    if retorno:
        volta = (f'<div style="display:flex;gap:10px;align-items:center;margin-top:2px;">'
                 f'<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="{t["acc"]}" stroke-width="2.2" '
                 f'stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 3-6.7"/><path d="M3 4v5h5"/></svg>'
                 f'<span class="sans" data-edit-id="slide{n}-loop" style="font-size:14px;color:{t["mute"]};">{retorno}</span></div>')
    return f'<div style="margin-top:{gap_top}px;text-align:left;">{out}{volta}</div>'


# ---------------------------------------------------------------- elementos desenhados (regra "slide sem vazio", 2026-10-19)
def calendario(t, dia=15, rotulo="reunião", primeiro=3, dias=31, gap_top=26, ch=26):
    """Mês em grade, com um único dia marcado: a CIPA reduzida a uma data."""
    sem = "".join(f'<span class="sans" style="font-size:12px;font-weight:600;color:{t["mute"]};text-align:center;">{d}</span>'
                  for d in "DSTQQSS")
    cel = "".join("<span></span>" for _ in range(primeiro))
    for d in range(1, dias + 1):
        if d == dia:
            cel += (f'<span class="sans" style="height:{ch}px;border-radius:6px;background:{t["acc"]};color:{t["bg"]};'
                    f'font-size:13px;font-weight:700;display:flex;align-items:center;justify-content:center;">{d}</span>')
        else:
            cel += (f'<span class="sans" style="height:{ch}px;font-size:13px;color:{t["mute"]};display:flex;'
                    f'align-items:center;justify-content:center;">{d}</span>')
    return (f'<div style="margin-top:{gap_top}px;padding:16px 16px 12px;border:1.5px solid {t["line"]};border-radius:12px;">'
            f'<div style="display:grid;grid-template-columns:repeat(7,1fr);gap:4px 6px;">{sem}{cel}</div>'
            f'<div class="sans" style="margin-top:10px;font-size:13px;color:{t["acc"]};font-weight:600;text-align:right;">'
            f'● {rotulo}</div></div>')


def ciclo_roda(n, t, etapas, centro="todo mês", tam=360):
    """Etapas em volta de um círculo, com setas no sentido do ciclo."""
    import math
    c, r = tam / 2, tam * 0.25
    k = len(etapas)
    svg = (f'<svg width="{tam}" height="{tam}" viewBox="0 0 {tam} {tam}" style="position:absolute;inset:0;">'
           f'<circle cx="{c}" cy="{c}" r="{r}" fill="none" stroke="{t["line"]}" stroke-width="2"/>')
    html = ""
    for i, txt in enumerate(etapas):
        a = -math.pi / 2 + 2 * math.pi * i / k
        x, y = c + r * math.cos(a), c + r * math.sin(a)
        am = a + math.pi / k  # seta no meio do arco
        ax, ay = c + r * math.cos(am), c + r * math.sin(am)
        rot = math.degrees(am) + 90
        svg += (f'<path d="M -6 -5 L 4 0 L -6 5" fill="none" stroke="{t["acc"]}" stroke-width="2.2" stroke-linecap="round" '
                f'stroke-linejoin="round" transform="translate({ax:.1f},{ay:.1f}) rotate({rot:.1f})"/>')
        svg += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="15" fill="{t["acc"]}"/>'
        svg += (f'<text x="{x:.1f}" y="{y + 5:.1f}" text-anchor="middle" font-family="Poppins" font-size="14" font-weight="700" '
                f'fill="{t["bg"]}">{i + 1}</text>')
        lx, ly = c + (r + 26) * math.cos(a), c + (r + 26) * math.sin(a)
        cosv = math.cos(a)
        if math.sin(a) > 0.5:  # nós de baixo: rótulo embaixo do nó, puxado para fora
            ly = y + 22
            if cosv > 0:
                pos = f"left:{x - 18:.0f}px;width:{tam + 20 - x + 18:.0f}px;text-align:left;"
            else:
                pos = f"right:{tam - x - 18:.0f}px;width:{x + 38:.0f}px;text-align:right;"
            tr = "none"
        elif abs(cosv) < 0.2:
            pos = f"left:{lx - 90:.0f}px;width:180px;text-align:center;"
            tr = "translateY(-100%)" if math.sin(a) < 0 else "none"
        elif cosv > 0:
            pos = f"left:{lx:.0f}px;width:{tam + 20 - lx:.0f}px;text-align:left;"
            tr = "translateY(-50%)"
        else:
            pos = f"right:{tam - lx:.0f}px;width:{lx + 20:.0f}px;text-align:right;"
            tr = "translateY(-50%)"
        html += (f'<span class="sans" data-edit-id="slide{n}-step-{i + 1}" style="position:absolute;top:{ly:.0f}px;{pos}'
                 f'transform:{tr};font-size:16px;line-height:1.22;font-weight:600;color:{t["h"]};">{txt}</span>')
    svg += "</svg>"
    meio = (f'<span class="serif" data-edit-id="slide{n}-center" style="position:absolute;left:0;right:0;top:{c - 14}px;'
            f'text-align:center;font-size:22px;font-style:italic;color:{t["acc"]};">{centro}</span>')
    return f'<div style="position:relative;width:{tam}px;height:{tam}px;margin:14px auto 0;">{svg}{meio}{html}</div>'


def alerta(t, tam=130):
    return (f'<svg width="{tam}" height="{tam}" viewBox="0 0 100 100" style="display:block;margin:0 auto 22px;">'
            f'<path d="M50 8 L94 88 H6 Z" fill="none" stroke="{t["acc"]}" stroke-width="6" stroke-linejoin="round"/>'
            f'<path d="M50 36 V60" stroke="{t["acc"]}" stroke-width="8" stroke-linecap="round"/>'
            f'<circle cx="50" cy="74" r="5" fill="{t["acc"]}"/></svg>')


def grade2x2(n, t, itens, size=30, gap_top=24):
    out = ""
    for k, txt in enumerate(itens, 1):
        bl = f"border-left:1.5px solid {t['line']};" if k % 2 == 0 else ""
        bt = f"border-top:1.5px solid {t['line']};" if k > 2 else ""
        out += (f'<div class="serif" data-edit-id="slide{n}-item-{k}" style="padding:22px 10px;font-size:{size}px;font-weight:600;'
                f'color:{t["h"]};text-align:center;{bl}{bt}">{txt}</div>')
    return f'<div style="display:grid;grid-template-columns:1fr 1fr;margin-top:{gap_top}px;">{out}</div>'


def ficha(n, t, campos, gap_top=22):
    """Ficha de registro desenhada: rótulo + linha para preencher."""
    out = ""
    for k, txt in enumerate(campos, 1):
        out += (f'<div style="padding:14px 0 6px;"><span class="sans" data-edit-id="slide{n}-field-{k}" style="font-size:17px;'
                f'font-weight:600;color:{t["h"]};">{txt}</span>'
                f'<div style="margin-top:22px;border-bottom:2px dashed {t["line"]};"></div></div>')
    return (f'<div style="margin-top:{gap_top}px;padding:14px 22px 18px;border:2px solid {t["acc"]};border-radius:10px;text-align:left;">'
            f'{out}</div>')


def numero_passo(num, total, t, size=150):
    trilha = "".join(f'<span style="flex:1;height:4px;border-radius:2px;background:{t["acc"] if k < num else t["line"]};"></span>'
                     for k in range(total))
    return (f'<div style="display:flex;align-items:flex-end;gap:16px;margin-bottom:6px;">'
            f'<span class="serif" style="font-size:{size}px;line-height:0.8;font-weight:600;color:{t["acc"]};">{num}</span>'
            f'<div style="flex:1;padding-bottom:10px;"><span class="sans" style="display:block;font-size:13px;font-weight:600;'
            f'color:{t["mute"]};margin-bottom:8px;">passo {num} de {total}</span><div style="display:flex;gap:5px;">{trilha}</div>'
            f'</div></div>')


def checklist(n, t, itens, marcados=0, size=19, gap_top=24):
    out = ""
    for k, txt in enumerate(itens, 1):
        on = k <= marcados
        box = (f'<span style="flex:none;width:26px;height:26px;border-radius:5px;border:2px solid {t["acc"]};'
               f'background:{t["acc"] if on else "transparent"};display:flex;align-items:center;justify-content:center;">'
               + (f'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="{t["bg"]}" stroke-width="3.2" '
                  f'stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5 9-10"/></svg>' if on else "")
               + "</span>")
        out += (f'<div style="display:flex;gap:14px;align-items:center;padding:9px 0;">{box}'
                f'<span class="sans" data-edit-id="slide{n}-check-{k}" style="font-size:{size}px;font-weight:500;'
                f'color:{t["h"]};">{txt}</span></div>')
    return f'<div style="margin-top:{gap_top}px;text-align:left;">{out}</div>'


# ---------------------------------------------------------------- moldura + navegação + painel
CHEV = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
        'stroke-linecap="round" stroke-linejoin="round"><path d="{d}"/></svg>')


def pagina(titulo, subtitulo, legenda, slides, labels, pasta_rel):
    total = len(slides)
    dots = "".join(f'<button class="ig-dot" type="button" aria-label="Ir para o slide {i + 1}" data-go="{i}"></button>'
                   for i in range(total))
    nav = (f'<div class="ig-dots ig-nav"><button class="ig-nav-btn" id="ig-prev" type="button" aria-label="Slide anterior">'
           f'{CHEV.format(d="M15 6l-6 6 6 6")}</button><div class="ig-nav-dots">{dots}</div>'
           f'<span class="ig-nav-count" id="ig-count">1/{total}</span><button class="ig-nav-btn" id="ig-next" type="button" '
           f'aria-label="Próximo slide">{CHEV.format(d="M9 6l6 6-6 6")}</button></div>')
    font = ("https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,500;1,600&"
            "family=Poppins:wght@400;500;600;700&display=swap")
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo} | {NAME}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{font}" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin:0; background:#efeee9; display:flex; gap:24px; align-items:flex-start; padding:24px; font-family:'{BF}', sans-serif; }}
  .serif {{ font-family:'{HF}', serif; }}
  .sans {{ font-family:'{BF}', sans-serif; }}
  .ig-frame {{ width:420px; flex:none; background:#fff; border-radius:16px; overflow:hidden; box-shadow:0 8px 40px rgba(0,0,0,0.12); border:1px solid #efefef; }}
  .ig-header {{ display:flex; align-items:center; gap:10px; padding:12px 14px; }}
  .ig-avatar {{ width:36px; height:36px; border-radius:50%; background:{LBG}; flex:none; display:flex; align-items:center; justify-content:center; padding:5px; overflow:hidden; border:1px solid {LBR}; }}
  .ig-avatar img {{ width:100%; height:100%; object-fit:contain; }}
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
    <div class="ig-avatar"><img src="{LOGO}" alt=""></div>
    <div class="ig-header-text"><span class="ig-header-handle">{HANDLE.lstrip('@')}</span><span class="ig-header-sub">{subtitulo}</span></div>
  </div>
  <div class="ig-viewport"><div class="ig-track">{''.join(slides)}</div></div>
  {nav}
  <div class="ig-actions">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M12 21s-7.5-4.9-10-9.2C.3 8.6 1.7 5 5.2 4.2 7.4 3.7 9.6 4.7 12 7.3c2.4-2.6 4.6-3.6 6.8-3.1 3.5.8 4.9 4.4 3.2 7.6C19.5 16.1 12 21 12 21z" stroke="#262626" stroke-width="1.5"/></svg>
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v10z" stroke="#262626" stroke-width="1.5"/></svg>
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M22 2 11 13M22 2l-7 20-4-9-9-4 20-7z" stroke="#262626" stroke-width="1.5" stroke-linejoin="round"/></svg>
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style="margin-left:auto;"><path d="M6 3h12v18l-6-4-6 4V3z" stroke="#262626" stroke-width="1.5" stroke-linejoin="round"/></svg>
  </div>
  <div class="ig-caption"><b>{HANDLE.lstrip('@')}</b> {legenda}<span class="ts">2 HORAS ATRÁS</span></div>
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
