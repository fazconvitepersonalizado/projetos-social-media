# PROJETOS SOCIAL MEDIA — Padrão Geral

Este arquivo é carregado automaticamente pelo Claude Code em qualquer sessão
aberta dentro desta pasta ou de qualquer subpasta/projeto que exista ou vier
a existir aqui. Ele reúne **orientações gerais**, reaproveitáveis em
qualquer tipo de projeto desta pasta — carrossel, vídeo, copy, planilha, o
que for.

O que **não** entra aqui: nome de cliente, tom de voz, paleta de cores,
valores fixos de um projeto específico (ex.: tamanho de logo em pixels de UM
cliente). Isso fica no `README.md` ou nos arquivos de configuração daquele
projeto. O que entra aqui é o **princípio geral** por trás de uma instrução,
mesmo quando ela foi dada no contexto de um projeto específico.

## Protocolo para novas orientações
Sempre que eu (Thiago) der uma instrução nova — uma correção, uma preferência,
uma regra de qualidade — que ainda não está registrada nem aqui nem no
projeto atual, pergunte antes de só aplicar e seguir:

> "Isso deve virar padrão pra todos os projetos, ou vale só pra este
> projeto/conteúdo específico?"

- **Padrão geral** → registrar nesta pasta (seção certa deste arquivo) e, se
  fizer sentido, aplicar retroativamente nos outros projetos já existentes.
- **Só este projeto** → aplicar apenas no arquivo local daquele projeto
  (README, brand-kit.json, skill local), sem tocar aqui.
- Não precisa perguntar quando eu já disser o escopo de forma explícita
  ("isso é só pra esse cliente" / "isso vale pra todo mundo").

## Elementos visuais fixos (logo, marca, medidas recorrentes)
- Depois que um valor recorrente for definido para um projeto (tamanho de
  logo, espessura de borda, proporção de lockup, etc.), reutilizar esse
  mesmo valor em todo conteúdo novo daquele projeto — não redefinir do zero
  a cada peça. Guardar o valor fixado e a data/motivo no arquivo de
  configuração do próprio projeto.
- **Checagem de legibilidade (regra geral, vale pra qualquer logo/marca
  d'água):** antes de posicionar um logo ou marca sobre uma imagem/fundo,
  confirmar contraste real contra o fundo **daquele ponto específico da
  peça** — não contra uma cor "padrão" de referência. Nunca usar uma
  variante clara sobre área clara, nem uma variante escura/colorida sobre
  área escura ou poluída visualmente. Se existir mais de uma variante de
  cor, escolher sempre a que tiver melhor contraste real naquele lugar,
  mesmo que isso fuja da regra "padrão" de qual variante usar em qual tipo
  de fundo.

## Imagens e fotos
- Nunca embutir uma foto crua (sem tratamento) na peça final — sempre passar
  por um recorte/ajuste antes (proporção certa, brilho/contraste levemente
  ajustado, leve aproximação com a cor da marca quando fizer sentido).
  Manter o arquivo original (raw) separado do editado, pra poder refazer o
  ajuste sem precisar buscar a imagem de novo.
- Ao cortar uma foto com pessoa, evitar cortar rosto/cabeça — enquadrar com
  viés pra cima quando a foto for mais alta que o espaço final.
- Tratamento visual (tinta de marca, filtro) deve ser sutil — o objetivo é a
  foto parecer parte do design, não um filtro pesado por cima. Na dúvida,
  menos é mais.
- Ao buscar foto (quando eu não fornecer uma): usar só bancos livres para
  uso comercial sem pedir permissão (ex.: Unsplash, Pexels, Pixabay) —
  nunca resultado de busca de imagem genérica ou site de terceiros, que
  normalmente tem direito autoral.
- A busca deve ser pelo conteúdo específico daquele trecho/peça, não pelo
  tema geral do projeto — busca genérica traz foto genérica, que parece
  "de banco de imagens" e não da marca.
- Antes de baixar/usar a foto escolhida, mostrar 2–3 opções e perguntar qual
  usar — nunca decidir sozinho e já aplicar, pra não gastar trabalho de
  edição numa foto que pode ser trocada.

## Comunicação e estilo de trabalho
<!-- Ex: respostas diretas e curtas, sempre em português -->

## Organização de projetos
<!-- Princípios gerais de estrutura de pastas, nomenclatura, README, o que fica fora do git, etc. -->

## Manutenção entre projetos
- Quando um projeto ganha uma melhoria de processo que **não** é exclusiva
  daquele cliente/formato, replicar nos demais projetos da pasta e registrar
  no log abaixo.

## Log de decisões
- 2026-09-25 — Criado este `CLAUDE.md` como padrão geral da pasta.
- 2026-09-25 — Adicionado o protocolo de "perguntar antes de padronizar" e
  generalizadas as regras de legibilidade de logo e tratamento de imagens
  (extraídas de instruções já dadas nos projetos CONSULTORIA A&J e
  Sandra-Behrens), removendo valores específicos de cada cliente.
