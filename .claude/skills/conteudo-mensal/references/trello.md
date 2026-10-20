# Estrutura no Trello

Referência compartilhada pelas skills `conteudo-mensal`, `alterar-conteudo`,
`briefing-design` e `designs-no-trello`. Estrutura aprovada pelo Thiago em
2026-10-19: **um quadro por cliente, listas por etapa, mês como etiqueta**.

## Regra de ouro: a pasta local é a fonte da verdade
- O conteúdo vive em `<cliente>/conteudos/planos/<AAAA-MM>.md` (plano do mês)
  e em `<cliente>/conteudos/<AAAA-MM-DD>-<slug>/` (carrossel com arte), tudo
  versionado no git.
- O Trello é o **espelho** para organizar, entregar e aprovar. Toda escrita no
  Trello sai do arquivo local; se os dois divergirem, avisar o Thiago e
  perguntar qual vale antes de sobrescrever qualquer lado.

## Acesso
- Pelo conector do Trello. Os nomes das ferramentas variam conforme o
  conector; localizar com `ToolSearch` (busca "trello") antes da primeira
  chamada.
- Se as ferramentas do Trello não aparecerem na sessão, **dizer isso
  exatamente** (não fingir que escreveu), seguir só com os arquivos locais e
  deixar anotado no plano o que falta espelhar ("Pendente no Trello").
- Limites do conector do claude.ai (testado em 2026-10-19): cria quadro,
  lista e cartão, edita, move, comenta e liga/desliga etiqueta que **já
  existe**, mas **não cria nem renomeia etiquetas** e **não envia anexos**.
  O que falta é feito pela API oficial com a chave do Thiago
  (`TRELLO_KEY`/`TRELLO_TOKEN` no `.env`, fora do git), pelo script
  `conteudo-mensal/scripts/trello_api.py`:
  `etiquetas "<cliente>" [AAAA-MM]` cria/nomeia as etiquetas de formato e
  de mês e grava os IDs no `trello.json` (rodar ao abrir cada mês novo);
  `anexar <cartão> <arquivos>` sobe os PNGs. Sem `.env`, dizer isso e não
  inventar etiqueta.
- Ler é ação sem efeito. **Criar, editar, mover ou anexar** é ação com efeito:
  mostrar o que vai ser feito e esperar o OK antes de escrever em massa.

## Quadro por cliente
- Nome: `<Nome do cliente> · Conteúdo` (ex.: `Sandra Behrens · Conteúdo`).
- Listas, nesta ordem:
  1. `Gaveta` (ideias e temas reserva; equivale ao "POST [GAVETA]")
  2. `Planejado`
  3. `Em produção`
  4. `Aprovação do cliente`
  5. `Ajustes`
  6. `Agendado`
  7. `Publicado`
- Etiquetas:
  - **Mês:** `Nov/2026`, `Dez/2026`… (uma por mês, criada quando o mês começa).
  - **Formato:** `carrossel`, `post único`, `frase`, `roteiro`, `reels`,
    `terceiros`, `corte`, `stories`.
  - **Pilar** (opcional): os pilares da base estratégica/marca do cliente.

### IDs de cada cliente (registro local)
Na primeira vez que um cliente for usado com o Trello, guardar os IDs em
`<cliente>/trello.json` (não é segredo; vai para o git):

```json
{
  "quadro": {"id": "...", "nome": "Sandra Behrens · Conteúdo", "url": "..."},
  "listas": {"Gaveta": "...", "Planejado": "...", "Em produção": "...",
             "Aprovação do cliente": "...", "Ajustes": "...",
             "Agendado": "...", "Publicado": "..."},
  "etiquetas": {"Nov/2026": "...", "carrossel": "...", "post único": "..."},
  "atualizado_em": "AAAA-MM-DD"
}
```

- Se `trello.json` não existir: procurar o quadro pelo nome. Se não existir,
  **propor criar** (quadro + listas + etiquetas), esperar o OK, criar e salvar
  os IDs.
- Se uma lista ou etiqueta do registro sumir (renomeada/apagada no Trello),
  avisar em vez de recriar sozinho.
- Nunca guardar token, chave ou senha nesse arquivo nem em lugar nenhum do
  projeto fora do `.env`.

## Cartão de post (formato aprovado em 2026-10-19)
Página de aprovação e cartão saem da MESMA fonte (manifesto da página +
plano do mês), montados pelo script
`.claude/skills/pagina-aprovacao/scripts/sincronizar_trello.py cartoes`.
Não escrever o cartão à mão quando houver página do mês.
- **Nome:** `DD/MM · POST NN · Formato · tema` (data na frente para o
  quadro ficar em ordem; NN numerado dentro do mês; ex.:
  `17/09 · POST 03 · Post único · Quanto custa não prevenir?`).
  Slots de vídeo sem tema: `DD/MM · POST NN · Terceiros`.
- **Data de entrega (due):** a data do post, 09:00 de Brasília (12:00Z).
- **Etiquetas:** mês + formato, criadas e nomeadas pelo `trello_api.py
  etiquetas` (formato com cor fixa: carrossel verde, post único amarelo;
  mês com cor em rodízio). IDs no `trello.json`; o conector só as aplica
  nos cartões. Nunca pedir ao Thiago para cadastrar etiqueta à mão.
- **Descrição em seções (Markdown):** linha de resumo (data, dia da semana,
  formato, nº de slides) + link da página de aprovação do mês + caminho dos
  arquivos; `## Legenda` (pronta para copiar); `## Texto da arte` com
  `**Slide N · capa/encerramento**`; `## Aprovação` (aguardando, aprovado,
  ou os pedidos de ajuste por slide e o comentário geral da cliente).
- **Checklist "Etapas":** Texto revisado, Arte pronta, Enviado para
  aprovação, Aprovado pela cliente, Agendado, Publicado; marcar conforme a
  lista em que o cartão está.

## Página de aprovação ↔ Trello (os dois sempre iguais)
- **Antes de gerar ou republicar a página de um mês:** ler os cartões do
  mês pelo conector, gravar em `<cliente>/aprovacao/<AAAA-MM>/trello-export.json`
  (`{"cartoes": [{"nome","desc","due","lista","url"}]}`) e rodar
  `sincronizar_trello.py comparar`. Diferença encontrada (post só de um
  lado, data, legenda ou texto de um slide): **mostrar ao Thiago e ele
  escolhe qual lado vale**; o escolhido atualiza o outro (Trello vence →
  plano/carousel.html via aplicar_respostas; local vence → cartão).
- **Depois de gerar:** `sincronizar_trello.py cartoes` e gravar nome,
  descrição, etiquetas e checklist de cada cartão.
- **Quando a cliente responde:** seção `## Aprovação` do cartão recebe a
  decisão e os pedidos por slide, checklist marca "Aprovado pela cliente"
  e o cartão vai para `Agendado` ou `Ajustes` (confirmando antes).
- Todo post em `Aprovação do cliente` precisa estar numa página de
  aprovação, e vice-versa.

## Formato antigo (até 2026-10-19, só referência)
- **Nome:** `POST NN · [formato] tema`.
- **Etiquetas:** mês + formato (+ pilar, se houver).
- **Lista inicial:** `Planejado` na Fase 1 aprovada; `Em produção` quando o
  conteúdo for escrito; daí em diante o Thiago (ou a skill, se ele pedir)
  move.
- **Descrição** (texto simples, mesma estrutura do plano local):

  Carrossel:
  ```
  Referências e observações:
  <links, pedidos do cliente, ou "nenhuma">

  Texto da arte:
  Card 1 (headline)
  <texto>
  Card 2
  <texto>
  ...
  Card 8 (encerramento)
  <texto>

  Legenda:
  <legenda>

  Arquivo local: <cliente>/conteudos/planos/<AAAA-MM>.md (POST NN)
  ```

  Post único ("leia legenda"):
  ```
  Referências e observações:

  Texto da arte:
  Arte única com a headline
  <headline>

  Legenda:
  <legenda com os pontos>

  Arquivo local: ...
  ```

  Frase: `Texto da arte:` com a frase; `Legenda:` curta.
  Roteiro: `Roteiro:` com as falas; `Legenda:`.
  Terceiros/corte: descrição em branco até o vídeo chegar (Fase 3).

- **Anexos:** os PNGs finais, na ordem dos slides (ver skill
  `designs-no-trello`).

## Achar os posts de um mês
1. Ler `<cliente>/trello.json` para o ID do quadro e da etiqueta do mês.
2. Listar os cartões do quadro (todas as listas) e filtrar pela etiqueta do
   mês. Nunca filtrar só pela lista: um post do mês pode estar em qualquer
   etapa.
3. Casar pelo número `POST NN` do nome. Os números podem não ser contínuos;
   casar pelo número, não pela ordem.
4. Ignorar cartões da lista `Gaveta`, a não ser que o pedido seja sobre ela.

## Fase 3: vídeo de terceiros/corte
- O vídeo chega como anexo ou comentário no cartão (muitas vezes link do
  Google Drive), ou como arquivo/print enviado no chat.
- O arquivo de vídeo em si não é legível. A transcrição vem de: (a) painel de
  transcrição do Drive aberto no navegador, (b) texto colado pelo Thiago, ou
  (c) print do painel de transcrição.

## Lista Publicado → página de aprovação
A lista `Publicado` é a fonte de "o que já foi ao ar" para a grade da skill
`pagina-aprovacao`. Mover para `Publicado` só o que foi publicado de fato,
com a data de entrega igual à data real do post. Antes de gerar uma página
de aprovação, exportar essa lista para `<cliente>/trello-publicados.json`
(formato e passos no `SKILL.md` da `pagina-aprovacao`).

## Quadro de trends
Quadro separado, usado pela skill `trend-finder` (estrutura descrita lá).
