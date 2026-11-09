# Marca Publipost — regras para criar posts no Instagram

Fonte única das regras da marca Publipost. Use este arquivo para criar carrosséis, capas, stories e legendas.
O manual visual completo está em `manual/manual-publipost.html` (abre no navegador, com as imagens em `manual/img/`; link publicado: https://claude.ai/artifact/Gs1oPBCeRh7EtQDB4rvnnC).
Um carrossel de exemplo pronto está em `conteudos/2026-11-08-importancia-social-media/` (`slides.html` gera os PNGs).

Referência de método: perfil @v4company (estrutura e ritmo). Nenhum elemento gráfico da V4 deve ser copiado.

---

## 1. Essência
- **Conceito:** "Todo post é uma aula de negócio." Nenhum post é só notícia: sempre termina em algo que o leitor aplica.
- **Público:** donos de empresa e times de marketing, ocupados, que leem no celular, salvam e encaminham.
- **Personalidade:** direta, curiosa, bem-informada. Usa dados reais e cita a fonte.
- **Fórmula editorial:** notícia ou tema quente → explicação → virada → nome do fenômeno → lição para o negócio do leitor → CTA fixo.

## 2. Perfil
- @ recomendado: `@publipost` (alternativas: `@publipost.br`, `@soupublipost`, `@publipost.mkt`). **Conferir disponibilidade.**
- Nome de exibição: `Publipost | Marketing & Conteúdo`
- Bio:
  ```
  Publipost | Marketing & Conteúdo
  Toda notícia vira uma decisão pro seu negócio.
  +[nº] marcas atendidas | conteúdo novo todo dia útil.
  👇 Peça seu diagnóstico de conteúdo grátis
  publipost.com.br/diagnostico
  ```
- Destaques: Fale conosco · Clientes · Serviços · Diagnóstico · Bastidores · Vagas (círculo azul, ícone branco de traço grosso).
- Nunca inventar números de prova social: `[nº]` fica até ter o dado real.

## 3. Assinatura
- **Wordmark:** "publipost" em Archivo Black/900, minúsculas, letter-spacing −4,5%, seguido de um quadradinho azul.
- **Monograma:** quadrado azul com raio 20%, "P" branco e um quadradinho branco no pé (o "post"). SVG (viewBox 0 0 100 100):
  ```svg
  <rect width="100" height="100" rx="20" fill="#1A4DFF"/>
  <path fill="#fff" d="M27 20h28c14.4 0 24 9.2 24 22.5S69.4 65 55 65H43v15H27V20Zm16 14v17h11c5.4 0 8.6-3.2 8.6-8.5S59.4 34 54 34H43Z"/>
  <rect x="64" y="70" width="12" height="12" rx="2" fill="#fff"/>
  ```
  Versão invertida: fundo branco, P e quadradinho em #1A4DFF (usar sobre azul ou foto escura).
- Respiro mínimo: 40% da largura do monograma. Proibido esticar, recolorir, girar, aplicar sombra.

## 4. Cores
| Token | Hex | Uso |
|---|---|---|
| Azul Publi (destaque) | `#1A4DFF` | tarjas, barra de continuação, selos, palavra-chave |
| Azul Fundo | `#0B2A99` | fim do degradê (160°) dos slides azuis |
| Marinho Noite | `#070D24` | fundos escuros, degradê sobre fotos |
| Gelo | `#F2F4F9` | fundo claro dos slides (nunca branco puro) |
| Ciano Sinal | `#2EE6FF` | marca-texto, sublinhado à mão, tarja de impacto (máx. 5% da peça) |
| Grafite | `#10142A` | texto sobre claro |
| Cinza Azulado | `#5B6280` | créditos, fontes, legendas de foto |
| Branco | `#FFFFFF` | texto sobre azul/marinho, cartões |

- Alternativa de destaque: Azul Céu `#0A84FF` / `#0050B8` (branco só em texto grande: contraste 3,6:1).
- Texto sobre Azul Publi: sempre branco (5,9:1). Texto sobre Ciano: sempre marinho.
- Proporção no feed: Gelo 38% · Marinho 30% · Azul 22% · Branco 6% · Ciano 4%.

## 5. Tipografia (Google Fonts, todas no Canva)
| Papel | Fonte | Uso |
|---|---|---|
| Destaque | **Anton** | só caixa alta, palavras gigantes de capa e impacto, entrelinha 0,9 |
| Títulos e texto | **Archivo** | títulos 800, corpo 400, negritos 700/800 |
| Utilitária | **Caveat** 700 | anotações à mão com seta |
| Só recorte de manchete | Source Serif 4 Bold | simular manchete de jornal |

Escala no arquivo 1080 × 1440:
| Elemento | Fonte | Tamanho | Regra |
|---|---|---|---|
| Palavra gigante da capa | Anton | 230–270 px | 1 linha até 10 caracteres |
| Frase de apoio da capa | Archivo 800 | 56–60 px | até 32 caracteres |
| Título do slide | Archivo 800 | 70 px | máx. 2 linhas (~50 caracteres), palavra-chave em azul |
| Corpo | Archivo 400/700 | 40–44 px | parágrafos até 140 caracteres, máx. 3 por slide |
| Barra de continuação | Archivo 700 | 42 px | 3 a 6 palavras + seta |
| Anotação à mão | Caveat 700 | 48–60 px | sempre com seta, girada −4° a −6° |
| Fonte / crédito | Archivo 400 | 26–28 px | cinza azulado, rodapé |

## 6. Grade base (todos os slides)
- Arquivo **1080 × 1440 px (3:4)**, exportar PNG.
- Margens: 76 px laterais e topo. Área útil: x 76 → 1004 (928 px).
- Monograma 96 × 96: x 76, y 76 (internos) ou x 492, y 76 (capas e slides centralizados).
- Título começa sempre em **y 210**.
- **Barra de continuação:** 972 × 119 em x 54, y 1321, cantos de cima raio 28. Texto Archivo Bold 42 px + seta em quadrado de 58 px com contorno de 5 px e raio 14. Em slide azul, a barra é branca com texto azul.
- Nada importante abaixo de y 1290.
- Duas colunas: texto x 76 → 520 (444 px), imagem x 556 → 1004 (448 px) ou sangrando.
- Raios: fotos/prints 26 px, tarjas 8 px, selo numérico 13 px.

## 7. Receitas das variações

### Capas
- **C1 Capa notícia** (fundo foto): foto sangrada; degradê marinho de 0% em y 500 a 95% em y 1440; monograma centralizado; bloco centralizado terminando em y ~1350: frase de apoio 56 px → PALAVRA Anton 250 px → complemento 58 px em tarja azul ou com sublinhado ciano. Olhos da pessoa entre y 380 e 520. Nunca texto sobre o rosto.
- **C2 Capa tipográfica (série)** (fundo gelo): monograma central; linha 1 Archivo 800 96 px; bordão Anton 300 px azul ("NÃO É"); complemento Archivo 800 80 px; objeto recortado de y 830 a 1350.
- **C3 Capa guia numerado** (foto): tarja azul "Guia com as N…" 58 px; palavra Anton 220–260; tarja branca com texto azul 48 px. O número precisa bater com a quantidade de slides.
- **C4 Frase de autoridade** (gelo + foto P&B): texto em x 0–580, foto P&B em x 580–1080; faixa azul vertical x 650–820 em modo multiplicar; aspas Anton 240 azul; citação Archivo 54 px até 120 caracteres; linha 4 px; nome Archivo Bold Itálico 30 px + cargo 26 px.
- **C5 Antes e depois**: duas fotos 1080 × 720; tarja azul "Primeiro você começa…" e tarja ciano "Depois você melhora." (Archivo 800 60 px, x 60).

### Slides internos
- **I1 Contexto** (gelo): título 70 px; corpo 42 px em 2–3 parágrafos com negrito; dado forte em tarja azul; imagem embaixo (x 76–1004, y 830–1290) ou coluna direita; barra.
- **I2 Numerado** (gelo ou marinho): selo 96 × 74 azul raio 13 com "01" Archivo 800 44 px + título 64 px na mesma linha; texto à esquerda (444 px), prova à direita (448 px); bloco "Mas atenção:" em azul; anotação Caveat com seta; barra.
- **I3 Prova** (marinho): até 2 cartões brancos de manchete (820 px, padding 34 × 40, raio 18, girados −2° e +1,5°); veículo Archivo 800 26 px azul caixa alta + manchete Source Serif 48 px. Variação: prints de comentários reais (620 px, ±2°). Sempre fonte real, nunca manchete inventada.
- **I4 Impacto** (foto escurecida, marinho ou azul): palavra Anton 170–220 px em tarja ciano (texto marinho) de borda a borda (x 40–1040), até ~13 caracteres; frase de contexto acima e de fecho abaixo. Máx. 1 por carrossel.
- **I5 Dado** (degradê azul): título branco 70 px; barras de 34 px com trilho branco 18%, a barra principal em ciano; rótulos 38 px com valor; fonte obrigatória 28 px no rodapé; barra de continuação branca.
- **I6 Print de app** (gelo): mockup de celular (borda preta 22 px, raio 60) em x 570–1030; lista com checks 40 px; contorno azul 6 px no ponto que importa.
- **I7 Conceito** (gelo, centralizado): "Isso tem nome: [conceito em azul]" 70 px; explicação 42 px; frase Anton 150–190 px azul; anotação Caveat cinza.
- **I8 Lição** (gelo, **sem barra**): título fixo "O que isso *muda no seu negócio*" (parte em azul itálico); ponte 42 px; "Antes de [ação], pergunte:" Archivo 800 azul; checklist 3–5 itens 40 px.

### Fechamento
- **F1 CTA fixo** (foto da equipe): degradê marinho; cartão branco com print do perfil (x 120, y 690, 840 px, raio 28) e link contornado em azul 4 px; chamada Archivo 800 54 px "Clique no link da bio e peça seu diagnóstico de conteúdo". Igual em todos os carrosséis.

## 8. Sequências por tipo de post
| Tipo | Sequência | Total |
|---|---|---|
| Notícia que vira lição | C1 → I1 → I2 ou I1 → I3 → I5 ou I4 → I7 → I8 → F1 | 8 |
| Guia numerado | C3 → I1 → I2 × 3–5 → I8 → F1 | 7–9 |
| Série de anáfora | C2 → C2 × 4–6 → I8 → F1 | 7–9 |
| Comparativo de dados | C1/C3 → I1 → I5 × 2–3 → I2 → I8 → F1 | 8 |
| Novidade de app | C1 → I6 × 3–4 → I7 → I8 → F1 | 7–8 |
| Case de cliente | C1 → I1 → I4 → I5 → I3 → I8 → F1 | 7 |
| Frase de autoridade | C4 sozinha ou C4 + I1 + I8 + F1 | 1 ou 4 |
| Bastidores | C5 → fotos com tarja → F1 | 4–6 |

**Regras de fundo:** nunca 3 slides seguidos iguais; slide azul inteiro no máx. 2 vezes e nunca colado na capa; sequência padrão foto → gelo → gelo → marinho → azul → gelo → gelo → foto. Na grade, no máx. 2 capas claras seguidas.

**Frases para a barra de continuação** (uma diferente por slide): Mas tem um detalhe · E isso muda tudo · Agora, a verdade · E aí veio a virada · Isso tem nome · E o que isso ensina? · Só que tem um problema · Agora, no seu negócio · E não para por aí · E tem o mais importante.

**Checklist antes de exportar:** monograma na mesma posição; título em y 210; uma palavra azul por título, uma tarja por slide, no máx. um marca-texto ciano; cada barra com frase diferente; toda prova com fonte; nenhum texto sobre rosto.

## 9. Imagem
- Rosto em close com expressão clara, pessoa recortada com o tema ao fundo, produto em destaque, prints reais.
- Contraste alto, cor levemente fria, degradê marinho embaixo nas capas, autoridade em P&B. Nunca filtro quente/sépia.
- Preferir banco licenciado, imagens oficiais de imprensa ou IA sem rostos reais.
- Prompt base (IA):
  > Editorial photograph for a business news Instagram cover, 3:4 vertical. [cena]. Close-up, strong facial expression, sharp focus, high contrast, slightly cool color grade, subtle electric blue (#1A4DFF) rim light. Bottom 40% of the frame darker and less busy to receive large headline text. No text, no logos.
- Pessoas geradas por IA não existem e não podem ser apresentadas como clientes ou equipe.

## 10. Tom de voz
| Evitar | Usar |
|---|---|
| Neste post vamos falar sobre a importância do branding. | Branding não é o seu logo. |
| Muitas empresas tiveram resultados positivos. | A marca vendeu 27% mais em 4 meses. (só com dado real) |
| Confira mais no próximo slide! | Mas tem um detalhe → |
| Somos especialistas em soluções 360°. | Em 30 dias, a gente organiza o seu conteúdo para o ano todo. |
| Arrasta pro lado 🔥🔥🔥 | Encaminhe para quem precisa saber disso. |

**Estrutura da legenda:**
1. Abre com a pergunta que a pessoa digitaria na busca.
2. Conta a história em parágrafos de 1 a 3 frases.
3. Vira para o negócio do leitor ("E é aqui que entra o seu negócio…").
4. Fecha com `👇 Clique no link da bio e peça seu diagnóstico de conteúdo.`

## 11. Conteúdo
- Pilares: Notícia → lição 40% · Guias 25% · Autoridade 15% · Cases 10% · Oferta 10%.
- Frequência: 5 carrosséis por semana (um por dia útil) + 2 Reels + Stories diários com enquete puxando para o post do dia.

## 12. Pendências
- Conferir @publipost e domínio publipost.com.br; busca no INPI (classe 35).
- Trocar todos os `[nº]` por números reais.
- Escolher cor final (Azul Publi ou Azul Céu).
- Fotografar a equipe para o slide F1.
- Montar templates no Canva com estas medidas.
- Validar o monograma com um designer.
