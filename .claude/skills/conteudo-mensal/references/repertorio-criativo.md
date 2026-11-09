# Repertório criativo (tipos de post, viradas, recursos, quadros fixos)

Padrão geral desde 2026-11-08, tirado do estudo da marca Publipost (que se inspirou no método
do perfil @v4company). Serve para variar o **conteúdo** de um carrossel para o outro, e não só o
tema e a composição.

**Regra de ouro: entra o esqueleto, não a pele.** Daqui vem a estrutura da história e o
repertório de recursos. Fonte, cor, logo, tom e jeito de falar continuam sendo da marca de cada
cliente. Um recurso que não combina com a marca não é usado; nunca se força a marca a caber no
recurso. Nada daqui substitui o que já existe (história primeiro, sorteio, anti-IA, verificação
visual); complementa.

## 1. Tipos de post (o "formato da história")

O sorteio (`sorteio_carrossel.py`) sorteia a estrutura e nunca repete a do carrossel anterior.
No plano do mês, alternar os tipos do mesmo jeito que se alternam os temas. Cada tipo traz a
sequência de funções do roteiro; a quantidade de slides se ajusta ao tema.

| Tipo (no sorteio) | Sequência de funções | Pede material real? |
|---|---|---|
| tema-que-vira-licao | gancho · contexto · por que importa · virada · conceito · lição · chamada | não |
| mito-e-verdade | gancho · contexto · virada · por que importa · como fazer · chamada | não |
| erro-comum | gancho · por que importa · exemplo · o que muda · como fazer · chamada | não |
| passo-a-passo / guia-rapido | gancho (com o número de itens) · por que importa · item × N · lição · chamada | não |
| serie-de-anafora | gancho com o bordão · bordão × 4 a 6 (cada um com uma ideia) · lição · chamada | não |
| comparacao | gancho · contexto · lado A · lado B · virada · lição · chamada | não |
| dado-comparativo | gancho · contexto · dado × 2 a 3 · conceito · lição · chamada | **dado real com fonte** |
| perguntas-e-respostas | gancho · pergunta/resposta × 3 a 5 · chamada | dúvida real ajuda |
| historia-de-caso | gancho · contexto · virada · consequência · conceito · lição · chamada | **caso real** |
| um-dia-na-rotina / bastidores | gancho · momentos do dia × 3 a 5 · lição · chamada | foto real ajuda |
| antes-e-depois | gancho (antes x depois) · antes · virada · depois · lição · chamada | caso ou foto real |
| frase-de-autoridade | frase grande sozinha, ou frase · contexto · lição · chamada | **fala real** |

Tipo que pede material real só entra quando o material existe (`material-real/`); nunca inventar
dado, caso, fala nem manchete.

O conferidor (`conferir_carrossel.py --roteiro`) lê a linha `Tipo:` de cada post. Em
`serie-de-anafora`, `perguntas-e-respostas`, `frase-de-autoridade` e `um-dia-na-rotina` ele não
exige "por que importa", "o que muda" e "como fazer", porque a história desses tipos é outra.
A função "lição" conta como "como fazer".

## 2. Viradas de história (as duas funções novas)

- **conceito** ("Isso tem nome: …"): dá nome ao que o carrossel mostrou. Só nome real e
  reconhecido na área do cliente; nunca inventar termo.
- **lição** ("O que isso muda em você / na sua empresa"): ponte de uma frase + 3 a 5 perguntas
  que o leitor faz a si mesmo ("Antes de [decidir], pergunte:"). Fica no lugar da frase de efeito
  do fim e é o slide que a pessoa salva.

## 3. Recursos de slide (para "nenhum slide só com fundo e texto")

Somam-se aos que já existem (traço temático, forma de cor, recorte, foto). O sorteio sugere 2 por
carrossel, sem repetir os 2 do carrossel anterior. Limites: uma palavra destacada por título,
uma faixa ou marca-texto por slide, um marca-texto por carrossel.

| Recurso | O que é | Como a marca veste |
|---|---|---|
| anotacao-a-mao | frase curta e inclinada (−4° a −6°) comentando o slide, com setinha | na fonte manuscrita ou de assinatura da marca; marca sem essa fonte **não usa** |
| palavra-impacto | uma palavra ou frase de até 3 palavras, gigante, numa faixa de borda a borda; máx. 1 por carrossel | fonte de título da marca, cor de destaque; em data temática, cor da campanha |
| marca-texto | fundo de cor atrás de 1 a 3 palavras do apoio | cor clara da marca (nunca uma cor de fora da paleta) |
| selo-numerico | número do item em selo (01, 02) ao lado do título, nos guias | forma e raio dos elementos da marca |
| prova-real | print, manchete ou comentário real em cartão, levemente girado, com fonte | cartão no fundo claro da marca; **só com material real** |
| mockup-celular | tela de celular desenhada com o conteúdo do slide | só para assunto de app, rede social ou mensagem |
| dois-cartoes | comparativo "sem x com" em dois cartões, o segundo na cor da marca | cores da marca; texto curto, item por linha |
| frase-ponte | frase no pé do slide que puxa o próximo ("Mas tem um detalhe →"), uma diferente por slide | conta como indicador de arraste: **só quando o Thiago escolher essa opção** na pergunta do indicador |

## 4. Quadros fixos por cliente

Cada cliente pode ter 1 ou 2 quadros recorrentes (1 vez por mês cada), com nome, tipo de post e
um elemento visual próprio que se repete. É variedade com identidade: o seguidor reconhece o
quadro no feed. Os quadros ficam registrados na marca do cliente (`marca-cliente/template.md`,
seção "Repertório criativo") e só são criados com o OK do Thiago.

## 5. Como cada cliente veste o repertório (preencher ao usar pela 1ª vez)

### Sandra Behrens (acolhedora, sem promessa, segunda pessoa)
- anotacao-a-mao: sim, na Parisienne (assinatura), em dourado escuro no claro e dourado claro no escuro.
- palavra-impacto: Cormorant Garamond itálico grande, faixa em areia ou oliva; frase de cuidado, nunca de cobrança.
- lição: "O que isso muda em você", perguntas gentis de autopercepção, nunca diagnóstico.
- conceito: só termo real da psicologia ou da Arteterapia, explicado em linguagem simples.
- prova-real: só fala de paciente com autorização escrita; não usar print de comentário de terceiro.
- Quadros fixos (aprovados pelo Thiago em 2026-11-08): série "Menopausa não é…" (serie-de-anafora); "Cores da mandala" (uma cor por mês).

### CONSULTORIA A&J (técnica, prática, segurança do trabalho)
- anotacao-a-mao: não usa (a marca não tem fonte manuscrita); no lugar, nota curta em Lora itálico.
- palavra-impacto: Lora em faixa verde da marca; em Outubro Rosa e Novembro Azul, na cor da campanha.
- lição: "O que isso muda na sua empresa", checklist "Antes de [ação], confira:".
- conceito: termo da NR ou da SST ("Isso tem nome: ato inseguro"), com a norma citada.
- prova-real: manchete ou dado oficial (MPT, OIT, Observatório de SST) com fonte.
- Quadros fixos (aprovados pelo Thiago em 2026-11-08): "NR em 1 minuto"; "Acidente da semana" (caso real anonimizado, só com material real).

### Publipost
- Repertório completo no próprio manual (`Publipost/manual/MARCA-PUBLIPOST.md`).

## 6. Fora do padrão (não trazer da Publipost)
- Barra de continuação fixa em todo slide e chamada idêntica em todos os posts.
- Fontes, cores e monograma da Publipost em outro cliente.
- Pessoas geradas por IA apresentadas como equipe ou cliente.
- Formato 3:4 (1080 × 1440): o projeto segue em 1080 × 1350 até decisão do Thiago.
