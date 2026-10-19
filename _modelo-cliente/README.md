# {{NOME}}

Pasta do cliente {{NOME}} (slug `{{SLUG}}`), criada em {{DATA}} pelo fluxo
de cliente novo (skill `novo-cliente`, na raiz de PROJETOS SOCIAL MEDIA).

Andamento do onboarding: ver [ONBOARDING.md](ONBOARDING.md).

## Estrutura

```
briefing/briefing.md            # briefing respondido (Etapa 2, opcional)
estrategia/diagnostico-perfil.md # o que o perfil atual mostra (Etapa 3, só com Instagram)
estrategia/base-estrategica.md  # fonte única: briefing + perfil + nome (Etapa 4)
manual/                         # manual da marca: HTML/PDF/links (Etapa 5)
brand-kit.json                  # cores, fontes e logo usados nos carrosséis (Etapa 5)
skills/marca-{{SLUG}}/SKILL.md  # identidade da marca: tom, pilares, restrições (Etapa 5)
estrategia/criacao-perfil.md    # checklist do perfil novo (Etapa 6, só sem Instagram)
apresentacoes/                  # apresentação de estratégia + calendario.md (Etapa 7)
logo/                           # logo-primary / logo-white / logo-dark (SVG ou PNG)
assets/raw/                     # fotos originais, sem tratamento
conteudos/<YYYY-MM-DD>-<slug>/  # um carrossel por pasta (Etapa 8)
conteudos/planos/<AAAA-MM>.md   # plano do mês (skill conteudo-mensal); fonte da verdade
relatorios/<AAAA-MM>/           # relatório de métricas em PDF (skill instagram-metrics-report)
trello.json                     # IDs do quadro do cliente no Trello (criado no 1º uso)
skills/instagram-carousel/      # geração dos carrosséis (HTML + exportação PNG)
skills/instagram-publish/       # publicação via Meta API
export_carousel.py              # exportador HTML -> PNG 1080x1350
```

## Requisitos (uma vez por máquina)

```bash
pip install -r requirements.txt
playwright install chromium
```

## Exportar um carrossel manualmente

```bash
python export_carousel.py conteudos/<YYYY-MM-DD>-<slug> --slides 8
```
