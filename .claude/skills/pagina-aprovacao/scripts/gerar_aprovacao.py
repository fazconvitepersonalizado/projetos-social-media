#!/usr/bin/env python3
"""
Gera a página de aprovação de posts de uma cliente para um mês.

Uso (na raiz do projeto):
    python .claude/skills/pagina-aprovacao/scripts/gerar_aprovacao.py "<pasta do cliente>" <AAAA-MM>
        [--posts pasta1 pasta2 ...]      # pastas de conteudos/ (padrão: conteudos/<AAAA-MM>-*)
        [--arquivo pasta=outro.html]     # usar outro HTML naquela pasta (padrão: carousel.html)
        [--saida <pasta>]                # padrão: <cliente>/aprovacao/<AAAA-MM>/

Lê, nesta ordem: o plano do mês (<cliente>/conteudos/planos/<AAAA-MM>.md, se
existir: número, legenda e pasta da arte de cada post) e as pastas de
carrossel. De cada carousel.html tira o painel de edição e os scripts, marca
os textos editáveis (assets/campos.js), lê a legenda e faz a miniatura da capa.

Saída:
    aprovacao.html           página completa, para mandar como arquivo
    aprovacao-artifact.html  mesma página sem <html>/<head>, para publicar no claude.ai
    manifesto.json           posts, arquivos de origem e campos (usado por aplicar_respostas.py)
"""
import argparse
import base64
import json
import re
import sys
from datetime import date
from pathlib import Path

from playwright.sync_api import sync_playwright

SKILL = Path(__file__).resolve().parents[1]
CAMPOS_JS = (SKILL / "assets" / "campos.js").read_text(encoding="utf-8")
TEMPLATE = (SKILL / "assets" / "pagina.html").read_text(encoding="utf-8")
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]

# CSS injetado no documento de cada post: mostra só a área dos slides.
INJETAR = """
html,body{margin:0!important;padding:0!important;background:transparent!important;
  overflow:hidden!important;display:block!important;min-height:0!important;height:auto!important}
.ig-frame{max-width:none!important;margin:0!important;padding:0!important;border:0!important;
  border-radius:0!important;box-shadow:none!important}
.ig-header,.ig-dots,.ig-actions,.ig-caption,#carousel-editor{display:none!important}
.ig-viewport,.carousel-viewport{overflow:hidden!important;border-radius:0!important;margin:0!important}
"""

EXTRAIR = """
() => {
  const frame = document.querySelector('.ig-frame');
  if (!frame) return {erro: 'não achei .ig-frame'};
  const track = APCampos.trilho(frame);
  if (!track) return {erro: 'não achei .ig-track nem .carousel-track'};
  document.querySelectorAll('#carousel-editor, #carousel-editor-script').forEach(e => e.remove());
  const cs = APCampos.campos(document);
  const campos = cs.map(c => ({id: c.id, slide: c.slide, papel: c.papel, texto: APCampos.ler(c.el)}));
  let legenda = '';
  const cap = frame.querySelector('.ig-caption p');
  if (cap) {
    const cl = cap.cloneNode(true);
    const h = cl.querySelector('strong'); if (h && /^@/.test(h.textContent.trim())) h.remove();
    cl.querySelectorAll('br').forEach(b => b.replaceWith('\\n'));
    legenda = cl.textContent.replace(/[ \\t]+/g, ' ').split('\\n').map(l => l.trim()).join('\\n').trim();
  }
  const head = document.head.cloneNode(true);
  head.querySelectorAll('script').forEach(s => s.remove());
  const fc = frame.cloneNode(true);
  fc.querySelectorAll('script').forEach(s => s.remove());
  const slides = APCampos.slides(document);
  const vp = frame.querySelector('.ig-viewport, .carousel-viewport') || track.parentElement;
  vp.setAttribute('data-ap-vp', '1');
  const r = vp.getBoundingClientRect();
  return {head: head.innerHTML, frame: fc.outerHTML, campos, legenda, n: slides.length,
          w: Math.round(frame.getBoundingClientRect().width), h: Math.round(r.height),
          passo: slides.length ? slides[0].getBoundingClientRect().width : r.width};
}
"""


# ---------------------------------------------------------------- cores
def hx(h):
    h = h.strip().lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

def css(c):
    return "#" + "".join(f"{round(max(0, min(1, v)) * 255):02x}" for v in c)

def mix(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))

def lum(c):
    f = lambda v: v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (f(v) for v in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contraste(a, b):
    x, y = sorted((lum(a), lum(b)), reverse=True)
    return (x + 0.05) / (y + 0.05)

def ate(c, fundo, minimo, rumo):
    for _ in range(40):
        if contraste(c, fundo) >= minimo:
            break
        c = mix(c, rumo, 0.06)
    return c

BRANCO, PRETO = (1, 1, 1), (0, 0, 0)

def tokens(derived):
    p = hx(derived.get("BRAND_PRIMARY", "#4A5560"))
    dk = hx(derived.get("BRAND_DARK") or derived.get("BRAND_PRIMARY", "#2F3740"))
    bg = hx(derived.get("LIGHT_BG", "#F3F0EA"))
    bd = hx(derived.get("LIGHT_BORDER", "#DDD6CA"))
    tx = hx(derived.get("DARK_BG", "#22272D"))

    # claro
    sup = mix(bg, BRANCO, 0.55)
    ink = ate(tx, bg, 10, PRETO)
    acc = p if contraste(p, sup) >= 4.5 else dk
    acc = ate(acc, sup, 4.5, PRETO)
    on = BRANCO if contraste(acc, BRANCO) >= contraste(acc, ink) else ink
    claro = {
        "bg": css(bg), "surface": css(sup), "ink": css(ink), "muted": css(mix(ink, bg, 0.42)),
        "line": css(bd), "line-strong": css(mix(bd, ink, 0.2)), "accent": css(acc),
        "accent-deep": css(mix(acc, PRETO, 0.15)), "on-accent": css(on),
        "accent-soft": css(mix(acc, sup, 0.88)), "accent-line": css(mix(acc, sup, 0.6)),
        "track": css(mix(bg, bd, 0.55)), "hover": css(mix(sup, ink, 0.045)), "chip": "#ffffff",
        "field": css(mix(sup, BRANCO, 0.6)), "stage": css(mix(bg, bd, 0.7)),
        "dot": css(mix(bd, ink, 0.25)), "scrim": "rgba(15,15,15,.48)",
        "ok": "#2E7D4F", "on-ok": "#ffffff", "warn": "#E0A83A", "on-warn": "#2A1D05", "warn-ink": "#93600E",
    }
    # escuro (mesma marca, fundo escuro)
    bgd = mix(tx, PRETO, 0.35)
    supd = mix(tx, PRETO, 0.12)
    inkd = mix(bg, BRANCO, 0.3)
    accd = ate(p, supd, 4.5, BRANCO)
    ond = PRETO if contraste(accd, PRETO) >= contraste(accd, BRANCO) else BRANCO
    escuro = {
        "bg": css(bgd), "surface": css(supd), "ink": css(inkd), "muted": css(mix(inkd, bgd, 0.4)),
        "line": css(mix(supd, inkd, 0.14)), "line-strong": css(mix(supd, inkd, 0.26)), "accent": css(accd),
        "accent-deep": css(mix(accd, BRANCO, 0.12)), "on-accent": css(mix(ond, supd, 0.1)),
        "accent-soft": css(mix(accd, supd, 0.82)), "accent-line": css(mix(accd, supd, 0.5)),
        "track": css(mix(supd, inkd, 0.08)), "hover": css(mix(supd, inkd, 0.06)), "chip": css(mix(bg, BRANCO, 0.5)),
        "field": css(mix(supd, PRETO, 0.25)), "stage": css(mix(bgd, PRETO, 0.3)),
        "dot": css(mix(supd, inkd, 0.3)), "scrim": "rgba(0,0,0,.6)",
        "ok": "#3E9A63", "on-ok": "#ffffff", "warn": "#E0A83A", "on-warn": "#2A1D05", "warn-ink": "#E8B85A",
    }
    return claro, escuro

def bloco_tokens(claro, escuro, f_titulo, f_corpo):
    decl = lambda d: " ".join(f"--{k}: {v};" for k, v in d.items())
    fontes = (f"--f-display: '{f_titulo}', Georgia, 'Times New Roman', serif; "
              f"--f-body: '{f_corpo}', system-ui, -apple-system, 'Segoe UI', sans-serif;")
    return (f":root {{ {decl(claro)} {fontes} }}\n"
            f"@media (prefers-color-scheme: dark) {{ :root:not([data-theme=\"light\"]) {{ {decl(escuro)} color-scheme: dark; }} }}\n"
            f":root[data-theme=\"dark\"] {{ {decl(escuro)} color-scheme: dark; }}")

def link_fontes(t, c):
    fam = lambda n, eixo: "family=" + n.replace(" ", "+") + eixo
    partes = [fam(t, ":ital,wght@0,400;0,600;1,400")]
    if c != t:
        partes.append(fam(c, ":wght@300;400;500;600"))
    return "https://fonts.googleapis.com/css2?" + "&".join(partes) + "&display=swap"


# ---------------------------------------------------------------- dados
def data_uri(p: Path):
    tipo = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".svg": "image/svg+xml", ".webp": "image/webp"}.get(p.suffix.lower())
    if not tipo:
        return None
    return f"data:{tipo};base64," + base64.b64encode(p.read_bytes()).decode()

def achar_logo(cli: Path, bk: dict):
    lg = bk.get("logo") or {}
    cands = []
    for k in ("primary", "dark"):
        v = (lg.get("variants") or {}).get(k)
        if v:
            cands.append(v)
    if lg.get("path"):
        cands.append(lg["path"])
    for c in cands:
        p = Path(c)
        if not p.is_absolute():
            p = cli / p
        elif not p.exists():
            p = cli / "logo" / p.name      # caminho antigo de outra máquina
        if p.exists():
            return data_uri(p)
    for p in sorted((cli / "logo").glob("*")):
        if p.suffix.lower() in (".svg", ".png", ".jpg", ".jpeg", ".webp"):
            return data_uri(p)
    return None

def ler_plano(arq: Path):
    """POST NN do plano → {pasta, legenda, formato, tema}."""
    if not arq.exists():
        return {}
    posts, atual, em_legenda = {}, None, False
    for linha in arq.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^###\s+POST\s+0*(\d+)\s*·?\s*(?:\[([^\]]+)\])?\s*(.*)$", linha.strip(), re.I)
        if m:
            atual = int(m.group(1))
            posts[atual] = {"formato": (m.group(2) or "").lower(), "tema": m.group(3).strip(), "legenda": [], "pasta": None}
            em_legenda = False
            continue
        if atual is None:
            continue
        s = linha.strip()
        m = re.match(r"^Pasta da arte:\s*(.+)$", s, re.I)
        if m:
            v = m.group(1).strip().strip("`")
            posts[atual]["pasta"] = None if v.lower().startswith("ainda") else v.rstrip("/\\")
            continue
        if re.match(r"^Legenda:\s*$", s, re.I):
            em_legenda = True
            continue
        if em_legenda:
            if re.match(r"^(Revisão anti-IA|Referências|Texto da arte|Roteiro)\b", s, re.I) or s.startswith("### "):
                em_legenda = False
            else:
                posts[atual]["legenda"].append(linha.rstrip())
    for p in posts.values():
        p["legenda"] = "\n".join(p["legenda"]).strip()
    return posts

def curto(texto, limite):
    # "]][[" = linhas do título em blocos separados, sem espaço no HTML.
    t = texto.replace("]][[", " ").replace("[[", "").replace("]]", "")
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) <= limite:
        return t
    corte = t[:limite].rsplit(" ", 1)[0].rstrip(",;:.")
    return corte + "…"

def humanizar(slug):
    s = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", slug).replace("-", " ")
    return s[:1].upper() + s[1:]


# ---------------------------------------------------------------- principal
def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("cliente")
    ap.add_argument("mes", help="AAAA-MM")
    ap.add_argument("--posts", nargs="*")
    ap.add_argument("--arquivo", action="append", default=[])
    ap.add_argument("--saida")
    a = ap.parse_args()

    cli = Path(a.cliente).resolve()
    ano, mes = map(int, a.mes.split("-"))
    bk_path = cli / "brand-kit.json"
    bk = json.loads(bk_path.read_text(encoding="utf-8")) if bk_path.exists() else {}
    if not bk:
        print("Aviso: sem brand-kit.json; usando cores e fontes neutras.")
    cfg = json.loads((SKILL / "config.json").read_text(encoding="utf-8"))
    outros = dict(x.split("=", 1) for x in a.arquivo)

    plano = ler_plano(cli / "conteudos" / "planos" / f"{a.mes}.md")
    if a.posts:
        pastas = [cli / "conteudos" / Path(p).name for p in a.posts]
    elif plano and any(v["pasta"] for v in plano.values()):
        pastas = [(cli / v["pasta"]) for _, v in sorted(plano.items()) if v["pasta"]]
    else:
        pastas = sorted(p for p in (cli / "conteudos").glob(f"{a.mes}-*") if p.is_dir())
    pastas = [p for p in pastas if (p / outros.get(p.name, "carousel.html")).exists()]
    if not pastas:
        print("Nenhum carrossel encontrado para", a.mes); sys.exit(1)
    num_por_pasta = {Path(v["pasta"]).name: n for n, v in plano.items() if v.get("pasta")}

    posts, manifesto = [], []
    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        ctx = nav.new_context(viewport={"width": 480, "height": 900}, device_scale_factor=540 / 420,
                              java_script_enabled=False)
        for i, pasta in enumerate(pastas, 1):
            arq = pasta / outros.get(pasta.name, "carousel.html")
            pg = ctx.new_page()
            pg.goto(arq.as_uri(), wait_until="load", timeout=60000)
            pg.evaluate("document.fonts.ready.then(() => true)")
            pg.wait_for_timeout(400)
            pg.evaluate("(() => {" + CAMPOS_JS + "; window.APCampos = APCampos; return true; })()")
            info = pg.evaluate(EXTRAIR)
            if info.get("erro"):
                print(f"Pulando {pasta.name}: {info['erro']}")
                pg.close(); continue
            # add_style_tag trava com o JavaScript da página desligado; inserir direto.
            pg.evaluate("css => { const s = document.createElement('style'); s.textContent = css; document.head.appendChild(s); }",
                        INJETAR + f".ig-frame{{width:{info['w']}px!important}}")
            pg.wait_for_timeout(150)
            thumb = pg.locator("[data-ap-vp]").first.screenshot(type="jpeg", quality=82)
            pg.close()

            doc = ("<!doctype html><html lang=\"pt-BR\"><head>" + info["head"] +
                   "<style>" + INJETAR + f".ig-frame{{width:{info['w']}px!important}}</style></head><body>" +
                   info["frame"] + "</body></html>")
            num = num_por_pasta.get(pasta.name, i)
            pl = plano.get(num, {})
            d = None
            m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", pasta.name)
            if m:
                d = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            capa = [c for c in info["campos"] if c["slide"] == 1]
            # Título = headline da capa; sem headline marcada, o texto mais longo
            # da capa que não seja o nome da marca nem o @.
            marca_nome = (bk.get("brand_name") or "").strip().lower()
            cand = [c for c in capa if c["papel"].endswith("headline")] or sorted(
                [c for c in capa if c["texto"].strip().lower() != marca_nome
                 and not c["texto"].strip().startswith("@")],
                key=lambda c: -len(c["texto"]))
            titulo = curto(cand[0]["texto"], 110) if cand else humanizar(pasta.name)
            legenda = pl.get("legenda") or info["legenda"]
            post = {
                "id": pasta.name, "num": num, "tipo": "carrossel", "slides": info["n"],
                "titulo": titulo, "rotulo": curto(pl.get("tema") or titulo, 30),
                "legenda": legenda, "largura": info["w"], "altura": info["h"], "passo": info["passo"],
                "dataCurta": f"{d.day} {MESES[d.month - 1][:3]}" if d else "",
                "dataLonga": f"{d.day} de {MESES[d.month - 1]}" if d else "",
                "thumb": "data:image/jpeg;base64," + base64.b64encode(thumb).decode(),
                "campos": [{"id": c["id"], "slide": c["slide"], "papel": c["papel"]} for c in info["campos"]],
                "doc": doc,
            }
            posts.append(post)
            manifesto.append({"id": pasta.name, "num": num, "arquivo": str(arq.relative_to(cli)),
                              "campos": info["campos"], "legenda": legenda})
            print(f"POST {num:02d} · {pasta.name}: {info['n']} slides, {len(info['campos'])} textos editáveis"
                  + ("" if legenda else " · sem legenda"))
        nav.close()

    posts.sort(key=lambda p: p["num"])
    marca = bk.get("brand_name") or cli.name
    rotulo_mes = f"{MESES[mes - 1].capitalize()} de {ano}"
    dados = {
        "chave": f"{cli.name}:{a.mes}",
        "mes": rotulo_mes,
        "marca": {"nome": marca, "handle": bk.get("instagram_handle", ""), "logo": achar_logo(cli, bk)},
        "whatsapp": cfg.get("whatsapp", ""),
        "posts": posts,
    }
    f_t = bk.get("heading_font") or "Lora"
    f_c = bk.get("body_font") or "Poppins"
    claro, escuro = tokens(bk.get("derived") or {})
    json_txt = json.dumps(dados, ensure_ascii=False).replace("<", "\\u003c")

    pagina = (TEMPLATE
              .replace("__TITULO__", f"Aprovação {marca} · {MESES[mes - 1].capitalize()}")
              .replace("__FONTES__", link_fontes(f_t, f_c))
              .replace("/*__TOKENS__*/", bloco_tokens(claro, escuro, f_t, f_c))
              .replace("/*__CAMPOS_JS__*/", CAMPOS_JS)
              .replace("__DADOS__", json_txt))

    saida = Path(a.saida) if a.saida else cli / "aprovacao" / a.mes
    saida.mkdir(parents=True, exist_ok=True)
    (saida / "aprovacao-artifact.html").write_text(pagina, encoding="utf-8")
    corte = pagina.index('<div class="app">')
    completa = ("<!doctype html>\n<html lang=\"pt-BR\">\n<head>\n<meta charset=\"utf-8\">\n"
                "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">\n"
                + pagina[:corte] + "</head>\n<body>\n" + pagina[corte:] + "\n</body>\n</html>\n")
    (saida / "aprovacao.html").write_text(completa, encoding="utf-8")
    (saida / "manifesto.json").write_text(json.dumps({"cliente": cli.name, "mes": a.mes, "posts": manifesto},
                                                     ensure_ascii=False, indent=1), encoding="utf-8")
    mb = (saida / "aprovacao.html").stat().st_size / 1_048_576
    print(f"\nPágina gerada em {saida} ({len(posts)} posts, {mb:.1f} MB)")
    if mb > 15:
        print("Aviso: acima de 15 MB; o claude.ai aceita no máximo 16 MB. Divida o mês com --posts.")


if __name__ == "__main__":
    main()
