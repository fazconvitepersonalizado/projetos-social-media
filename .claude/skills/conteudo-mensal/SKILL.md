---
name: conteudo-mensal
description: >-
  Planeja e produz o conteúdo mensal de Instagram de qualquer cliente desta
  pasta, em 3 fases (temas e formatos no chat → produção no plano local e no
  Trello → headline e legenda dos vídeos de terceiros/corte). Use quando o
  Thiago pedir para montar, planejar ou produzir o conteúdo de um mês para um
  cliente, ex.: "monta o conteúdo de novembro da Sandra", "plano do mês da
  A&J", "cria os posts de dezembro". Cobre também a Fase 3 (headline + legenda
  a partir da transcrição de um vídeo) e pedidos avulsos na voz do cliente
  (um carrossel ou legenda extra, sequência de stories, caixinha de
  perguntas). NÃO usar para alterar posts de um mês já produzido (ver
  alterar-conteudo), exportar o texto das artes (ver briefing-design),
  anexar artes no Trello (ver designs-no-trello) nem relatório de métricas
  (ver instagram-metrics-report).
---

# Conteúdo mensal

Produz o conteúdo de Instagram de um cliente, mês a mês, em **3 fases**:
Fase 1 (temas e formatos, no chat) → Fase 2 (produção no plano local, com
espelho no Trello) → Fase 3 (reativa: headline e legenda dos vídeos).

## O que o Thiago fornece
- **Cliente** e **mês** (ex.: "Sandra", "novembro").
- Se faltar um dos dois, perguntar. Se o cliente for ambíguo, perguntar qual.

## De onde vem a voz do cliente (ordem de leitura)
Não existe ficha de cliente dentro desta skill: a identidade vem da pasta
do cliente, que já é a fonte única do projeto. Ler nesta ordem e parar de
procurar só quando tiver voz, pilares, restrições, CTA e frequência:

1. `<cliente>/estrategia/base-estrategica.md` (fonte principal: pilares,
   tom, formatos e frequência, primeiros temas, restrições, "a confirmar").
2. `<cliente>/skills/marca-<slug>/SKILL.md` (tom, expressões, restrições,
   estrutura do carrossel de 8 cards, frequência). Ver skill `marca-cliente`.
3. `<cliente>/brand-kit.json` (`tone`, `language`, `brand_manual`: voz,
   pilares, frases de exemplo) + `<cliente>/README.md`.
4. Carrosséis já feitos em `<cliente>/conteudos/` (temas já tratados e tom
   real usado; também para não repetir tema).
5. Calendário já aprovado em `<cliente>/apresentacoes/**/calendario.md`, se
   existir: é o **ponto de partida** da Fase 1 para o mês que ele cobre.

Se não houver voz ou pilares definidos em nenhum desses lugares, **não
inventar**: avisar e oferecer criar a marca pela skill `marca-cliente` (ou o
fluxo `novo-cliente`, se for cliente novo). Cadência ou rotação de formatos
que não estiverem em lugar nenhum: perguntar ao Thiago (escolhas fechadas) e
oferecer registrar a resposta na marca do cliente.

Referências desta skill:
- `references/formatos.md`: o **como** de cada formato.
- `references/plano-mensal.md`: modelo do arquivo do mês (fonte da verdade).
- `references/trello.md`: **onde/como** espelhar no Trello (quadro, listas,
  etiquetas, cartão, registro de IDs `trello.json`).

## Fase 1: temas e formatos (no chat)
1. Ler a marca do cliente (ordem acima). Calcular quantos posts o mês tem
   pela **cadência** do cliente e as **datas reais** de cada post (dias da
   semana certos, feriados avisados, não chutar).
2. Se houver `calendario.md` aprovado para o mês, partir dele (mesmos temas,
   formatos e datas), completando só o que faltar.
3. Aplicar a **rotação de formatos** do cliente para sugerir um formato por
   post, respeitando o pacote contratado e restrições (ex.: não grava vídeo).
   Conferir a rotação descrita contra o histórico real (pastas em
   `conteudos/`, planos anteriores, cartões em `Publicado`): às vezes a
   praticada difere da descrita; se diferir, mostrar e perguntar qual vale.
4. Para cada post de **conteúdo** (carrossel, post único, frase, roteiro),
   sugerir **tema principal + 2 alternativas**, na voz e nos pilares do
   cliente, com etiqueta de origem ([B]/[P]/[S]) e sem repetir tema já
   publicado em `conteudos/`. Posts de **vídeo** (terceiros, corte) entram
   como **slot**, sem tema.
5. Apresentar a tabela **do mês inteiro, agrupada por semana**
   (`# | Dia | Formato | Pilar | Tema | Alternativas`). Nunca uma amostra.
6. **Pausa obrigatória para o OK.** O Thiago troca formatos, troca temas
   (pelas alternativas), corta ou acrescenta. Só avançar com aprovação
   explícita.

## Fase 2: produção
Só depois do OK da Fase 1.
1. Criar/atualizar `<cliente>/conteudos/planos/<AAAA-MM>.md` conforme
   `references/plano-mensal.md`, com o calendário aprovado.
2. Para cada **carrossel**, rodar o sorteio na raiz do projeto antes de
   escrever a copy:
   `python sorteio_carrossel.py "<pasta do cliente>" --tema "<tema>" --slides 8`.
   Escrever os 8 cards seguindo a estrutura e o gancho sorteados e anotar no
   post "Sorteio: estrutura · gancho · seed". Quando a arte for produzida
   depois (skill `instagram-carousel`), **reaproveitar esse sorteio** (mesmo
   `--seed`, ou o resultado anotado) em vez de sortear de novo, para a arte
   bater com a copy aprovada.
3. Escrever cada post de conteúdo no modelo do formato (`formatos.md` + voz
   do cliente). Slots de vídeo: só o cabeçalho `POST NN · [terceiros]`.
4. **Revisão anti-IA** de toda copy por `references/anti-ia-copy.md` da skill
   `instagram-carousel` do cliente; anotar a nota (mínimo 35/50; abaixo
   disso, reescrever antes de mostrar). A voz do cliente fica.
5. Mostrar o mês produzido no chat (pode ser por blocos de semana) e pedir o
   OK do conteúdo.
6. **Espelhar no Trello** (`references/trello.md`): localizar o quadro do
   cliente pelo `trello.json` (ou propor criar), mostrar o que será
   criado (N cartões, lista `Em produção`, etiquetas) e **confirmar antes de
   escrever em massa**. Cada cartão: nome `POST NN · [formato] tema`, data =
   dia do post, etiquetas mês + formato (+ pilar), descrição no modelo.
   Anotar o link de cada cartão no plano.
7. Commit local quando o mês estiver aprovado (protocolo de salvamento do
   `CLAUDE.md` da raiz) e avisar o que foi salvo.

**Arte:** esta skill produz o **texto**. A arte dos carrosséis sai pela skill
`instagram-carousel` do cliente (com todas as perguntas e verificações
obrigatórias do `CLAUDE.md`); peças desenhadas por outra pessoa usam o texto
exportado pela skill `briefing-design`.

## Fase 3: reativa (vídeos de terceiros/corte)
Quando o vídeo de um slot chegar (anexo/comentário no cartão, link do Drive
ou arquivo no chat):
1. Obter a **transcrição** (o arquivo de vídeo em si não é legível):
   - pelo navegador, abrindo o link do Drive e o painel de transcrição
     (requer sessão iniciada); ou
   - texto ou **print** do painel de transcrição enviado pelo Thiago.
2. Gerar **headline** (vira o nome do post: `POST NN · [formato] headline`)
   + **legenda curta**, na voz e nas regras do cliente, sem transcrever o
   vídeo: destilar a mensagem central.
3. Atualizar o plano local e, depois do OK, o cartão no Trello.

## Pedidos avulsos e stories (fora do plano mensal)
Quando o pedido for uma peça única (carrossel ou legenda extra, sequência de
stories, caixinha de perguntas, headlines para um vídeo), **não precisa do
fluxo das 3 fases**:
1. Ler a marca do cliente (ordem acima).
2. Produzir a peça seguindo `formatos.md` e a marca (carrossel avulso: o
   modo rápido de 8 cards da marca do cliente já cobre).
3. Entregar no chat; salvar no plano do mês ou criar cartão no Trello só se
   o Thiago pedir.

## Regras transversais
- **Voz, CTA, tabus e idioma** vêm SEMPRE da marca do cliente. Nunca
  inventar nem presumir; o que faltar vira pergunta ou "a confirmar".
- Idioma padrão: **português do Brasil**, salvo se a marca do cliente
  definir outro.
- O que já existe no projeto tem prioridade: estrutura de 8 cards, sorteio,
  regras anti-IA, regra de não usar travessão, verificação visual das artes.
- Nunca mexer no Trello sem confirmação quando for criar, editar ou mover
  vários cartões.
