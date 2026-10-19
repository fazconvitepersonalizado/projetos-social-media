# Formatos: método de produção

A voz, o CTA e os tabus vêm sempre da marca do cliente (ordem de leitura em
`SKILL.md`). Aqui está só a **mecânica** de cada formato. Se a marca do
cliente definir outra estrutura, **a marca vence**.

Regras que valem para todo formato (do `CLAUDE.md` da raiz):
- Sem travessão/traço na copy; ponto e vírgula para unir frases.
- Revisão anti-IA da copy por `references/anti-ia-copy.md` da skill
  `instagram-carousel` do cliente (nota mínima 35/50) antes de entregar.
- Nunca inventar fato, caso, número ou fala do cliente.

## Carrossel
- Conteúdo criado na Fase 2.
- **8 cards** (padrão do projeto, seção "Carrossel a partir de um tema" da
  marca do cliente / `marca-cliente/template.md`):
  - Card 1 = headline (gancho que prende).
  - Cards 2 a 6 = desenvolvimento (informação relevante, dica prática,
    argumento; narrativa fluida ou pontos, conforme a marca).
  - Card 7 = CTA (comentar, compartilhar ou salvar).
  - Card 8 = encerramento estratégico (reforça a mensagem e convida para a
    oferta de entrada do cliente).
- Até 25 a 30 palavras por card; ganchos que puxam para o próximo card.
- **Estrutura narrativa e gancho vêm do sorteio** (`sorteio_carrossel.py`,
  ver Fase 2 do `SKILL.md`). Uma referência útil de fluxo emocional, quando
  o sorteio permitir: identificação → consciência do problema → raiz →
  virada → chamada.
- Acompanha **legenda curta** (2 a 3 linhas) que complementa o gancho sem
  repetir o carrossel e sem "deslize para o lado"/"esse carrossel é para".

## Post único com conteúdo na legenda ("leia legenda")
- Conteúdo criado na Fase 2. Arte única com a headline; o conteúdo está na
  legenda.
- Estrutura: introdução breve (1 a 2 parágrafos) → pontos (numerados `1.`,
  `2.`, `3.` ou subtítulos, conforme a marca) → fechamento reflexivo → CTA.

## Frase
- Conteúdo criado na Fase 2. A **frase** para a arte + **legenda curta** que
  complementa sem repetir.

## Roteiro (Reels para gravar)
- Conteúdo criado na Fase 2. Gancho (0 a 3s) → desenvolvimento
  (identificação) → virada → CTA. Duração e formato das falas conforme a
  marca (ex.: só falas, sem indicação de câmera). Acompanha legenda.
- Se a marca disser que o cliente **não grava vídeo**, não propor roteiro;
  propor o formato substituto que a marca indicar.

## Reels (sem roteiro)
- Conteúdo criado na Fase 2: só **legenda** (o vídeo já existe ou é editado
  a partir de material do cliente).

## Terceiros e corte (vídeos editados)
- **Fase 2: só o slot**: nome `POST NN · [terceiros]` / `[corte]`, sem
  conteúdo.
- **Fase 3:** a partir da transcrição do vídeo, gerar **headline** (vira o
  nome do post) + **legenda curta**, na voz do cliente.

## Stories (sequência)
- Fluxo narrativo: gancho → desenvolvimento → reflexão + CTA, transições
  suaves, tom conversacional. Interativos (enquete, caixinha, quiz) conforme
  a marca.
- Caixinha de perguntas: texto da caixinha pronto + perguntas e respostas
  curtas, com profundidade.
