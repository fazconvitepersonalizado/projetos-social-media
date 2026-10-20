# -*- coding: utf-8 -*-
"""POST 04 · out/2026 · Outubro Rosa: o lembrete que vale pra ela também.
2026-10-20 (2): conteúdo refeito a pedido do Thiago (o anterior soava como manual de RH); layout mantido.
Sorteio: comparacao · cena-do-dia-a-dia · seed 65 · esquerda.
2026-10-20: data temática usa a cor da campanha (rosa domina; verde da A&J só no logo) + texto curto;
capa com foto no slide inteiro e véu vinho; rosa-claro só nos slides 3 e 5; fotos full no miolo
sorteadas: 0 (seed 219932269); selo "arraste" na capa + setinha até o 7.
História: capa (ela lembra a equipe), mês do lembrete (INCA), segurança x saúde, rotina dela, pergunta, três passos, SUS, chamada.
Nenhum slide só com fundo e texto: linha do ano (2), meio círculo (3), laço em traço (5), calendário em traço (6),
estetoscópio em traço (7)."""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent))
from _carrossel_base import *  # noqa: E402,F403

RC, V, VE, RF, CR, F = tom("rosa"), tom("vinho"), tom("vinho_escuro"), tom("rosa_forte"), tom("cta_rosa"), tom("foto")
IND, N = "selo", 8
ED = BASE / "assets" / "edited"
CAPA, FOTO3 = foto(ED / "slide1-full.jpg"), foto(ED / "slide3-photo.jpg")
VR_ESC = "94,24,56"  # vinho escuro em rgb, para o véu da capa


def linha_do_ano(n, t):
    meses = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
    cols = ""
    for m in meses:
        out = m == "out"
        d = 26 if out else 10
        borda = "box-shadow:0 0 0 7px rgba(229,103,154,0.22);" if out else "border:1.5px solid " + t["line"] + ";"
        cols += (f'<div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:12px;">'
                 f'<div style="height:26px;display:flex;align-items:center;"><span style="display:block;width:{d}px;height:{d}px;'
                 f'border-radius:50%;background:{ROSA if out else "#fff"};{borda}"></span></div>'
                 f'<span class="sans" style="font-size:{16 if out else 13}px;font-weight:{700 if out else 500};'
                 f'color:{VINHO if out else t["mute"]};">{m.upper() if out else m}</span></div>')
    return (f'<div data-ap-fixo style="position:relative;margin-top:22px;">'
            f'<div style="position:absolute;left:4%;right:4%;top:12px;height:2px;background:{t["line"]};"></div>'
            f'<div style="position:relative;display:flex;">{cols}</div></div>')


s = []
# 1 · capa: laço no slide inteiro + véu vinho, título embaixo
s.append(slide(F,
    foto_full(CAPA, rgb=VR_ESC, ate=0.70, pos="30% 50%", nota="pexels.com/photo/8385421")
    + f'<div style="position:absolute;top:22px;left:24px;z-index:3;">'
      f'{logo_lockup(F, size=26, fs=12, align="left", gap_below=0, chip="rgba(94,24,56,0.55)")}</div>'
    + bloco(h(1, "Ela lembra a equipe do protetor auricular todo dia.", F, size=36, lh=1.08)
            + p(1, f"Em outubro, o lembrete é {it('pra ela.', F, color='#fff')}", F, role="sub", size=21, gap=16,
                weight=500, color="#fff"),
            anchor="bottom", pad="64px 34px 66px")
    + indicador(IND, 0, N, F)))
# 2 · por que importa: o mês do lembrete + linha do ano · claro 1/2
s.append(slide(RC, bloco(
    h(2, "Outubro é o mês do lembrete.", RC, size=42, lh=1.04)
    + linha_do_ano(2, RC)
    + p(2, "O câncer de mama é o mais comum entre as brasileiras. O exame é simples.", RC, size=21, gap=26,
        weight=500, color=VINHO, extra="font-family:'Lora',serif;line-height:1.3;")
    + p(2, "Fonte: INCA", RC, role="fonte", size=13, gap=12, weight=500),
    anchor="center", pad="40px 30px 56px") + indicador(IND, 1, N, RC)))
# 3 · o que muda: segurança x saúde, em vinho (os cabeçalhos são o título)
s.append(slide(V, bloco(
    comparacao(3, V, "Na segurança", "Na saúde", [
        ("Inspeção do andaime", "Mamografia de rotina"),
        ("Antes de dar problema", "Antes de sentir qualquer coisa"),
    ], size=21, gap_top=0, cab_serif=True, cab_size=38),
    anchor="center") + indicador(IND, 2, N, V),
    layers=circulo(ROSA, 420, 525, 150, op=0.9)))
# 4 · a rotina dela: foto à esquerda, texto à direita em rosa-claro · claro 2/2
s.append(slide(RC,
    '<!-- foto: pexels.com/photo/8487402 -->'
    f'<img src="{FOTO3}" alt="" style="position:absolute;left:0;top:0;width:200px;height:525px;object-fit:cover;object-position:50% 25%;">'
    + f'<div style="position:absolute;left:200px;right:0;top:0;bottom:0;z-index:2;display:flex;flex-direction:column;'
      f'justify-content:center;padding:40px 22px 70px 22px;">'
    + h(4, "Cuidar da equipe já é rotina dela.", RC, size=29, lh=1.12)
    + p(4, "Marcar o próprio exame cabe na mesma agenda.", RC, size=18, gap=18, weight=600, color=VINHO)
    + "</div>" + indicador(IND, 3, N, RC, foto_no_canto=True)))
# 5 · a pergunta, em rosa forte
s.append(slide(RF, bloco(
    h(5, "E a sua, já está marcada?", RF, size=56, lh=1.04),
    anchor="center") + indicador(IND, 4, N, RF),
    layers=traco("laco", "#fff", 196, 332, 250, op=0.4, sw=5, rot=-8)))
# 6 · como fazer: três passos, em vinho
s.append(slide(V, bloco(
    h(6, "Três passos, uma manhã", V, size=40)
    + passos_verticais(6, V, [
        "Vá ao posto de saúde mais perto",
        "Peça a mamografia pelo SUS",
        "Anote a data da próxima",
    ], seta=True, gap_top=24, size=20)
    + p(6, "Manda pra uma mulher que você quer bem.", V, role="cta", size=18, weight=600, color=ROSA_SUAVE, gap=14),
    anchor="center", pad="64px 118px 76px 32px") + indicador(IND, 5, N, V),
    layers=traco("calendario", ROSA_SUAVE, 300, 150, 230, op=0.8, sw=5, rot=-8)))
# 7 · mamografia pelo SUS (Ministério da Saúde, set/2025), em vinho escuro
s.append(slide(VE, bloco(
    h(7, "Mamografia pelo SUS", VE, size=42, lh=1.06)
    + comparacao(7, VE, "Idade", "Exame", [
        ("50 a 74 anos", "A cada 2 anos"),
        ("40 a 49 anos", "Conversar com o profissional do posto"),
    ], size=19, gap_top=24, cab_size=15)
    + p(7, "Fonte: Ministério da Saúde, 2025", VE, role="fonte", size=13, gap=14, weight=500),
    anchor="bottom", pad="64px 36px 64px") + indicador(IND, 6, N, VE),
    layers=traco("estetoscopio", ROSA_SUAVE, 292, -26, 150, op=0.85, sw=5, rot=10)))
# 8 · CTA no degradê da campanha
s.append(slide(CR, bloco(
    logo_lockup(CR, size=38, fs=14)
    + h(8, "A A&amp;J cuida de quem trabalha, o ano todo.", CR, size=38, lh=1.06, align="center")
    + p(8, "Em outubro, com um laço rosa no capacete.", CR, size=19, align="center", gap=16)
    + botao(8, "Manda pra ela", bg="#fff", fg=VINHO)
    + p(8, HANDLE, CR, role="handle", size=15, align="center", gap=16, weight=500),
    align="center") + indicador(IND, 7, N, CR)))

LABELS = {1: "Capa", 2: "Mês do lembrete", 3: "Segurança x saúde", 4: "Foto + rotina", 5: "Pergunta", 6: "Três passos", 7: "SUS", 8: "CTA"}
html = pagina("Outubro Rosa: o lembrete que vale pra ela", "Saúde e segurança do trabalho",
              "Outubro Rosa: o lembrete que vale pra ela também.", s, LABELS,
              "conteudos/2026-10-28-outubro-rosa-na-empresa")
# moldura da prévia: navegação no rosa da campanha
html = html.replace(f"background:{P}; }}", f"background:{ROSA}; }}").replace(
    f"background:{P}; color:#fff; border-color:{P};", f"background:{ROSA}; color:#fff; border-color:{ROSA};")
(BASE / "carousel.html").write_text(html, encoding="utf-8")
print("ok", len(html))
