# -*- coding: utf-8 -*-
"""POST 04 · out/2026 · Outubro Rosa na empresa: além do laço no crachá.
Sorteio: comparacao · cena-do-dia-a-dia · seed 65 · esquerda.
2026-10-20: data temática usa a cor da campanha (rosa domina; verde da A&J só no logo) + texto curto;
capa com foto no slide inteiro e véu vinho; rosa-claro só nos slides 3 e 5; fotos full no miolo
sorteadas: 0 (seed 219932269); selo "arraste" na capa + setinha até o 7.
Nenhum slide só com fundo e texto: meio círculo (2), laço em traço (4), estetoscópio em traço (6)."""
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
    return (f'<div data-ap-fixo style="position:relative;margin-top:34px;">'
            f'<div style="position:absolute;left:4%;right:4%;top:12px;height:2px;background:{t["line"]};"></div>'
            f'<div style="position:relative;display:flex;">{cols}</div></div>')


s = []
# 1 · capa: laço no slide inteiro + véu vinho, título embaixo
s.append(slide(F,
    foto_full(CAPA, rgb=VR_ESC, ate=0.70, pos="30% 50%", nota="pexels.com/photo/8385421")
    + f'<div style="position:absolute;top:22px;left:24px;z-index:3;">'
      f'{logo_lockup(F, size=26, fs=12, align="left", gap_below=0, chip="rgba(94,24,56,0.55)")}</div>'
    + bloco(h(1, f"Em outubro, o laço rosa aparece no crachá. Em novembro, {it('some.', F, color='#fff')}", F,
              size=38, lh=1.08),
            anchor="bottom", pad="64px 34px 66px")
    + indicador(IND, 0, N, F)))
# 2 · comparação em vinho (os cabeçalhos são o título)
s.append(slide(V, bloco(
    comparacao(2, V, "Fachada", "Cuidado", [
        ("Foto de rosa", "Horário livre para o exame"),
        ("Palestra em outubro", "Informação o ano todo"),
    ], size=21, gap_top=0, cab_serif=True, cab_size=40),
    anchor="center") + indicador(IND, 1, N, V),
    layers=circulo(ROSA, 420, 525, 150, op=0.9)))
# 3 · foto dividida: foto à esquerda, texto à direita em rosa-claro · claro 1/2
s.append(slide(RC,
    '<!-- foto: pexels.com/photo/8487402 -->'
    f'<img src="{FOTO3}" alt="" style="position:absolute;left:0;top:0;width:200px;height:525px;object-fit:cover;object-position:50% 25%;">'
    + f'<div style="position:absolute;left:200px;right:0;top:0;bottom:0;z-index:2;display:flex;flex-direction:column;'
      f'justify-content:center;padding:40px 22px 70px 22px;">'
    + h(3, "Exame que depende de favor ao chefe fica para depois.", RC, size=27, lh=1.14)
    + p(3, "Combinar a saída custa pouco.", RC, size=18, gap=18, weight=600, color=VINHO)
    + "</div>" + indicador(IND, 2, N, RC)))
# 4 · pergunta grande em rosa forte
s.append(slide(RF, bloco(
    h(4, "Quem precisa sair para um exame sabe como pedir?", RF, size=50, lh=1.05),
    anchor="center") + indicador(IND, 3, N, RF),
    layers=traco("laco", "#fff", 196, 332, 250, op=0.4, sw=5, rot=-8)))
# 5 · diagrama: linha do ano · claro 2/2
s.append(slide(RC, bloco(
    h(5, "Outubro abre a conversa", RC, size=46, lh=1.04)
    + linha_do_ano(5, RC)
    + p(5, "Os outros onze meses mostram se a empresa levou a sério.", RC, size=22, gap=34, weight=500, color=VINHO,
        extra="font-family:'Lora',serif;line-height:1.3;"),
    anchor="center", pad="64px 30px 76px") + indicador(IND, 4, N, RC)))
# 6 · comparação em vinho escuro
s.append(slide(VE, bloco(
    h(6, "Quando alguém está em tratamento", VE, size=38, lh=1.06)
    + comparacao(6, VE, "Sem cuidado", "Com cuidado", [
        ("Comentário no corredor", "Conversa reservada com o RH"),
        ("Volta sem plano", "Retorno avaliado pela medicina do trabalho (NR&#8209;7)"),
    ], size=19, gap_top=24, cab_size=15),
    anchor="bottom", pad="64px 36px 64px") + indicador(IND, 5, N, VE),
    layers=traco("estetoscopio", ROSA_SUAVE, 292, -26, 150, op=0.85, sw=5, rot=10)))
# 7 · diagrama: do aviso ao exame, em vinho
s.append(slide(V, bloco(
    h(7, "Do aviso ao exame", V, size=46)
    + passos_verticais(7, V, [
        "Informação com fonte (INCA, Ministério da Saúde)",
        "Horário combinado",
        "Exame feito",
    ], seta=True, gap_top=28, size=21)
    + p(7, "Salva e manda pro RH.", V, role="cta", size=19, weight=600, color=ROSA_SUAVE, gap=12),
    anchor="center") + indicador(IND, 6, N, V)))
# 8 · CTA no degradê da campanha
s.append(slide(CR, bloco(
    logo_lockup(CR, size=38, fs=14)
    + h(8, "Saúde da mulher também é saúde do trabalho.", CR, size=40, lh=1.06, align="center")
    + p(8, "A A&amp;J ajuda a montar ações que passam de outubro.", CR, size=19, align="center", gap=16)
    + botao(8, "Chama no direct", bg="#fff", fg=VINHO)
    + p(8, HANDLE, CR, role="handle", size=15, align="center", gap=16, weight=500),
    align="center") + indicador(IND, 7, N, CR)))

LABELS = {1: "Capa", 2: "Fachada x cuidado", 3: "Foto + exame", 4: "Pergunta", 5: "Linha do ano", 6: "Tratamento", 7: "Do aviso ao exame", 8: "CTA"}
html = pagina("Outubro Rosa na empresa", "Saúde e segurança do trabalho",
              "Outubro Rosa na empresa: ações de saúde que continuam depois do laço.", s, LABELS,
              "conteudos/2026-10-28-outubro-rosa-na-empresa")
# moldura da prévia: navegação no rosa da campanha
html = html.replace(f"background:{P}; }}", f"background:{ROSA}; }}").replace(
    f"background:{P}; color:#fff; border-color:{P};", f"background:{ROSA}; color:#fff; border-color:{ROSA};")
(BASE / "carousel.html").write_text(html, encoding="utf-8")
print("ok", len(html))
