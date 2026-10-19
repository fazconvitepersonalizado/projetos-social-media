# {{NOME}}

Pasta do cliente {{NOME}} (slug `{{SLUG}}`), criada em {{DATA}} pelo fluxo
de cliente novo (skill `novo-cliente`, na raiz de PROJETOS SOCIAL MEDIA).

Andamento do onboarding: ver [ONBOARDING.md](ONBOARDING.md).

## Estrutura

```
briefing/briefing.md            # briefing respondido (Etapa 3, opcional)
manual/                         # manual da marca: HTML/PDF/links (Etapa 4, opcional)
brand-kit.json                  # cores, fontes e logo usados nos carrosséis (Etapa 2)
skills/marca-{{SLUG}}/SKILL.md  # identidade da marca: tom, pilares, restrições (Etapa 2)
apresentacoes/                  # apresentação de estratégia (Etapa 5)
logo/                           # logo-primary / logo-white / logo-dark (SVG ou PNG)
assets/raw/                     # fotos originais, sem tratamento
conteudos/<YYYY-MM-DD>-<slug>/  # um carrossel por pasta (Etapa 6)
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
