# -*- coding: utf-8 -*-
"""POST 05 · 24/11/2026 · Menopausa e autoestima: como acolher as mudanças do próprio corpo? (6 slides).
Roteiro aprovado em 2026-11-08. Sorteio seed 1; foto emoldurada trocada do 2 para o 3; comparação virou lista no 5.
Fotos: capa recortada (6A pexels 6874412) e card no 3 (7A pexels 10221832), suaves. Sem indicador.
Recursos: linha do tempo (2), foto (3), meio círculo (4), mão no peito (5), assinatura (6). Creme no 2 e no 5."""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent))
from _carrossel_base import *  # noqa: E402,F403

C, O, G = tom("creme"), tom("oliva"), tom("dourado")
N = 6
ED = BASE / "assets" / "edited"
CAPA, ESPELHO = foto(ED / "slide1-recortada.jpg"), foto(ED / "slide3-card.jpg")


def linha_do_tempo(t, w=348):
    pts = [20, 100, 180, 260, 330]
    svg = (f'<svg width="{w}" height="60" viewBox="0 0 {w} 60"><path d="M0 30H{w}" stroke="{P}" stroke-width="4"/>'
           + "".join(f'<circle cx="{x}" cy="30" r="{18 if k == 3 else 10}" fill="{PD if k == 3 else LBG}" '
                     f'stroke="{P}" stroke-width="3"/>' for k, x in enumerate(pts)) + "</svg>")
    return (f'<div data-ap-fixo style="position:relative;margin-top:70px;">{svg}'
            f'<span class="sans" style="position:absolute;left:{pts[3] - 24}px;top:58px;font-size:15px;font-weight:600;'
            f'color:#6E5424;">agora</span></div>')


s = []
# 1 · capa: foto recortada à direita, título encostado embaixo, logo no alto à esquerda
s.append(slide(G,
    f'<div style="position:absolute;left:190px;top:0;z-index:1;">'
    f'{foto_card(CAPA, 230, 300, pos="50% 30%", nota="pexels.com/photo/6874412", r=0, sombra=False)}</div>'
    + f'<div style="position:absolute;top:28px;left:22px;z-index:3;">{logo_lockup(G, w=160, align="left", gap_below=0)}</div>'
    + bloco(h(1, f"Menopausa e autoestima: como acolher as mudanças do {it('próprio corpo?', G)}", G, size=36, lh=1.04),
            anchor="bottom", pad="0 36px 40px")))
# 2 · por que importa: creme, linha do tempo com o "agora"
s.append(slide(C, bloco(
    h(2, f"As mudanças hormonais trazem transformações físicas e {it('emocionais.', C)}", C, size=36, lh=1.05)
    + p(2, "E elas afetam a maneira como a mulher se percebe.", C, size=19, gap=16)
    + linha_do_tempo(C),
    anchor="top", pad="76px 36px 60px") + marca_canto(1, N, C),
    layers=circulo(AREIA, 400, 540, 150, op=0.8)))
# 3 · virada: oliva, foto do espelho
s.append(slide(O, bloco(
    h(3, "Talvez você esteja se olhando de um jeito diferente.", O, size=34, lh=1.05)
    + p(3, "Sentindo insegurança ou comparando seu corpo com o de outras fases da vida.", O, size=17, gap=12)
    + f'<div style="margin-top:20px;">{foto_card(ESPELHO, 348, 200, pos="50% 40%", nota="pexels.com/photo/10221832")}</div>',
    anchor="top", pad="62px 36px 40px") + marca_canto(2, N, O)))
# 4 · o que muda: dourado, meio círculo oliva saindo pela base
s.append(slide(G, bloco(
    h(4, f"Seu valor não está na aparência nem na {it('idade.', G, color=OLIVA_TXT)}", G, size=46, lh=1.02)
    + p(4, "Nem na capacidade de manter a mesma versão de si para sempre.", G, size=19, gap=18, weight=500),
    anchor="top", pad="80px 36px 76px") + marca_canto(3, N, G),
    layers=circulo(DBG, 330, 560, 170, op=0.9)))
# 5 · como fazer: creme, mão no peito
s.append(slide(C, bloco(
    h(5, "Comece respeitando seu corpo.", C, size=42, lh=1.04)
    + lista(5, C, ["Reconheça suas necessidades", "Cuide da sua saúde", "Viva essa fase com menos cobrança"], size=19, gap_top=22),
    anchor="top", pad="76px 36px 60px") + marca_canto(4, N, C),
    layers=traco("mao", P, 250, 330, 220, op=0.55, sw=4, rot=-6)))
# 6 · chamada: oliva, logo completa e assinatura
s.append(slide(O, bloco(
    logo_lockup(O, w=280, gap_below=18)
    + h(6, f"Seu corpo tem uma {it('história.', O)}", O, size=42, lh=1.04, align="center")
    + p(6, "Olhe para ele com mais carinho e permita-se construir uma nova relação consigo mesma.", O, size=18,
        gap=14, align="center")
    + assinatura(6, O, size=32, gap=20, align="center"),
    align="center", pad="50px 36px 56px"),
    layers=circulo(PL, 420, 525, 90, op=0.25, contorno=2) + circulo(PL, 0, 0, 70, op=0.25, contorno=2)))

LABELS = {1: "Capa", 2: "Hormônios", 3: "Espelho", 4: "Seu valor", 5: "Como começar", 6: "CTA"}
html = pagina("Menopausa e autoestima", "Menopausa",
              "Menopausa e autoestima: como acolher as mudanças do próprio corpo? Seu corpo tem uma história. "
              "Vamos conversar sobre você? O link para agendar está na bio.",
              s, LABELS, "conteudos/2026-11-24-menopausa-e-autoestima")
(BASE / "carousel.html").write_text(html, encoding="utf-8")
print("ok", len(html))
