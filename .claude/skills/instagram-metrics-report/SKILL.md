---
name: instagram-metrics-report
description: >-
  Gera o Relatório de Métricas do Instagram de um cliente (PDF de 2 a 3
  páginas, nas cores do brand-kit do próprio cliente) a partir de prints do
  Instagram Insights. Use SEMPRE que o Thiago enviar capturas de tela/prints
  de métricas do Instagram e pedir relatório mensal, relatório de métricas,
  relatório de desempenho ou análise de uma conta, mesmo que diga só "monta
  o relatório da [cliente] de [mês]" ou "relatório do Instagram". Também
  cobre incluir os 5 melhores conteúdos do mês. Não usar para relatórios que
  não sejam de Instagram nem para simples leitura de uma imagem sem pedido de
  relatório.
---

# Relatório de métricas do Instagram

Transforma prints do Instagram Insights num PDF profissional, **na
identidade visual do próprio cliente** (cores do `brand-kit.json`). O
relatório tem 2 páginas fixas (visão geral + comparativo por formato) e uma
3ª página opcional com o **Top 5 conteúdos do mês**.

## O que o Thiago fornece
Pensada para rodar todo mês, para vários clientes. Em cada pedido:
1. **Prints do Instagram Insights** (visão geral do período, seguidores vs
   não seguidores, alcance, interações por formato e, para o Top 5, o
   "Conteúdo principal").
2. **Cliente** (nome da pasta dele neste projeto, ex.: "Sandra-Behrens").
3. **Mês de referência** (ex.: "Outubro", "Novembro 2026").
4. **Perfil** (@ ou link): se não vier, usar o `instagram_handle` do
   `brand-kit.json` do cliente.

Cada relatório é independente. Se faltar o cliente ou o mês, perguntar de
forma curta antes de gerar. Se faltarem prints, **não inventar números**:
pedir os que faltam.

## Fluxo de trabalho
1. **Ler este SKILL.md inteiro** e depois `references/data_schema.md` para o
   formato exato do JSON.
2. **Extrair as métricas dos prints** (imagens no chat ou arquivos indicados
   pelo Thiago). Mapear cada valor para os campos do schema (tabela abaixo).
   Manter os números EXATAMENTE como aparecem nos prints.
3. **Montar o Top 5** (ordenado por visualizações, a partir do que o Thiago
   enviar); ver "Top 5 conteúdos do mês".
4. **Escrever `dados.json`** (molde: `references/exemplo_dados.json`, que é
   fictício) em `<cliente>/relatorios/<AAAA-MM>/dados.json`.
5. **Gerar o PDF** (na raiz do projeto):
   ```bash
   python .claude/skills/instagram-metrics-report/scripts/generate_report.py "<cliente>/relatorios/<AAAA-MM>/dados.json" "<cliente>/relatorios/<AAAA-MM>/Relatorio_Metricas_<Cliente>_<Mes>_<Ano>.pdf" --brand "<cliente>/brand-kit.json"
   ```
   - Sem `brand-kit.json`, o script usa uma paleta neutra; avisar o Thiago.
   - Se o script avisar que a fonte do cliente não foi encontrada, dizer
     isso na entrega (ver "Identidade visual").
6. **Verificação visual (obrigatória):** renderizar cada página como imagem
   (ex.: `pymupdf`, `page.get_pixmap(dpi=110)`) e ler de volta: números
   batem com os prints, nada cortado/sobreposto, texto legível contra o
   fundo daquele ponto. Se achar problema, **avisar antes de mexer**.
7. **Entregar:** caminho do PDF + resumo curto (2 a 3 frases) dos destaques.
   Não despejar todos os números no chat; o PDF já mostra.
8. Commit local do relatório finalizado (protocolo do `CLAUDE.md` da raiz).
   Prints com dados do cliente ficam fora do git só se o Thiago pedir.

## Mapeamento de métricas (Instagram Insights → JSON)
O Insights muda de tela conforme a versão, mas os valores são os mesmos:

| No print procure por…                              | Campo JSON              |
|----------------------------------------------------|-------------------------|
| Visualizações totais do período                     | `views_total`          |
| Interações totais                                  | `interacoes_total`     |
| Contas alcançadas                                  | `contas_alcancadas`    |
| Total de seguidores (atual)                        | `total_seguidores`     |
| Novos seguidores no período                        | `novos_seguidores`     |
| Seguiram / Follows                                 | `follows`              |
| Deixaram de seguir / Unfollows                     | `unfollows`            |
| Saldo (follows − unfollows)                        | `net` (calcular se faltar) |
| Nº de publicações no período                        | `publicacoes`          |
| % de views de seguidores / não seguidores          | `views_seg_pct` / `views_nonseg_pct` |
| % de interações de seguidores / não seguidores     | `inter_seg_pct` / `inter_nonseg_pct` |
| Views por formato (Posts/Reels/Stories) em %       | `views_formato`        |
| Interações por formato em %                         | `inter_formato`        |
| Variação das contas alcançadas (ex.: −14,6%)       | `contas_alcancadas_var`|
| @ ou link do perfil (do Thiago ou do brand-kit)    | `perfil`               |

Regras importantes:
- **Valores estimados/aproximados**: quando o número for arredondado ou lido
  de um gráfico (ex.: "~35%"), escrever como string com til: `"~35"`. O
  gerador mostra o "~" e formata. Valores exatos vão como número (`41.3`).
- As porcentagens por formato devem **somar ~100%** dentro de cada grupo
  (views e interações separadamente). Se não somarem, revisar a leitura.
- No JSON, ponto decimal (`41.3`); o gerador formata em pt-BR (milhar com
  ".", decimal com ",").
- O **índice de engajamento** por formato (% interações ÷ % views) é
  calculado automaticamente. Não fornecer.

## Top 5 conteúdos do mês
O Top 5 é **ordenado por visualizações** e os **conteúdos vêm do Thiago**
(print, lista ou texto do "Conteúdo principal" do Insights). Usar exatamente
o que ele enviar, **da maior para a menor view**.

Para cada um dos 5:
1. **Ordenar por views**, do maior para o menor (1º lugar = mais views).
2. **`titulo`** curto a partir do tema; **`formato`** (Reels, Posts,
   Carrossel, Stories); **`obs`** opcional de 1 linha.
3. **`metricas`**: começa sempre por `views` e inclui as outras que ele
   enviar (interações, alcance, salvamentos, compartilhamentos,
   comentários). Não inventar valores; mostrar só o que existe.
4. **`link`** do post (abaixo).

Dica: os carrosséis do cliente estão em `<cliente>/conteudos/` e o plano do
mês em `<cliente>/conteudos/planos/<AAAA-MM>.md`; ajudam a nomear o tema e o
formato de cada post do Top 5 (sem trocar o que o Insights mostrou).

### Link de cada post
Cada cartão mostra "Ver publicação →" e fica **clicável**. O `link` precisa
ser um permalink **real**:
- Se o Thiago enviar os links, usar como estão.
- Se não enviar, tentar encontrar: com o `perfil` e o tema, buscar na web
  (ex.: `site:instagram.com <handle> <tema>`) o permalink real e confirmar o
  tema abrindo a página, se possível.
- Se não der para confirmar o post certo (o Instagram às vezes exige
  login), **pedir o link**. **Nunca inventar URL**; sem link, deixar vazio.

Sem página de Top 5 no mês: omitir o campo `top5` (relatório com 2 páginas).

> Os links no PDF são anotações clicáveis padrão e funcionam em leitores
> normais (Acrobat, navegador, celular). Algumas pré-visualizações dentro de
> apps não tornam o link clicável; baixar/abrir o PDF resolve.

## Destaques e recomendações
Os blocos "Destaques do período" e "Recomendações" da página 2 (e os selos
das caixas de origem do público) são gerados **a partir dos números**: o
texto muda conforme o tamanho do alcance externo, o saldo de seguidores e a
relação alcance × base, então serve para contas pequenas e grandes. Para
personalizar, fornecer `destaques` e `recomendacoes` no JSON (uma frase por
item), em tom objetivo e orientado a ação, **sem travessão** (regra do
`CLAUDE.md` da raiz) e sem prometer resultado.

## Idioma
Português do Brasil.

## Identidade visual (implementada no gerador)
- **Cores:** vêm do bloco `derived` do `brand-kit.json` do cliente
  (`--brand`). O gerador escolhe a cor dos painéis pela legibilidade real:
  usa `BRAND_PRIMARY` se ela aguentar texto branco (contraste ≥ 4,5) e, se
  não, `BRAND_DARK` (escurecida até atingir o contraste). Fundo =
  `LIGHT_BG`; texto = `DARK_BG`; a segunda série dos gráficos é um tom claro
  da cor dos painéis. Verde/vermelho de "subiu/caiu" são fixos.
- **Fontes:** títulos/números na `heading_font` do cliente e corpo na
  `body_font`, **se** houver TTF estático em `<cliente>/assets/fonts/` (ou
  na pasta passada em `--fonts`), com nomes `<Família>-<Peso>.ttf` sem
  espaço (ex.: `CormorantGaramond-Regular.ttf`, `Lora-Bold.ttf`). O zip
  "Download family" do Google Fonts traz esses arquivos na pasta `static/`.
  Sem o arquivo, cai em **Playfair Display** (títulos) + **Poppins** (corpo),
  que vêm na skill (`assets/fonts/`, licença livre OFL), e o script avisa.
- Layout, tamanhos e posições não mudam sem pedido.

## Estrutura da skill

```
instagram-metrics-report/
├── SKILL.md
├── scripts/
│   └── generate_report.py     # gerador ReportLab (JSON → PDF, --brand, --fonts)
├── references/
│   ├── data_schema.md         # campos do JSON, detalhado
│   └── exemplo_dados.json     # exemplo FICTÍCIO completo (molde)
└── assets/
    └── fonts/                 # Playfair Display, Poppins, Symbols (fallback)
```

## Notas técnicas
- Dependência: `reportlab` (`pip install reportlab`). Para a verificação
  visual: `pymupdf` (`pip install pymupdf`).
- Uso: `python scripts/generate_report.py dados.json saida.pdf [--brand brand-kit.json] [--fonts pasta]`.
- Páginas: 2 se `top5` estiver ausente/vazio; 3 se tiver itens.
- Saída padrão: `<cliente>/relatorios/<AAAA-MM>/`.
