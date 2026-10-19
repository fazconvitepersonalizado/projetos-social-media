---
name: marca-cliente
description: Identidade de marca de qualquer cliente desta pasta (atual ou futuro). Use sempre que pedirem conteúdo para um cliente específico (post, carrossel de 8 cards a partir de um tema, story, legenda, bio, destaques, imagem) ou pedirem para criar/atualizar a "skill de marca", "manual de marca" ou "identidade" de um cliente. Localiza a marca do cliente e, se ainda não existir, gera a partir do modelo template.md.
---

# Marca do cliente (genérica, para qualquer cliente)

Esta skill não guarda dados de nenhum cliente. Ela tem dois papéis:

1. **Usar** a marca de um cliente que já tem a skill preenchida.
2. **Criar/atualizar** a marca de um cliente (novo ou existente) a partir do
   modelo [template.md](template.md).

## Onde fica a marca de cada cliente

```
<Pasta do cliente>/skills/marca-<slug>/SKILL.md
```

Ex.: `Sandra-Behrens/skills/marca-sandra-behrens/SKILL.md`,
`CONSULTORIA A&J/skills/marca-aej-solucoes/SKILL.md`. O slug é o nome do
cliente em minúsculas, sem acento, com hífen.

## 1. Pediram conteúdo para um cliente

1. Identifique o cliente (pelo nome no pedido ou pela pasta onde a sessão foi
   aberta). Se for ambíguo, pergunte qual.
2. Leia `<cliente>/skills/marca-*/SKILL.md` e siga **exatamente** o que está
   lá (tom, pilares, restrições, formato de resposta do carrossel de 8 cards).
3. Se o arquivo não existir, avise e ofereça criar agora (seção 2). Enquanto
   isso, dá pra seguir usando `brand-kit.json` + `README.md` do cliente como
   referência mínima, deixando claro que a marca completa ainda não existe.
4. **Artes visuais** (só se pedirem): a marca define cores, fontes, estilo de
   foto e modelos de peça; a produção do HTML/PNG segue a skill
   `instagram-carousel` da pasta do cliente e todas as regras do `CLAUDE.md`
   da raiz (perguntas obrigatórias sobre fotos, chip de logo, verificação
   visual, legibilidade). Se a marca do cliente e o `brand-kit.json`
   divergirem em cor/fonte/logo, avise e pergunte qual vale antes de produzir.
5. Regras gerais que valem por cima de qualquer marca (do `CLAUDE.md` da raiz):
   sem travessão/traço dentro da copy dos cards (usar ponto e vírgula); os
   rótulos do formato de resposta ("Card 1 — Headline") não contam como copy.

## 2. Criar ou atualizar a marca de um cliente

1. **Juntar o que já existe** antes de perguntar qualquer coisa, na pasta do
   cliente: `estrategia/base-estrategica.md` (fonte principal quando
   existir: posicionamento, público, pilares, tom, restrições, marca pelo
   nome; manter as etiquetas [S] como proposta e "A confirmar" como
   Pendências), `briefing/briefing.md`, `brand-kit.json` (nome, @, cores
   derivadas, fontes, tom, e `brand_manual` se houver), `README.md`, logos em `logo/`, e os carrosséis em
   `conteudos/` (temas já tratados, tom real usado). Para cliente novo sem
   pasta, criar `<Nome do Cliente>/skills/` primeiro.
2. **Preencher o [template.md](template.md)** com esses dados. Cores e fontes
   devem bater com o `brand-kit.json` (mesmos HEX e mesmas fontes); não
   inventar valores novos para o que já está fixado.
3. **Perguntar só o que faltar**, de uma vez, agrupado por seção (Quem é,
   Conceito, Perfil, Tom, Restrições, Conteúdo, Modelos de peça). Usar
   escolhas fechadas quando der. O que o Thiago não souber responder vai para
   "Pendências com o cliente", nunca chutado como fato. Cor ainda não definida
   usa o bloco "A DEFINIR" que está comentado no modelo.
4. **Nunca** incluir dados de contrato (CPF/CNPJ, endereço, nome de documento).
5. Remover do resultado todos os `{{...}}` e o comentário HTML do modelo; se
   uma seção não se aplica ao cliente, apagar a linha em vez de deixar
   placeholder. Conferir no final com uma busca por `{{` no arquivo.
6. Salvar em `<cliente>/skills/marca-<slug>/SKILL.md`, com `name: marca-<slug>`
   no cabeçalho, mostrar um resumo do que foi preenchido e do que ficou em
   Pendências, e fazer o commit local (protocolo de salvamento do `CLAUDE.md`).

## Melhorias no modelo

Mudança que vale para todos os clientes (nova seção, nova regra de formato)
vai no [template.md](template.md) e é replicada nas marcas já preenchidas,
registrando no "Log de decisões" do `CLAUDE.md` da raiz. Mudança de um
cliente só vai no `SKILL.md` daquele cliente.
