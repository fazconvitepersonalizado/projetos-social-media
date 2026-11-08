# -*- coding: utf-8 -*-
"""POST 01 · 12/11/2026 · Mandalaterapia: muito além de colorir (6 slides).
Roteiro aprovado em 2026-11-08 (conteudos/roteiros/2026-11.md). Sorteio seed 23; composições
redistribuídas pela história. Foto só na capa (dividida, 1A pexels 7181612). Sem indicador de arraste.
Nenhum slide só com fundo e texto: mandala em traço (2), lápis (3), lápis coloridos x mandala (4),
três mandalas (5), meia mandala (6). Creme só no 3."""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent))
from _carrossel_base import *  # noqa: E402,F403

C, O, G, GE, F = tom("creme"), tom("oliva"), tom("dourado"), tom("ouro_escuro"), tom("foto")
N = 6
CAPA = foto(BASE / "assets" / "edited" / "slide1-dividida.jpg")
LILAS, VINHO = "#B9A3C8", "#7A3B4E"


def lapis_coloridos(cores, x0=0, w=150, hgt=120):
    out = ""
    passo = w / len(cores)
    for k, cor in enumerate(cores):
        x = x0 + k * passo + passo / 2
        out += (f'<path d="M{x - 8:.0f} {hgt - 10} V30 L{x:.0f} 8 L{x + 8:.0f} 30 V{hgt - 10} Z" fill="{cor}" stroke="none"/>'
                f'<path d="M{x - 8:.0f} 30 H{x + 8:.0f}" stroke="rgba(0,0,0,0.25)" stroke-width="1.5"/>')
    return f'<svg width="{w}" height="{hgt}" viewBox="0 0 {w} {hgt}">{out}</svg>'


def mandala_colorida(w=130):
    s = ""
    cores = [ROSA_ANTIGO, LILAS, P, TERRACOTA]
    for k in range(12):
        a = 360 * k / 12
        s += (f'<ellipse cx="100" cy="62" rx="14" ry="34" fill="{cores[k % 4]}" opacity="0.9" '
              f'transform="rotate({a:.0f} 100 100)"/>')
    s += f'<circle cx="100" cy="100" r="26" fill="{VINHO}"/><circle cx="100" cy="100" r="10" fill="{AREIA}"/>'
    s += f'<circle cx="100" cy="100" r="94" fill="none" stroke="{AREIA}" stroke-width="2"/>'
    return f'<svg width="{w}" height="{w}" viewBox="0 0 200 200">{s}</svg>'


s = []
# 1 · capa: foto dividida (mãos colorindo a mandala) em cima, título no oliva embaixo
s.append(slide(O,
    f'<!-- foto: pexels.com/photo/7181612 --><img src="{CAPA}" alt="" style="position:absolute;left:0;top:0;width:420px;'
    f'height:270px;object-fit:cover;object-position:50% 45%;">'
    + f'<div style="position:absolute;top:16px;left:18px;z-index:3;">'
      f'{logo_lockup(F, w=160, align="left", gap_below=0, chip="rgba(62,66,52,0.62)")}</div>'
    + bloco(h(1, f"Mandalaterapia: muito além de {it('colorir', O)}", O, size=40, lh=1.02)
            + p(1, "Um caminho de conexão, expressão e autoconhecimento.", O, role="subhead", size=18, gap=12),
            anchor="bottom", pad="0 36px 40px")))
# 2 · por que importa: dourado, mandala grande em traço saindo pela borda
s.append(slide(G, bloco(
    h(2, f"Já parou para olhar para {it('dentro', G, color=OLIVA_TXT)} de si?", G, size=46, lh=1.02)
    + p(2, "Alguns minutos com uma mandala podem ser essa oportunidade.", G, size=19, gap=18, weight=500),
    anchor="top", pad="76px 36px 76px") + marca_canto(1, N, G),
    layers=traco("mandala", OLIVA_TXT, 150, 250, 380, op=0.32, sw=2.2)))
# 3 · como fazer: creme, lápis em traço, os dois gestos da prática
s.append(slide(C, bloco(
    h(3, "A prática convida você a desacelerar.", C, size=42, lh=1.04)
    + lista(3, C, ["Concentrar a atenção", "Se conectar com o momento presente"], size=21, gap_top=24),
    anchor="top", pad="76px 36px 76px") + marca_canto(2, N, C),
    layers=traco("lapis", PD, 190, 270, 270, op=0.6, sw=4, rot=-8)))
# 4 · o que muda: oliva, lápis coloridos x mandala colorida
s.append(slide(O, bloco(
    h(4, f"Escolher as cores também é explorar {it('sentimentos.', O)}", O, size=38, lh=1.04)
    + p(4, "Dá espaço para expressar emoções e exercitar a criatividade.", O, size=18, gap=14),
    anchor="top", pad="70px 36px 60px") + marca_canto(3, N, O),
    layers=f'<div data-ap-fixo style="position:absolute;left:30px;top:318px;z-index:1;">{lapis_coloridos([ROSA_ANTIGO, LILAS, P, TERRACOTA, SALVIA], w=170, hgt=150)}</div>'
    + f'<div data-ap-fixo style="position:absolute;left:214px;top:384px;z-index:1;"><svg width="44" height="20" viewBox="0 0 44 20">'
      f'<path d="M2 10h38M30 2l10 8-10 8" fill="none" stroke="{PL}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg></div>'
    + f'<div data-ap-fixo style="position:absolute;left:262px;top:300px;z-index:1;">{mandala_colorida(180)}</div>'))
# 5 · virada: dourado escuro, três mandalas diferentes
s.append(slide(GE, bloco(
    h(5, f"Cada pessoa vive esse processo de um jeito {it('único.', GE)}", GE, size=40, lh=1.04)
    + p(5, "Respeitando suas experiências, suas emoções e o seu tempo.", GE, size=19, gap=16),
    anchor="top", pad="76px 36px 76px") + marca_canto(4, N, GE),
    layers=traco("mandala8", OURO_CLARO, -30, 330, 170, op=0.55, sw=3)
    + traco("mandala16", OURO_CLARO, 125, 360, 150, op=0.55, sw=3)
    + traco("mandala", OURO_CLARO, 270, 310, 190, op=0.55, sw=3)))
# 6 · chamada: dourado chapado, logo completa e a assinatura
s.append(slide(G, bloco(
    logo_lockup(G, w=280, gap_below=18)
    + h(6, "Permita-se experimentar.", G, size=44, lh=1.04, align="center")
    + p(6, "Às vezes, tudo o que precisamos é de um momento para nos reconectar conosco.", G, size=19, gap=16,
        align="center", weight=500)
    + assinatura(6, G, size=34, gap=24, align="center", cor=OLIVA_TXT),
    align="center", pad="56px 36px 60px"),
    layers=traco("mandala16", OLIVA_TXT, -120, 380, 300, op=0.16, sw=2)))

LABELS = {1: "Capa", 2: "Olhar para dentro", 3: "Desacelerar", 4: "Cores e sentimentos", 5: "Jeito único", 6: "CTA"}
html = pagina("Mandalaterapia", "Mandalaterapia",
              "Mandalaterapia: muito além de colorir. Um caminho de conexão, expressão e autoconhecimento. "
              "Vamos conversar sobre você? O link para agendar está na bio.",
              s, LABELS, "conteudos/2026-11-12-mandalaterapia")
(BASE / "carousel.html").write_text(html, encoding="utf-8")
print("ok", len(html))
