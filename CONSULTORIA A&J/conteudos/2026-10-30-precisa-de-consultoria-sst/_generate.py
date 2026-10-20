# -*- coding: utf-8 -*-
"""POST 05 · out/2026 · Sua empresa precisa de consultoria em SST?
Sorteio: passo-a-passo · pergunta · seed 62 · misto (capa e CTA centralizados).
2026-10-20: texto curto + número do passo, pergunta gigante e checklist; capa colorida (verde); foto full
no miolo sorteada: slide 4 (seed 219932269), com o rosto e o protetor em cima e o texto embaixo; creme só nos
slides 2 e 3; selo "arraste" na capa + setinha até o 7. Nenhum slide só com fundo e texto: pastas recortadas (2),
balão em traço (5), bloco de cor (6)."""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent))
from _carrossel_base import *  # noqa: E402,F403

C, E, PT, V, F, CTA = tom("claro"), tom("escuro"), tom("petroleo"), tom("verde"), tom("foto"), tom("cta")
IND, N = "selo", 8
ED = BASE / "assets" / "edited"
FOTO3, FOTO4 = foto(ED / "slide3-photo.jpg"), foto(ED / "slide4-split.jpg")
PASTAS = png(ED / "slide2-pastas.png")
PAD = "56px 36px 64px"


def casinhas(t, qtd=4, tam=40):
    box = (f'<span style="width:{tam}px;height:{tam}px;border-radius:7px;border:2.5px solid {t["acc"]};display:block;"></span>')
    return f'<div style="display:flex;justify-content:center;gap:16px;margin-top:30px;">{box * qtd}</div>'


s = []
# 1 · capa tipográfica em verde chapado + 4 casinhas vazias
s.append(slide(V, bloco(
    logo_lockup(V, gap_below=24)
    + h(1, f"Sua empresa {it('precisa', V)} de consultoria em SST?", V, size=48, lh=1.04, align="center")
    + p(1, "Faça o teste de 4 passos.", V, role="subhead", size=21, align="center", gap=18, weight=600)
    + casinhas(V),
    align="center") + indicador(IND, 0, N, V)))
# 2 · passo 1: lista · creme 1/2
s.append(slide(C, bloco(
    numero_passo(1, 4, C, size=100)
    + h(2, "Separe os documentos", C, size=40, extra="margin-top:18px;")
    + lista(2, C, ["PGR", "PCMSO", "Laudos (como o LTCAT)", "Certificados dos treinamentos de NR"], size=20, gap_top=18),
    anchor="bottom", pad=PAD) + indicador(IND, 1, N, C),
    layers=recorte(PASTAS, 252, -92, 180, rot=-8, nota="pexels.com/photo/16978372")))
# 3 · passo 2: foto emoldurada · creme 2/2
s.append(slide(C, bloco(
    numero_passo(2, 4, C, size=96)
    + '<!-- foto: pexels.com/photo/8293680 -->'
    f'<div style="border-radius:12px;overflow:hidden;margin-top:16px;"><img src="{FOTO3}" alt="" style="display:block;'
    'width:100%;height:170px;object-fit:cover;object-position:55% 45%;"></div>'
    + h(3, "Confira as datas.", C, size=36, extra="margin-top:16px;")
    + p(3, "Entrou máquina nova, mudou o layout, surgiu uma função? O PGR precisa acompanhar.", C, size=19, gap=10),
    anchor="bottom", pad="40px 36px 56px") + indicador(IND, 2, N, C)))
# 4 · passo 3: foto grande em cima (rosto e protetor no pescoço inteiros), texto embaixo em petróleo
s.append(slide(PT,
    '<!-- foto: pexels.com/photo/8960995 -->'
    f'<img src="{FOTO4}" alt="" style="position:absolute;left:0;top:0;width:420px;height:230px;object-fit:cover;object-position:50% 35%;">'
    + bloco(numero_passo(3, 4, PT, size=50)
            + h(4, "Compare papel e rotina", PT, size=26, extra="margin-top:6px;")
            + comparacao(4, PT, "No PGR", "Na rotina", [
                ("Protetor auricular previsto", "Protetor no pescoço"),
                ("Equipe treinada", "Novato sem integração"),
            ], size=15, gap_top=8, cab_size=13),
            anchor="top", pad="244px 36px 34px")
    + indicador(IND, 3, N, PT)))
# 5 · passo 4: pergunta gigante (a pausa escura)
s.append(slide(E, bloco(
    numero_passo(4, 4, E, size=120)
    + p(5, "Pergunte a quem faz o serviço:", E, role="step", size=21, weight=500, gap=20, color="#fff")
    + h(5, "“Qual é o risco da sua tarefa?”", E, size=46, lh=1.05, role="question", extra="margin-top:10px;")
    + p(5, "Resposta vaga: o documento não chegou até ele.", E, size=19, gap=18),
    anchor="bottom", pad=PAD) + indicador(IND, 4, N, E),
    layers=traco("balao", PL, 192, -34, 206, op=0.55, sw=5)))
# 6 · comparação em petróleo
s.append(slide(PT, bloco(
    h(6, "Resolver dentro ou chamar consultoria?", PT, size=40, lh=1.05)
    + comparacao(6, PT, "Resolver dentro", "Chamar consultoria", [
        ("Ajuste que a equipe já sabe", "Documentos desatualizados"),
        ("Dúvida pontual", "Riscos novos, como os psicossociais (NR&#8209;1)"),
    ], size=19, gap_top=26, cab_size=15),
    anchor="bottom", pad=PAD) + indicador(IND, 5, N, PT),
    layers=bloco_cor(DBG, 216, 0, 204, 525)))
# 7 · checklist dos 4 passos em verde chapado
s.append(slide(V, bloco(
    h(7, "Salva o teste e faz esta semana.", V, size=40, lh=1.05)
    + checklist(7, V, ["Documentos separados", "Datas conferidas", "Papel x rotina comparados", "Equipe ouvida"], gap_top=22)
    + p(7, "Dúvida em mais de um passo? Já vale uma conversa.", V, size=19, gap=20, weight=600, color=DBG),
    anchor="bottom", pad=PAD) + indicador(IND, 6, N, V),
    layers=traco("prancheta", "#fff", 226, -118, 210, op=0.9, sw=6, rot=12)))
# 8 · CTA (degradê assinatura)
s.append(slide(CTA, bloco(
    logo_lockup(CTA, size=40, fs=15)
    + h(8, "A A&amp;J faz o diagnóstico e acompanha o depois.", CTA, size=38, lh=1.08, align="center")
    + botao(8, "Chama no direct")
    + p(8, HANDLE, CTA, size=15, role="handle", align="center", gap=18, weight=500),
    align="center")))

LABELS = {1: "Capa", 2: "Passo 1", 3: "Passo 2", 4: "Passo 3", 5: "Passo 4", 6: "Dentro x consultoria", 7: "Checklist", 8: "CTA"}
html = pagina("Sua empresa precisa de consultoria em SST?", "Consultoria em SST",
              "Consultoria em SST: um teste rápido para saber se a sua empresa precisa.", s, LABELS,
              "conteudos/2026-10-30-precisa-de-consultoria-sst")
(BASE / "carousel.html").write_text(html, encoding="utf-8")
print("ok", len(html))
