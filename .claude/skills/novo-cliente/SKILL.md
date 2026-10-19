---
name: novo-cliente
description: Passo a passo de entrada de um cliente novo nesta pasta, do briefing aos primeiros carrosséis (pasta do cliente → identidade mínima → briefing e manual da marca opcionais → apresentação de estratégia → carrosséis). Use quando disserem "cliente novo", "entrou um cliente", "começar um cliente", "onboarding" ou pedirem para retomar o onboarding de um cliente.
---

# Cliente novo: passo a passo

Esta skill só orquestra. Cada etapa chama a skill que já faz aquele trabalho
e segue todas as regras do `CLAUDE.md` da raiz (perguntas obrigatórias de
carrossel, chip de logo, verificação visual, sem travessão na copy, commit
local a cada marco).

```
1 Pasta → 2 Identidade mínima → [3 Briefing] → [4 Manual da marca] → 5 Apresentação → 6 Carrosséis
                                 └──── opcionais: enriquecem, não travam ────┘
```

**Obrigatório** é só a pasta e a identidade mínima (o que os carrosséis
precisam para sair com a cara do cliente). **Briefing e manual da marca são
opcionais**: quando existem, enriquecem tom, pilares, público e visual de
tudo que vem depois; quando não existem, o fluxo segue e o que faltar vira
"a confirmar"/Pendências. Nunca bloquear a produção esperando briefing ou
manual; também nunca inventar o que eles diriam.

## Etapa 0 · Abertura (sempre)

1. Pegar o nome do cliente. Se não veio na mensagem, perguntar.
2. Se já existir uma pasta com esse nome (ou parecido), ler o
   `ONBOARDING.md` dela, dizer em uma linha em que etapa parou e retomar
   dali. Cliente antigo sem `ONBOARDING.md`: criar o arquivo a partir de
   `_modelo-cliente/ONBOARDING.md`, marcando o que já existe na pasta.
3. Cliente novo: fazer de uma vez, como escolhas fechadas (AskUserQuestion):
   - O cliente já tem Instagram? (sim, com @ · não)
   - Briefing? (já tenho respondido: vou colar/anexar · preencher agora
     juntos · gerar questionário pra enviar ao cliente · pular por agora)
   - Manual da marca? (cliente já tem · criar agora · pular por agora)
   - Logo? (tenho os arquivos · ainda não · cliente não tem logo)

## Etapa 1 · Pasta do cliente (obrigatória)

A pasta vem primeiro porque é onde tudo é salvo; se a sessão cair, nada se
perde.

1. Confirmar o nome da pasta (como deve aparecer na galeria) e o slug.
2. Rodar na raiz: `python novo_cliente.py "Nome do Cliente"` (ou com
   `--slug`). O script copia `_modelo-cliente/` e preenche README e
   `ONBOARDING.md`. Nunca sobrescreve pasta existente.
3. Se o Thiago enviou arquivos de logo, copiar para `<cliente>/logo/` como
   `logo-primary`, `logo-white`, `logo-dark` (mesma extensão do original).
4. Commit local: "Cria pasta do cliente <Nome>".

## Etapa 2 · Identidade mínima (obrigatória)

O mínimo para produzir: nome, @, nicho, cor principal, fontes, logo (ou
inicial), tom e idioma.

1. Se o manual vai ser criado agora (Etapa 4), pular esta etapa: o
   manual já gera a identidade completa.
2. Senão, gerar `brand-kit.json` pela Phase 1 da skill
   `skills/instagram-carousel` da pasta do cliente
   (`references/brand-kit.md`), aproveitando o que já se sabe e perguntando
   só o resto, de uma vez. Logo com caminhos absolutos dentro de
   `<cliente>/logo/`, conferidos com `Path.exists()`.
3. Gerar uma `skills/marca-<slug>/SKILL.md` enxuta pela skill
   `marca-cliente` (seção 2): preencher o que houver, apagar o que não se
   aplica e mandar o resto para "Pendências com o cliente".
4. Marcar a etapa, commit local: "Identidade mínima do cliente <Nome>".

## Etapa 3 · Briefing (opcional, enriquece)

Fazer quando o Thiago escolher na abertura ou quando o briefing chegar
depois (inclusive com carrosséis já em produção).

1. Usar o questionário [briefing.md](briefing.md).
   - **Já respondido:** extrair as respostas do texto/arquivo; perguntar só
     as ★ que faltarem, e só se o Thiago souber responder agora.
   - **Preencher agora:** perguntar bloco por bloco, escolhas fechadas onde
     houver opções; uma rodada por bloco. Pergunta sem resposta vai para
     Pendências, sem insistir.
   - **Enviar ao cliente:** gerar a versão limpa do questionário (sem ★ e
     sem notas pro agente), salvar em
     `<cliente>/briefing/questionario-cliente.md`, entregar o texto pronto
     para colar no WhatsApp/e-mail e **seguir o fluxo** enquanto as
     respostas não chegam.
2. Salvar em `<cliente>/briefing/briefing.md` com as seções do
   questionário e uma seção final "Pendências com o cliente". Nunca
   inventar resposta.
3. Mostrar um resumo de 5 a 8 linhas (quem é, objetivo, público, tom,
   restrições, pacote) para o Thiago conferir.
4. **Enriquecer o que já existe:** atualizar `marca-<slug>` (tom, público,
   pilares, restrições) e tirar das Pendências o que foi respondido. Se o
   briefing contradisser algo já usado em carrossel (cor, tom, tema
   proibido), avisar antes de mudar.
5. Marcar a etapa, commit local: "Briefing do cliente <Nome>".

## Etapa 4 · Manual da marca (opcional, enriquece)

1. Seguir a skill `manual-de-marca-instagram` usando o que existir como
   fonte (briefing, identidade mínima, perfil atual). Caminho A se tem @,
   Caminho B se não tem. Sem briefing, ela faz só as perguntas da Etapa 1
   dela e registra as suposições nas pendências. Se o cliente já tem
   manual pronto, só extrair os dados dele.
2. Guardar as entregas em `<cliente>/manual/` (HTML e PDF de cada versão,
   e um `links.md` com os links dos artifacts/design). Imagens geradas ou
   fotos reais tratadas vão em `assets/` (originais em `assets/raw/`).
3. Se o manual tiver 2 opções de cor, perguntar qual o cliente escolheu.
   Enquanto não houver escolha, a cor fica "A DEFINIR" e só o visual dos
   carrosséis espera essa resposta (a copy pode seguir).
4. Atualizar (ou criar) `brand-kit.json` com os mesmos HEX, fontes e
   logo do manual, mais o bloco `brand_manual` com o resumo, e atualizar
   `skills/marca-<slug>/SKILL.md` pela `marca-cliente`. Se isso mudar algo
   que já estava em uso nos carrosséis (cor, fonte, tamanho de logo),
   avisar antes e registrar a mudança.
5. Registrar a cor escolhida e outras decisões em "Decisões fixadas",
   marcar a etapa, commit local: "Manual da marca do cliente <Nome>".

## Etapa 5 · Apresentação de estratégia

1. Seguir a skill `apresentacao-estrategia-conteudo` (4 partes) com o que
   existir: briefing, `marca-<slug>`, manual, pacote contratado. Sem
   briefing/manual, a apresentação sai mais enxuta e com mais itens "a
   confirmar"; deixar isso visível na lista final.
2. Salvar em `<cliente>/apresentacoes/<YYYY-MM-DD>-estrategia-conteudo/`.
   O calendário da Parte 3 deve listar os temas dos primeiros carrosséis,
   indicando quais vieram do cliente e quais foram propostos.
3. **Portão:** perguntar se o cliente aprovou a apresentação e o calendário
   (aprovado · aprovado com ajustes · aguardando).
4. Salvar o calendário aprovado também em
   `<cliente>/apresentacoes/calendario.md` (data, tema, pilar, formato,
   objetivo, CTA), que vira a fila de produção. Marcar a etapa, commit
   local: "Apresentação de estratégia do cliente <Nome>".

## Etapa 6 · Carrosséis

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

No primeiro carrossel do cliente, ao final, marcar a Etapa 6 no
`ONBOARDING.md` e lembrar que os valores fixados nele (tamanho de logo,
posições) passam a valer para todos os próximos (registrar no
`brand-kit.json`).

## Fechamento de cada sessão

Listar commits locais ainda não enviados e perguntar se pode dar push
(protocolo do `CLAUDE.md`). Dizer em uma linha qual é a próxima etapa do
cliente e, se briefing ou manual ainda não foram feitos, lembrar que dá
pra enriquecer a marca com eles quando houver material.
