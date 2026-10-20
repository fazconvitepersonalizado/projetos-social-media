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
- **Barra lateral (marca da cliente):** seção **Meses** com todos os meses
  da cliente (atual em destaque; meses com página viram link: caminho local
  no arquivo, link do claude.ai na versão publicada; meses só com posts em
  `conteudos/` aparecem como "N publicados"), progresso do mês, lista dos
  posts (miniatura, número, título, data, situação) e "Enviar respostas".
  No celular vira menu ("Posts e meses").
- **Divisão por mês na grade:** divisória "Mês · N posts para aprovar"
  acima dos novos e "Mês · N publicados" acima dos de cada mês anterior.
- **Perfil no formato do Instagram (compacto, até 700px):** cabeçalho
  do perfil (logo como foto, @, nome, bio = `bio` ou `brand_manual.tagline`
  do brand-kit; números só do que existe: posts novos e já publicados, nunca
  seguidores inventados), abas e grade 3 colunas em **3:4**, que corta as
  bordas como o Instagram faz hoje.
- **Posts já publicados** (até `--anteriores`, padrão 9, das pastas de meses
  anteriores) aparecem esmaecidos abaixo dos novos, para a cliente ver como
  o mês encaixa no feed.
- **Post aberto no formato do Instagram:** mídia à esquerda e coluna com
  cabeçalho do @, legenda como comentário do @ (hashtags/menções
  destacadas), ícones e data; no celular, tela cheia como no app. Slides
  deslizam com setas, pontos, arrasto e teclado; reel com capa e play.
  Fecha com X, Esc ou clique fora; setas laterais trocam de post.
- Sem logo nem nome do Instagram: só o formato visual; a página é da cliente.
- **Editar textos:** cada texto de cada slide vira um campo; a arte muda na
  hora. `[[trecho]]` mantém o destaque do design (span/em/strong); quebra de
  linha vira `<br>`. A legenda também é editável. "Desfazer" volta ao
  original. Pontinho laranja nos slides alterados.
- **Decisão por post:** Aprovar / Pedir ajuste + comentário.
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
- **Só mandar para a cliente o que já passou pela aprovação interna** (copy
  revisada, verificação visual do `instagram-carousel` feita). Se houver
  duas versões do mesmo carrossel (ex.: `carousel.html` e
  `carousel-foto.html`), perguntar qual vai.
- Saída em `<cliente>/aprovacao/<AAAA-MM>/`: `aprovacao.html` (arquivo
  completo), `aprovacao-artifact.html` (para publicar) e `manifesto.json`.
  Limite de 16 MB no claude.ai; acima de 15 MB o script avisa (dividir o mês
  com `--posts`).

### 2. Conferir (uma vez)
Abrir `aprovacao.html` no navegador (Playwright) em largura de desktop e de
celular e olhar: grade, um carrossel aberto, a aba de edição. Problema
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
  comentário no cartão), confirmando antes de mover em massa;
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
