# -*- coding: utf-8 -*-
"""POST 06 · 26/11/2026 · Você não precisa dar conta de tudo, o tempo todo (6 slides).
Roteiro aprovado em 2026-11-08. Sorteio seed 64; foto emoldurada trocada do 4 para o 5.
Visual limpo, um elemento por slide (orientação "minimalista", sem deixar slide vazio).
Fotos: capa recortada (8A pexels 6874521) e card no 5 (9A pexels 1115692), suaves. Sem indicador.
Recursos: agenda (2), xícara (3), folha (4), foto (5). Creme no 2 e no 5."""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent))
from _carrossel_base import *  # noqa: E402,F403

C, O, G = tom("creme"), tom("oliva"), tom("dourado")
N = 6
ED = BASE / "assets" / "edited"
CAPA, LIVRO = foto(ED / "slide1-recortada.jpg"), foto(ED / "slide5-card.jpg")

s = []
# 1 · capa: oliva, título no alto, foto em bloco encostada embaixo à direita
s.append(slide(O,
    f'<div style="position:absolute;left:150px;top:255px;z-index:1;">'
    f'{foto_card(CAPA, 270, 270, pos="50% 35%", nota="pexels.com/photo/6874521", r=0, sombra=False)}</div>'
    + bloco(logo_lockup(O, w=160, align="left", gap_below=18)
            + h(1, f"Você não precisa dar conta de tudo, o {it('tempo todo.', O)}", O, size=38, lh=1.04),
            anchor="top", pad="30px 36px 0")))
# 2 · contexto: creme, agenda cheia
s.append(slide(C, bloco(
    h(2, "Vivemos tentando cumprir compromissos e atender expectativas.", C, size=36, lh=1.05)
    + p(2, "E resolver tudo o que está ao nosso redor.", C, size=19, gap=16),
    anchor="top", pad="76px 36px 76px") + marca_canto(1, N, C),
    layers=traco("agenda", P, 200, 290, 260, op=0.55, sw=4, rot=6)))
# 3 · por que importa: dourado, xícara grande, frase gigante
s.append(slide(G, bloco(
    h(3, f"Nessa rotina, esquecemos de perceber nossos sinais de {it('cansaço.', G)}", G, size=44, lh=1.03),
    anchor="top", pad="80px 36px 76px") + marca_canto(2, N, G),
    layers=traco("xicara", OLIVA_TXT, 150, 300, 260, op=0.35, sw=3)))
# 4 · como fazer: oliva, lista de 4 com folha
s.append(slide(O, bloco(
    h(4, "Respeitar seus limites também significa:", O, size=34, lh=1.05)
    + lista(4, O, ["Descansar quando precisa", "Dizer não", "Reservar momentos para si",
                   "Deixar para amanhã o que pode esperar"], size=18, gap_top=18),
    anchor="top", pad="70px 36px 50px") + marca_canto(3, N, O),
    layers=traco("folha", PL, 290, 380, 190, op=0.35, sw=3)))
# 5 · o que muda: creme, foto da leitura ao ar livre
s.append(slide(C, bloco(
    h(5, f"Desacelerar é reconhecer que você também precisa de {it('cuidado.', C)}", C, size=36, lh=1.05)
    + f'<div style="margin-top:26px;">{foto_card(LIVRO, 348, 230, pos="40% 50%", nota="pexels.com/photo/1115692")}</div>',
    anchor="top", pad="70px 36px 50px") + marca_canto(4, N, C)))
# 6 · chamada: dourado, logo completa e assinatura
s.append(slide(G, bloco(
    logo_lockup(G, w=280, gap_below=18)
    + h(6, "Não espere chegar ao limite para cuidar de si.", G, size=36, lh=1.04, align="center")
    + p(6, "Permita-se respirar, descansar e recomeçar.", G, size=19, gap=14, align="center", weight=500)
    + assinatura(6, G, size=32, gap=20, align="center", cor=OLIVA_TXT),
    align="center", pad="50px 36px 56px"),
    layers=traco("folha", OLIVA_TXT, -40, 400, 160, op=0.18, sw=3, rot=-30)))

LABELS = {1: "Capa", 2: "Rotina", 3: "Cansaço", 4: "Limites", 5: "Desacelerar", 6: "CTA"}
html = pagina("Não precisa dar conta de tudo", "Autocuidado",
              "Você não precisa dar conta de tudo, o tempo todo. Permita-se respirar, descansar e recomeçar. "
              "Vamos conversar sobre você? O link para agendar está na bio.",
              s, LABELS, "conteudos/2026-11-26-nao-precisa-dar-conta-de-tudo")
(BASE / "carousel.html").write_text(html, encoding="utf-8")
print("ok", len(html))
