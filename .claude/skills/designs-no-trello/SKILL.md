---
name: designs-no-trello
description: >-
  Anexa as artes prontas de um cliente nos cartões certos do mês no Trello,
  na ordem dos slides, sempre confirmando o casamento arte → post antes de
  subir. Aceita as artes exportadas pela skill instagram-carousel (lidas a
  partir do plano do mês) ou artes de designer organizadas em UMA PASTA POR
  POST (post-05/ com os slides dentro, ou um .zip com essas pastas). Use
  quando o Thiago pedir para subir/organizar/anexar/colocar os designs (ou
  as artes, os finais) de um cliente num mês no Trello, ex.: "sobe as artes
  da Sandra de novembro no Trello", "anexa os finais da A&J nos posts",
  "coloca os designs do post 5". Cobre pedidos parciais ("só o post 5", "do
  3 ao 8"). NÃO produz conteúdo (ver conteudo-mensal), NÃO gera a arte (ver
  instagram-carousel), NÃO exporta texto (ver briefing-design) nem relatório
  de métricas (ver instagram-metrics-report).
---

# Designs no Trello

Fecha o ciclo da produção: as artes estão prontas e esta skill **anexa cada
arte no cartão certo** do mês no Trello. Dado **cliente + mês** e a origem
das artes, casa cada conjunto de arquivos com o `POST NN` e sobe na ordem,
depois de o Thiago **conferir e aprovar o casamento**.

Estrutura do quadro, etiquetas e registro de IDs:
`../conteudo-mensal/references/trello.md` (**ler primeiro**). Detalhes de
anexo: `references/anexos-trello.md`.

## O que o Thiago fornece
- **Cliente** e **mês** (ex.: "Sandra", "novembro").
- **Origem das artes** (perguntar se não estiver claro):
  - **A. Artes do Claude** (padrão): exportadas pela `instagram-carousel` em
    `<cliente>/conteudos/<AAAA-MM-DD>-<slug>/slides/`. O vínculo com o post
    está na linha `Pasta da arte:` de cada post do plano do mês.
  - **B. Artes de designer/Canva**: uma pasta por post (`post-05/`,
    `POST 05/`, `post 5/`, `05/`), com os arquivos na ordem do nome (`01,
    02, 03…` ou `slide1, slide2…`). Arte única = pasta com um arquivo.
    Aceita também um **.zip** com essas pastas.
- Opcional: filtro parcial ("só o 5", "do 3 ao 8").

## Fluxo

### 1. Mapear as artes
Rodar o script (lida com .zip, lixo de macOS/Windows e ordem natural dos
slides). Na raiz do projeto, com o mapa numa pasta temporária:

```bash
# A. artes do Claude, a partir do plano do mês
python .claude/skills/designs-no-trello/scripts/mapear_designs.py --plano "<cliente>/conteudos/planos/<AAAA-MM>.md" --out "<pasta temporária>/mapa.json"

# B. pastas por post
python .claude/skills/designs-no-trello/scripts/mapear_designs.py "<pasta das artes>" --out "<pasta temporária>/mapa.json"
```

Devolve, por post: número, pasta, nº de slides e a **lista de arquivos na
ordem**. Também `soltos` (artes fora de uma pasta de post reconhecível) e
`avisos` (pasta da arte inexistente, nada exportado). Se vier algo em
`soltos`, **avisar** e perguntar a que post pertence; não adivinhar.

**Só arte aprovada sobe:** no modo A, conferir que o carrossel já passou
pela exportação da `instagram-carousel` (Fase 5, com aprovação explícita);
se a pasta tiver só `carousel.html` sem `slides/`, avisar em vez de exportar
por conta própria.

### 2. Achar os cartões do mês no Trello
1. `<cliente>/trello.json` → ID do quadro e da etiqueta do mês. Se não
   existir, seguir `trello.md` (procurar o quadro pelo nome; se não houver,
   avisar: sem cartões não há onde anexar).
2. Listar os cartões com a etiqueta do mês (todas as listas, menos `Gaveta`)
   e guardar o `id` de cada `POST NN`.

### 3. Pré-visualizar o casamento e CONFIRMAR
Montar uma tabela **arte → POST NN** e mostrar **antes de anexar qualquer
coisa**. Sinalizar explicitamente:
- **Arte sem cartão** correspondente (ex.: `post-31`, que não existe no mês).
- **Cartão sem arte** (nenhuma arte enviada para aquele post): só informa,
  não é erro.
- **Cartão que já tem anexo**: anexar **adiciona** (não substitui); perguntar
  se é para somar ou pular esse.
- Nº de slides por carrossel, para bater o olho (ex.: "POST 05 → 8 slides").

Anexar é **ação com efeito**: só seguir depois do "pode subir". Com filtro
parcial, mostrar só esses posts.

### 4. Anexar
Para cada post aprovado, na **ordem dos slides** (slide 1, depois 2, 3…),
anexar o arquivo ao cartão pela ferramenta de anexo do conector do Trello
(ver `references/anexos-trello.md`, inclusive o plano B se o conector não
aceitar arquivo local). A ordem de envio é a ordem em que o Trello mostra os
anexos; respeitar a sequência mantém o carrossel na ordem certa.

### 5. Relatar
Resumir: quantos posts receberam arte, quantos slides cada um, o que ficou
de fora (`soltos`, artes sem cartão, cartões sem arte) e os avisos. Se algo
falhar no meio, dizer exatamente em que post parou; anexos já enviados não
se desfazem sozinhos. Anotar no plano local, em cada post, "Arte anexada no
Trello em <data>".

## Opcional: mover o cartão de lista
Por padrão a skill **só anexa** e não move cartão. Se o Thiago pedir ("e
manda para aprovação"), mover para a lista certa (`Aprovação do cliente`,
`Agendado`…), confirmando o nome exato da lista no `trello.json`.

## Regras
- **Nunca anexar sem o OK** sobre o casamento (passo 3).
- Casar pela **pasta/plano → número do post**, nunca pela ordem de upload.
- Carrossel: respeitar a ordem dos slides que o script devolveu.
- Não apagar nem substituir anexos existentes; só adicionar (e perguntar
  antes se o cartão já tinha arte).
- Em `soltos` ou dúvida de casamento, perguntar; não adivinhar o post.
