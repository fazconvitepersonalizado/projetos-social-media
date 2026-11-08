# -*- coding: utf-8 -*-
"""POST 04 · 19/11/2026 · O que as cores escolhidas em uma mandala podem representar? (7 slides).
Roteiro aprovado em 2026-11-08. Sorteio seed 62; comparações viraram título e apoio com a mandala na cor
(um slide por cor, como pede a orientação). Foto emoldurada só no 3 (5A pexels 7181600). Sem indicador.
A cor de cada slide aparece só na mandala e na palavra da cor; fundos na paleta da marca. Creme no 3 e no 5."""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent))
from _carrossel_base import *  # noqa: E402,F403

C, O, G, GE = tom("creme"), tom("oliva"), tom("dourado"), tom("ouro_escuro")
N = 7
AMARELO_FOTO = foto(BASE / "assets" / "edited" / "slide3-card.jpg")
# cor da mandala / cor da palavra (ajustada ao fundo para contraste)
AZUL, AZUL_TXT = "#6F95CC", "#A9C4EA"
AMARELO, AMARELO_TXT = "#E2B23A", "#8A6410"
VERDE, VERDE_TXT = "#A8CF8C", "#CFE7BD"
VERMELHO, VERMELHO_TXT = "#B8433A", "#A3342B"
LILAS, LILAS_TXT = "#C2ACD4", "#D9CBE6"


def arcos(cores, cx, cy, r0=70, passo=26, sw=14):
    out = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r0 + k * passo}" fill="none" stroke="{c}" stroke-width="{sw}" '
                  f'stroke-dasharray="6 5" opacity="0.9"/>' for k, c in enumerate(cores))
    return (f'<div data-ap-fixo style="position:absolute;inset:0;z-index:1;pointer-events:none;">'
            f'<svg width="420" height="525" viewBox="0 0 420 525">{out}'
            f'<circle cx="{cx}" cy="{cy}" r="{r0 - 26}" fill="none" stroke="{PL}" stroke-width="3"/></svg></div>')


def cor_slide(n, t, nome, cor_txt, qualidades, apoio):
    return (h(n, f'<span style="color:{cor_txt};font-style:italic;">{nome}:</span> {qualidades}', t, size=46, lh=1.02)
            + p(n, apoio, t, size=19, gap=18))


s = []
# 1 · capa tipográfica: oliva, arcos de mandala nas cinco cores saindo pela borda
s.append(slide(O, bloco(
    logo_lockup(O, w=160, align="left", gap_below=26)
    + h(1, f"O que as cores escolhidas em uma mandala podem {it('representar?', O)}", O, size=42, lh=1.04),
    anchor="top", pad="40px 36px 76px"),
    layers=arcos([AZUL, AMARELO, VERDE, VERMELHO, LILAS], 400, 530)))
# 2 · azul
s.append(slide(O, bloco(cor_slide(2, O, "Azul", AZUL_TXT, "tranquilidade e serenidade.",
                                  "Uma cor frequentemente associada à calma, à confiança e à introspecção."),
                        anchor="top", pad="76px 36px 76px") + marca_canto(1, N, O),
               layers=traco("mandala", AZUL, 200, 270, 300, op=0.9, sw=3)))
# 3 · amarelo: creme + foto de mandala amarela
s.append(slide(C, bloco(cor_slide(3, C, "Amarelo", AMARELO_TXT, "alegria e vitalidade.",
                                  "Uma cor que pode remeter à energia, ao otimismo e à criatividade."),
                        anchor="top", pad="76px 36px 76px") + marca_canto(2, N, C),
               layers=f'<div style="position:absolute;left:180px;top:300px;z-index:1;">'
                      f'{foto_card(AMARELO_FOTO, 230, 230, nota="pexels.com/photo/7181600", r=115)}</div>'))
# 4 · verde: dourado escuro + mandala verde saindo pela base
s.append(slide(GE, bloco(cor_slide(4, GE, "Verde", VERDE_TXT, "equilíbrio e renovação.",
                                   "Uma cor associada à natureza, ao crescimento e à sensação de harmonia."),
                         anchor="top", pad="76px 36px 76px") + marca_canto(3, N, GE),
               layers=traco("mandala16", VERDE, 60, 330, 300, op=0.9, sw=3)))
# 5 · vermelho: creme + meia mandala vermelha saindo pela base
s.append(slide(C, bloco(cor_slide(5, C, "Vermelho", VERMELHO_TXT, "intensidade e energia.",
                                  "Uma cor que pode representar força, movimento e emoções intensas."),
                        anchor="top", pad="76px 36px 76px") + marca_canto(4, N, C),
               layers=traco("mandala8", VERMELHO, 90, 340, 320, op=0.8, sw=3)))
# 6 · lilás: oliva + mandala lilás saindo pela esquerda
s.append(slide(O, bloco(cor_slide(6, O, "Lilás", LILAS_TXT, "sensibilidade e espiritualidade.",
                                  "Uma cor frequentemente relacionada à imaginação, à delicadeza e à introspecção."),
                        anchor="top", pad="76px 36px 76px") + marca_canto(5, N, O),
               layers=traco("mandala", LILAS, -110, 290, 300, op=0.9, sw=3)))
# 7 · chamada: dourado, cinco pontos de cor, logo completa
pontos = "".join(f'<span style="width:18px;height:18px;border-radius:50%;background:{c};display:inline-block;"></span>'
                 for c in (AZUL, AMARELO, "#6E9B5A", VERMELHO, LILAS))
s.append(slide(G, bloco(
    logo_lockup(G, w=280, gap_below=14)
    + f'<div data-ap-fixo style="display:flex;gap:12px;justify-content:center;margin-bottom:22px;">{pontos}</div>'
    + h(7, "Não existe uma interpretação única para cada cor.", G, size=36, lh=1.04, align="center")
    + p(7, "O significado também passa pelas suas experiências. E você, quais cores costuma escolher?", G,
        size=18, gap=14, align="center", weight=500),
    align="center", pad="50px 36px 56px"),
    layers=traco("mandala16", OLIVA_TXT, -110, 360, 300, op=0.16, sw=2) + traco("mandala8", OLIVA_TXT, 300, -90, 220, op=0.16, sw=2)))

LABELS = {1: "Capa", 2: "Azul", 3: "Amarelo", 4: "Verde", 5: "Vermelho", 6: "Lilás", 7: "CTA"}
html = pagina("Cores da mandala", "Mandalaterapia",
              "O que as cores escolhidas em uma mandala podem representar? Não existe uma interpretação única: "
              "o significado também passa pelas suas experiências. E você, quais cores costuma escolher?",
              s, LABELS, "conteudos/2026-11-19-cores-da-mandala")
(BASE / "carousel.html").write_text(html, encoding="utf-8")
print("ok", len(html))
