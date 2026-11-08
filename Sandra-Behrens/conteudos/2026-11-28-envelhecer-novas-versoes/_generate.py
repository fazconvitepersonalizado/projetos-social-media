# -*- coding: utf-8 -*-
"""POST 07 · 28/11/2026 · Envelhecer também é descobrir novas versões de si mesma (6 slides).
Roteiro aprovado em 2026-11-08. Sorteio seed 30; comparação do 2 virou título e apoio com traço.
Fotos no slide inteiro: 1 (10A pexels 8417222, texto no alto, sobre as árvores) e 6 (11B pexels 8829200,
texto embaixo), suaves. Sem indicador. Recursos: bússola (2), pincel e mala (3), faixa (4), flor (5). Creme só no 3."""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent))
from _carrossel_base import *  # noqa: E402,F403

C, O, G, GE, F = tom("creme"), tom("oliva"), tom("dourado"), tom("ouro_escuro"), tom("foto")
N = 6
ED = BASE / "assets" / "edited"
CAPA, CTA_FOTO = foto(ED / "slide1-full.jpg"), foto(ED / "slide6-full.jpg")
CHIP = "rgba(62,66,52,0.6)"

s = []
# 1 · capa: mulher de bicicleta no caminho; texto no alto (véu de cima), logo embaixo à esquerda
s.append(slide(F,
    foto_full(CAPA, ate=0.58, pos="50% 50%", nota="pexels.com/photo/8417222", de="cima")
    + f'<div style="position:absolute;bottom:18px;left:18px;z-index:3;">{logo_lockup(F, w=160, align="left", gap_below=0, chip=CHIP)}</div>'
    + bloco(h(1, f"Envelhecer também é descobrir novas {it('versões', F)} de si mesma.", F, size=40, lh=1.04),
            anchor="top", pad="44px 36px 0")))
# 2 · contexto: dourado, bússola
s.append(slide(G, bloco(
    h(2, "Com os anos, mudam nossos desejos e prioridades.", G, size=44, lh=1.03)
    + p(2, "E também a maneira como enxergamos o mundo.", G, size=19, gap=18, weight=500),
    anchor="top", pad="80px 36px 76px") + marca_canto(1, N, G),
    layers=traco("bussola", OLIVA_TXT, 210, 290, 280, op=0.32, sw=3)))
# 3 · o que muda: creme, pincel e mala
s.append(slide(C, bloco(
    h(3, f"Você pode descobrir novos {it('interesses.', C)}", C, size=44, lh=1.03)
    + p(3, "Desenvolver habilidades e viver experiências que antes nem imaginava.", C, size=19, gap=18),
    anchor="top", pad="80px 36px 76px") + marca_canto(2, N, C),
    layers=traco("pincel", P, 40, 330, 170, op=0.6, sw=4) + traco("mala", P, 230, 320, 170, op=0.6, sw=4)))
# 4 · o que muda: oliva, faixa dourada diagonal
s.append(slide(O, bloco(
    h(4, "Também pode aprender a respeitar mais seus limites.", O, size=40, lh=1.04)
    + p(4, "Reconhecer suas conquistas e largar cobranças que já não fazem sentido.", O, size=19, gap=18),
    anchor="top", pad="80px 36px 76px") + marca_canto(3, N, O),
    layers=bloco_cor(P, -60, 420, 560, 64, op=0.9, rot=-12) + bloco_cor(PL, -60, 480, 560, 18, op=0.6, rot=-12)))
# 5 · virada: dourado escuro, flor abrindo, frase gigante
s.append(slide(GE, bloco(
    h(5, f"Envelhecer não significa deixar de {it('sonhar.', GE)}", GE, size=48, lh=1.0)
    + p(5, "Nem de desejar, aprender ou construir novos caminhos.", GE, size=19, gap=18),
    anchor="top", pad="80px 36px 76px") + marca_canto(4, N, GE),
    layers=traco("flor", OURO_CLARO, 190, 270, 270, op=0.55, sw=3)))
# 6 · chamada: foto inteira na praia, texto embaixo
s.append(slide(F,
    foto_full(CTA_FOTO, ate=0.62, pos="50% 30%", nota="pexels.com/photo/8829200")
    + f'<div style="position:absolute;top:18px;left:18px;z-index:3;">{logo_lockup(F, w=160, align="left", gap_below=0, chip=CHIP)}</div>'
    + bloco(h(6, f"Você não precisa ser a mesma mulher de {it('ontem.', F)}", F, size=40, lh=1.03)
            + p(6, "Ainda existem muitas versões suas esperando para florescer.", F, size=18, gap=12, weight=500),
            anchor="bottom", pad="64px 36px 44px")))

LABELS = {1: "Capa", 2: "Desejos", 3: "Interesses", 4: "Limites", 5: "Sonhar", 6: "CTA"}
html = pagina("Envelhecer: novas versões", "Maturidade",
              "Envelhecer também é descobrir novas versões de si mesma. Ainda existem muitas versões suas esperando para florescer. "
              "Vamos conversar sobre você? O link para agendar está na bio.",
              s, LABELS, "conteudos/2026-11-28-envelhecer-novas-versoes")
(BASE / "carousel.html").write_text(html, encoding="utf-8")
print("ok", len(html))
