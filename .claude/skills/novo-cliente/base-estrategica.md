# Base estratégica (modelo)

Usado na Etapa 4 da skill `novo-cliente`. É o documento que junta **tudo o
que se sabe do cliente** (briefing, perfil atual, nome) numa visão única e
decidida. Manual da marca, `marca-<slug>`, apresentação de estratégia e
carrosséis leem daqui primeiro.

Salvar em `<cliente>/estrategia/base-estrategica.md`.

## Cenários

| Cenário | Tem perfil? | Tem briefing? | De onde vem a base |
|---|---|---|---|
| A | não | sim | briefing + marca pelo nome ([marca-pelo-nome.md](marca-pelo-nome.md)) |
| B | não | não | nome + nicho + poucas perguntas; quase tudo "proposta" e "a confirmar" |
| C | sim | sim | **cruzamento** briefing × diagnóstico do perfil (seção 5) |
| D | sim | não | diagnóstico do perfil; o que o perfil não mostra vira "a confirmar" |

## Regra de origem (não inventar)

Toda afirmação sobre o cliente leva a etiqueta de onde veio:

- **[B]** dito no briefing
- **[P]** observado no perfil (diagnóstico)
- **[B+P]** briefing e perfil concordam (é o que tem mais peso)
- **[S]** sugestão nossa (proposta, precisa de validação do cliente)

Nada sem etiqueta. Número de seguidores, curtidas ou alcance só se estiver
visível no perfil ou foi informado; nunca estimar.

---

## Modelo do documento

```markdown
# Base estratégica · <Nome>

Cenário: <A/B/C/D> · Fontes: briefing (<data> ou "não há") · perfil @<x>
analisado em <data> (ou "sem perfil") · atualizado em <data>

## 1. Quem é
Síntese em 3 a 4 linhas: profissão, trajetória, onde/como atende, o que
oferece, carro-chefe e oferta de entrada. Com etiquetas.

## 2. Objetivo no Instagram
Objetivo principal (1, no máximo 2) e o que conta como sucesso, sem
prometer número.

## 3. Público
Perfil · dores · desejos · objeções · perguntas frequentes. Com etiquetas.
No cenário C, apontar se o público que o perfil atrai hoje [P] é o mesmo
que o cliente quer atingir [B].

## 4. Posicionamento e diferencial
Uma frase de posicionamento: "<Nome> ajuda <público> a <resultado>
por meio de <diferencial>." + 2 a 3 provas do diferencial.

## 5. Cruzamento briefing × perfil  (só cenário C)
| Ponto | Briefing diz [B] | Perfil mostra [P] | Decisão |
|---|---|---|---|
| Público | | | |
| Tom de voz | | | |
| Visual (cores, fontes, fotos) | | | |
| Oferta e CTA | | | |
| Bio e nome de exibição | | | |
| Destaques | | | |
| Temas e pilares | | | |
| Formatos e frequência | | | |

- **Manter** (funciona e bate com o briefing; o público já reconhece):
- **Corrigir** (perfil contradiz o briefing ou é inconsistente):
- **Criar** (o briefing pede e o perfil ainda não tem):
- **Oportunidades** (força do perfil que o briefing não citou, ex.: tipo
  de post com mais comentários visíveis):
- **Contradições a confirmar com o cliente** (quando não dá pra decidir
  sozinho qual lado vale):

## 6. Marca pelo nome  (só cenários A e B)
@ escolhido/recomendado e alternativas, nome de exibição, bio, monograma,
conceito. Seguir [marca-pelo-nome.md](marca-pelo-nome.md).

## 7. Pilares de conteúdo
Pilar · % · função (educar, identificar, autoridade, relacionamento,
quebrar objeção, vender) · exemplos de tema.

## 8. Tom de voz
3 a 4 adjetivos, 2 exemplos "usar" e 2 "evitar", expressões da marca.

## 9. Formatos e frequência
Só o que o pacote contratado cobre. Restrições de formato (não grava
vídeo, não mostra o rosto) e o que propor no lugar.

## 10. Primeiros temas
8 a 12 temas para o primeiro mês, cada um com pilar, objetivo e origem:
[B] ideia do cliente · [P] assunto que já funcionou no perfil · [S] proposto.

## 11. Restrições
Éticas/legais do conselho profissional, temas proibidos, uso de imagem.

## 12. A confirmar com o cliente
Lista objetiva; cada item com a pergunta pronta para enviar.
```

## Ao terminar

- Mostrar ao Thiago o resumo: cenário, posicionamento (1 frase), pilares,
  e no cenário C as 3 a 5 decisões mais importantes do cruzamento e as
  contradições a confirmar.
- Itens de "A confirmar" vão também para Pendências do `ONBOARDING.md`.
- Quando o briefing chegar depois, ou o perfil for criado/mudar,
  **atualizar** este documento (não criar outro), trocando o cenário e as
  etiquetas, e avisar o que mudou nas decisões.
