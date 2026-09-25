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
  viés pra cima quando a foto for mais alta que o espaço final. Se o
  recorte final (na proporção real de exibição, não só na proporção
  intermediária do arquivo) empurrar a pessoa/rosto pra fora do quadro,
  ajustar `object-position` (ou recorte manual) até o sujeito aparecer.
- Tratamento visual (tinta de marca, filtro) deve ser sutil — o objetivo é a
  foto parecer parte do design, não um filtro pesado por cima. Na dúvida,
  menos é mais.
- Ao buscar foto (quando eu não fornecer uma): usar só bancos livres para
  uso comercial sem pedir permissão (ex.: Unsplash, Pexels, Pixabay) —
  nunca resultado de busca de imagem genérica ou site de terceiros, que
  normalmente tem direito autoral. Cuidado com variantes pagas dentro do
  mesmo banco (ex.: Unsplash+/Getty) — confirmar que a licença é gratuita
  antes de baixar, não só que o site é "livre" no geral.
- A busca deve ser pelo conteúdo específico daquele trecho/peça, não pelo
  tema geral do projeto — busca genérica traz foto genérica, que parece
  "de banco de imagens" e não da marca.
- Antes de baixar/usar a foto escolhida, mostrar 2–3 opções e perguntar qual
  usar — nunca decidir sozinho e já aplicar, pra não gastar trabalho de
  edição numa foto que pode ser trocada. Exceção: se eu autorizar
  explicitamente ("escolhe você, com critério lógico") para aquela rodada,
  pode escolher direto, mas ainda assim justificando a escolha.

## Carrosséis: perguntas obrigatórias antes de montar
- Sempre que um carrossel novo (qualquer marca) for incluir fotos reais,
  perguntar de uma vez, como escolhas fechadas (nunca como "como você quer
  que eu decida isso"):
  1. Slides com foto: escolha aleatória (o agente decide) ou manual (eu
     indico)?
  2. Estilo de imagem: emoldurada (card), full-bleed (slide inteiro), ou
     variado (mistura dos dois no mesmo carrossel)?
  3. Texto sobre full-bleed: centralizado, ou deslocado pra cima/baixo
     conforme o espaço vazio daquela foto específica?
  4. Opacidade da foto: vívida ou suave/esmaecida?
  5. Indicador de swipe: manter a barra de progresso segmentada + contador
     padrão do design system, ou usar outro indicador (ex.: selo discreto
     "ARRASTE PARA O LADO →" só na capa)? Não é regra fixa pra nenhum lado.
  6. Foto própria ou buscar uma livre de direitos?
  Não repetir a(s) mesma(s) posição(ões) de foto do carrossel anterior da
  mesma marca.
- Logo/marca-d'água nunca sobre rosto em foto: reposicionar pra uma área sem
  rosto quando necessário. Toda instância de logo num carrossel com fotos
  (capa, watermark, CTA) leva um "chip" de fundo justo (raio ~6-8px,
  padding ~6-8px, cantos levemente arredondados) usando os tokens da
  própria marca (ex.: `LIGHT_BG`/`LIGHT_BORDER` translúcido em fundo claro,
  `rgba(0,0,0,0.22-0.24)` em fundo escuro/gradiente) — nunca um quadrado
  forçado nem cor de outra marca.
- Tamanhos de fonte do design-system podem ficar pequenos demais no
  celular: antes de fechar, gerar um preview (screenshot na escala real de
  exportação) e checar legibilidade; se precisar aumentar, também apertar
  o espaçamento pra caber no slide de 525px.
- No slide de CTA com fundo gradiente da marca, nunca colorir uma frase ou
  título inteiro com o tom escuro da marca (baixo contraste) — esse tom só
  em destaque pontual de 1-2 palavras dentro de uma frase branca/clara.
- **Verificação visual obrigatória antes de apresentar (qualquer carrossel
  com foto):** depois de gerar ou editar o HTML, sempre renderizar cada
  slide como imagem (screenshot) e ler de volta, conferindo por slide: (1)
  o texto está legível de fato contra o que está atrás dele naquele ponto
  específico, não contra a cor teórica do token; (2) a parte da foto que
  sobrou depois do recorte (`object-fit:cover`) ainda mostra o que o texto
  daquele slide está falando, sem cortar o sujeito/ação relevante pra fora
  do quadro. Rodar de novo a cada correção. Se achar problema, **sempre
  avisar antes de mexer**, mesmo em ajuste técnico pequeno (object-position,
  opacidade de overlay) — nunca corrigir silenciosamente. Se estiver tudo
  certo, dizer isso explicitamente em vez de simplesmente seguir em frente.
- **Receita pra corrigir legibilidade de texto sobre foto** (qualquer
  carrossel, qualquer cliente), quando a verificação acima achar problema:
  1. Dimensionar o degradê de proteção pela altura real do bloco de texto
     (headline + subtítulo + qualquer selo/legenda), não por uma
     porcentagem arbitrária — se o texto vai até 68% da altura do slide, o
     degradê precisa continuar com opacidade útil até lá, não sumir aos 55%.
  2. Reforçar com uma camada uniforme leve (`rgba` baixo, ex.: 0.15-0.18) por
     cima do degradê direcional, como rede de segurança pros pontos onde o
     gradiente já enfraqueceu.
  3. Nunca usar a cor clara/pálida da marca (`BRAND_LIGHT`) em destaque de
     texto sobre foto — perde contraste fácil contra céu/fundo claro; usar
     branco/creme e conseguir o efeito de "peso misto" só com
     peso+itálico.
  4. Textos pequenos/discretos (selo de "arraste", legenda) que ficam bem a
     ~0.5-0.6 de opacidade sobre fundo liso (`LIGHT_BG`/`DARK_BG`/gradiente)
     precisam de mais opacidade (~0.75-0.85) e mais peso quando estão sobre
     uma foto de verdade.
  Receita completa com exemplos de código em `references/visual-qa.md` da
  skill `instagram-carousel` ("Fixing text-over-photo legibility").

## Salvamento automático (git)
- Sempre que um **marco relevante** for concluído em qualquer projeto desta
  pasta — um conteúdo finalizado, uma correção de skill/padrão, uma
  atualização de configuração — fazer `git add` + `git commit` local com uma
  mensagem descritiva, **sem precisar perguntar antes**, e avisar em seguida
  o que foi salvo (ex.: "Salvei localmente: ajuste no fundo do slide 3 do
  carrossel X").
- Não commitar a cada edição intermediária/exploratória — só quando algo
  chegar a um estado concluído/estável.
- **Não dar `git push` automaticamente.** De vez em quando (ou quando fizer
  sentido, tipo ao final de uma sessão de trabalho), resumir quais commits
  locais ainda não foram enviados ao GitHub e perguntar se já pode enviar.
  Só fazer push depois de confirmação explícita.

## Comunicação e estilo de trabalho
- Evitar travessão/traço (—, -) na copy de qualquer peça; usar ponto e
  vírgula no lugar quando for unir duas frases relacionadas.

## Organização de projetos
- `galeria.html` na raiz desta pasta lista todos os carrosséis de todos os
  clientes (miniatura da capa + título + data), agrupados por marca; clicar
  num card abre o `carousel.html` original direto. Gerado por
  `generate_gallery.py` (também na raiz) — roda automaticamente ao final da
  Fase 5 (exportação) de qualquer carrossel novo (ver skill
  `instagram-carousel`), ou pode ser rodado manualmente (`python
  generate_gallery.py`, ou `--force` pra regerar todas as miniaturas). As
  miniaturas ficam em `.gallery-cache/` (fora do git).

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
- 2026-09-25 — Repositório único `projetos-social-media` criado no GitHub
  (privado). Definido o protocolo de salvamento: commit local automático a
  cada marco concluído (com aviso do que foi salvo); push só mediante
  confirmação, revisado periodicamente.
- 2026-09-25 — Padronizado evitar travessão/traço na copy de qualquer
  carrossel; usar ponto e vírgula no lugar (pedido durante o carrossel
  "5 motivos de acidentes de trabalho" da A&J).
- 2026-09-25 — Recuperadas e unificadas aqui várias regras de qualidade de
  carrossel (perguntas obrigatórias sobre fotos/indicador de swipe, chip de
  proteção de logo, checagem de legibilidade de fonte, contraste no CTA de
  gradiente) que existiam apenas em memórias de sessões antigas presas em
  pastas `Downloads\Sandra-Behrens` e `Downloads\instagram-carrossel-main`,
  nunca migradas pra esta pasta — por isso não estavam sendo aplicadas em
  novos carrosséis como o da A&J.
- 2026-09-25 — Criada a etapa de verificação visual obrigatória (renderizar
  e ler cada slide de volta, checando legibilidade de texto e se a foto
  recortada ainda bate com o texto), como `references/visual-qa.md` na
  skill `instagram-carousel` de ambos os projetos (A&J e Sandra-Behrens).
  Qualquer problema encontrado deve ser reportado antes de qualquer ajuste,
  mesmo pequeno; nunca corrigir sozinho sem avisar.
- 2026-09-25 — Criada `galeria.html` + `generate_gallery.py` na raiz da
  pasta: página única listando todos os carrosséis de todos os clientes,
  com miniatura clicável que abre o carrossel original. Integrada à Fase 5
  da skill `instagram-carousel` pra rodar automaticamente após cada
  exportação.
- 2026-09-25 — Registrada a receita de correção de legibilidade de texto
  sobre foto (degradê dimensionado pelo texto real, camada uniforme de
  reforço, evitar cor clara da marca em destaque sobre foto, opacidade maior
  pra legendas pequenas sobre foto), em `references/visual-qa.md` de ambos
  os projetos — derivada da correção iterativa do slide 1 do carrossel
  "5 motivos de acidentes de trabalho" da A&J.
