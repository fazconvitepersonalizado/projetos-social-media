"""Sorteio da estrutura de um carrossel novo, sem repetir nada que o cliente já teve.

Uso:
    python sorteio_carrossel.py "<pasta do cliente>" --tema "Carboidrato à noite engorda?"
    python sorteio_carrossel.py "<pasta do cliente>" --tema "..." --slides 10 --seed 42
    python sorteio_carrossel.py "<pasta do cliente>" --tema "..." --simular   # não grava no histórico

O que é sorteado (a "fórmula"): estrutura narrativa, tipo de gancho, ritmo de
fundos, composição de cada slide (capa, miolo e CTA), quais slides levam foto,
alinhamento, onde o texto se apoia e o indicador de arraste.

Regras de "nunca igual" contra o histórico do cliente
(<cliente>/conteudos/historico-sorteios.json):
  1. a combinação completa (impressão digital) nunca se repete;
  2. as posições das fotos nunca repetem as do carrossel anterior;
  3. estrutura + gancho nunca repetem os do carrossel anterior;
  4. a composição slide a slide coincide em no máximo 40% com qualquer um
     dos últimos 6 carrosséis;
  5. dentro do carrossel: a mesma composição nunca aparece em dois slides
     seguidos nem mais de 2 vezes.
Tudo que é sorteado aqui é estrutura; cor, fonte e tom continuam vindo da
marca do cliente (brand-kit.json / skill marca-<slug>).
"""
import argparse
import hashlib
import json
import random
import sys
from datetime import date
from pathlib import Path

ESTRUTURAS = {
    "mito-e-verdade": "Desmonta uma crença comum e mostra o que vale de fato.",
    "erro-comum": "Mostra um erro que o público comete e como corrigir.",
    "passo-a-passo": "Ensina a fazer algo em etapas curtas.",
    "historia-de-caso": "Conta um caso real (cliente, paciente, bastidor) e tira a lição dele.",
    "perguntas-e-respostas": "Responde as dúvidas que o público mais manda.",
    "comparacao": "Coloca duas opções lado a lado e dá o veredito.",
    "guia-rapido": "Reúne o essencial de um assunto para salvar e consultar.",
    "um-dia-na-rotina": "Segue um dia (ou uma refeição, uma reunião) do começo ao fim.",
}

GANCHOS = {
    "pergunta": "Pergunta que o público já se fez.",
    "contra-o-senso-comum": "Afirmação que contraria o que todo mundo repete.",
    "numero-concreto": "Número real (de estudo, do consultório, do cliente) no título.",
    "cena-do-dia-a-dia": "Descreve uma cena que o público reconhece na hora.",
    "frase-real": "Frase que o cliente ou um paciente disse de verdade.",
}

RITMOS = {
    "alternado": "Claro e escuro alternando a cada slide.",
    "blocos": "Dois claros, dois escuros, dois claros...",
    "claro-com-pausa": "Quase tudo claro, com um único slide escuro no meio como pausa.",
    "escuro-dominante": "Quase tudo escuro, com respiros claros.",
    "cor-da-marca": "Cor principal da marca domina; claro e escuro entram como contraste.",
}

CAPAS = {
    "capa-foto-cheia": "Foto no slide inteiro, título no espaço livre da foto.",
    "capa-tipografica": "Sem foto: título enorme ocupando a capa.",
    "capa-foto-dividida": "Metade foto, metade título.",
    "capa-foto-recortada": "Foto em bloco (emoldurada) com o título encostado nela.",
}

MIOLO = {
    "frase-gigante": "Uma frase só, enorme, ocupando o slide.",
    "titulo-e-apoio": "Título com texto de apoio logo abaixo, no mesmo bloco.",
    "foto-cheia": "Foto no slide inteiro, texto no espaço livre.",
    "foto-dividida": "Foto ocupando metade do slide, texto na outra metade.",
    "foto-emoldurada": "Foto em bloco dentro do slide, texto junto dela.",
    "dado-em-destaque": "Um dado real grande com a explicação colada nele (só com dado real).",
    "diagrama": "Desenho simples e exato (prato, linha do tempo, escala, antes/depois).",
    "lista-curta": "Dois a quatro itens curtos, sem ícone decorativo.",
    "comparacao-lado-a-lado": "Duas colunas ou duas metades: isso x aquilo.",
    "fala-real": "Citação real do cliente ou de um paciente (só com fala real).",
    "pergunta-grande": "Pergunta grande para o público responder nos comentários.",
}
COM_FOTO = {"capa-foto-cheia", "capa-foto-dividida", "capa-foto-recortada",
            "foto-cheia", "foto-dividida", "foto-emoldurada", "cta-foto"}

CTAS = {
    "cta-cor-chapada": "Fundo chapado na cor da marca, convite e botão.",
    "cta-foto": "Foto do cliente ou do serviço, convite no espaço livre.",
    "cta-tipografico": "Fundo claro, convite grande em tipografia, sem enfeite.",
    "cta-pergunta-e-convite": "Pergunta curta seguida do convite para a consulta/serviço.",
}

ALINHAMENTOS = ["esquerda", "centralizado", "misto (capa e CTA centralizados, miolo à esquerda)"]
APOIO_DO_TEXTO = ["topo", "base", "centro", "varia por slide"]
INDICADORES = ["selo 'arraste' só na capa", "contador discreto (n/total)", "barra de progresso segmentada", "sem indicador"]


def historico_path(cliente: Path) -> Path:
    return cliente / "conteudos" / "historico-sorteios.json"


def carregar(cliente: Path) -> list:
    p = historico_path(cliente)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else []


def digital(s: dict) -> str:
    chave = "|".join([s["estrutura"], s["gancho"], s["ritmo"], s["alinhamento"], s["apoio_do_texto"],
                      s["indicador"], ",".join(s["composicao"]), ",".join(map(str, s["slides_com_foto"]))])
    return hashlib.sha1(chave.encode("utf-8")).hexdigest()[:12]


def sortear_composicao(rng: random.Random, n: int) -> list:
    capa = rng.choice(list(CAPAS))
    cta = rng.choice(list(CTAS))
    fotos_alvo = rng.randint(1, max(1, n // 3))  # "não exagere": até 1 a cada 3 slides
    fotos_alvo -= (capa in COM_FOTO) + (cta in COM_FOTO)
    miolo = []
    for _ in range(n - 2):
        opcoes = [m for m in MIOLO
                  if (not miolo or m != miolo[-1]) and miolo.count(m) < 2
                  and (m not in COM_FOTO or sum(x in COM_FOTO for x in miolo) < fotos_alvo)]
        miolo.append(rng.choice(opcoes))
    if "pergunta-grande" in miolo and cta == "cta-pergunta-e-convite":
        cta = rng.choice([c for c in CTAS if c != "cta-pergunta-e-convite"])
    return [capa] + miolo + [cta]


def sobreposicao(a: list, b: list) -> float:
    n = min(len(a), len(b))
    return sum(a[i] == b[i] for i in range(n)) / n if n else 0.0


def problemas(s: dict, hist: list) -> list:
    erros = []
    if any(h.get("digital") == s["digital"] for h in hist):
        erros.append("combinação idêntica a um carrossel anterior")
    if hist:
        ult = hist[-1]
        if ult.get("slides_com_foto") == s["slides_com_foto"] and s["slides_com_foto"]:
            erros.append("fotos nas mesmas posições do carrossel anterior")
        if (ult.get("estrutura"), ult.get("gancho")) == (s["estrutura"], s["gancho"]):
            erros.append("mesma estrutura e mesmo gancho do carrossel anterior")
    for h in hist[-6:]:
        if sobreposicao(s["composicao"], h.get("composicao", [])) > 0.4:
            erros.append(f"composição parecida demais com '{h.get('tema')}'")
    return erros


def sortear(n: int, hist: list, seed: int) -> dict:
    rng = random.Random(seed)
    for tentativa in range(1, 2001):
        comp = sortear_composicao(rng, n)
        s = {
            "estrutura": rng.choice(list(ESTRUTURAS)),
            "gancho": rng.choice(list(GANCHOS)),
            "ritmo": rng.choice(list(RITMOS)),
            "alinhamento": rng.choice(ALINHAMENTOS),
            "apoio_do_texto": rng.choice(APOIO_DO_TEXTO),
            "indicador": rng.choice(INDICADORES),
            "composicao": comp,
            "slides_com_foto": [i + 1 for i, c in enumerate(comp) if c in COM_FOTO],
        }
        s["digital"] = digital(s)
        if not problemas(s, hist):
            s["tentativas"] = tentativa
            return s
    sys.exit("Não achei combinação inédita em 2000 tentativas; aumente o número de slides ou revise o histórico.")


def imprimir(s: dict, tema: str):
    desc = {**CAPAS, **MIOLO, **CTAS}
    print(f"\nSORTEIO · {tema}  (seed {s['seed']}, digital {s['digital']})\n")
    print(f"Estrutura:  {s['estrutura']}: {ESTRUTURAS[s['estrutura']]}")
    print(f"Gancho:     {s['gancho']}: {GANCHOS[s['gancho']]}")
    print(f"Fundos:     {s['ritmo']}: {RITMOS[s['ritmo']]}")
    print(f"Alinhamento: {s['alinhamento']} · texto apoiado: {s['apoio_do_texto']} · indicador: {s['indicador']}")
    print(f"Fotos nos slides: {s['slides_com_foto'] or 'nenhum'}\n")
    for i, c in enumerate(s["composicao"], 1):
        print(f"  {i:>2}. {c:<24} {desc[c]}")
    print("\nSe um slide pedir material que não existe (dado real, fala real, foto do cliente),"
          "\nre-sorteie com outro --seed em vez de inventar o material.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cliente", help="pasta do cliente (ex.: 'TESTE Marina Couto')")
    ap.add_argument("--tema", required=True)
    ap.add_argument("--slides", type=int, default=8)
    ap.add_argument("--seed", type=int, default=None, help="repete um sorteio específico")
    ap.add_argument("--simular", action="store_true", help="mostra o sorteio sem gravar no histórico")
    a = ap.parse_args()

    cliente = Path(a.cliente)
    if not (cliente / "conteudos").is_dir():
        sys.exit(f"Pasta de conteúdos não encontrada em: {cliente}")
    if a.slides < 5:
        sys.exit("Use pelo menos 5 slides.")
    hist = carregar(cliente)
    seed = a.seed if a.seed is not None else random.SystemRandom().randint(1, 10**9)
    s = sortear(a.slides, hist, seed)
    s = {"data": date.today().isoformat(), "tema": a.tema, "seed": seed, **s}
    imprimir(s, a.tema)
    if not a.simular:
        hist.append(s)
        historico_path(cliente).write_text(json.dumps(hist, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nGravado em {historico_path(cliente)} ({len(hist)} sorteios no histórico).")


if __name__ == "__main__":
    main()
