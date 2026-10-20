"""Conferidor automático das regras de carrossel (CLAUDE.md da raiz), antes de mostrar ao Thiago.

Uso:
    python conferir_carrossel.py "<cliente>/conteudos/<pasta>"            # um carrossel (pasta ou carousel.html)
    python conferir_carrossel.py "<pasta 1>" "<pasta 2>" ...               # vários
    python conferir_carrossel.py --mes "<cliente>" 2026-10                 # todos do mês + regras do mês
    python conferir_carrossel.py --roteiro "<cliente>/conteudos/roteiros/2026-10.md"
    ... --folha "<pasta temporária>"   # grava os slides renderizados e uma folha com todos (verificação visual)

Dois níveis:
  ACHADO  quebra uma regra escrita; corrigir (avisando o Thiago antes) ou justificar.
  AVISO   vale olhar; pode estar certo.
Não substitui a verificação visual (legibilidade sobre foto, foto que mostra o texto) nem o
detector do Impeccable: pega as regras mensuráveis para elas não chegarem ao Thiago.
Sai com código 1 quando há achado.

Regras conferidas na arte (renderizada no navegador, 420x525 por slide):
  capa em fundo claro · mais de 2 slides de fundo claro · slide só com fundo e texto ·
  faixa vazia maior que 1/3 do slide · título com mais de ~10 palavras · apoio com mais de ~15 ·
  travessão · contador "n/total" · seta no último slide · letra menor que 12px · número em
  destaque sem fonte · mais de 2 fotos full no miolo · títulos repetindo a mesma ideia · erro de JS.
  No --mes: pelo menos 2 capas com foto no slide inteiro.
No roteiro: começo, meio e fim (gancho primeiro, chamada no fim, por que importa antes de como
fazer) · tamanho de título e apoio · travessão · dado sem fonte e dado demais · slide sem recurso
visual · fundo claro demais · ideia repetida.
"""
import argparse
import asyncio
import io
import re
import sys
import unicodedata
from pathlib import Path

W, H = 420, 525
LIMITE_TITULO, LIMITE_APOIO = 10, 15        # "~10" e "~15" do CLAUDE.md
TOLERANCIA = 2                              # até +2 palavras é aviso; acima, achado
MIN_FONTE = 12
VISUAL_MIN, VISUAL_BOM = 0.06, 0.12         # pegada do recurso visual (fração do slide): abaixo de MIN é achado
VAZIO_MAX = 1 / 3
GRANDE = 48                                 # px: texto deste tamanho conta como elemento visual (número gigante)
FUNCOES = ["gancho", "por que importa", "o que muda", "como fazer", "chamada"]
FUNCOES_EXTRAS = ["contexto", "consequência", "virada", "exemplo", "pergunta", "dado"]
PARADAS = set("""a o as os um uma uns umas de do da dos das no na nos nas em por para pra com sem que se
e ou mas é ser foi são tem ter sua seu suas seus isso esta este essa esse não sim mais menos
muito pouco quando como onde qual quem já só também aqui ali lá ao aos à às""".split())


# ---------------------------------------------------------------- utilidades
def palavras(txt: str) -> list:
    return [w for w in re.split(r"\s+", txt.strip()) if re.search(r"[\wÀ-ÿ]", w)]


def sem_acento(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


def ideia(txt: str) -> set:
    return {w for w in re.findall(r"[a-z0-9]+", sem_acento(txt)) if len(w) > 3 and w not in PARADAS}


def parecidos(titulos: dict) -> list:
    """Pares de slides cujos títulos dividem 2+ palavras de conteúdo (metade ou mais), fora as palavras do
    tema, que aparecem em 3+ títulos (como "cipa" num carrossel sobre CIPA)."""
    from collections import Counter
    conta = Counter(w for v in titulos.values() for w in ideia(v))
    tema = {w for w, c in conta.items() if c >= 3}
    pares, itens = [], [(k, ideia(v) - tema) for k, v in titulos.items() if v]
    for i in range(len(itens)):
        for j in range(i + 1, len(itens)):
            (a, A), (b, B) = itens[i], itens[j]
            if len(A & B) >= 2 and len(A & B) / min(len(A), len(B)) >= 0.5:
                pares.append((a, b, sorted(A & B)))
    return pares


TRAVESSAO = re.compile(r"—|(?<!\d)–|–(?!\d)|\s-\s")  # intervalo numérico (2026–2028) passa
CONTADOR = re.compile(r"^\s*\d{1,2}\s*/\s*\d{1,2}\s*$")


class Relatorio:
    def __init__(self, nome):
        self.nome, self.itens = nome, []

    def achado(self, onde, msg):
        self.itens.append(("ACHADO", onde, msg))

    def aviso(self, onde, msg):
        self.itens.append(("AVISO", onde, msg))

    @property
    def n_achados(self):
        return sum(1 for t, _, _ in self.itens if t == "ACHADO")

    def imprimir(self, extra=""):
        n_av = len(self.itens) - self.n_achados
        print(f"\n== {self.nome}  ·  {self.n_achados} achado(s), {n_av} aviso(s){extra}")
        if not self.itens:
            print("   tudo certo nas regras mensuráveis.")
        for tipo, onde, msg in sorted(self.itens, key=lambda x: (x[0] != "ACHADO", str(x[1]))):
            print(f"   {tipo:<6} {onde:<10} {msg}")


# ---------------------------------------------------------------- arte (render)
JS_MEDIR = """(i) => {
  const track = document.querySelector('.ig-track, .carousel-track');
  const s = track.children[i];
  const r0 = s.getBoundingClientRect();
  const textos = [], imgs = [];
  for (const el of s.querySelectorAll('*')) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) === 0) continue;
    const proprio = [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join('').trim();
    if (proprio) textos.push({tag: el.tagName.toLowerCase(), fs: parseFloat(cs.fontSize), proprio,
                              edit: el.closest('[data-edit-id]')?.getAttribute('data-edit-id') || '',
                              fixo: !!el.closest('[data-ap-fixo]')});
    if (el.tagName === 'IMG') {
      const r = el.getBoundingClientRect();
      const x0 = Math.max(r.left, r0.left), y0 = Math.max(r.top, r0.top);
      const x1 = Math.min(r.right, r0.right), y1 = Math.min(r.bottom, r0.bottom);
      imgs.push({area: Math.max(0, x1 - x0) * Math.max(0, y1 - y0) / (r0.width * r0.height)});
    }
  }
  const blocos = [...s.querySelectorAll('[data-edit-id], h1, h2, h3, p')]
    .filter(el => !el.parentElement.closest('[data-edit-id], h1, h2, h3, p'))
    .map(el => ({tag: el.tagName.toLowerCase(), edit: el.getAttribute('data-edit-id') || '',
                 txt: el.innerText.replace(/\\s+/g, ' ').trim()}));
  return {textos, imgs, blocos, todo: s.innerText};
}"""

JS_ESCONDER_TEXTO = r"""(i) => {
  const s = document.querySelector('.ig-track, .carousel-track').children[i];
  const r0 = s.getBoundingClientRect();
  const some = el => el.style.setProperty('visibility', 'hidden', 'important');
  // indicador de arraste e logo não contam como recurso visual
  for (const el of s.querySelectorAll('[data-ap-fixo]'))
    if (/→|arraste|^\s*\d+\s*\/\s*\d+\s*$/i.test(el.innerText.trim())) some(el);
  for (const im of s.querySelectorAll('img')) {
    const r = im.getBoundingClientRect();
    if (r.width * r.height < 0.03 * r0.width * r0.height) some(im.closest('[data-ap-fixo]') || im);
  }
  // texto comum some; fica o texto gigante (número, sinal) e o de desenhos fixos (calendário, linha do ano)
  for (const el of s.querySelectorAll('*')) {
    const proprio = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (proprio && !el.closest('[data-ap-fixo]') && parseFloat(getComputedStyle(el).fontSize) < %d) {
      el.style.setProperty('color', 'transparent', 'important');
      el.style.setProperty('text-shadow', 'none', 'important');
    }
  }
}""" % GRANDE


def pegada(ocupado, cel=17):
    """Fração de células (~35px no slide) tocadas por recurso visual: desenho em traço fino conta pela área que cobre."""
    import numpy as np
    h, w = ocupado.shape
    hh, ww = h // cel * cel, w // cel * cel
    blocos = ocupado[:hh, :ww].reshape(hh // cel, cel, ww // cel, cel).sum(axis=(1, 3))
    return float((blocos >= 3).mean())


def analisar_pixels(png_bytes):
    """Cor de fundo dominante, se é clara, quanto do slide não é fundo e a maior faixa vazia."""
    import numpy as np
    from PIL import Image
    im = np.asarray(Image.open(io.BytesIO(png_bytes)).convert("RGB").resize((W // 2, H // 2)), dtype=np.int16)
    q = (im >> 4).reshape(-1, 3)
    chaves = q[:, 0] * 256 + q[:, 1] * 16 + q[:, 2]
    moda = np.bincount(chaves).argmax()
    fundo = im.reshape(-1, 3)[chaves == moda].mean(axis=0)
    dif = np.abs(im - fundo).max(axis=2) > 12
    rgb = fundo / 255
    lin = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    lum = 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]
    return {"fundo_frac": float((chaves == moda).mean()), "lum": float(lum), "ocupado": dif}


def maior_faixa(mascara_linhas):
    melhor = atual = 0
    for vazio in mascara_linhas:
        atual = atual + 1 if vazio else 0
        melhor = max(melhor, atual)
    return melhor / len(mascara_linhas)


async def renderizar(html_path: Path, folha: Path | None):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        erros = []
        page.on("pageerror", lambda e: erros.append(str(e)))
        await page.set_content(html_path.read_text(encoding="utf-8"), wait_until="networkidle")
        await page.wait_for_timeout(1500)
        legenda = await page.evaluate("() => document.querySelector('.ig-caption')?.innerText || ''")
        await page.evaluate("""() => {
            const vp = document.querySelector('.ig-viewport, .carousel-viewport');
            document.body.innerHTML = ''; document.body.appendChild(vp);
            document.body.style.cssText = 'padding:0;margin:0;display:block;overflow:hidden;background:#000;';
            vp.style.cssText = 'position:relative;width:420px;height:525px;overflow:hidden;background:#000;';
            document.querySelector('.ig-track, .carousel-track').style.transition = 'none';
        }""")
        n = await page.evaluate("() => document.querySelector('.ig-track, .carousel-track').children.length")
        slides = []
        for i in range(n):
            await page.evaluate("(i) => { document.querySelector('.ig-track, .carousel-track').style.transform = 'translateX(' + (-i*420) + 'px)'; }", i)
            await page.wait_for_timeout(120)
            dom = await page.evaluate(JS_MEDIR, i)
            com_texto = await page.screenshot(clip={"x": 0, "y": 0, "width": W, "height": H})
            slides.append({"dom": dom, "png": com_texto})
        for i in range(n):  # segunda passada, sem o texto pequeno: o que sobra é fundo + recursos visuais
            await page.evaluate("(i) => { document.querySelector('.ig-track, .carousel-track').style.transform = 'translateX(' + (-i*420) + 'px)'; }", i)
            await page.evaluate(JS_ESCONDER_TEXTO, i)
            await page.wait_for_timeout(80)
            slides[i]["png_sem_texto"] = await page.screenshot(clip={"x": 0, "y": 0, "width": W, "height": H})
        await b.close()
    if folha:
        salvar_folha(folha / html_path.parent.name, [s["png"] for s in slides])
    return slides, legenda, erros


def salvar_folha(destino: Path, pngs):
    from PIL import Image
    destino.mkdir(parents=True, exist_ok=True)
    ims = []
    for k, b in enumerate(pngs, 1):
        (destino / f"slide_{k}.png").write_bytes(b)
        ims.append(Image.open(io.BytesIO(b)).convert("RGB"))
    cols = 4
    sheet = Image.new("RGB", (cols * (W + 10) + 10, ((len(ims) + cols - 1) // cols) * (H + 10) + 10), "white")
    for k, im in enumerate(ims):
        sheet.paste(im, (10 + (k % cols) * (W + 10), 10 + (k // cols) * (H + 10)))
    sheet.save(destino / "folha.png")


def papel(bloco):
    """headline / body / outro, pelo data-edit-id (slideN-papel) ou pela tag."""
    m = re.match(r"slide\d+-(.+)", bloco["edit"])
    r = m.group(1) if m else ""
    if bloco["tag"] in ("h1", "h2", "h3") or re.match(r"(headline|title|titulo|question)", r):
        return "titulo"
    if bloco["tag"] == "p" and not re.match(r"(handle|cta|fonte|source|tag)", r):
        return "apoio"
    return "outro"


def conferir_arte(html_path: Path, folha: Path | None):
    rel = Relatorio(html_path.parent.name)
    slides, legenda, erros = asyncio.run(renderizar(html_path, folha))
    n = len(slides)
    for e in erros:
        rel.achado("página", f"erro de JS: {e[:90]}")
    claros, fotos_full_miolo, titulos = [], [], {}
    info = {"capa_foto_full": False}
    for i, s in enumerate(slides, 1):
        onde, dom = f"slide {i}", s["dom"]
        px = analisar_pixels(s["png"])
        px_sem = analisar_pixels(s["png_sem_texto"])
        foto_full = any(im["area"] >= 0.85 for im in dom["imgs"])
        foto_algum = any(im["area"] >= 0.03 for im in dom["imgs"])
        if i == 1:
            info["capa_foto_full"] = foto_full
        claro = not foto_full and px_sem["fundo_frac"] >= 0.35 and px_sem["lum"] >= 0.6
        if claro:
            claros.append(i)
            if i == 1:
                rel.achado(onde, "capa em fundo claro (capa nunca branca/creme)")
        if foto_full and 1 < i < n:
            fotos_full_miolo.append(i)
        visual = pegada(px_sem["ocupado"])
        if not foto_algum and visual < VISUAL_MIN:
            rel.achado(onde, f"só fundo e texto (recurso visual cobre {visual:.0%}); falta traço, forma ou recorte")
        elif not foto_algum and visual < VISUAL_BOM:
            rel.aviso(onde, f"recurso visual pequeno (cobre {visual:.0%} do slide)")
        if not foto_full:
            linhas_vazias = px["ocupado"].mean(axis=1) < 0.01
            cols_vazias = px["ocupado"].mean(axis=0) < 0.01
            faixa = max(maior_faixa(linhas_vazias), maior_faixa(cols_vazias))
            if faixa > VAZIO_MAX:
                rel.achado(onde, f"faixa vazia de {faixa:.0%} do slide (máximo 1/3)")
        # texto
        for b in dom["blocos"]:
            pw, tipo = len(palavras(b["txt"])), papel(b)
            lim = {"titulo": LIMITE_TITULO, "apoio": LIMITE_APOIO}.get(tipo)
            if lim and pw > lim + TOLERANCIA:
                rel.achado(onde, f"{tipo} com {pw} palavras (até ~{lim}): \"{b['txt'][:60]}\"")
            elif lim and pw > lim:
                rel.aviso(onde, f"{tipo} com {pw} palavras (até ~{lim}): \"{b['txt'][:60]}\"")
            if tipo == "titulo":
                titulos[i] = (titulos.get(i, "") + " " + b["txt"]).strip()
        total = sum(len(palavras(t["proprio"])) for t in dom["textos"] if not t["fixo"])  # sem calendário, logo e selo
        if total > 45:
            rel.aviso(onde, f"{total} palavras no slide; parece texto demais")
        if TRAVESSAO.search(dom["todo"]):
            rel.achado(onde, "travessão ou traço entre palavras (usar ponto e vírgula)")
        pequenas = []
        for t in dom["textos"]:
            if CONTADOR.match(t["proprio"]):
                rel.achado(onde, f"contador \"{t['proprio']}\" (saiu do padrão)")
            elif t["fs"] < MIN_FONTE and not t["fixo"]:
                pequenas.append(t)
        if pequenas:
            menor = min(pequenas, key=lambda t: t["fs"])
            mais = f" e mais {len(pequenas) - 1}" if len(pequenas) > 1 else ""
            rel.achado(onde, f"letra de {menor['fs']:.0f}px (mínimo {MIN_FONTE}): \"{menor['proprio'][:40]}\"{mais}")
        if i == n and any(t["fixo"] and ("→" in t["proprio"] or "ARRASTE" in t["proprio"].upper()) for t in dom["textos"]):
            rel.achado(onde, "seta ou selo de arraste no último slide")
        grandes = [t["proprio"] for t in dom["textos"] if t["fs"] >= 48 and re.search(r"\d{2,}|%", t["proprio"])]
        if grandes and "fonte" not in sem_acento(dom["todo"]):
            rel.achado(onde, f"número em destaque sem fonte no slide: \"{grandes[0][:30]}\"")
    if len(claros) > 2:
        rel.achado("carrossel", f"{len(claros)} slides de fundo claro (máximo 2): {claros}")
    if len(fotos_full_miolo) > 2:
        rel.achado("carrossel", f"{len(fotos_full_miolo)} fotos full no miolo (máximo 2): {fotos_full_miolo}")
    for a, b, comum in parecidos(titulos):
        rel.aviso(f"slides {a}/{b}", f"títulos com a mesma ideia? ({', '.join(comum)})")
    if TRAVESSAO.search(legenda):
        rel.achado("legenda", "travessão ou traço entre palavras")
    info.update(n=n, claros=claros, fotos_full_miolo=fotos_full_miolo)
    return rel, info


# ---------------------------------------------------------------- roteiro (markdown)
def ler_roteiro(path: Path):
    """Cada post: '## POST NN · tema', linha 'Arco: ...' e a tabela | # | Função | Título | Apoio | Dado e fonte | Visual |."""
    posts, atual = [], None
    for linha in path.read_text(encoding="utf-8").splitlines():
        if linha.startswith("## "):
            atual = {"nome": linha[3:].strip(), "arco": "", "slides": []}
            posts.append(atual)
        elif atual and linha.lower().startswith("arco:"):
            atual["arco"] = linha.split(":", 1)[1].strip()
        elif atual and linha.startswith("|"):
            cel = [c.strip() for c in linha.strip().strip("|").split("|")]
            if len(cel) >= 6 and re.match(r"^\d+$", cel[0]):
                atual["slides"].append(dict(zip(["n", "funcao", "titulo", "apoio", "dado", "visual"], cel[:6])))
    return posts


def conferir_roteiro(path: Path):
    rels = []
    for post in ler_roteiro(path):
        rel, sl = Relatorio(post["nome"]), post["slides"]
        rels.append(rel)
        if not sl:
            rel.achado("roteiro", "sem tabela de slides")
            continue
        if not post["arco"]:
            rel.achado("roteiro", "falta a linha 'Arco:' (de onde a história parte e aonde chega)")
        funcs = [sem_acento(s["funcao"]) for s in sl]
        conhecidas = {sem_acento(f) for f in FUNCOES + FUNCOES_EXTRAS}
        for s, f in zip(sl, funcs):
            if f not in conhecidas:
                rel.aviso(f"slide {s['n']}", f"função '{s['funcao']}' fora da lista ({', '.join(FUNCOES + FUNCOES_EXTRAS)})")
        if funcs[0] != "gancho":
            rel.achado("história", "o primeiro slide não é o gancho")
        if funcs[-1] != "chamada":
            rel.achado("história", "o último slide não é a chamada")
        for f in FUNCOES[1:4]:
            if sem_acento(f) not in funcs:
                rel.achado("história", f"falta um slide de '{f}' (gancho → por que importa → o que muda → como fazer → chamada)")
        if "por que importa" in funcs and "como fazer" in funcs and funcs.index("por que importa") > funcs.index("como fazer"):
            rel.achado("história", "'por que importa' vem depois de 'como fazer'")
        dados, claros = 0, []
        titulos = {}
        for s in sl:
            onde = f"slide {s['n']}"
            for campo, lim in (("titulo", LIMITE_TITULO), ("apoio", LIMITE_APOIO)):
                pw = len(palavras(s[campo]))
                if pw > lim + TOLERANCIA:
                    rel.achado(onde, f"{campo} com {pw} palavras (até ~{lim})")
                elif pw > lim:
                    rel.aviso(onde, f"{campo} com {pw} palavras (até ~{lim})")
            if TRAVESSAO.search(" ".join([s["titulo"], s["apoio"], s["dado"]])):
                rel.achado(onde, "travessão ou traço entre palavras")
            if s["dado"] and s["dado"] not in ("-", "·"):
                dados += 1
                if "fonte" not in sem_acento(s["dado"]):
                    rel.achado(onde, "dado sem 'Fonte:' (nunca inventar; fonte oficial no slide e na legenda)")
            if not s["visual"] or s["visual"] in ("-", "·"):
                rel.achado(onde, "sem recurso visual (traço, forma, recorte ou foto)")
            if re.search(r"\b(creme|branco|claro)\b", sem_acento(s["visual"])):
                claros.append(s["n"])
                if s["n"] == "1":
                    rel.achado(onde, "capa em fundo claro")
            titulos[s["n"]] = s["titulo"]
        if dados > 2:
            rel.aviso("roteiro", f"{dados} dados no carrossel (moderação: cerca de 1)")
        if len(claros) > 2:
            rel.achado("roteiro", f"{len(claros)} slides de fundo claro (máximo 2): {claros}")
        for a, b, comum in parecidos(titulos):
            rel.aviso(f"slides {a}/{b}", f"títulos com a mesma ideia? ({', '.join(comum)})")
    return rels


# ---------------------------------------------------------------- main
def achar_html(alvo: Path) -> Path:
    return alvo / "carousel.html" if alvo.is_dir() else alvo


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("alvos", nargs="*", help="pastas de carrossel ou carousel.html")
    ap.add_argument("--mes", nargs=2, metavar=("CLIENTE", "AAAA-MM"))
    ap.add_argument("--roteiro", type=Path)
    ap.add_argument("--folha", type=Path, help="pasta para gravar os slides renderizados e a folha")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    if a.roteiro:
        rels = conferir_roteiro(a.roteiro)
        for r in rels:
            r.imprimir()
        sys.exit(1 if any(r.n_achados for r in rels) else 0)

    alvos = [achar_html(Path(x)) for x in a.alvos]
    if a.mes:
        alvos += sorted(Path(a.mes[0], "conteudos").glob(f"{a.mes[1]}-*/carousel.html"))
    if not alvos:
        ap.error("informe uma pasta de carrossel, --mes ou --roteiro")
    total, capas_foto = 0, 0
    for h in alvos:
        if not h.exists():
            print(f"\n== {h}: não encontrado")
            total += 1
            continue
        rel, info = conferir_arte(h, a.folha)
        rel.imprimir(f"  ·  {info['n']} slides, claros {info['claros'] or 'nenhum'}")
        total += rel.n_achados
        capas_foto += info["capa_foto_full"]
    if a.mes:
        print(f"\n== mês {a.mes[1]}  ·  {capas_foto} capa(s) com foto no slide inteiro")
        if capas_foto < 2 and len(alvos) >= 2:
            print("   ACHADO mês        menos de 2 capas com foto full e véu no mês")
            total += 1
    if a.folha:
        print(f"\nSlides renderizados em {a.folha}")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
