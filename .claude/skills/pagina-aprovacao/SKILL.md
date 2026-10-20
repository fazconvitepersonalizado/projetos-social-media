---
name: pagina-aprovacao
description: >-
  Gera a página de aprovação de posts do mês para a cliente: feed do perfil
  em grade, carrossel deslizante com os slides reais, legenda, edição dos
  textos dos slides ao vivo (como no painel do instagram-carousel) e decisão
  por post (aprovar / pedir ajuste + comentário). Sai como link do claude.ai
  e como arquivo HTML. Depois lê as respostas (banco da página, WhatsApp ou
  dados colados) e aplica os textos aprovados nos carousel.html. Use quando o
  Thiago pedir "página de aprovação", "manda pra cliente aprovar", "validação
  dos posts", "link de aprovação do mês", ou trouxer as respostas de uma
  cliente para aplicar.
---

# Página de aprovação de posts

Página que a cliente abre para **ver, ajustar e aprovar** os posts do mês.
Adaptada de um modelo de terceiros: a identidade é **a marca da própria
cliente** (cores, fontes e logo do `brand-kit.json`), sem assinatura de
agência, e os slides são os `carousel.html` reais, então os textos podem ser
editados ao vivo, como no painel do template atual.

## Organização (na pasta da cliente)
```
<cliente>/aprovacao/
├── index.html               # todos os meses: capas, nº de posts, "Abrir página", "Link da cliente"
├── links.json               # {"AAAA-MM": "<link do claude.ai>"}, atualizado a cada publicação
└── <AAAA-MM>/
    ├── aprovacao.html           # arquivo para mandar
    ├── aprovacao-artifact.html  # versão publicada no claude.ai
    ├── manifesto.json           # posts, arquivos de origem e campos
    ├── miniaturas/NN.jpg        # capas (usadas no índice)
    └── respostas.json           # quando as respostas chegarem
```
O índice é refeito a cada geração. Depois de publicar um mês, gravar o link
em `links.json` e refazer o índice (`gerar_indice` do script).

## O que a página faz
- **Barra lateral (marca da cliente):** seletor **Mês** em dropdown com
  todos os meses da cliente ("Setembro de 2026 · 6 posts"; o atual vem
  marcado; escolher outro abre a página daquele mês: caminho local no
  arquivo, link do claude.ai em outra aba na versão publicada; mês sem
  página aparece desativado, "· sem página"), progresso do mês, lista dos
  posts (miniatura, número, título, data, situação) e "Enviar respostas".
  No celular vira menu ("Posts e meses").
- **Divisão por mês na grade:** divisória "Mês · N posts para aprovar"
  acima dos novos e "Mês · N publicados" acima dos de cada mês anterior.
- **Perfil no formato do Instagram (compacto, até 700px):** cabeçalho
  do perfil (logo como foto, @, nome, bio = `bio` ou `brand_manual.tagline`
  do brand-kit; números só do que existe: posts novos e já publicados, nunca
  seguidores inventados), abas e grade 3 colunas em **3:4**, que corta as
  bordas como o Instagram faz hoje.
- **Posts publicados** (até `--anteriores`, padrão 9) aparecem esmaecidos
  abaixo dos novos, para a cliente ver como o mês encaixa no feed. **Fonte:
  a lista `Publicado` do Trello da cliente**, exportada antes de gerar (ver
  "Registro de publicados"). Sem esse registro, a página não afirma
  publicação: mostra as pastas de meses anteriores de `conteudos/` como
  "anterior · não confirmado".

## Registro de publicados (antes de gerar)
1. Com o conector do Trello disponível, ler `<cliente>/trello.json` e listar
   os cartões da lista `Publicado` (ver `conteudo-mensal/references/trello.md`).
2. Para cada cartão, achar a pasta da arte: linha "Arquivo local" da
   descrição → post do plano do mês → `Pasta da arte:`. Data = data de
   entrega (due) do cartão, que é a data do post.
3. Gravar `<cliente>/trello-publicados.json` (vai para o git, não tem
   segredo):
   ```json
   {"atualizado_em": "AAAA-MM-DD", "fonte": "Trello · lista Publicado",
    "posts": [{"cartao": "POST 03 · [carrossel] tema", "data": "AAAA-MM-DD",
               "pasta": "conteudos/AAAA-MM-DD-slug", "url_cartao": "https://trello.com/c/..."}]}
   ```
4. Cartão publicado sem pasta encontrada (ex.: post feito fora daqui) fica
   fora da grade; avisar o Thiago quais foram.
5. Sem Trello na sessão: dizer isso, não criar o arquivo e gerar mesmo
   assim (sai "não confirmado"). Arquivo antigo: avisar a data de
   `atualizado_em` antes de usar.
- **Post aberto no formato do Instagram:** mídia à esquerda e coluna com
  cabeçalho do @, legenda como comentário do @ (hashtags/menções
  destacadas) com botão "Copiar legenda", ícones e data; no celular e no
  tablet em pé, tela cheia como no app. Slides
  deslizam com setas, pontos, arrasto e teclado; reel com capa e play.
  Fecha com X, Esc ou clique fora; setas laterais trocam de post.
- Sem logo nem nome do Instagram: só o formato visual; a página é da cliente.
- **Editar textos:** cada texto de cada slide vira um campo; a arte muda na
  hora. `[[trecho]]` mantém o destaque do design (span/em/strong); quebra de
  linha vira `<br>`. A legenda também é editável. "Desfazer" volta ao
  original. Pontinho laranja nos slides alterados.
- **Decisão por post:** Aprovar / Pedir ajuste + comentário. Em carrossel,
  "Pedir ajuste" abre o campo **"Ajuste no slide N de M"**, que acompanha o
  slide aberto: a cliente passa os slides e escreve em cada um; slides com
  pedido ganham contorno no pontinho e aparecem em "Pedidos em: Slide 2,
  Slide 5" (clicáveis). O comentário vira "Comentário geral do post".
  Salvo em `ajustes` (`{"3": "texto"}`), no banco, no resumo do WhatsApp e
  no "Copiar dados completos".
- **Enviar respostas:** resumo de tudo + botão do WhatsApp (mensagem pronta
  para o número em `config.json`) + "Copiar resumo" + "Copiar dados
  completos" (JSON com os textos alterados, para colar aqui).

## Como as respostas voltam (as duas vias ficam ligadas)
1. **Banco da página** (só no link do claude.ai): grava cada resposta
   sozinho na coleção `respostas`, um documento por post. Só funciona para
   quem pode gravar: o Thiago, membros da organização como Contributor ou
   acima, e pessoas de fora **convidadas por e-mail como Editor** (e só
   enquanto a página não estiver compartilhada por link público). Quem abre
   por link público ou como Viewer só lê; para essa pessoa a página mostra
   que as respostas vão pelo envio.
2. **WhatsApp / copiar:** funciona para qualquer pessoa, no link e no
   arquivo. É a via garantida para clientes sem conta no claude.ai.

## Fluxo

### 0. Conferir com o Trello (página e cartões sempre iguais)
Antes de gerar ou republicar: ler os cartões do mês, gravar
`<cliente>/aprovacao/<AAAA-MM>/trello-export.json` e rodar
```bash
python .claude/skills/pagina-aprovacao/scripts/sincronizar_trello.py comparar "<pasta do cliente>" <AAAA-MM> "<cliente>/aprovacao/<AAAA-MM>/trello-export.json"
```
Cada diferença (post só de um lado, data, legenda, texto de um slide) vai
para o Thiago escolher qual lado vale. Depois de gerar, `... cartoes` monta
nome, descrição, etiquetas e checklist dos cartões a partir do mesmo
manifesto da página; gravar no Trello pelo conector. Formato do cartão e
regras em `conteudo-mensal/references/trello.md`.

### 1. Gerar
Na raiz do projeto:
```bash
python .claude/skills/pagina-aprovacao/scripts/gerar_aprovacao.py "<pasta do cliente>" <AAAA-MM>
```
- Posts: do plano do mês (`conteudos/planos/<AAAA-MM>.md`: número, legenda
  e "Pasta da arte") se existir; senão, todas as pastas
  `conteudos/<AAAA-MM>-*` com `carousel.html`. `--posts` escolhe pastas;
  `--arquivo pasta=carousel-foto.html` usa outra versão do HTML.
- Legenda: a do plano; se não houver, a do `.ig-caption` do carrossel.
  Post sem legenda aparece como "sem legenda cadastrada"; avisar o Thiago.
- **Legenda pronta para busca (regra desta página, pedido do Thiago em
  2026-10-19):** antes de gerar, conferir se cada legenda do plano tem
  palavra-chave do assunto na primeira linha e de novo no texto (do jeito
  que o público procuraria: "NR-1", "PGR", "menopausa", "saúde emocional da
  mulher"), um chamado no fim (salvar, comentar, agendar pelo link da bio)
  e **até 5 hashtags de nicho** no final (limite do Instagram), em
  CamelCase e sem acento. Legenda curta ou sem hashtag: reescrever no
  plano, na voz da marca e pela revisão anti-IA (sem travessão, sem fato
  novo), e espelhar no cartão do Trello. Na página, cada legenda tem o
  botão **Copiar legenda** (copia a versão atual, com as edições da
  cliente).
- **Só mandar para a cliente o que já passou pela aprovação interna** (copy
  revisada, verificação visual do `instagram-carousel` feita). Se houver
  duas versões do mesmo carrossel (ex.: `carousel.html` e
  `carousel-foto.html`), perguntar qual vai.
- Saída em `<cliente>/aprovacao/<AAAA-MM>/`: `aprovacao.html` (arquivo
  completo), `aprovacao-artifact.html` (para publicar) e `manifesto.json`.
  Limite de 16 MB no claude.ai; acima de 15 MB o script avisa (dividir o mês
  com `--posts`).

### 2. Conferir (uma vez)
Abrir `aprovacao.html` no navegador (Playwright) nas larguras 320, 390,
768, 1024 e 1440 e olhar: sem rolagem lateral (`scrollWidth` igual à
largura), grade, um post aberto com a legenda e o botão "Copiar legenda"
visíveis, a aba de edição. Até 960px o post abre em tela cheia (celular e
tablet em pé); acima disso, arte e legenda lado a lado. Problema
encontrado: **avisar antes de mexer** (regra do `CLAUDE.md`).

### 3. Entregar
- **Link:** publicar `aprovacao-artifact.html` com a ferramenta Artifact,
  `capabilities: {db: {}, user: {}}`, `icon: "check"`, título já vem do
  arquivo. Depois da primeira publicação, ler a coleção `respostas` uma vez
  (ArtifactData `list`) para confirmar que o banco responde. Republicar o
  mesmo arquivo atualiza o mesmo link (as respostas ficam).
- **Arquivo:** `aprovacao.html` (abre em qualquer navegador; precisa de
  internet só para as fontes).
- Explicar ao Thiago as duas vias de resposta e o convite por e-mail como
  Editor, se ele quiser que a cliente grave direto.

### 4. Trazer as respostas
- Do link: ArtifactData `list` da coleção `respostas` → salvar em
  `<cliente>/aprovacao/<AAAA-MM>/respostas.json`.
- Do WhatsApp/cópia: o Thiago cola o texto aqui. "Copiar dados completos"
  já é o JSON; o resumo do WhatsApp é lido e convertido para o mesmo
  formato (status, comentário, textos por slide, legenda).
- Mostrar um resumo por post (aprovado / aprovado com alterações / ajuste /
  sem resposta).

### 5. Aplicar (só depois do OK do Thiago)
```bash
python .claude/skills/pagina-aprovacao/scripts/aplicar_respostas.py "<pasta do cliente>" <AAAA-MM> "<cliente>/aprovacao/<AAAA-MM>/respostas.json"
```
Mostra antes → depois de cada texto. Conferir as mudanças da cliente pelas
regras do projeto (sem travessão, anti-IA, contraste) e **avisar** se algo
quebra uma regra antes de aplicar. Com o OK, rodar de novo com `--aplicar`.
Depois:
- textos alterados: rodar a verificação visual e a exportação do
  `instagram-carousel` de novo para esses carrosséis;
- legenda nova e status: atualizar o plano do mês;
- Trello: mover cartões (aprovado → `Agendado`; ajuste → `Ajustes`, com o
  comentário geral e os pedidos por slide no cartão, um por linha:
  "Slide 3: ..."), confirmando antes de mover em massa;
- commit local.

## Arquivos
```
pagina-aprovacao/
├── SKILL.md
├── config.json               # número do WhatsApp que recebe as respostas
├── assets/
│   ├── pagina.html           # página (CSS + JS); tokens e dados entram pelo gerador
│   └── campos.js             # regra única de localizar/ler/escrever os textos dos slides
└── scripts/
    ├── gerar_aprovacao.py    # carrosséis do mês → página + manifesto
    └── aplicar_respostas.py  # respostas → carousel.html (simula; --aplicar grava)
```

## Regras
- Identidade da cliente; nada de cor, fonte ou nome de outra marca.
- Logo sempre num chip claro (legível em tema claro e escuro).
- Copy da página sem travessão.
- Nunca aplicar edição da cliente sem mostrar antes → depois ao Thiago.
- A página não substitui a verificação visual nem a exportação: texto
  alterado pela cliente só vira PNG depois de passar pelo `instagram-carousel`.
