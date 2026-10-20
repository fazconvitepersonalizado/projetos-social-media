#!/usr/bin/env python3
"""
Aplica nos carousel.html originais os textos que a cliente alterou na página
de aprovação.

Uso (na raiz do projeto):
    python .claude/skills/pagina-aprovacao/scripts/aplicar_respostas.py "<pasta do cliente>" <AAAA-MM> <respostas.json> [--aplicar]

<respostas.json> aceita:
  - o texto do botão "Copiar dados completos" da página: {"respostas": {"<post>": {...}}}
  - a lista de documentos da coleção "respostas" do banco da página
    (cada um com "post", "status", "comentario", "edicoes", "legenda" e
    "ajustes", os pedidos por slide: {"3": "texto"}).

Sem --aplicar, só mostra o que mudaria (antes → depois). Com --aplicar,
grava os arquivos. Usa o manifesto.json gerado junto com a página para saber
de qual arquivo veio cada post; os textos são localizados pela mesma regra
de assets/campos.js.
"""
import argparse
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

SKILL = Path(__file__).resolve().parents[1]
CAMPOS_JS = (SKILL / "assets" / "campos.js").read_text(encoding="utf-8")

APLICAR = """
([edicoes, legenda]) => {
  const out = {mudancas: [], faltando: []};
  const cs = APCampos.campos(document);
  const por = {};
  cs.forEach(c => por[c.id] = c);
  Object.keys(edicoes).forEach(id => {
    const c = por[id];
    if (!c) { out.faltando.push(id); return; }
    const antes = APCampos.ler(c.el);
    if (antes === edicoes[id]) return;
    APCampos.escrever(c.el, edicoes[id], APCampos.moldes(c.el));
    out.mudancas.push({id, antes, depois: edicoes[id]});
  });
  if (legenda != null) {
    const p = document.querySelector('.ig-caption p');
    if (p) {
      const h = p.querySelector('strong');
      const handle = h && /^@/.test(h.textContent.trim()) ? h.cloneNode(true) : null;
      while (p.firstChild) p.removeChild(p.firstChild);
      if (handle) { p.appendChild(handle); p.appendChild(document.createTextNode(' ')); }
      legenda.split('\\n').forEach((l, i) => { if (i) p.appendChild(document.createElement('br')); p.appendChild(document.createTextNode(l)); });
      out.mudancas.push({id: 'legenda', antes: '(legenda do carrossel)', depois: legenda});
    } else {
      out.faltando.push('legenda (o arquivo não tem .ig-caption; atualizar só no plano)');
    }
  }
  document.querySelectorAll('[data-ap-id]').forEach(e => e.removeAttribute('data-ap-id'));
  const dt = document.doctype ? '<!DOCTYPE ' + document.doctype.name + '>\\n' : '';
  out.html = dt + document.documentElement.outerHTML + '\\n';
  return out;
}
"""


def carregar_respostas(arq: Path):
    dados = json.loads(arq.read_text(encoding="utf-8"))
    if isinstance(dados, dict) and "respostas" in dados:
        return dados["respostas"]
    if isinstance(dados, list):
        out = {}
        for d in dados:
            corpo = d.get("data", d) if isinstance(d, dict) else {}
            pid = corpo.get("post") or d.get("id")
            if pid:
                out[pid] = corpo
        return out
    if isinstance(dados, dict):
        return dados
    raise SystemExit("Formato de respostas não reconhecido.")


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("cliente")
    ap.add_argument("mes")
    ap.add_argument("respostas")
    ap.add_argument("--aplicar", action="store_true")
    a = ap.parse_args()

    cli = Path(a.cliente).resolve()
    man_path = cli / "aprovacao" / a.mes / "manifesto.json"
    if not man_path.exists():
        raise SystemExit(f"Manifesto não encontrado: {man_path}. Gere a página antes.")
    manifesto = {p["id"]: p for p in json.loads(man_path.read_text(encoding="utf-8"))["posts"]}
    respostas = carregar_respostas(Path(a.respostas))

    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        ctx = nav.new_context(java_script_enabled=False)
        for pid, r in sorted(respostas.items(), key=lambda kv: manifesto.get(kv[0], {}).get("num", 99)):
            m = manifesto.get(pid)
            st = r.get("status") or "sem resposta"
            if not m:
                print(f"{pid}: não está no manifesto deste mês; ignorado.")
                continue
            print(f"\nPOST {m['num']:02d} · {pid}: {st}" + (f" · comentário: {r['comentario']}" if r.get("comentario") else ""))
            # Pedidos de ajuste por slide ({"3": "texto"}); só contam com status "ajuste".
            if r.get("status") == "ajuste":
                for s, t in sorted((r.get("ajustes") or {}).items(), key=lambda kv: int(kv[0])):
                    if str(t).strip():
                        print(f"   ajuste no slide {s}: {str(t).strip()}")
            edicoes = r.get("edicoes") or {}
            legenda = r.get("legenda")
            if not edicoes and legenda is None:
                print("   sem textos alterados")
                continue
            arq = cli / m["arquivo"]
            pg = ctx.new_page()
            pg.goto(arq.as_uri(), wait_until="load", timeout=60000)
            pg.evaluate("(() => {" + CAMPOS_JS + "; window.APCampos = APCampos; return true; })()")
            res = pg.evaluate(APLICAR, [edicoes, legenda])
            pg.close()
            for mu in res["mudancas"]:
                print(f"   {mu['id']}:\n      antes:  {mu['antes']!r}\n      depois: {mu['depois']!r}")
            for f in res["faltando"]:
                print(f"   AVISO: não encontrei {f} no arquivo")
            if a.aplicar and res["mudancas"]:
                arq.write_text(res["html"], encoding="utf-8")
                print(f"   gravado em {m['arquivo']}")
        nav.close()
    if not a.aplicar:
        print("\nNada foi gravado (simulação). Rode de novo com --aplicar depois de conferir.")


if __name__ == "__main__":
    main()
