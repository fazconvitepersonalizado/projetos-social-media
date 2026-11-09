# Onboarding · Publipost

Checklist do fluxo de cliente novo (skill `novo-cliente`). Marcar cada etapa
ao concluir, com a data. Ao abrir uma sessão nova, o agente lê este arquivo e
retoma dali. Etapa que não se aplica ao cenário: marcar como "não se aplica";
etapa opcional pulada: "pulada por agora".

**Cenário:** B · sem Instagram, sem briefing. Marca genérica criada do zero,
com método inspirado no perfil @v4company (estudo de 15 carrosséis, ~50 capas
e legendas, feito em 2026-11-08).

- [x] **Etapa 1 · Pasta do cliente criada** (2026-11-08)
- [ ] **Etapa 2 · Briefing (opcional)** → pulada por agora (marca genérica, sem cliente real)
- [x] **Etapa 3 · Diagnóstico do perfil** → não se aplica (sem Instagram)
- [ ] **Etapa 4 · Base estratégica** → `estrategia/base-estrategica.md` (ainda não criada; hoje a fonte das regras é `manual/MARCA-PUBLIPOST.md`)
- [~] **Etapa 5 · Manual da marca / identidade** (2026-11-08) → feito: `manual/manual-publipost.html`, `manual/MARCA-PUBLIPOST.md`, `brand-kit.json`, `logo/`; falta: `skills/marca-publipost/SKILL.md` (gerar pela skill `marca-cliente` a partir do MARCA-PUBLIPOST.md)
- [~] **Etapa 6 · Criação do perfil** → @, nome de exibição, bio e destaques definidos no manual; falta conferir disponibilidade do @
- [ ] **Etapa 7 · Apresentação de estratégia** → `apresentacoes/`, `apresentacoes/calendario.md`
- [~] **Etapa 8 · Carrosséis** → 1º carrossel pronto: `conteudos/2026-11-08-importancia-social-media/` (9 slides + legenda; feito antes do fluxo do projeto, sem `sorteio_carrossel.py`)

## Decisões fixadas
- 2026-11-08 · Cor principal: Azul Publi #1A4DFF (alternativa Azul Céu #0A84FF no manual). Neutros: Marinho #070D24, Gelo #F2F4F9; sinal Ciano #2EE6FF só como marca-texto.
- 2026-11-08 · Fontes: Anton (destaque, caixa alta), Archivo (títulos e texto), Caveat (anotações à mão).
- 2026-11-08 · Formato dos slides no manual: 1080 × 1440 (3:4). Atenção: o `export_carousel.py` padrão do projeto exporta 1080 × 1350; decidir qual formato vale para a Publipost antes do próximo carrossel.
- 2026-11-08 · Monograma 96 × 96 em x76,y76 (internos) ou centralizado (capas); barra de continuação 972 × 119 colada na base; título sempre em y 210.
- 2026-11-08 · Estrutura padrão do carrossel: capa → contexto → desenvolvimento → prova/dado → conceito → lição "O que isso muda no seu negócio" → CTA fixo (receitas completas no MARCA-PUBLIPOST.md).

## Pendências com o cliente
- Conferir disponibilidade de @publipost e do domínio publipost.com.br; busca no INPI (classe 35).
- Trocar os [nº] da bio e do slide final por números reais.
- Escolher cor final (Azul Publi ou Azul Céu).
- Fotos reais da equipe para o slide final (as atuais são geradas por IA, em baixa resolução, e as pessoas não existem).
- Validar o monograma com um designer.
