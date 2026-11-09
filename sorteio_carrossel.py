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
  3. a estrutura (tipo de post) nunca repete a do carrossel anterior, nem os 2
     recursos de slide sugeridos;
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
    # repertório criativo (2026-11-08, estudo da Publipost): .claude/skills/conteudo-mensal/references/repertorio-criativo.md
    "tema-que-vira-licao": "Parte de um tema do momento, mostra a virada, dá nome ao fenômeno e tira a lição para o leitor.",
    "serie-de-anafora": "Um bordão que se repete em cada slide ('Menopausa não é...'), cada vez com uma ideia nova.",
    "dado-comparativo": "Compara números reais (antes x depois, nós x média) e tira a lição (só com dado real).",
    "antes-e-depois": "Mostra o antes, a virada e o depois de uma situação (com caso ou foto real).",
    "frase-de-autoridade": "Uma frase forte de alguém real, com contexto e lição (só com fala real).",
}

# sequência de funções do roteiro para cada estrutura (o tamanho se ajusta ao tema)
SEQUENCIAS = {
    "mito-e-verdade": "gancho · contexto · virada · por que importa · como fazer · chamada",
    "erro-comum": "gancho · por que importa · exemplo · o que muda · como fazer · chamada",
    "passo-a-passo": "gancho (com o número de passos) · por que importa · passo × N · lição · chamada",
    "historia-de-caso": "gancho · contexto · virada · consequência · conceito · lição · chamada",
    "perguntas-e-respostas": "gancho · pergunta e resposta × 3 a 5 · chamada",
    "comparacao": "gancho · contexto · lado A · lado B · virada · lição · chamada",
    "guia-rapido": "gancho (com o número de itens) · por que importa · item × N · lição · chamada",
    "um-dia-na-rotina": "gancho · momento do dia × 3 a 5 · lição · chamada",
    "tema-que-vira-licao": "gancho · contexto · por que importa · virada · conceito · lição · chamada",
    "serie-de-anafora": "gancho com o bordão · bordão × 4 a 6 · lição · chamada",
    "dado-comparativo": "gancho · contexto · dado × 2 a 3 · conceito · lição · chamada",
    "antes-e-depois": "gancho · antes · virada · depois · lição · chamada",
    "frase-de-autoridade": "frase · contexto · lição · chamada",
}
PEDE_MATERIAL = {"historia-de-caso": "caso real", "dado-comparativo": "dado real com fonte",
                 "antes-e-depois": "caso ou foto real", "frase-de-autoridade": "fala real"}

# recursos de slide do repertório: o sorteio sugere 2 por carrossel, sem repetir os do anterior.
# A marca do cliente decide como cada um se veste; recurso que não combina com a marca não entra.
RECURSOS = {
    "anotacao-a-mao": "Frase curta inclinada com setinha, na fonte manuscrita/assinatura da marca (sem essa fonte, troque).",
    "palavra-impacto": "Uma palavra ou frase curta gigante numa faixa de borda a borda (máx. 1 por carrossel).",
    "marca-texto": "Cor clara da marca atrás de 1 a 3 palavras do apoio (1 por carrossel).",
    "selo-numerico": "Número do item em selo ao lado do título (guias e listas).",
    "dois-cartoes": "Comparativo 'sem x com' em dois cartões, o segundo na cor da marca.",
    "mockup-celular": "Tela de celular desenhada (só para assunto de app, rede ou mensagem).",
    "prova-real": "Print, manchete ou comentário real em cartão, com fonte (só com material real).",
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
    "capa-guia-numerado": "Número grande do guia + título; o número bate com a quantidade de itens.",
    "capa-serie": "Bordão gigante do quadro fixo ou da série, sempre com o mesmo desenho.",
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
    "isso-tem-nome": "'Isso tem nome: ...' com o conceito real em destaque e a explicação curta.",
    "licao-perguntas": "'O que isso muda em você / na sua empresa': ponte + 3 a 5 perguntas para o leitor.",
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
# Barra de progresso saiu em 2026-10-20 (Thiago). O indicador sorteado é só sugestão:
# perguntar ao Thiago, post a post, antes de montar (CLAUDE.md, pergunta 5).
INDICADORES = ["selo 'arraste' na capa + setinha até o penúltimo", "sem indicador"]


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
        if ult.get("estrutura") == s["estrutura"]:
            erros.append("mesma estrutura (tipo de post) do carrossel anterior")
        if set(ult.get("recursos", [])) & set(s["recursos"]):
            erros.append("recurso de slide repetido do carrossel anterior")
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
            "recursos": rng.sample(sorted(RECURSOS), 2),
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
    print(f"Sequência:  {SEQUENCIAS[s['estrutura']]}")
    if s["estrutura"] in PEDE_MATERIAL:
        print(f"            (pede {PEDE_MATERIAL[s['estrutura']]}; sem isso, sorteie de novo com outro --seed)")
    print(f"Gancho:     {s['gancho']}: {GANCHOS[s['gancho']]}")
    print(f"Fundos:     {s['ritmo']}: {RITMOS[s['ritmo']]}")
    print(f"Alinhamento: {s['alinhamento']} · texto apoiado: {s['apoio_do_texto']} · indicador (sugestão, confirmar com o Thiago): {s['indicador']}")
    print(f"Fotos nos slides: {s['slides_com_foto'] or 'nenhum'}")
    print("Recursos sugeridos: " + "; ".join(f"{r} ({RECURSOS[r]})" for r in s.get("recursos", [])) + "\n")
    for i, c in enumerate(s["composicao"], 1):
        print(f"  {i:>2}. {c:<24} {desc[c]}")
    print("\nRegras que valem por cima do sorteio (CLAUDE.md, 2026-10-20): capa nunca em fundo claro"
          "\n(pelo menos 2 capas por mês com foto full e véu da marca); fundo claro em no máximo 2"
          "\nslides; fotos full no miolo: 0 a 2, sorteadas; indicador perguntado (com ou sem)."
          "\nHistória primeiro: escreva começo, meio e fim; as composições acima podem trocar de lugar.")
    print("\nSe um slide pedir material que não existe (dado real, fala real, foto do cliente),"
          "\nre-sorteie com outro --seed em vez de inventar o material.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cliente", help="pasta do cliente (ex.: 'Sandra-Behrens')")
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
