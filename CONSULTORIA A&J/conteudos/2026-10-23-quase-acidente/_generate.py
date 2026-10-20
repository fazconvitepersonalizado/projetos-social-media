# -*- coding: utf-8 -*-
"""POST 02 · out/2026 · Quase acidente: o aviso que a empresa costuma ignorar.
Sorteio: mito-e-verdade · cena-do-dia-a-dia · seed 1 · fundos em blocos · centralizado · contador.
Revisão de 2026-10-20: texto curto por slide + elementos desenhados (alerta, grade de causas, ficha de registro)."""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent))
from _carrossel_base import *  # noqa: E402,F403

C, E = tom("claro"), tom("escuro")
IND, N = "nenhum", 8  # contador e barra retirados em 2026-10-20 (pedido do Thiago)
FOTO1 = foto(BASE / "assets" / "edited" / "slide1-photo.jpg")


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
# 1 · capa: foto emoldurada com o título encostado
s.append(slide(C, bloco(
    logo_lockup(C, gap_below=16)
    + '<!-- foto: pexels.com/photo/5498025 -->'
    f'<div style="border-radius:12px;overflow:hidden;"><img src="{FOTO1}" alt="" style="display:block;width:100%;height:172px;'
    'object-fit:cover;object-position:50% 45%;"></div>'
    + h(1, "O carrinho de carga tombou no corredor. Ninguém estava passando.", C, size=31, lh=1.08, align="center",
        extra="margin-top:18px;")
    + p(1, "E ninguém anotou nada.", C, role="subhead", size=20, align="center", gap=12),
    align="center", anchor="top", pad="40px 32px 56px") + indicador(IND, 0, N, C)))
# 2 · mito + alerta desenhado
s.append(slide(C, bloco(
    alerta(C, tam=120)
    + h(2, "Mito: ninguém se feriu, nada a registrar.", C, size=42, lh=1.05, align="center")
    + p(2, "O quase acidente mostra o risco antes da vítima.", C, size=21, align="center", gap=18),
    align="center") + indicador(IND, 1, N, C)))
# 3 · diagrama
s.append(slide(E, bloco(
    h(3, "O mesmo risco em três momentos", E, size=40, lh=1.05, align="center")
    + tres_momentos(3, E)
    + p(3, "É a última chance de agir antes da lesão.", E, size=22, align="center", gap=40, weight=500, color="#fff"),
    align="center", pad="64px 26px 76px") + indicador(IND, 2, N, E)))
# 4 · frase gigante
s.append(slide(E, bloco(
    h(4, f"Da próxima vez, o carrinho pode tombar {it('em cima de alguém.', E)}", E, size=54, lh=1.03, align="center"),
    align="center") + indicador(IND, 3, N, E)))
# 5 · mito + grade de causas
s.append(slide(C, bloco(
    h(5, "Mito: registrar é procurar culpado.", C, size=40, lh=1.05, align="center")
    + p(5, "O registro aponta a causa:", C, size=20, align="center", gap=16)
    + grade2x2(5, C, ["Piso", "Carga", "Pressa", "Equipamento"], size=27, gap_top=16),
    align="center") + indicador(IND, 4, N, C)))
# 6 · ficha de registro
s.append(slide(C, bloco(
    h(6, "Registrar é simples.", C, size=46, align="center")
    + ficha(6, C, ["O que houve", "Onde", "O que podia ter acontecido"], gap_top=24),
    align="center") + indicador(IND, 5, N, C)))
# 7 · pergunta grande
s.append(slide(E, bloco(
    h(7, "Qual foi o último quase acidente na sua empresa?", E, size=46, lh=1.06, align="center")
    + h(7, it("Alguém anotou?", E), E, size=46, lh=1.06, align="center", role="question", extra="margin-top:18px;"),
    align="center") + indicador(IND, 6, N, E)))
# 8 · CTA tipográfico (fundo claro, sem enfeite)
s.append(slide(C, bloco(
    logo_lockup(C, gap_below=26)
    + h(8, "Quer um jeito simples de registrar quase acidentes?", C, size=42, lh=1.06, align="center")
    + p(8, "A A&amp;J ajuda. Chama no direct.", C, role="cta", size=22, weight=600, align="center", gap=22, color=PD)
    + p(8, HANDLE, C, role="handle", size=15, align="center", gap=10, color=C["mute"]),
    align="center") + indicador(IND, 7, N, C)))

LABELS = {1: "Capa", 2: "Mito 1", 3: "Três momentos", 4: "Frase", 5: "Mito 2", 6: "Ficha", 7: "Pergunta", 8: "CTA"}
html = pagina("Quase acidente", "Prevenção de acidentes",
              "Quase acidente: por que registrar o que não machucou ninguém.", s, LABELS,
              "conteudos/2026-10-23-quase-acidente")
(BASE / "carousel.html").write_text(html, encoding="utf-8")
print("ok", len(html))
