---
name: novo-cliente
description: Passo a passo de entrada de um cliente novo nesta pasta, do briefing aos primeiros carrosséis (pasta do cliente → briefing → manual da marca → apresentação de estratégia → carrosséis). Use quando disserem "cliente novo", "entrou um cliente", "começar um cliente", "onboarding" ou pedirem para retomar o onboarding de um cliente.
---

# Cliente novo: passo a passo

Esta skill só orquestra. Cada etapa chama a skill que já faz aquele trabalho
e segue todas as regras do `CLAUDE.md` da raiz (perguntas obrigatórias de
carrossel, chip de logo, verificação visual, sem travessão na copy, commit
local a cada marco).

```
1 Pasta  →  2 Briefing  →  3 Manual da marca  →  4 Apresentação  →  5 Carrosséis
            (aprovação)     (aprovação)           (aprovação)
```

Não pular etapa nem avançar sem o portão de aprovação da etapa anterior. Se
o Thiago pedir explicitamente para pular (ex.: "o cliente já tem manual"),
registrar isso em "Decisões fixadas" do `ONBOARDING.md` e seguir.

## Etapa 0 · Abertura (sempre)

1. Pegar o nome do cliente. Se não veio na mensagem, perguntar.
2. Se já existir uma pasta com esse nome (ou parecido), ler o
   `ONBOARDING.md` dela, dizer em uma linha em que etapa parou e retomar
   da primeira etapa não marcada. Cliente antigo sem `ONBOARDING.md`:
   criar o arquivo a partir de `_modelo-cliente/ONBOARDING.md`, marcando o
   que já existe na pasta.
3. Cliente novo: fazer de uma vez, como escolhas fechadas (AskUserQuestion):
   - O cliente já tem Instagram? (sim, com @ · não)
   - Como está o briefing? (já tenho respondido: vou colar/anexar ·
     vamos preencher agora juntos · gerar questionário pra enviar ao cliente)
   - Já existe manual de marca/logo? (sim, completo · só logo · nada)

## Etapa 1 · Pasta do cliente

A pasta vem primeiro porque é onde briefing, manual e apresentação são
salvos; se a sessão cair, nada se perde.

1. Confirmar o nome da pasta (como deve aparecer na galeria) e o slug.
2. Rodar na raiz: `python novo_cliente.py "Nome do Cliente"` (ou com
   `--slug`). O script copia `_modelo-cliente/` e preenche README e
   `ONBOARDING.md`. Nunca sobrescreve pasta existente.
3. Se o Thiago enviou arquivos de logo, copiar para `<cliente>/logo/` como
   `logo-primary`, `logo-white`, `logo-dark` (mesma extensão do original).
4. Commit local: "Cria pasta do cliente <Nome>".

## Etapa 2 · Briefing

1. Usar o questionário [briefing.md](briefing.md).
   - **Já respondido:** extrair as respostas do texto/arquivo e perguntar
     só o que faltar das perguntas ★.
   - **Preencher agora:** perguntar bloco por bloco, escolhas fechadas onde
     houver opções; uma rodada por bloco, não pergunta por pergunta.
   - **Enviar ao cliente:** gerar a versão limpa do questionário (sem ★ e
     sem notas pro agente), salvar em `<cliente>/briefing/questionario-
     cliente.md`, entregar o texto pronto para colar no WhatsApp/e-mail e
     parar aqui até as respostas chegarem.
2. Salvar em `<cliente>/briefing/briefing.md` com as seções do
   questionário e uma seção final "Pendências com o cliente". Nunca
   inventar resposta; o que faltar vai para Pendências.
3. **Portão:** mostrar um resumo de 5 a 8 linhas (quem é, objetivo,
   público, tom, restrições, pacote) e perguntar se está correto.
4. Marcar a etapa no `ONBOARDING.md`, copiar pendências para lá, commit
   local: "Briefing do cliente <Nome>".

## Etapa 3 · Manual da marca

1. Seguir a skill `manual-de-marca-instagram` usando o `briefing.md` como
   fonte (Caminho A se tem @, Caminho B se não tem). As 5 perguntas da
   Etapa 1 dela já devem estar respondidas no briefing; só perguntar o que
   faltar. Se o cliente já tem manual completo, pular a geração e só
   extrair os dados dele.
2. Guardar as entregas na pasta do cliente: `<cliente>/manual/` (HTML e
   PDF de cada versão, e um `links.md` com os links dos artifacts/design).
   Imagens geradas ou fotos reais tratadas vão em `assets/` (originais em
   `assets/raw/`).
3. **Portão:** se o manual tiver 2 opções de cor, perguntar qual o cliente
   escolheu. Perguntar se o manual foi aprovado (aprovado · aprovado com
   ajustes · ainda aguardando). Aguardando: dá para seguir com a cor
   marcada "A DEFINIR", mas avisar que o visual dos carrosséis espera essa
   escolha.
4. Com o manual aprovado, gerar as duas fontes que as outras etapas leem:
   - `brand-kit.json` na pasta do cliente, conforme
     `skills/instagram-carousel/references/brand-kit.md` (cores com os
     mesmos HEX do manual, fontes, tom, tokens `derived`, logo com caminhos
     absolutos dentro de `<cliente>/logo/`, conferidos com
     `Path.exists()`), mais o bloco `brand_manual` com o resumo do manual.
   - `skills/marca-<slug>/SKILL.md` pela skill `marca-cliente` (seção 2),
     que reaproveita o `brand-kit.json` e o briefing.
5. Registrar cor escolhida e outras decisões em "Decisões fixadas", marcar
   a etapa, commit local: "Manual da marca do cliente <Nome>".

## Etapa 4 · Apresentação de estratégia

1. Seguir a skill `apresentacao-estrategia-conteudo` (4 partes) com briefing,
   `marca-<slug>` e pacote contratado como fonte.
2. Salvar em `<cliente>/apresentacoes/<YYYY-MM-DD>-estrategia-conteudo/`.
   O calendário da Parte 3 deve listar os temas dos primeiros carrosséis,
   indicando quais vieram do cliente e quais foram propostos.
3. **Portão:** perguntar se o cliente aprovou a apresentação e o calendário
   (aprovado · aprovado com ajustes · aguardando).
4. Salvar o calendário aprovado também em
   `<cliente>/apresentacoes/calendario.md` (data, tema, pilar, formato,
   objetivo, CTA), que vira a fila de produção. Marcar a etapa, commit
   local: "Apresentação de estratégia do cliente <Nome>".

## Etapa 5 · Carrosséis

Para cada tema do `calendario.md` (um por vez, na ordem):

1. **Copy:** a skill `marca-<slug>` gera os textos dos cards a partir do
   tema. Mostrar e aguardar aprovação.
2. **Visual:** skill `instagram-carousel` da pasta do cliente, com o
   `brand-kit.json` dela, usando a mesma quantidade de slides da copy
   aprovada. Antes de montar, as perguntas obrigatórias sobre fotos e
   indicador de swipe do `CLAUDE.md` (6 escolhas fechadas, numa rodada só).
3. Verificação visual obrigatória, revisão, exportação só com aprovação
   explícita; a exportação já atualiza a `galeria.html`.
4. Marcar o tema como feito no `calendario.md`, commit local por carrossel
   concluído.

No primeiro carrossel do cliente, ao final, marcar a Etapa 5 no
`ONBOARDING.md` e lembrar que os valores fixados nele (tamanho de logo,
posições) passam a valer para todos os próximos (registrar no
`brand-kit.json`).

## Fechamento de cada sessão

Listar commits locais ainda não enviados e perguntar se pode dar push
(protocolo do `CLAUDE.md`). Dizer em uma linha qual é a próxima etapa do
cliente.
