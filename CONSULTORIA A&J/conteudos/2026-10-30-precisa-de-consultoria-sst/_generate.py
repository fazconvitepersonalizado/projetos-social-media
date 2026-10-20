# -*- coding: utf-8 -*-
"""POST 05 · out/2026 · Sua empresa precisa de consultoria em SST?
Sorteio: passo-a-passo · pergunta · seed 62 · claro com pausa escura · misto (capa e CTA centralizados) · texto na base
· selo só na capa.
Revisão de 2026-10-20: texto curto por slide + número do passo, pergunta gigante e checklist desenhado."""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent))
from _carrossel_base import *  # noqa: E402,F403

C, E, CTA = tom("claro"), tom("escuro"), tom("cta")
IND, N = "selo", 8
FOTO3 = foto(BASE / "assets" / "edited" / "slide3-photo.jpg")
PAD = "56px 36px 64px"


def casinhas(t, qtd=4, tam=40):
    box = (f'<span style="width:{tam}px;height:{tam}px;border-radius:7px;border:2.5px solid {t["acc"]};display:block;"></span>')
    return f'<div style="display:flex;justify-content:center;gap:16px;margin-top:30px;">{box * qtd}</div>'


s = []
# 1 · capa tipográfica + 4 casinhas vazias
s.append(slide(C, bloco(
    logo_lockup(C, gap_below=24)
    + h(1, f"Sua empresa {it('precisa', C)} de consultoria em SST?", C, size=48, lh=1.04, align="center")
    + p(1, "Faça o teste de 4 passos.", C, role="subhead", size=21, align="center", gap=18)
    + casinhas(C),
    align="center") + indicador(IND, 0, N, C)))
# 2 · passo 1: lista
s.append(slide(C, bloco(
    numero_passo(1, 4, C, size=100)
    + h(2, "Separe os documentos", C, size=40, extra="margin-top:18px;")
    + lista(2, C, ["PGR", "PCMSO", "Laudos (como o LTCAT)", "Certificados dos treinamentos de NR"], size=20, gap_top=18),
    anchor="bottom", pad=PAD) + indicador(IND, 1, N, C)))
# 3 · passo 2: foto emoldurada
s.append(slide(C, bloco(
    numero_passo(2, 4, C, size=96)
    + '<!-- foto: pexels.com/photo/8293680 -->'
    f'<div style="border-radius:12px;overflow:hidden;margin-top:16px;"><img src="{FOTO3}" alt="" style="display:block;'
    'width:100%;height:170px;object-fit:cover;object-position:55% 45%;"></div>'
    + h(3, "Confira as datas.", C, size=36, extra="margin-top:16px;")
    + p(3, "Algo mudou no setor, na máquina ou na função depois do documento?", C, size=19, gap=10),
    anchor="bottom", pad="40px 36px 56px") + indicador(IND, 2, N, C)))
# 4 · passo 3: comparação
s.append(slide(C, bloco(
    numero_passo(3, 4, C, size=100)
    + h(4, "Compare papel e rotina", C, size=40, extra="margin-top:18px;")
    + comparacao(4, C, "No PGR", "Na rotina", [
        ("Protetor auricular previsto", "Protetor no pescoço"),
        ("Equipe treinada", "Novato sem integração"),
    ], size=19, gap_top=20, cab_size=15),
    anchor="bottom", pad=PAD) + indicador(IND, 3, N, C)))
# 5 · passo 4: pergunta gigante (a pausa escura)
s.append(slide(E, bloco(
    numero_passo(4, 4, E, size=120)
    + p(5, "Pergunte a quem faz o serviço:", E, role="step", size=21, weight=500, gap=20, color="#fff")
    + h(5, "“Qual é o risco da sua tarefa?”", E, size=46, lh=1.05, role="question", extra="margin-top:10px;")
    + p(5, "Resposta vaga: o documento não chegou até ele.", E, size=19, gap=18),
    anchor="bottom", pad=PAD) + indicador(IND, 4, N, E)))
# 6 · comparação
s.append(slide(C, bloco(
    h(6, "Resolver dentro ou chamar consultoria?", C, size=40, lh=1.05)
    + comparacao(6, C, "Resolver dentro", "Chamar consultoria", [
        ("Ajuste que a equipe já sabe", "Documentos desatualizados"),
        ("Dúvida pontual", "Riscos novos, como os psicossociais (NR-1)"),
    ], size=19, gap_top=26, cab_size=15),
    anchor="bottom", pad=PAD) + indicador(IND, 5, N, C)))
# 7 · checklist dos 4 passos
s.append(slide(C, bloco(
    h(7, "Salva o teste e faz esta semana.", C, size=40, lh=1.05)
    + checklist(7, C, ["Documentos separados", "Datas conferidas", "Papel x rotina comparados", "Equipe ouvida"], gap_top=22)
    + p(7, "Dúvida em mais de um passo? Já vale uma conversa.", C, size=19, gap=20, weight=500, color=DBG),
    anchor="bottom", pad=PAD) + indicador(IND, 6, N, C)))
# 8 · CTA (degradê assinatura)
s.append(slide(CTA, bloco(
    logo_lockup(CTA, size=40, fs=15)
    + h(8, "A A&amp;J faz esse diagnóstico com você e acompanha o que vem depois.", CTA, size=38, lh=1.08, align="center")
    + botao(8, "Chama no direct")
    + p(8, HANDLE, CTA, size=15, role="handle", align="center", gap=18, weight=500),
    align="center")))

LABELS = {1: "Capa", 2: "Passo 1", 3: "Passo 2", 4: "Passo 3", 5: "Passo 4", 6: "Dentro x consultoria", 7: "Checklist", 8: "CTA"}
html = pagina("Sua empresa precisa de consultoria em SST?", "Consultoria em SST",
              "Consultoria em SST: um teste rápido para saber se a sua empresa precisa.", s, LABELS,
              "conteudos/2026-10-30-precisa-de-consultoria-sst")
(BASE / "carousel.html").write_text(html, encoding="utf-8")
print("ok", len(html))
