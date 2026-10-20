# -*- coding: utf-8 -*-
"""POST 01 · out/2026 · A ata da CIPA ficou pronta antes da reunião.
Sorteio: erro-comum · cena-do-dia-a-dia · seed 1 · centralizado.
2026-10-20: história em arco (gancho, erro, por que importa, o que a norma espera, papel x funcionando, como
virar, chamada); capa colorida, creme só no slide 5; fotos full no miolo sorteadas: 0 (seed 219932269); selo "arraste" na capa + setinha até o 7.
Nenhum slide só com fundo e texto: traço da ata (1), calendário (2), número (3), prancheta (4), bloco de cor (5)."""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent))
from _carrossel_base import *  # noqa: E402,F403

C, E, PT, V, CTA = tom("claro"), tom("escuro"), tom("petroleo"), tom("verde"), tom("cta")
IND, N = "selo", 8
FOTO7 = foto(BASE / "assets" / "edited" / "slide7-photo.jpg")
PRANCHETA = png(BASE / "assets" / "edited" / "slide4-prancheta.png")

s = []
# 1 · capa tipográfica em petróleo
s.append(slide(PT, bloco(
    logo_lockup(PT, gap_below=26)
    + h(1, f"A ata da CIPA ficou pronta {it('antes', PT)} da reunião.", PT, size=54, lh=1.02, align="center")
    + p(1, "Aí a comissão existe só no papel.", PT, role="subhead", size=21, align="center", gap=22),
    align="center") + indicador(IND, 0, N, PT),
    layers=traco("ata", PL, -92, -92, 204, op=0.24, sw=4, rot=-12)))
# 2 · o erro: título e apoio + calendário
s.append(slide(E, bloco(
    h(2, "O erro: CIPA virar data no calendário.", E, size=36, lh=1.08, align="center")
    + p(2, "Reunião, ata assinada, pasta. O risco continua no lugar.", E, size=19, align="center", gap=14)
    + calendario(E, dia=15, rotulo="reunião da CIPA", gap_top=20, ch=24),
    align="center", pad="44px 40px 44px") + indicador(IND, 1, N, E)))
# 3 · por que importa: o dado em destaque, em petróleo
s.append(slide(PT, bloco(
    numero_destaque(3, "+700&nbsp;mil", "acidentes de trabalho registrados no Brasil em 2024",
                    "Fonte: Anuário Estatístico da Previdência Social", PT, size=80, align="center", gap_top=0)
    + h(3, "Prevenir é o motivo de a CIPA existir.", PT, size=38, lh=1.08, align="center", extra="margin-top:34px;"),
    align="center") + indicador(IND, 2, N, PT)))
# 4 · o que a norma espera: lista curta em verde chapado
s.append(slide(V, bloco(
    h(4, "O que a NR-5 espera da CIPA", V, size=42, lh=1.05, align="center")
    + lista(4, V, ["Identificar riscos", "Acompanhar a análise de acidentes", "Propor e cobrar melhorias", "Prevenir o assédio"],
            size=21, gap_top=24),
    align="center") + indicador(IND, 3, N, V),
    layers=recorte(PRANCHETA, 300, 392, 132, rot=14, nota="pexels.com/photo/12039583")))
# 5 · no papel x funcionando: uma comparação só · creme 1/1
s.append(slide(C, bloco(
    comparacao(5, C, "No papel", "Funcionando", [
        ("Ata copiada", "Ata com o que foi visto no setor"),
        ("Lê a ata e encerra", "Revisa cada pendência"),
        ("Sem prazo", "Cada ação com responsável e data"),
    ], size=19, gap_top=0, cab_serif=True, cab_size=30),
    align="center") + indicador(IND, 4, N, C),
    layers=bloco_cor(PL, 216, 0, 204, 525)))
# 6 · ciclo em roda
s.append(slide(E, bloco(
    h(6, "Um ciclo por mês", E, size=40, align="center")
    + ciclo_roda(6, E, ["Ouvir a equipe", "Registrar", "Levar à reunião", "Definir responsável e prazo",
                        "Conferir na reunião seguinte"]),
    align="center", pad="46px 30px 30px") + indicador(IND, 5, N, E)))
# 7 · foto dividida (foto em cima, texto embaixo em petróleo)
s.append(slide(PT,
    '<!-- foto: pexels.com/photo/8961064 -->'
    f'<img src="{FOTO7}" alt="" style="position:absolute;left:0;top:0;width:420px;height:262px;object-fit:cover;object-position:50% 30%;">'
    + bloco(h(7, "Manda pra quem é da CIPA e salva pra próxima reunião.", PT, size=34, lh=1.12, align="center"),
            align="center", anchor="center", pad="290px 36px 40px") + indicador(IND, 6, N, PT, foto_no_canto=True)))
# 8 · CTA (degradê assinatura)
s.append(slide(CTA, bloco(
    logo_lockup(CTA, size=40, fs=15)
    + h(8, f"Quer ajuda pra tirar a CIPA {it('do papel?', CTA, color='#fff')}", CTA, size=44, align="center")
    + botao(8, "Chama a A&amp;J no direct")
    + p(8, HANDLE, CTA, size=15, role="handle", align="center", gap=18, weight=500),
    align="center")))

LABELS = {1: "Capa", 2: "O erro", 3: "Por que importa", 4: "NR-5", 5: "Papel x funcionando", 6: "Ciclo", 7: "Foto + chamada", 8: "CTA"}
html = pagina("A ata da CIPA ficou pronta antes da reunião", "Segurança do Trabalho",
              "CIPA: sua comissão previne acidentes ou só assina ata?", s, LABELS,
              "conteudos/2026-10-21-cipa-no-papel")
(BASE / "carousel.html").write_text(html, encoding="utf-8")
print("ok", len(html))
