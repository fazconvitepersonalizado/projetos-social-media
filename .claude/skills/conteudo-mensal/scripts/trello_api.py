#!/usr/bin/env python3
"""
O que o conector do Trello no claude.ai não faz (criar/nomear etiquetas,
anexar arquivos), feito pela API oficial do Trello com a chave do Thiago.

Chave e token ficam no .env da raiz (nunca vai para o git):
    TRELLO_KEY=...
    TRELLO_TOKEN=...

Uso (na raiz do projeto):
    python .claude/skills/conteudo-mensal/scripts/trello_api.py testar
        Confere se a chave funciona (mostra o usuário conectado).

    python .claude/skills/conteudo-mensal/scripts/trello_api.py etiquetas "<cliente>" [AAAA-MM ...]
        Garante no quadro do cliente as etiquetas de formato e de cada mês
        pedido (ou de todos os meses com plano em conteudos/planos/): dá nome
        às que já existem sem nome, cria as que faltam e grava os IDs no
        <cliente>/trello.json.

    python .claude/skills/conteudo-mensal/scripts/trello_api.py anexar <id do cartão> <arquivo> [<arquivo> ...]
        Anexa arquivos (ex.: os PNGs dos slides, na ordem) a um cartão.
"""
import json
import os
import re
import sys
from pathlib import Path

import requests

RAIZ = Path(__file__).resolve().parents[4]
API = "https://api.trello.com/1"
MESES = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
# Formato: cor fixa em todos os quadros.
FORMATOS = {"carrossel": "green", "post único": "yellow", "reels": "red", "frase": "sky",
            "roteiro": "lime", "terceiros": "pink", "corte": "pink", "stories": "orange"}
# Meses: cores em rodízio, pulando as que outro mês do mesmo quadro já usa.
CORES_MES = ["blue", "purple", "orange", "sky", "red", "lime", "pink", "black",
             "blue_dark", "purple_dark", "orange_dark", "sky_dark"]
COR_PT = {"azul": "blue", "roxo": "purple", "verde": "green", "amarelo": "yellow", "laranja": "orange",
          "vermelho": "red", "céu": "sky", "lima": "lime", "rosa": "pink", "preto": "black"}


def credenciais():
    env = RAIZ / ".env"
    vals = {}
    if env.exists():
        for linha in env.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\s*([A-Z_]+)\s*=\s*(.*?)\s*$", linha)
            if m:
                vals[m.group(1)] = m.group(2).strip('"').strip("'")
    key = os.environ.get("TRELLO_KEY") or vals.get("TRELLO_KEY", "")
    token = os.environ.get("TRELLO_TOKEN") or vals.get("TRELLO_TOKEN", "")
    if not key or not token or "cole" in key.lower() or "cole" in token.lower():
        print("Falta TRELLO_KEY e/ou TRELLO_TOKEN no .env da raiz do projeto.")
        sys.exit(2)
    return {"key": key, "token": token}


def chamar(metodo, caminho, **kw):
    params = dict(kw.pop("params", {}), **credenciais())
    r = requests.request(metodo, API + caminho, params=params, timeout=60, **kw)
    if r.status_code >= 400:
        # Nunca imprimir a URL inteira: ela leva a chave e o token.
        print(f"Erro {r.status_code} em {metodo} {caminho}: {r.text[:200]}")
        sys.exit(1)
    return r.json() if r.text else {}


def obj_id(ari):
    """ARI do conector (ari:cloud:trello::board/workspace/<ws>/<id>) → id da API."""
    return str(ari).rstrip("/").split("/")[-1]


def meses_do_cliente(cli: Path):
    return sorted(p.stem for p in (cli / "conteudos" / "planos").glob("????-??.md"))


def etiquetas(cli: Path, meses):
    arq = cli / "trello.json"
    reg = json.loads(arq.read_text(encoding="utf-8"))
    quadro = obj_id(reg["quadro"]["id"])
    existentes = chamar("GET", f"/boards/{quadro}/labels", params={"limit": 1000})
    por_id = {l["id"]: l for l in existentes}

    # Registro antigo: {"Set/2026 (azul)": "<ari>"} → {"Set/2026": {"id", "cor"}}
    novo = {}
    for nome, v in (reg.get("etiquetas") or {}).items():
        if isinstance(v, dict):
            novo[nome] = v; continue
        m = re.match(r"^(.*?)\s*\((\w+)\)$", nome)
        nome_limpo, cor = (m.group(1), COR_PT.get(m.group(2), m.group(2))) if m else (nome, None)
        novo[nome_limpo] = {"id": obj_id(v), "cor": cor}

    desejadas = {}
    for f, cor in FORMATOS.items():
        if f in novo or f in ("carrossel", "post único"):
            desejadas[f] = cor
    usadas = {v.get("cor") for k, v in novo.items() if "/" in k}
    for mes in meses:
        ano, m = map(int, mes.split("-"))
        rot = f"{MESES[m - 1]}/{ano}"
        if rot in novo:
            desejadas[rot] = novo[rot].get("cor"); continue
        cor = next((c for c in CORES_MES if c not in usadas), "black")
        usadas.add(cor)
        desejadas[rot] = cor

    feitas = []
    for nome, cor in desejadas.items():
        atual = novo.get(nome, {})
        lab = por_id.get(atual.get("id"))
        if not lab:  # procurar por nome, depois uma da mesma cor ainda sem nome
            lab = next((l for l in existentes if l["name"] == nome), None) or \
                  next((l for l in existentes if l["color"] == cor and not l["name"]), None)
        if lab and lab["name"] != nome:
            lab = chamar("PUT", f"/labels/{lab['id']}", params={"name": nome})
            feitas.append(f"nomeada: {nome} ({lab['color']})")
        elif not lab:
            lab = chamar("POST", f"/boards/{quadro}/labels", params={"name": nome, "color": cor})
            existentes.append(lab)
            feitas.append(f"criada:  {nome} ({cor})")
        else:
            feitas.append(f"ok:      {nome} ({lab['color']})")
        novo[nome] = {"id": lab["id"], "cor": lab["color"]}

    reg["etiquetas"] = novo
    reg.pop("pendente", None)
    arq.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{reg['quadro']['nome']}:")
    for f in feitas:
        print("  " + f)


def anexar(card, arquivos):
    for a in arquivos:
        p = Path(a)
        with p.open("rb") as fh:
            r = chamar("POST", f"/cards/{obj_id(card)}/attachments", params={"name": p.name}, files={"file": (p.name, fh)})
        print(f"anexado: {p.name} → {r.get('url', '')[:80]}")


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "testar":
        me = chamar("GET", "/members/me", params={"fields": "username,fullName"})
        print(f"Conectado como @{me['username']} ({me['fullName']}).")
    elif cmd == "etiquetas" and len(sys.argv) >= 3:
        cli = Path(sys.argv[2]).resolve()
        etiquetas(cli, sys.argv[3:] or meses_do_cliente(cli))
    elif cmd == "anexar" and len(sys.argv) >= 4:
        anexar(sys.argv[2], sys.argv[3:])
    else:
        print(__doc__); sys.exit(1)


if __name__ == "__main__":
    main()
