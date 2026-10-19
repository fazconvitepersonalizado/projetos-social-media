---
name: "apresentacao-estrategia-conteudo"
description: "Cria uma apresentação de estratégia de conteúdo para Instagram, em 4 partes, para qualquer cliente, a partir do briefing e da estratégia definida."
---

# Apresentação de estratégia de conteúdo (Instagram)

## Antes de começar
1. Localize e leia os materiais do cliente: briefing respondido, guia ou manual da marca, estratégia já desenvolvida, ideias, temas e roteiros enviados pelo cliente, e o pacote contratado.
2. Se a marca tiver mais de uma opção de cor principal ainda não escolhida, pergunte qual usar antes de montar o visual. Pode adiantar o conteúdo enquanto espera.
3. Respeite as restrições específicas do cliente (formatos que ele não faz, temas proibidos, dados pessoais que não podem aparecer).

## Objetivo
Apresentar ao cliente, de forma clara, visual e estratégica, o planejamento que orientará a gestão do perfil, mostrando que cada conteúdo tem um propósito alinhado aos objetivos do negócio.

## PARTE 1 — ENTENDIMENTO DO CLIENTE
- Quem é o cliente: história, área de atuação, serviços e posicionamento atual.
- Objetivo principal no Instagram (atrair clientes, autoridade, reconhecimento, vendas).
- Público-alvo: características, necessidades, dores, desejos e comportamentos.
- Diferencial competitivo: o que o torna único e por que o público deveria escolhê-lo.
Linguagem simples e estratégica, mostrando que entendemos a essência do negócio.

## PARTE 2 — ESTRATÉGIA DE CONTEÚDO
- Pilares de conteúdo e a função estratégica de cada um.
- Tom de voz: características, linguagem, nível de formalidade e exemplos práticos (certo e a evitar).
- Público mapeado: dores, dúvidas, necessidades, desejos e objeções, e como serão abordados.
- Diferenciação frente a outros profissionais do segmento.
- Direcionamento estratégico: como pilares, comunicação e formatos levam ao objetivo.
Explique o motivo de cada decisão; nada genérico.

## PARTE 3 — CALENDÁRIO DE CONTEÚDO
Visão geral do mês:
- Distribuição ao longo das semanas.
- Tema de cada publicação e pilar relacionado.
- Formatos variados (estático, carrossel, Reels, Stories) conforme o pacote contratado.
- Objetivo de cada post (educar, gerar identificação, autoridade, relacionamento, quebrar objeções, vender).
- CTA adequado a cada objetivo.
Organize de forma visual e explique a lógica da distribuição.
Use as ideias, temas e roteiros do cliente como base. Não invente informações sobre o negócio nem atribua ao cliente ideias que ele não deu; se os temas forem propostos por você, diga isso no slide.

## PARTE 4 — PRÓXIMOS PASSOS
- Início da produção: informações, materiais e aprovações necessárias.
- Cronograma: prazos de envio de materiais, produção, revisões e entregas, conforme o pacote.
- Comunicação: canal para alinhamentos, dúvidas e aprovações.
- Responsabilidades: o que é do social media e o que o cliente fornece ou aprova.
- Fluxo de entrega: das ideias e roteiros até a entrega final.
- Continuidade: como acompanhar resultados e ajustar, dentro do escopo contratado.

## Diretrizes
- Linguagem profissional, acolhedora, objetiva e fácil de entender.
- Pouco texto por slide, títulos claros, tópicos curtos e exemplos práticos.
- Identidade visual moderna, elegante e coerente com a marca do cliente (cores, fontes e estilo de imagem do guia).
- Cada decisão vem com sua justificativa.
- Não prometa resultados garantidos (seguidores, vendas).
- Não invente dados, métricas, referências ou características do público.
- Onde faltar informação, marque "a confirmar" e liste no fim o que precisa ser confirmado.
- Use só os serviços e formatos do pacote contratado.
- Não inclua dados pessoais ou de contrato do cliente.

## Entrega
Uma apresentação em slides (artifact de apresentação ou HTML de slides), com link para o usuário. Na resposta, liste em poucas linhas o que ficou "a confirmar" e se os temas do calendário vieram do cliente ou foram propostos.

## Neste projeto (PROJETOS SOCIAL MEDIA)
- **Fonte principal:** `estrategia/base-estrategica.md` (gerada pela skill `novo-cliente`), que já junta briefing, diagnóstico do perfil e marca pelo nome, com etiqueta de origem em cada afirmação ([B] briefing, [P] perfil, [B+P], [S] sugestão nossa). Itens [S] entram na apresentação como proposta; "A confirmar" da base vai para a lista final. No cenário com perfil + briefing, usar o cruzamento (manter / corrigir / criar) para justificar as decisões da Parte 2; no cliente sem Instagram, incluir na Parte 4 a criação do perfil e o plano de estreia (`estrategia/criacao-perfil.md`).
- **Onde estão os outros materiais do cliente**, na pasta dele: `skills/marca-<slug>/SKILL.md` (identidade completa: tom, pilares, restrições, pendências; ver skill `marca-cliente`), `brand-kit.json` (cores HEX, fontes, logo, `brand_manual`), `README.md`, `logo/` e `conteudos/` (carrosséis já feitos, úteis pra mostrar temas e tom já usados). Briefing, estratégia, roteiros e pacote contratado podem estar soltos na pasta do cliente; procurar antes de perguntar. O que não estiver em lugar nenhum vira "a confirmar".
- Se o cliente ainda não tem `marca-<slug>/SKILL.md`, avisar e oferecer criar pela skill `marca-cliente` antes (ou junto) da apresentação.
- Visual: cores e fontes exatamente as do `brand-kit.json`/marca do cliente; logo com contraste real no ponto onde for posicionado (regra de legibilidade do `CLAUDE.md` da raiz).
- Copy dos slides segue as regras gerais do `CLAUDE.md` da raiz: sem travessão/traço no texto (usar ponto e vírgula).
- Se gerar HTML local, salvar em `<cliente>/apresentacoes/<YYYY-MM-DD>-estrategia-conteudo/`, e fazer o commit local quando a apresentação estiver aprovada/finalizada.
