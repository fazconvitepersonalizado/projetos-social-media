---
name: briefing-design
description: >-
  Lê o conteúdo já produzido de um cliente num mês (plano local, com o
  Trello como alternativa) e devolve, EM TEXTO no chat, só o texto que vai
  na arte de cada post: os cards dos carrosséis e as headlines/frases das
  artes únicas, formatado limpo para desenhar, revisar ou mandar para
  aprovação. Use quando o Thiago pedir o conteúdo escrito de um mês "para
  desenhar / fazer o design / em texto / para o cliente aprovar", ex.: "me
  passa o texto das artes da Sandra de novembro", "exporta os carrosséis da
  A&J em texto", "lista o que tem pra desenhar no mês". Cobre pedidos
  parciais ("só os carrosséis", "posts 3, 5 e 7", "do 10 ao 15"). NÃO cria
  conteúdo (ver conteudo-mensal), NÃO gera a arte (ver instagram-carousel),
  NÃO é relatório de métricas (ver instagram-metrics-report).
---

# Briefing de design

Extrai o conteúdo **já produzido** de um cliente num mês e devolve, **em
texto no chat**, apenas o que vai **na arte**: os cards de cada carrossel e
as headlines/frases das artes únicas. Sem legenda, sem referências, sem CTA
de legenda: só o texto da arte.

Serve para três usos:
- passar para uma pessoa desenhar (designer ou o próprio Thiago no Canva);
- mandar para o cliente revisar o texto antes da arte;
- conferir rapidamente o mês inteiro.

Os carrosséis que o Claude desenha saem pela skill `instagram-carousel`, que
continua sendo o caminho principal da arte; esta skill não substitui nada
dela.

## O que o Thiago fornece
- **Cliente** e **mês** (ex.: "Sandra", "novembro").
- Opcional: filtro parcial; posts específicos (`3, 5, 7`, `do 10 ao 15`) ou
  por formato (`só os carrosséis`).

## Fluxo
1. **Ler o plano local** `<cliente>/conteudos/planos/<AAAA-MM>.md` (estrutura
   em `../conteudo-mensal/references/plano-mensal.md`).
2. **Se não houver plano local**, ler os cartões do Trello do cliente
   filtrando pela etiqueta do mês (`../conteudo-mensal/references/trello.md`:
   `trello.json` → quadro → cartões com a etiqueta). Avisar que o plano local
   não existe. Se houver dúvida sobre qual mês/ano, **confirmar** antes.
3. Se plano e Trello divergirem num post, usar o plano local e avisar qual
   post diverge.
4. **Extrair só o texto da arte** de cada post (regras abaixo).
5. **Devolver no chat** no formato de saída, na ordem do número do post.

Ler é ação sem efeito; não precisa confirmar. Nunca editar nada aqui.

## Como extrair o texto de cada formato
O formato está no **nome** do post: `POST NN · [formato] tema`. O texto da
arte está entre `Texto da arte:` e `Legenda:`. Sempre **descartar** a
legenda, "Referências e observações" e tudo que não for arte.

- **`[carrossel]`** → lista `Card 1`, `Card 2`… (8 no padrão do projeto).
  Cada card vira um **slide**, na ordem, com o texto tal e qual.
- **`[post único]`** → arte única; a linha depois de "Arte única com a
  headline" sai como **headline**.
- **`[frase]`** → a frase da arte sai como **frase**.
- **`[roteiro]` / `[reels]`** → vídeo: normalmente sem arte de texto. Se
  houver headline/título de capa, sai como **headline**; senão, marcar
  `(vídeo, sem arte)`.
- **`[terceiros]` / `[corte]`** → se já tem headline (Fase 3 feita), sai como
  **headline**; se está vazio, marcar `(aguardando vídeo)`.

A estrutura pode variar um pouco entre clientes e posts antigos. Ler com
critério: o objetivo é o **texto que vai na arte**, não a marcação exata.

## Formato de saída (texto no chat)
Cabeçalho com cliente + mês, depois um bloco por post, na ordem do número:

```
<Cliente> · <Mês>

POST 01 · [carrossel] <tema>
slide 1: <texto do card 1>
slide 2: <texto do card 2>
slide 3: <...>
...

POST 02 · [post único] <tema>
headline: <headline>

POST 03 · [frase] <tema>
frase: <frase>

POST 04 · [terceiros]
(aguardando vídeo)
```

Manter o texto dos slides/headline **exatamente** como está no plano (é o
que vai para a arte). Não reescrever, resumir nem "melhorar". Se um post não
tiver texto de arte, mostrar mesmo assim com a marcação entre parênteses,
para o calendário aparecer completo.

Se o Thiago pedir em arquivo (para mandar ao cliente ou designer), salvar o
mesmo conteúdo em `<cliente>/conteudos/planos/<AAAA-MM>-texto-das-artes.md`.

## Pedidos parciais
- **Posts específicos** ("3, 5 e 7", "do 10 ao 15") → só esses números.
- **Por formato** ("só os carrosséis") → só os posts desse formato.
- Sem filtro = mês inteiro.
