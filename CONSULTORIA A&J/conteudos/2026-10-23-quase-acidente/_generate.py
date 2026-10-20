# -*- coding: utf-8 -*-
"""POST 02 · out/2026 · Quase acidente: o aviso que a empresa costuma ignorar.
Sorteio: mito-e-verdade · cena-do-dia-a-dia · seed 1 · centralizado.
2026-10-20: texto curto + elementos desenhados; capa com foto no slide inteiro e véu; creme só nos slides
2 e 5; fotos full no miolo sorteadas: 0 (seed 219932269); selo "arraste" na capa + setinha até o 7.
História: cena, consequência, mito 1 + dado, três momentos, mito 2, ficha, pergunta, chamada.
Nenhum slide só com fundo e texto: carrinho em traço (2), "?" vazado (7), caneta em traço (8)."""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent))
from _carrossel_base import *  # noqa: E402,F403

C, E, PT, V, F = tom("claro"), tom("escuro"), tom("petroleo"), tom("verde"), tom("foto")
IND, N = "selo", 8
CAPA = foto(BASE / "assets" / "edited" / "slide1-full.jpg")
CHIP_FOTO = "rgba(18,63,60,0.6)"


def tres_momentos(n, t):
    """Linha horizontal: condição de risco → quase acidente (destaque) → acidente."""
    nos = [("Condição de risco", False), ("Quase acidente", True), ("Acidente", False)]
    pontos = ""
    for k, (txt, destaque) in enumerate(nos, 1):
        d = 34 if destaque else 18
        cor = PL if destaque else "rgba(255,255,255,0.5)"
        pontos += (f'<div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:14px;">'
                   f'<div style="height:34px;display:flex;align-items:center;"><span style="display:block;width:{d}px;height:{d}px;'
                   f'border-radius:50%;background:{cor};{"box-shadow:0 0 0 8px rgba(217,232,214,0.18);" if destaque else ""}"></span></div>'
                   f'<span class="sans" data-edit-id="slide{n}-node-{k}" style="font-size:{19 if destaque else 16}px;'
                   f'font-weight:{700 if destaque else 500};color:{"#fff" if destaque else E["mute"]};text-align:center;'
                   f'line-height:1.25;">{txt}</span></div>')
    return (f'<div style="position:relative;margin-top:34px;">'
            f'<div style="position:absolute;left:16%;right:16%;top:16px;height:2px;background:rgba(255,255,255,0.3);"></div>'
            f'<div style="position:relative;display:flex;">{pontos}</div></div>')


s = []
# 1 · capa: foto no slide inteiro + véu, título embaixo
s.append(slide(F,
    foto_full(CAPA, ate=0.72, pos="50% 40%", nota="pexels.com/photo/5498025")
    + f'<div style="position:absolute;top:22px;left:24px;z-index:3;">{logo_lockup(F, size=26, fs=12, align="left", gap_below=0, chip=CHIP_FOTO)}</div>'
    + bloco(h(1, "O carrinho de carga tombou no corredor. Ninguém estava passando.", F, size=36, lh=1.08)
            + p(1, "E ninguém anotou nada.", F, role="subhead", size=21, gap=14, weight=500),
            anchor="bottom", pad="64px 36px 66px")
    + indicador(IND, 0, N, F)))
# 2 · a consequência: frase gigante em verde chapado + carrinho em traço
s.append(slide(V, bloco(
    h(2, f"Da próxima vez, o carrinho pode tombar {it('em cima de alguém.', V)}", V, size=48, lh=1.03, align="center"),
    align="center", anchor="top", pad="54px 36px 76px") + indicador(IND, 1, N, V),
    layers=traco("carrinho", "#fff", 96, 292, 280, op=0.9, sw=6)))
# 3 · mito 1 + o dado (Bird) · creme 1/2
s.append(slide(C, bloco(
    h(3, "Mito: ninguém se feriu, nada a registrar.", C, size=42, lh=1.05, align="center")
    + numero_destaque(3, "600", "quase acidentes para cada acidente grave",
                      "Fonte: Frank Bird, estudo de 1969 com 297 empresas", C, size=110, align="center", gap_top=26),
    align="center") + indicador(IND, 2, N, C)))
# 4 · diagrama: o mesmo risco em três momentos
s.append(slide(E, bloco(
    h(4, "O mesmo risco em três momentos", E, size=40, lh=1.05, align="center")
    + tres_momentos(4, E)
    + p(4, "É a última chance de agir antes da lesão.", E, size=22, align="center", gap=40, weight=500, color="#fff"),
    align="center", pad="64px 26px 76px") + indicador(IND, 3, N, E)))
# 5 · mito + grade de causas · creme 2/2
s.append(slide(C, bloco(
    h(5, "Mito: registrar é procurar culpado.", C, size=40, lh=1.05, align="center")
    + p(5, "O registro aponta a causa:", C, size=20, align="center", gap=16)
    + grade2x2(5, C, ["Piso", "Carga", "Pressa", "Equipamento"], size=27, gap_top=16),
    align="center") + indicador(IND, 4, N, C)))
# 6 · ficha de registro em petróleo
s.append(slide(PT, bloco(
    h(6, "Registrar é simples.", PT, size=46, align="center")
    + ficha(6, PT, ["O que houve", "Onde", "O que podia ter acontecido"], gap_top=24),
    align="center") + indicador(IND, 5, N, PT)))
# 7 · pergunta grande
s.append(slide(E, bloco(
    h(7, "Qual foi o último quase acidente na sua empresa?", E, size=46, lh=1.06, align="center")
    + h(7, it("Alguém anotou?", E), E, size=46, lh=1.06, align="center", role="question", extra="margin-top:18px;"),
    align="center") + indicador(IND, 6, N, E),
    layers=sinal("?", PL, 210, 30, 470, op=0.16, contorno=4)))
# 8 · CTA tipográfico em verde chapado
s.append(slide(V, bloco(
    logo_lockup(V, gap_below=26)
    + h(8, "Quer um jeito simples de registrar quase acidentes?", V, size=42, lh=1.06, align="center")
    + p(8, "A A&amp;J ajuda. Chama no direct.", V, role="cta", size=22, weight=700, align="center", gap=22, color=DBG)
    + p(8, HANDLE, V, role="handle", size=15, align="center", gap=12, weight=600, color="#fff",
        extra=f"display:table;margin-left:auto;margin-right:auto;background:{DBG};padding:5px 12px;border-radius:6px;"),
    align="center") + indicador(IND, 7, N, V),
    layers=traco("caneta", "#fff", -40, 372, 170, op=0.75, sw=6)))

LABELS = {1: "Capa", 2: "Consequência", 3: "Mito 1", 4: "Três momentos", 5: "Mito 2", 6: "Ficha", 7: "Pergunta", 8: "CTA"}
html = pagina("Quase acidente", "Prevenção de acidentes",
              "Quase acidente: por que registrar o que não machucou ninguém.", s, LABELS,
              "conteudos/2026-10-23-quase-acidente")
(BASE / "carousel.html").write_text(html, encoding="utf-8")
print("ok", len(html))
