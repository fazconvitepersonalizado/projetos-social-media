# Plano do mês (arquivo local)

Salvar em `<cliente>/conteudos/planos/<AAAA-MM>.md` (ex.:
`Sandra-Behrens/conteudos/planos/2026-11.md`). É a fonte da verdade do mês;
o Trello espelha este arquivo.

## Modelo

```markdown
# Plano de conteúdo · <Nome do cliente> · <Mês> de <AAAA>

Status: Fase 1 aprovada em <data> · Fase 2 em <data> · Trello: espelhado em <data> (ou "pendente")
Cadência: <ex.: carrossel 2×/semana + post único 1×/semana> · Fonte: <base-estrategica / marca-<slug> / brand-kit + README>
Calendário de partida: <apresentacoes/.../calendario.md, ou "nenhum">

## Calendário

### Semana 1 (<dd/mm> a <dd/mm>)
| # | Dia | Formato | Pilar | Tema | Origem |
|---|---|---|---|---|---|
| 01 | seg 03/11 | carrossel | <pilar> | <tema> | [B]/[P]/[S] |
| 02 | qua 05/11 | terceiros | | (slot) | |

### Semana 2 ...

## Posts

### POST 01 · [carrossel] <tema>
Data: <AAAA-MM-DD> · Pilar: <pilar> · Objetivo: <educar/identificar/...> · Trello: <link do cartão ou "pendente">
Sorteio: estrutura <x> · gancho <y> · seed <n> (gravado no histórico do cliente)
Pasta da arte: <conteudos/AAAA-MM-DD-slug/ ou "ainda não produzida">

Referências e observações:
<...>

Texto da arte:
Card 1 (headline)
<texto>
Card 2
<texto>
...
Card 8 (encerramento)
<texto>

Legenda:
<legenda>

Revisão anti-IA: <nota>/50

### POST 02 · [terceiros]
Data: ... · aguardando vídeo
```

## Regras
- Uma seção `### POST NN` por post, na ordem do número; o cabeçalho é igual
  ao nome do cartão no Trello.
- Etiquetas de origem do tema, como na base estratégica: **[B]** ideia do
  cliente/briefing, **[P]** assunto que já funcionou no perfil, **[S]**
  sugestão nossa.
- Temas trocados ou posts refeitos (skill `alterar-conteudo`) substituem o
  bloco do post; o histórico fica no git, sem cópias "v2" no arquivo.
