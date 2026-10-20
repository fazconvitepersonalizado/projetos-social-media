# -*- coding: utf-8 -*-
"""POST 01 · out/2026 · A ata da CIPA ficou pronta antes da reunião.
Sorteio: erro-comum · cena-do-dia-a-dia · seed 1 · fundos alternados · centralizado · selo só na capa.
Revisão de 2026-10-20: texto curto por slide + elementos desenhados (calendário, ciclo em roda)."""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent))
from _carrossel_base import *  # noqa: E402,F403

C, E, CTA = tom("claro"), tom("escuro"), tom("cta")
IND, N = "selo", 8
FOTO7 = foto(BASE / "assets" / "edited" / "slide7-photo.jpg")

s = []
# 1 · capa tipográfica
s.append(slide(C, bloco(
    logo_lockup(C, gap_below=26)
    + h(1, f"A ata da CIPA ficou pronta {it('antes', C)} da reunião.", C, size=54, lh=1.02, align="center")
    + p(1, "Aí a comissão existe só no papel.", C, role="subhead", size=21, align="center", gap=22),
    align="center") + indicador(IND, 0, N, C)))
# 2 · título e apoio + calendário
s.append(slide(E, bloco(
    h(2, "O erro: CIPA virar data no calendário.", E, size=36, lh=1.08, align="center")
    + p(2, "Reunião, ata assinada, pasta. O risco continua no lugar.", E, size=19, align="center", gap=14)
    + calendario(E, dia=15, rotulo="reunião da CIPA", gap_top=20, ch=24),
    align="center", pad="44px 40px 44px") + indicador(IND, 1, N, E)))
# 3 · comparação (os cabeçalhos são o título)
s.append(slide(C, bloco(
    comparacao(3, C, "No papel", "Funcionando", [
        ("Ata copiada", "Ata com o que foi visto no setor"),
        ("Membro que só assina", "Membro que traz a voz da equipe"),
    ], size=20, gap_top=0, cab_serif=True, cab_size=30),
    align="center") + indicador(IND, 2, N, C)))
# 4 · lista curta
s.append(slide(E, bloco(
    h(4, "O que a NR-5 espera da CIPA", E, size=42, lh=1.05, align="center")
    + lista(4, E, ["Identificar riscos", "Acompanhar a análise de acidentes", "Propor e cobrar melhorias", "Prevenir o assédio"],
            size=21, gap_top=24),
    align="center") + indicador(IND, 3, N, E)))
# 5 · comparação
s.append(slide(C, bloco(
    h(5, "Cumpre tabela ou previne?", C, size=46, lh=1.04, align="center")
    + comparacao(5, C, "Cumpre tabela", "Previne", [
        ("Lê a ata e encerra", "Revisa cada pendência"),
        ("Sem prazo", "Cada ação com responsável e data"),
    ], size=20, gap_top=28, cab_size=15),
    align="center") + indicador(IND, 4, N, C)))
# 6 · ciclo em roda
s.append(slide(E, bloco(
    h(6, "Um ciclo por mês", E, size=40, align="center")
    + ciclo_roda(6, E, ["Ouvir a equipe", "Registrar", "Levar à reunião", "Definir responsável e prazo",
                        "Conferir na reunião seguinte"]),
    align="center", pad="46px 30px 30px") + indicador(IND, 5, N, E)))
# 7 · foto dividida (foto em cima, texto embaixo)
s.append(slide(C,
    '<!-- foto: pexels.com/photo/8961064 -->'
    f'<img src="{FOTO7}" alt="" style="position:absolute;left:0;top:0;width:420px;height:262px;object-fit:cover;object-position:50% 30%;">'
    + bloco(h(7, "Manda pra quem é da CIPA e salva pra próxima reunião.", C, size=34, lh=1.12, align="center"),
            align="center", anchor="center", pad="290px 36px 40px") + indicador(IND, 6, N, C)))
# 8 · CTA (degradê assinatura)
s.append(slide(CTA, bloco(
    logo_lockup(CTA, size=40, fs=15)
    + h(8, f"Quer ajuda pra tirar a CIPA {it('do papel?', CTA, color='#fff')}", CTA, size=44, align="center")
    + botao(8, "Chama a A&amp;J no direct")
    + p(8, HANDLE, CTA, size=15, role="handle", align="center", gap=18, weight=500),
    align="center")))

LABELS = {1: "Capa", 2: "O erro", 3: "Comparação", 4: "NR-5", 5: "Reunião", 6: "Ciclo", 7: "Foto + chamada", 8: "CTA"}
html = pagina("A ata da CIPA ficou pronta antes da reunião", "Segurança do Trabalho",
              "CIPA: sua comissão previne acidentes ou só assina ata?", s, LABELS,
              "conteudos/2026-10-21-cipa-no-papel")
(BASE / "carousel.html").write_text(html, encoding="utf-8")
print("ok", len(html))
