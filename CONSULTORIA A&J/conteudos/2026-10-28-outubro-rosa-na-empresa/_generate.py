# -*- coding: utf-8 -*-
"""POST 04 · out/2026 · Outubro Rosa na empresa: além do laço no crachá.
Sorteio: comparacao · cena-do-dia-a-dia · seed 65 · fundos em blocos · esquerda · texto varia · barra segmentada.
Revisão de 2026-10-20: data temática usa a cor da campanha (rosa domina; verde da A&J só no logo) + texto curto."""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent))
from _carrossel_base import *  # noqa: E402,F403

RC, V, CR = tom("rosa"), tom("vinho"), tom("cta_rosa")
IND, N = "selo", 8  # 2026-10-20: sem contador nem barra; selo "arraste" só na capa (pedido do Thiago)
ED = BASE / "assets" / "edited"
FOTO1, FOTO3 = foto(ED / "slide1-photo.jpg"), foto(ED / "slide3-photo.jpg")
VR = "140,36,83"  # VINHO em rgb


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
# 1 · capa: foto emoldurada com o título encostado
s.append(slide(RC, bloco(
    logo_lockup(RC, align="left", gap_below=16)
    + '<!-- foto: pexels.com/photo/8385421 -->'
    f'<div style="border-radius:12px;overflow:hidden;"><img src="{FOTO1}" alt="" style="display:block;width:100%;height:186px;'
    'object-fit:cover;object-position:40% 50%;"></div>'
    + h(1, f"Em outubro, o laço rosa aparece no crachá. Em novembro, {it('some.', RC)}", RC, size=34, lh=1.08,
        extra="margin-top:20px;"),
    anchor="top", pad="42px 34px 60px") + indicador(IND, 0, N, RC)))
# 2 · comparação (os cabeçalhos são o título)
s.append(slide(RC, bloco(
    comparacao(2, RC, "Fachada", "Cuidado", [
        ("Foto de rosa", "Horário livre para o exame"),
        ("Palestra em outubro", "Informação o ano todo"),
    ], size=21, gap_top=0, cab_serif=True, cab_size=40),
    anchor="center") + indicador(IND, 1, N, RC)))
# 3 · foto dividida: foto à esquerda, texto à direita
s.append(slide(V,
    '<!-- foto: pexels.com/photo/8487402 -->'
    f'<img src="{FOTO3}" alt="" style="position:absolute;left:0;top:0;width:200px;height:525px;object-fit:cover;object-position:50% 25%;">'
    f'<div style="position:absolute;left:0;bottom:0;width:200px;height:64px;z-index:1;'
    f'background:linear-gradient(0deg,rgba({VR},0.85) 0%,rgba({VR},0.55) 55%,rgba({VR},0) 100%);"></div>'
    + f'<div style="position:absolute;left:200px;right:0;top:0;bottom:0;z-index:2;display:flex;flex-direction:column;'
      f'justify-content:center;padding:40px 22px 70px 22px;">'
    + h(3, "Exame que depende de favor ao chefe fica para depois.", V, size=27, lh=1.14)
    + p(3, "Combinar a saída custa pouco.", V, size=18, gap=18, weight=500, color=ROSA_SUAVE)
    + "</div>" + indicador(IND, 2, N, V)))
# 4 · pergunta grande
s.append(slide(V, bloco(
    h(4, "Quem precisa sair para um exame sabe como pedir?", V, size=50, lh=1.05),
    anchor="center") + indicador(IND, 3, N, V)))
# 5 · diagrama: linha do ano
s.append(slide(RC, bloco(
    h(5, "Outubro abre a conversa", RC, size=46, lh=1.04)
    + linha_do_ano(5, RC)
    + p(5, "Os outros onze meses mostram se a empresa levou a sério.", RC, size=22, gap=34, weight=500, color=VINHO,
        extra="font-family:'Lora',serif;line-height:1.3;"),
    anchor="center", pad="64px 30px 76px") + indicador(IND, 4, N, RC)))
# 6 · comparação
s.append(slide(RC, bloco(
    h(6, "Quando alguém está em tratamento", RC, size=38, lh=1.06)
    + comparacao(6, RC, "Sem cuidado", "Com cuidado", [
        ("Comentário no corredor", "Conversa reservada com o RH"),
        ("Volta sem plano", "Retorno avaliado pela medicina do trabalho (NR&#8209;7)"),
    ], size=19, gap_top=24, cab_size=15),
    anchor="center") + indicador(IND, 5, N, RC)))
# 7 · diagrama: do aviso ao exame
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
