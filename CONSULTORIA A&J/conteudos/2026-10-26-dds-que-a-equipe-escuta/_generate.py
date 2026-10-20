# -*- coding: utf-8 -*-
"""POST 03 · out/2026 · DDS que a equipe escuta.
Sorteio: passo-a-passo · pergunta · seed 43 · fundos em blocos · misto (capa e CTA centralizados, miolo à esquerda)
· texto varia por slide · contador.
Revisão de 2026-10-20: texto curto por slide + número grande do passo com trilha "passo x de 5"."""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent))
from _carrossel_base import *  # noqa: E402,F403

C, E, F = tom("claro"), tom("escuro"), tom("foto")
IND, N = "contador", 8
ED = BASE / "assets" / "edited"
FOTO1, FOTO2, FOTO8 = foto(ED / "slide1-photo.jpg"), foto(ED / "slide2-photo.jpg"), foto(ED / "slide8-photo.jpg")
R = "18,63,60"  # DARK_BG em rgb, para os degradês de legibilidade
SERIF_APOIO = "font-family:'Lora',serif;line-height:1.28;"

s = []
# 1 · capa: foto em cima, título embaixo
s.append(slide(C,
    '<!-- foto: pexels.com/photo/35082106 -->'
    f'<img src="{FOTO1}" alt="" style="position:absolute;left:0;top:0;width:420px;height:236px;object-fit:cover;object-position:62% 25%;">'
    + bloco(logo_lockup(C, size=26, fs=12, gap_below=14)
            + h(1, "Sua equipe escuta o DDS ou só espera ele acabar?", C, size=37, lh=1.06, align="center"),
            align="center", anchor="center", pad="250px 30px 44px")
    + indicador(IND, 0, N, C)))
# 2 · foto no slide inteiro, texto no espaço de baixo
s.append(slide(F,
    '<!-- foto: pexels.com/photo/30179842 -->'
    f'<img src="{FOTO2}" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 20%;">'
    f'<div style="position:absolute;inset:0;z-index:1;background:linear-gradient(0deg,rgba({R},0.94) 0%,rgba({R},0.88) 28%,'
    f'rgba({R},0.62) 42%,rgba({R},0.26) 56%,rgba({R},0) 68%);"></div>'
    f'<div style="position:absolute;inset:0;z-index:1;background:rgba({R},0.16);"></div>'
    + bloco(h(2, "Roda, tema lido, alguém no celular.", F, size=36, lh=1.08)
            + p(2, "Na hora do serviço, ninguém lembra.", F, size=21, gap=14),
            anchor="bottom", pad="64px 36px 58px")
    + indicador(IND, 1, N, F)))
# 3 · passo 1 (frase gigante)
s.append(slide(E, bloco(
    numero_passo(1, 5, E)
    + h(3, "Fale do serviço de hoje.", E, size=46, lh=1.04, extra="margin-top:22px;")
    + p(3, "Nada de tema genérico da lista.", E, size=21, gap=16),
    anchor="center") + indicador(IND, 2, N, E)))
# 4 · passo 2 (pergunta grande)
s.append(slide(E, bloco(
    numero_passo(2, 5, E)
    + p(4, "Abra com uma pergunta:", E, role="step", size=22, weight=500, gap=22, color="#fff")
    + h(4, it("“O que pode dar errado hoje?”", E, color="#fff"), E, size=46, lh=1.06, role="question", extra="margin-top:12px;"),
    anchor="center") + indicador(IND, 3, N, E)))
# 5 · passo 3 (frase gigante)
s.append(slide(C, bloco(
    numero_passo(3, 5, C)
    + h(5, "Use o que aconteceu aqui.", C, size=46, lh=1.04, extra="margin-top:22px;")
    + p(5, "O quase acidente da semana ensina mais que a apostila.", C, size=23, gap=16, weight=500, color=DBG, extra=SERIF_APOIO),
    anchor="center") + indicador(IND, 4, N, C)))
# 6 · passo 4 (pergunta grande)
s.append(slide(C, bloco(
    numero_passo(4, 5, C)
    + p(6, "Feche com um combinado:", C, role="step", size=22, weight=500, gap=22, color=DBG)
    + h(6, "“Quem confere o quê antes de começar?”", C, size=42, lh=1.06, role="question", extra="margin-top:12px;"),
    anchor="center") + indicador(IND, 5, N, C)))
# 7 · passo 5 (título e apoio)
s.append(slide(E, bloco(
    numero_passo(5, 5, E)
    + h(7, "Reveze quem conduz.", E, size=46, lh=1.04, extra="margin-top:22px;")
    + p(7, "Sai o tom de palestra.", E, size=21, gap=16)
    + p(7, "Salva e testa no próximo DDS.", E, role="cta", size=19, weight=600, color=PL, gap=18),
    anchor="center") + indicador(IND, 6, N, E)))
# 8 · CTA sobre foto
s.append(slide(F,
    '<!-- foto: pexels.com/photo/8961259 -->'
    f'<img src="{FOTO8}" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 40%;">'
    f'<div style="position:absolute;inset:0;z-index:1;background:linear-gradient(0deg,rgba({R},0.95) 0%,rgba({R},0.88) 26%,'
    f'rgba({R},0.58) 38%,rgba({R},0.18) 50%,rgba({R},0) 58%);"></div>'
    f'<div style="position:absolute;inset:0;z-index:1;background:rgba({R},0.16);"></div>'
    # logo no canto superior esquerdo, sobre a areia vazia, longe dos trabalhadores
    + f'<div style="position:absolute;top:22px;left:24px;z-index:3;">'
      f'{logo_lockup(F, size=26, fs=12, align="left", gap_below=0, chip="rgba(18,63,60,0.6)")}</div>'
    + bloco(h(8, "Precisa montar os temas de DDS da sua operação?", F, size=29, lh=1.1, align="center")
            + p(8, "Chama a A&amp;J no direct.", F, role="cta", size=20, weight=600, align="center", gap=14, color="#fff")
            + p(8, HANDLE, F, role="handle", size=15, align="center", gap=8, color=F["mute"]),
            align="center", anchor="bottom", pad="64px 36px 54px")
    + indicador(IND, 7, N, F)))

LABELS = {1: "Capa", 2: "A cena", 3: "Passo 1", 4: "Passo 2", 5: "Passo 3", 6: "Passo 4", 7: "Passo 5", 8: "CTA"}
html = pagina("DDS que a equipe escuta", "Treinamento e segurança",
              "DDS que funciona: 5 passos para o Diálogo Diário de Segurança sair do automático.", s, LABELS,
              "conteudos/2026-10-26-dds-que-a-equipe-escuta")
(BASE / "carousel.html").write_text(html, encoding="utf-8")
print("ok", len(html))
