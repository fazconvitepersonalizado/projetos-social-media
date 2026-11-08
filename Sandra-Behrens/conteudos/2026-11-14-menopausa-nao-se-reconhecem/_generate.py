# -*- coding: utf-8 -*-
"""POST 02 · 14/11/2026 · Menopausa: por que tantas mulheres sentem que já não se reconhecem? (7 slides).
Roteiro aprovado em 2026-11-08. Sorteio seed 13; pergunta-grande virou lista no 6.
Fotos no slide inteiro: 1 (2A pexels 6874398) e 7 (3A pexels 5473066), suaves, texto no espaço livre de baixo.
Sem indicador de arraste. Recursos: onda (2), lua e termômetro (3), meio círculo (4), espelho (5), livro (6).
Creme só no 3 e no 6."""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent))
from _carrossel_base import *  # noqa: E402,F403

C, O, G, F = tom("creme"), tom("oliva"), tom("dourado"), tom("foto")
N = 7
ED = BASE / "assets" / "edited"
CAPA, CTA_FOTO = foto(ED / "slide1-full.jpg"), foto(ED / "slide7-full.jpg")
CHIP = "rgba(62,66,52,0.6)"

s = []
# 1 · capa: mulher à janela, título embaixo
s.append(slide(F,
    foto_full(CAPA, ate=0.60, pos="50% 30%", nota="pexels.com/photo/6874398")
    + f'<div style="position:absolute;top:18px;right:18px;z-index:3;">{logo_lockup(F, w=160, align="right", gap_below=0, chip=CHIP)}</div>'
    + bloco(h(1, f"Menopausa: por que tantas mulheres sentem que já não se {it('reconhecem?', F)}", F, size=36, lh=1.06),
            anchor="bottom", pad="64px 36px 46px")))
# 2 · contexto: oliva, onda em traço saindo pela base
s.append(slide(O, bloco(
    h(2, f"O corpo muda e os hormônios se {it('transformam.', O)}", O, size=46, lh=1.02)
    + p(2, "Muitas vezes, as emoções parecem acompanhar essa nova fase.", O, size=19, gap=18),
    anchor="top", pad="80px 36px 76px") + marca_canto(1, N, O),
    layers=traco("onda", PL, -20, 175, 470, op=0.6, sw=3)))
# 3 · o que muda: creme, lista com lua e termômetro
s.append(slide(C, bloco(
    h(3, "O que pode fazer parte dessa experiência", C, size=38, lh=1.04)
    + lista(3, C, ["Alterações no sono", "Ondas de calor", "Irritabilidade", "Mudanças na disposição"], size=19, gap_top=20),
    anchor="top", pad="70px 36px 60px", maxw=360) + marca_canto(2, N, C),
    layers=traco("lua", P, 300, 330, 150, op=0.55, sw=4) + traco("termometro", P, 250, 380, 150, op=0.55, sw=4, rot=12)))
# 4 · o que muda: dourado, meio círculo areia saindo pela base
s.append(slide(G, bloco(
    h(4, "As mudanças vão além do corpo.", G, size=48, lh=1.0)
    + p(4, "A autoestima, a sexualidade e a forma como você se vê também podem mudar.", G, size=19, gap=18, weight=500),
    anchor="top", pad="80px 36px 76px") + marca_canto(3, N, G),
    layers=circulo(AREIA, 210, 560, 200, op=0.55)))
# 5 · por que importa: oliva, espelho oval em traço
s.append(slide(O, bloco(
    h(5, f"É comum não reconhecer o {it('próprio corpo.', O)}", O, size=46, lh=1.02)
    + p(5, "Ou sentir falta de quem você era antes.", O, size=20, gap=18),
    anchor="top", pad="80px 36px 76px") + marca_canto(4, N, O),
    layers=traco("espelho", PL, 200, 250, 290, op=0.5, sw=3)))
# 6 · como fazer: creme, livro aberto
s.append(slide(C, bloco(
    h(6, "Nesse momento, o que ajuda:", C, size=40, lh=1.04)
    + lista(6, C, ["Acolher suas emoções", "Buscar informação", "Contar com apoio profissional"], size=20, gap_top=22),
    anchor="top", pad="76px 36px 60px") + marca_canto(5, N, C),
    layers=traco("livro", P, 210, 340, 240, op=0.55, sw=4)))
# 7 · chamada: foto inteira, texto embaixo
s.append(slide(F,
    foto_full(CTA_FOTO, ate=0.66, pos="50% 25%", nota="pexels.com/photo/5473066")
    + f'<div style="position:absolute;top:18px;left:18px;z-index:3;">{logo_lockup(F, w=160, align="left", gap_below=0, chip=CHIP)}</div>'
    + bloco(h(7, f"Você não deixou de ser {it('você.', F)}", F, size=42, lh=1.02)
            + p(7, "Está vivendo uma nova fase e merece atravessá-la com acolhimento, cuidado e respeito.", F, size=18, gap=12)
            + assinatura(7, F, size=28, gap=14, cor="#fff"),
            anchor="bottom", pad="64px 36px 40px")))

LABELS = {1: "Capa", 2: "O corpo muda", 3: "Sintomas", 4: "Além do corpo", 5: "Não se reconhecer", 6: "O que ajuda", 7: "CTA"}
html = pagina("Menopausa: não se reconhecer", "Menopausa",
              "Menopausa: por que tantas mulheres sentem que já não se reconhecem? Você não deixou de ser você. "
              "Vamos conversar sobre você? O link para agendar está na bio.",
              s, LABELS, "conteudos/2026-11-14-menopausa-nao-se-reconhecem")
(BASE / "carousel.html").write_text(html, encoding="utf-8")
print("ok", len(html))
