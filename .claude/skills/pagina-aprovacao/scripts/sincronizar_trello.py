#!/usr/bin/env python3
"""
Mantém a página de aprovação e o Trello dizendo a mesma coisa.

A página e o cartão saem da MESMA fonte: o manifesto.json que o
gerar_aprovacao.py grava junto com a página (textos de cada slide e legenda,
exatamente como a cliente vê) + o plano do mês (data, formato, tema).

Uso (na raiz do projeto):
    python .claude/skills/pagina-aprovacao/scripts/sincronizar_trello.py cartoes "<cliente>" <AAAA-MM>
        Monta nome, descrição (Markdown), data, etiquetas e checklist de cada
        cartão em <cliente>/aprovacao/<AAAA-MM>/trello-cartoes.json, para o
        Claude gravar no Trello pelo conector.

    python .claude/skills/pagina-aprovacao/scripts/sincronizar_trello.py comparar "<cliente>" <AAAA-MM> <export.json>
        Compara o Trello (export.json: {"cartoes": [{"nome", "desc", "due",
        "lista", "url"}]}, lido pelo conector) com os arquivos locais e lista
        cada diferença: posts que só existem de um lado, data, legenda e texto
        de cada slide. Grava <cliente>/aprovacao/<AAAA-MM>/trello-diferencas.json.
        Nada é sobrescrito: o Thiago escolhe qual lado vale em cada diferença.

Opcional nos dois: respostas.json da pasta do mês (respostas da cliente) entra
na seção "Aprovação" do cartão.
"""
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

DIAS = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]
MESES = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
FORMATO = {"carrossel": "Carrossel", "post único": "Post único", "frase": "Frase", "reels": "Reels",
           "roteiro": "Roteiro", "terceiros": "Terceiros", "corte": "Corte", "stories": "Stories"}
ETAPAS = ["Texto revisado", "Arte pronta", "Enviado para aprovação", "Aprovado pela cliente", "Agendado", "Publicado"]
# Quantas etapas ficam marcadas em cada lista do quadro.
FEITAS_POR_LISTA = {"Gaveta": 0, "Planejado": 0, "Em produção": 1, "Aprovação do cliente": 3,
                    "Ajustes": 3, "Agendado": 5, "Publicado": 6}


def sem_marcas(t):
    return re.sub(r"\s+", " ", str(t or "").replace("]][[", " ").replace("[[", "").replace("]]", "")).strip()


def norm(t):
    """Comparação tolerante: ignora espaços, caixa e aspas tipográficas."""
    t = unicodedata.normalize("NFC", str(t or "")).replace("“", '"').replace("”", '"').replace("’", "'")
    return re.sub(r"\s+", " ", t).strip().lower()


def ler_plano(arq: Path):
    posts, atual = {}, None
    if not arq.exists():
        return posts
    for linha in arq.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^###\s+POST\s+0*(\d+)\s*·?\s*(?:\[([^\]]+)\])?\s*(.*)$", linha.strip())
        if m:
            atual = int(m.group(1))
            posts[atual] = {"formato": (m.group(2) or "").strip().lower(), "tema": m.group(3).strip()}
            continue
        m = re.match(r"^Data:\s*(\d{4}-\d{2}-\d{2})", linha.strip())
        if m and atual:
            posts[atual]["data"] = m.group(1)
    return posts


def campos_visiveis(post, marca):
    """Textos da arte por slide, como aparecem no cartão (sem o nome da marca
    repetido em cada slide e sem os marcadores [[ ]] do design)."""
    marca = norm(marca)
    out = {}
    for c in post.get("campos", []):
        t = sem_marcas(c["texto"])
        if not t or norm(t) == marca:
            continue
        out.setdefault(c["slide"], []).append({"id": c["id"], "texto": t})
    return out


def secao_aprovacao(r):
    if not r or not r.get("status"):
        return "Aguardando a cliente."
    if r["status"] == "aprovado":
        alt = bool(r.get("edicoes")) or r.get("legenda") is not None
        linhas = ["**Aprovado" + (" com alterações nos textos**" if alt else "**")]
    else:
        linhas = ["**Pediu ajuste**"]
        for s, t in sorted((r.get("ajustes") or {}).items(), key=lambda kv: int(kv[0])):
            if str(t).strip():
                linhas.append(f"- Slide {s}: {str(t).strip()}")
    if r.get("comentario"):
        linhas.append(f"- Comentário geral: {r['comentario'].strip()}")
    return "\n".join(linhas)


def montar(cli: Path, mes: str):
    pasta = cli / "aprovacao" / mes
    man = json.loads((pasta / "manifesto.json").read_text(encoding="utf-8"))
    bk = json.loads((cli / "brand-kit.json").read_text(encoding="utf-8")) if (cli / "brand-kit.json").exists() else {}
    marca = bk.get("brand_name", "")
    plano = ler_plano(cli / "conteudos" / "planos" / f"{mes}.md")
    links = json.loads((cli / "aprovacao" / "links.json").read_text(encoding="utf-8")) if (cli / "aprovacao" / "links.json").exists() else {}
    resp = {}
    if (pasta / "respostas.json").exists():
        bruto = json.loads((pasta / "respostas.json").read_text(encoding="utf-8"))
        bruto = bruto.get("respostas", bruto) if isinstance(bruto, dict) else {d.get("post"): d for d in bruto}
        resp = bruto
    ano, m = map(int, mes.split("-"))
    rot_mes = f"{MESES[m - 1]}/{ano}"
    cartoes = []
    for p in man["posts"]:
        n = p["num"]
        pl = plano.get(n, {})
        fmt = pl.get("formato") or ("carrossel" if len({c["slide"] for c in p.get("campos", [])}) > 1 else "post único")
        d = pl.get("data") or p["id"][:10]
        dt = date.fromisoformat(d)
        slides = campos_visiveis(p, marca)
        tema = pl.get("tema") or (slides.get(1, [{"texto": p["id"]}])[0]["texto"])
        nome = f"{dt:%d/%m} · POST {n:02d} · {FORMATO.get(fmt, fmt.title())} · {tema}"
        cab = f"**{dt:%d/%m/%Y} ({DIAS[dt.weekday()]}) · {FORMATO.get(fmt, fmt)}" + (f" · {len(slides)} slides" if len(slides) > 1 else "") + "**"
        linhas = [cab]
        if links.get(mes):
            linhas.append(f"Página de aprovação: [abrir a página do mês]({links[mes]})")
        linhas += [f"Arquivos: `{cli.name}/conteudos/planos/{mes}.md` · arte em `{p['arquivo'].replace(chr(92), '/')}`",
                   "", "---", "", "## Legenda", "", (p.get("legenda") or "_sem legenda_"), "", "---", "", "## Texto da arte", ""]
        for s in sorted(slides):
            rot = "capa" if s == 1 and len(slides) > 1 else ("encerramento" if s == max(slides) and len(slides) > 1 else "")
            linhas.append(f"**Slide {s}" + (f" · {rot}" if rot else "") + "**")
            linhas += [c["texto"] for c in slides[s]]
            linhas.append("")
        linhas += ["---", "", "## Aprovação", "", secao_aprovacao(resp.get(p["id"]))]
        cartoes.append({"num": n, "post": p["id"], "nome": nome, "due": f"{d}T12:00:00.000Z",
                        "etiquetas": [rot_mes, fmt], "desc": "\n".join(linhas),
                        "checklist": {"nome": "Etapas", "itens": ETAPAS}})
    return {"cliente": cli.name, "mes": mes, "cartoes": cartoes}


def ler_cartao(desc):
    """Extrai legenda e textos por slide de um cartão, no formato novo
    (## Legenda / **Slide N**) ou no antigo (Legenda: / Card N)."""
    legenda, slides, atual, modo = [], {}, None, None
    for linha in desc.splitlines():
        s = linha.strip()
        if re.match(r"^(##\s*)?Legenda:?$", s, re.I):
            modo = "leg"; continue
        if re.match(r"^(##\s*)?Texto da arte:?$", s, re.I):
            modo = "arte"; continue
        if re.match(r"^(##\s*Aprovação|Arquivo local:|Referências e observações:)", s, re.I):
            modo = None; continue
        if s == "---":
            continue
        if modo == "leg":
            legenda.append(linha.rstrip())
        elif modo == "arte":
            m = re.match(r"^\*{0,2}(?:Slide|Card)\s+(\d+)", s)
            if m:
                atual = int(m.group(1)); slides[atual] = []; continue
            if s.lower().startswith("arte única"):
                atual = 1; slides[1] = []; continue
            if s and atual:
                slides[atual].append(s)
    return "\n".join(legenda).strip(), slides


def comparar(cli: Path, mes: str, export: Path):
    local = montar(cli, mes)
    man = {p["id"]: p for p in json.loads((cli / "aprovacao" / mes / "manifesto.json").read_text(encoding="utf-8"))["posts"]}
    bk = json.loads((cli / "brand-kit.json").read_text(encoding="utf-8")) if (cli / "brand-kit.json").exists() else {}
    trello = json.loads(export.read_text(encoding="utf-8"))["cartoes"]
    por_num = {}
    for c in trello:
        if not str(c.get("due", "")).startswith(mes):
            continue
        m = re.search(r"POST\s+0*(\d+)", c.get("nome", ""))
        if m:
            por_num[int(m.group(1))] = c
    difs = []
    for lc in local["cartoes"]:
        tc = por_num.pop(lc["num"], None)
        if not tc:
            difs.append({"post": lc["num"], "tipo": "só na página", "detalhe": lc["nome"]})
            continue
        if tc.get("due", "")[:10] != lc["due"][:10]:
            difs.append({"post": lc["num"], "tipo": "data", "trello": tc["due"][:10], "local": lc["due"][:10]})
        leg_t, slides_t = ler_cartao(tc.get("desc", ""))
        leg_l = man[lc["post"]].get("legenda") or ""
        if norm(leg_t) != norm(leg_l):
            difs.append({"post": lc["num"], "tipo": "legenda", "trello": leg_t, "local": leg_l})
        slides_l = campos_visiveis(man[lc["post"]], bk.get("brand_name", ""))
        for s in sorted(set(slides_l) | set(slides_t)):
            tl = [c["texto"] for c in slides_l.get(s, [])]
            tt = slides_t.get(s, [])
            if norm(" ".join(tt)) != norm(" ".join(tl)):
                difs.append({"post": lc["num"], "tipo": f"texto do slide {s}", "trello": tt, "local": tl,
                             "campos": [c["id"] for c in slides_l.get(s, [])]})
    for n, tc in sorted(por_num.items()):
        difs.append({"post": n, "tipo": "só no Trello", "detalhe": tc.get("nome"), "lista": tc.get("lista")})
    return difs


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if len(sys.argv) < 4 or sys.argv[1] not in ("cartoes", "comparar"):
        print(__doc__); sys.exit(1)
    cmd, cli, mes = sys.argv[1], Path(sys.argv[2]).resolve(), sys.argv[3]
    pasta = cli / "aprovacao" / mes
    if not (pasta / "manifesto.json").exists():
        print(f"Sem {pasta / 'manifesto.json'}: gere a página do mês antes (gerar_aprovacao.py)."); sys.exit(1)
    if cmd == "cartoes":
        out = montar(cli, mes)
        (pasta / "trello-cartoes.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        for c in out["cartoes"]:
            print(c["nome"], "|", c["due"][:10], "|", ", ".join(c["etiquetas"]), "|", len(c["desc"]), "caracteres")
        print(f"\n{len(out['cartoes'])} cartões em {pasta / 'trello-cartoes.json'}")
    else:
        difs = comparar(cli, mes, Path(sys.argv[4]))
        (pasta / "trello-diferencas.json").write_text(json.dumps(difs, ensure_ascii=False, indent=1), encoding="utf-8")
        if not difs:
            print("Trello e página iguais: mesmos posts, datas, legendas e textos de cada slide.")
        for d in difs:
            print(f"POST {d['post']:02d} · {d['tipo']}")
            if "trello" in d:
                print(f"   Trello: {d['trello']}\n   Local:  {d['local']}")
            elif "detalhe" in d:
                print(f"   {d['detalhe']}")
        print(f"\n{len(difs)} diferença(s) em {pasta / 'trello-diferencas.json'}")


if __name__ == "__main__":
    main()
