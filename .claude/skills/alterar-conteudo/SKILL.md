---
name: alterar-conteudo
description: >-
  Altera ou refaz posts que JÁ EXISTEM no plano mensal de um cliente desta
  pasta: mostra o que está lá hoje, sugere tema novo na voz do cliente e,
  depois do OK, reescreve o post no plano local e no cartão do Trello,
  mantendo o post no lugar (mesmo número, mesma data). É a dupla da
  conteudo-mensal e usa a mesma voz, formatos e estrutura. Use quando o
  Thiago pedir para alterar, mudar, trocar, refazer, regerar ou substituir o
  conteúdo de um ou mais posts de um mês, ex.: "altera o post 1 e 2 de
  novembro da Sandra", "muda o tema do post 5 da A&J", "refaz todos os
  carrosséis do mês", "troca o formato do post 7 pra frase". Cobre seleção
  por número ("post 1 e 2", "do 3 ao 8"), por formato ("todos os
  carrosséis") ou "todos". NÃO usar para criar o mês do zero (ver
  conteudo-mensal), exportar o texto das artes (ver briefing-design), anexar
  artes (ver designs-no-trello) nem relatório de métricas (ver
  instagram-metrics-report).
---

# Alterar conteúdo

Refaz posts **que já existem** no plano do mês: localiza, mostra o que está
lá hoje, sugere tema novo na voz do cliente e, depois do OK, **reescreve o
conteúdo mantendo o post no lugar** (mesmo `POST NN`, mesma data, mesmo
cartão). Nada é apagado: o plano e o cartão são editados.

## Esta skill é a dupla da `conteudo-mensal`
Não duplicar voz, formatos nem estrutura aqui. **Ler sempre** (mesma pasta
de skills):
- `../conteudo-mensal/SKILL.md`, seção "De onde vem a voz do cliente": a
  ordem de leitura da marca do cliente (base estratégica → marca-<slug> →
  brand-kit/README). **É a fonte da verdade.**
- `../conteudo-mensal/references/formatos.md`: mecânica de cada formato.
- `../conteudo-mensal/references/plano-mensal.md`: estrutura do plano local.
- `../conteudo-mensal/references/trello.md`: quadro, etiquetas, cartão e
  registro `trello.json`.

Se o cliente não tiver voz definida em nenhum desses lugares, **não
inventar**: oferecer criar a marca pela skill `marca-cliente`.

## O que o Thiago fornece
- **Cliente** + **mês** (ex.: "Sandra", "novembro").
- **Seleção** dos posts a alterar. Se não disser quais, **perguntar**.

## Seleção de posts (interpretar o pedido)
- **Por número:** "post 1 e 2", "posts 3, 5 e 7", "do 3 ao 8" (intervalo).
- **Por formato:** "todos os carrosséis", "as frases", "os roteiros":
  filtrar pelos posts cujo nome tem `[carrossel]`, `[frase]` etc.
- **Todos:** "altera o mês todo", "refaz tudo".

Só mexer nos posts selecionados. **Nunca** tocar nos outros. Ignorar a lista
`Gaveta` do Trello, a não ser que o pedido seja sobre ela.

## Fluxo

### 1. Localizar o mês
Abrir `<cliente>/conteudos/planos/<AAAA-MM>.md`. Se não existir, procurar
os cartões no Trello pela etiqueta do mês (`references/trello.md`) e avisar
que o plano local não existe (oferecer recriá-lo a partir do Trello antes de
alterar). Se houver dúvida sobre qual mês ou ano, **confirmar** antes.

### 2. Ler o estado atual
Ler os posts selecionados no plano local e, se houver cartão, no Trello. Se
os dois divergirem, mostrar a diferença e perguntar qual vale. Mostrar no
chat, por post: **nome atual + tema atual** (resumo de 1 linha), só como
referência. Não reescrever ainda.

### 3. Propor o novo (no chat): PAUSA OBRIGATÓRIA
Para cada post selecionado, sugerir **tema novo + 2 alternativas**, na voz,
pilares e restrições do cliente, diferente do tema antigo e sem repetir tema
já publicado. Apresentar numa tabela:
`POST NN | Formato | Tema atual → Tema novo | Alternativas`.
**Esperar o OK.** O Thiago troca temas (pelas alternativas), ajusta ou pede
mais. Só avançar com aprovação explícita. **Não escrever nada nesta fase.**

### 4. Reescrever (só depois do OK)
Para cada post aprovado:
1. **Carrossel:** rodar o sorteio de novo para o tema novo
   (`python sorteio_carrossel.py "<pasta do cliente>" --tema "<tema novo>" --slides 8`)
   e escrever os 8 cards seguindo o resultado; anotar o novo sorteio no post.
2. Escrever o conteúdo novo no modelo do formato (`formatos.md`) e passar
   pela **revisão anti-IA** (`anti-ia-copy.md` da skill `instagram-carousel`
   do cliente; mínimo 35/50).
3. **Substituir o bloco do post** no plano local; renomear para
   `POST NN · [formato] tema` (NN com zero à esquerda).
4. **Manter** data, etiqueta do mês e número, a menos que o Thiago peça para
   mudar. Não mexer na data só porque o tema mudou.
5. Mostrar o resultado e, com o OK, **atualizar o cartão existente** no
   Trello (nome, descrição, etiqueta de formato se mudou). Editar o cartão;
   **nunca** criar cartão novo nem arquivar o antigo. Reescrever vários
   cartões é ação com efeito: confirmar antes.
6. Se o post já tinha **arte produzida** (pasta em `conteudos/` ou anexos no
   cartão), avisar que a arte ficou desatualizada e perguntar se é para
   refazer pela `instagram-carousel`; não apagar anexos nem a pasta antiga.
7. Commit local ao concluir (protocolo do `CLAUDE.md` da raiz).

## Casos especiais
- **Trocar formato** ("transforma o carrossel em frase", "o post 7 vira post
  único"): muda o formato **e** o tema; reescrever no modelo do **novo**
  formato e ajustar o `[formato]` no nome e a etiqueta no Trello. Por padrão
  o formato se mantém; só trocar se o Thiago pedir.
- **Slots de vídeo** (`[terceiros]`/`[corte]`): normalmente não têm tema.
  "Alterar" aqui é ou trocar o slot por um post de conteúdo (sugerir formato
  + tema), ou regerar headline/legenda a partir da transcrição (Fase 3 da
  `conteudo-mensal`). Confirmar qual dos dois antes de escrever.
- **"Altera todos os carrosséis"**: filtrar os `[carrossel]` do mês, propor
  um tema novo para cada (tabela única) e seguir o fluxo a partir do passo 3.

## Regras transversais
- Voz, CTA, restrições e idioma vêm SEMPRE da marca do cliente. Nunca
  inventar.
- O tema novo precisa ser **diferente** do antigo (não é reformular o mesmo).
- Respeitar à risca o estilo do cliente e as regras gerais do projeto: sem
  travessão na copy, sem cara de IA, português do Brasil salvo indicação da
  marca.
- Só mexer nos posts pedidos; deixar todos os outros exatamente como estão.
