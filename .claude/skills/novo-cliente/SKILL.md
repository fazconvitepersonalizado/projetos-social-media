---
name: novo-cliente
description: Passo a passo de entrada de um cliente novo nesta pasta (pasta → briefing → diagnóstico do perfil → base estratégica → manual/identidade → criação do perfil → apresentação → carrosséis). Sem Instagram, a marca nasce do nome e sobrenome do cliente; com perfil e briefing, os dois são cruzados numa base estratégica. Use quando disserem "cliente novo", "entrou um cliente", "começar um cliente", "onboarding" ou pedirem para retomar o onboarding de um cliente.
---

# Cliente novo: passo a passo

Esta skill só orquestra. Cada etapa chama a skill que já faz aquele trabalho
e segue todas as regras do `CLAUDE.md` da raiz (perguntas obrigatórias de
carrossel, chip de logo, verificação visual, sem travessão na copy, commit
local a cada marco).

```
1 Pasta → 2 Briefing → 3 Diagnóstico do perfil → 4 BASE ESTRATÉGICA → 5 Manual / identidade
          (opcional)   (só se tem @)              (sempre; junta tudo)
        → 6 Criação do perfil → 7 Apresentação → 8 Carrosséis
          (só se não tem @)
```

## Os quatro cenários

A abertura define o cenário; ele decide quais etapas rodam e de onde vem a
estratégia (detalhes em [base-estrategica.md](base-estrategica.md)).

| | Sem Instagram | Com Instagram |
|---|---|---|
| **Com briefing** | **A** · marca pelo **nome e sobrenome** + estratégia pelo briefing | **C** · **cruzamento** briefing × perfil |
| **Sem briefing** | **B** · marca pelo nome + nicho; quase tudo "proposta" | **D** · estratégia pelo diagnóstico do perfil |

Princípios:
- **Nada trava a produção** esperando briefing. O que faltar vira "a
  confirmar" e Pendências; nunca suposição apresentada como fato.
- **Sem Instagram, o manual é sempre feito** (é dele que saem @, bio,
  monograma e a prévia do perfil novo), a partir do nome do cliente.
- **Com Instagram, o manual é opcional**; sem ele, a identidade mínima sai
  do perfil atual + base estratégica.
- **A base estratégica é a fonte única.** Manual, `marca-<slug>`,
  apresentação e carrosséis leem dela. Briefing ou perfil que chegarem
  depois atualizam a base, que propaga para o resto (avisando antes de
  mudar algo já em uso).

## Etapa 0 · Abertura (sempre)

1. Pegar o nome do cliente. Se não veio na mensagem, perguntar.
2. Se já existir pasta com esse nome (ou parecido), ler o `ONBOARDING.md`,
   dizer em uma linha o cenário e em que etapa parou, e retomar dali.
   Cliente antigo sem `ONBOARDING.md`: criar a partir de
   `_modelo-cliente/ONBOARDING.md`, marcando o que já existe.
3. Cliente novo: perguntar de uma vez, como escolhas fechadas
   (AskUserQuestion):
   - Tem Instagram? (sim, o @ é… · não tem)
   - Briefing? (já respondido: vou colar/anexar · preencher agora juntos ·
     gerar questionário pra enviar ao cliente · pular por agora)
   - Manual da marca? (cliente já tem · criar · pular por agora). Só para
     quem tem Instagram; sem Instagram, o manual é sempre criado.
   - Logo? (tenho os arquivos · ainda não · não tem logo)
4. Registrar o cenário (A/B/C/D) em "Decisões fixadas" do `ONBOARDING.md`.

## Etapa 1 · Pasta do cliente (obrigatória)

1. Confirmar o nome da pasta (como deve aparecer na galeria) e o slug.
2. Rodar na raiz: `python novo_cliente.py "Nome do Cliente"` (ou com
   `--slug`). Nunca sobrescreve pasta existente.
3. Logos enviados → `<cliente>/logo/` como `logo-primary`, `logo-white`,
   `logo-dark` (mesma extensão do original).
4. Commit local: "Cria pasta do cliente <Nome>".

## Etapa 2 · Briefing (opcional, enriquece)

Roda quando o Thiago escolher na abertura ou quando o briefing chegar
depois (mesmo com carrosséis já em produção).

1. Usar o questionário [briefing.md](briefing.md).
   - **Já respondido:** extrair as respostas; perguntar só as ★ que
     faltarem, e só se o Thiago souber responder agora.
   - **Preencher agora:** bloco por bloco, escolhas fechadas onde houver
     opções; uma rodada por bloco.
   - **Enviar ao cliente:** gerar a versão limpa (sem ★ e sem notas pro
     agente) em `<cliente>/briefing/questionario-cliente.md`, entregar o
     texto pronto para WhatsApp/e-mail e **seguir o fluxo** enquanto as
     respostas não chegam.
2. Salvar em `<cliente>/briefing/briefing.md` com as seções do
   questionário e "Pendências com o cliente". Nunca inventar resposta.
3. Marcar a etapa, commit local: "Briefing do cliente <Nome>".
4. Se a base estratégica já existia (briefing chegou depois), voltar à
   Etapa 4 e **atualizá-la** (o cenário muda de B→A ou D→C).

## Etapa 3 · Diagnóstico do perfil (só cenários C e D)

1. Seguir [diagnostico-perfil.md](diagnostico-perfil.md): abrir o perfil
   (ou pedir prints) e registrar o que ele mostra hoje, separando fato de
   interpretação, sem estimar números.
2. Salvar em `<cliente>/estrategia/diagnostico-perfil.md`, prints em
   `<cliente>/estrategia/prints/`. Commit local.

## Etapa 4 · Base estratégica (sempre)

1. Montar `<cliente>/estrategia/base-estrategica.md` pelo modelo
   [base-estrategica.md](base-estrategica.md), com a etiqueta de origem em
   cada afirmação ([B] briefing, [P] perfil, [B+P] os dois, [S] sugestão).
   - **Cenário C (perfil + briefing):** preencher a tabela de cruzamento
     ponto a ponto e fechar com Manter / Corrigir / Criar / Oportunidades /
     Contradições. Onde briefing e perfil concordam, é a base mais forte;
     onde divergem e não dá para decidir, vai para "Contradições a
     confirmar" em vez de escolher um lado sozinho.
   - **Cenários A e B (sem Instagram):** a seção 6 segue
     [marca-pelo-nome.md](marca-pelo-nome.md) (confirmar nome e título,
     4 opções de @, nome de exibição, bio, monograma, conceito).
   - **Cenário D:** o que o perfil não mostra (objetivo, oferta, objeções)
     vai para "A confirmar", com a pergunta pronta para o cliente.
2. **Portão:** mostrar o resumo (cenário, posicionamento em 1 frase,
   pilares, primeiros temas; no cenário C, as decisões principais do
   cruzamento e as contradições) e pedir confirmação ao Thiago.
3. "A confirmar" → Pendências do `ONBOARDING.md`. Marcar a etapa, commit
   local: "Base estratégica do cliente <Nome>".

## Etapa 5 · Manual da marca / identidade

**Sem Instagram (A e B), sempre:** rodar `manual-de-marca-instagram` pelo
Caminho B com a marca pelo nome já decidida na base (não repetir
perguntas). Gerar o monograma e a assinatura do nome em SVG em
`<cliente>/logo/`.

**Com Instagram (C e D), opcional:**
- Manual escolhido: `manual-de-marca-instagram` pelo Caminho A, usando o
  diagnóstico e o cruzamento da base (o "Manter / Corrigir / Criar" vira o
  antes e depois do manual).
- Manual pulado: **identidade mínima** tirada do perfil atual + base
  (@, cores e logo que já existem, fontes, tom), perguntando só o que
  faltar.

Nos dois casos:
1. Entregas do manual em `<cliente>/manual/` (HTML e PDF de cada versão,
   `links.md` com os links dos artifacts/design). Imagens em `assets/`
   (originais em `assets/raw/`).
2. Se houver 2 opções de cor, perguntar qual o cliente escolheu. Sem
   escolha, a cor fica "A DEFINIR" e só o visual dos carrosséis espera.
3. Gerar/atualizar `brand-kit.json` (mesmos HEX, fontes e logo; caminhos
   absolutos dentro de `<cliente>/logo/`, conferidos com `Path.exists()`;
   bloco `brand_manual` com o resumo) conforme
   `skills/instagram-carousel/references/brand-kit.md`.
4. Gerar/atualizar `skills/marca-<slug>/SKILL.md` pela skill
   `marca-cliente`, usando a base estratégica como fonte principal.
5. Decisões em "Decisões fixadas", marcar a etapa, commit local:
   "Manual da marca do cliente <Nome>" (ou "Identidade mínima…").

## Etapa 6 · Criação do perfil (só cenários A e B)

Checklist para o Thiago/cliente, salvo em `<cliente>/estrategia/criacao-perfil.md`:
1. Conferir disponibilidade do @ recomendado; se ocupado, usar a próxima
   opção e **atualizar** base, `brand-kit.json` e `marca-<slug>`.
2. Criar a conta, nome de exibição e bio exatamente como no manual; link.
3. Foto de perfil: monograma (ou foto real tratada, se o cliente preferir).
4. Converter para conta Profissional (Comercial ou Criador de conteúdo).
5. Se nós vamos publicar (`instagram-publish`): conectar a uma página do
   Facebook e gerar o acesso da Meta API.
6. Capas e nomes dos destaques, conforme o manual.
7. Plano de estreia: os primeiros 6 a 9 posts publicados juntos para a
   grade não começar vazia (temas da base, seção 10).

Marcar a etapa quando o perfil existir de fato e o @ real estiver
confirmado.

## Etapa 7 · Apresentação de estratégia

1. Seguir a skill `apresentacao-estrategia-conteudo` com a **base
   estratégica** como fonte principal (+ manual e pacote contratado).
   - Cenário C: a Parte 1 mostra o que o perfil já conquistou e o que o
     briefing pede; a Parte 2 mostra as decisões do cruzamento (manter /
     corrigir / criar) com o porquê.
   - Cenários A e B: a Parte 4 inclui a criação do perfil e o plano de
     estreia.
   - Itens [S] aparecem como proposta, e "a confirmar" fica visível.
2. Salvar em `<cliente>/apresentacoes/<YYYY-MM-DD>-estrategia-conteudo/`.
3. **Portão:** o cliente aprovou a apresentação e o calendário?
   (aprovado · aprovado com ajustes · aguardando)
4. Salvar o calendário aprovado em `<cliente>/apresentacoes/calendario.md`
   (data, tema, pilar, formato, objetivo, CTA), que vira a fila de
   produção. Marcar a etapa, commit local.

## Etapa 8 · Carrosséis

Para cada tema do `calendario.md` (um por vez, na ordem):

1. **Copy:** a skill `marca-<slug>` gera os textos dos cards. Mostrar e
   aguardar aprovação.
2. **Visual:** skill `instagram-carousel` da pasta do cliente, com o
   `brand-kit.json` dela e a mesma quantidade de slides da copy aprovada.
   Antes de montar, as 6 perguntas obrigatórias sobre fotos e indicador de
   swipe do `CLAUDE.md`, numa rodada só.
3. Verificação visual obrigatória, revisão, exportação só com aprovação
   explícita; a exportação já atualiza a `galeria.html`.
4. **Antes de publicar** (cenários A e B): conferir que o perfil já existe
   e que o @ real é o mesmo dos carrosséis; se mudou, avisar e atualizar os
   carrosséis já feitos.
5. Marcar o tema como feito no `calendario.md`, commit local por carrossel.

No primeiro carrossel, marcar a Etapa 8 no `ONBOARDING.md` e lembrar que
os valores fixados nele (tamanho de logo, posições) valem para os próximos
(registrar no `brand-kit.json`).

## Fechamento de cada sessão

Listar commits locais ainda não enviados e perguntar se pode dar push.
Dizer em uma linha a próxima etapa do cliente e, se faltar briefing ou
diagnóstico, lembrar que a base estratégica fica mais forte com eles.
