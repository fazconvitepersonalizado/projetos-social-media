# -*- coding: utf-8 -*-
"""POST 03 · 17/11/2026 · Você cuida de todos, mas tem cuidado de si mesma? (post estático, 1 arte).
Roteiro aprovado em 2026-11-08. Fundo claro por pedido da orientação (a regra "capa nunca clara" é de capa de
carrossel). Foto emoldurada 4A (pexels 6874522), suave. Frase em destaque, poucos elementos."""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent))
from _carrossel_base import *  # noqa: E402,F403

C = tom("creme")
FOTO = foto(BASE / "assets" / "edited" / "post-card.jpg")

s = [slide(C, bloco(
    foto_card(FOTO, 348, 230, pos="50% 50%", nota="pexels.com/photo/6874522", r=12)
    + h(1, f"Você cuida de todos, mas tem cuidado de {it('si mesma?', C)}", C, size=36, lh=1.04,
        extra="margin-top:26px;")
    + p(1, "Não se deixe para depois. Você também merece atenção, carinho e cuidado.", C, size=18, gap=14)
    + f'<div style="margin-top:22px;">{logo_lockup(C, w=160, align="left", gap_below=0)}</div>',
    anchor="center", pad="40px 36px 40px"),
    layers=circulo(AREIA, 380, 470, 120, op=0.7))]

html = pagina("Você cuida de todos", "Autocuidado",
              "Você cuida de todos, mas tem cuidado de si mesma? Não se deixe para depois. "
              "Vamos conversar sobre você? O link para agendar está na bio.",
              s, {1: "Post"}, "conteudos/2026-11-17-voce-cuida-de-todos")
(BASE / "carousel.html").write_text(html, encoding="utf-8")
print("ok", len(html))
