# Design sem cara de IA

Regras de design para todo carrossel, derivadas do Impeccable (Paul Bakaus,
Apache 2.0; 61 regras automáticas de "visual de IA") e testadas em
2026-10-19 no carrossel "Carboidrato à noite engorda?" (Marina Couto): o
detector caiu de 15 problemas para 0 problemas reais. Vencem
`references/design-system.md` em caso de conflito.

## 1. A individualidade do cliente vem antes de tudo

Estas regras tiram **vícios genéricos de template**, não a identidade do
cliente. Cada cliente tem que continuar parecendo ele mesmo, e diferente
dos outros clientes da pasta.

- Antes de montar, leia a marca do cliente: `brand-kit.json`, a skill
  `skills/marca-<slug>/SKILL.md` (se existir), o manual e os carrosséis já
  aprovados em `conteudos/`.
- Cores, fontes, logo, tom, modelos de peça do manual e elementos que o
  cliente aprovou como dele **ficam**, mesmo que apareçam na lista abaixo.
  Ex.: se um cliente tem o degradê dourado como assinatura aprovada, ele
  continua, usado com intenção (ex.: só no CTA), não como fundo padrão de
  todo slide.
- Na primeira vez que um cliente passar por estas regras, liste para o
  Thiago o que nos carrosséis aprovados dele parece assinatura (fica) e o
  que parece vício do template antigo (sai), e confirme antes de mudar.
  Grave a decisão no README/brand-kit/skill de marca do cliente.
- Nunca copie a solução visual de um cliente para outro (paleta, fonte,
  elemento desenhado). O que é compartilhado é o princípio, não a cara.

## 2. O que não usar (vícios de template)

| Vício | Por quê | No lugar |
|---|---|---|
| Etiqueta em maiúsculas espaçadas acima do título ("O QUE CONTA", "DICA PRÁTICA"), com tracinho embaixo | É o sinal de template de IA mais citado; repetido em todo slide vira carimbo | O título carrega o assunto. Numeração "n/total" no rodapé pode. |
| Granulado (`feTurbulence`) | Lê como amador | Fundo limpo |
| Brilho difuso / degradê radial em malha como fundo padrão | O detector marca como "spotlight glow" de IA | Fundos chapados nas cores da marca. Degradê só se for assinatura do cliente (item 1). |
| Enfeite sem função em todo slide ("+" de canto, monograma marca-d'água, "01 / 07" no topo) | Decoração repetida = template | Só o que informa (numeração no rodapé, logo na capa e no CTA). |
| Itálico colorido em uma palavra de todo título | Virou o "editorial" padrão de IA | No máximo 1 ou 2 itálicos por carrossel, onde a marca pede. |
| Pílulas, card de vidro, caixa arredondada com sombra suave para texto, ícone em quadradinho arredondado | Parece interface de app, não peça editorial | Texto direto no fundo; lista simples. |
| Borda colorida lateral em citação | Vício de template | Citação grande em tipografia, sem borda. |
| Número gigante + legenda pequena (Big Stat) por obrigação | "Hero metric" genérico | Só com dado real que sustenta o slide. |
| Mesma composição em todo slide | Monotonia | Composição sorteada (`sorteio_carrossel.py`). |
| Fonte da moda que todo gerador usa (Inter, Plus Jakarta Sans, Space Grotesk, Fraunces) em marca nova | O detector marca como "overused font" | Na marca nova, escolher outra. Em marca existente, a fonte do cliente fica (item 1). |

## 3. O que fazer

- **Título e texto de apoio no mesmo bloco** (16 a 20px entre eles). Nunca
  um título no topo e o apoio lá embaixo com um vão no meio
  (proximidade: o que é relacionado fica junto).
- **Slide cheio de propósito**: ou o bloco de texto ocupa o slide com
  tipografia grande, ou divide o espaço com uma foto ou um elemento
  desenhado. Metade de slide vazia só se for intenção clara.
- **Contraste de escala**: títulos grandes (40 a 58px no slide de 420px),
  corpo de 17 a 18px, nada abaixo de 12px.
- **Elementos desenhados com função**, em SVG exato e nas cores da marca:
  linha do dia, prato dividido, escala, antes/depois, comparação. Nada de
  ilustração "fofinha" ou ícone decorativo.
- **Fotos**: no máximo 1 a cada 3 slides; mostram exatamente o que o texto
  daquele slide diz; estilo variado (slide inteiro, dividindo o slide,
  emoldurada); tratamento conforme a escolha da rodada (vívida/suave).
- **Fonte de título sem defeito de desenho**: confira o título grande no
  render. Se a fonte tiver eixos "estranhos" (ex.: Fraunces tem `WONK`, que
  entorta n/m/h), carregue com `opsz` e desligue o eixo
  (`font-variation-settings:'WONK' 0`), ou proponha outra fonte ao Thiago.

## 4. Detector automático (na verificação visual)

Depois do render, rode o detector do Impeccable no HTML (sem instalar
nada no projeto):

```
npx -y impeccable@4.7.0 detect --no-config <caminho>/carousel.html
```

Ignore achados da moldura falsa do Instagram (cabeçalho, legenda, "2 HORAS
ATRÁS", `#888`/`#999` em fundo branco), textos de SVG lidos como preto
(o detector não lê o `fill`), e fotos que encostam na borda de propósito.
Fonte da marca marcada como "overused" e itálico pedido pela marca ficam
(item 1). O resto entra no relatório da verificação visual, e como em
toda a verificação visual, avise antes de corrigir.
