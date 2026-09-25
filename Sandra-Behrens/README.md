# carrossel-instagram (template)

Projeto-template para gerar carrosséis do Instagram usando a skill
`instagram-carousel` com um fluxo próprio: brand kit persistido, planejamento
por tema, HTML com painel de edição e exportação em PNG por carrossel.

## Requisitos

- Python 3.10+
- [Claude Code](https://docs.claude.com/claude-code) (a skill `instagram-carousel` é executada por ele)

## Instalação

```bash
git clone <url-do-repo> carrossel-instagram
cd carrossel-instagram

python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
playwright install chromium
```

## Fluxo

1. **Phase 0 — Detecção:** o agente verifica `brand-kit.json` na raiz.
2. **Phase 1 — Brand kit** (se faltar): coleta nome, handle, cor primária,
   fontes, tom, idioma e salva em `brand-kit.json`.
3. **Phase 2 — Planejamento:** você passa o tema, a skill propõe sequência e
   plano por slide — incluindo quais slides levam foto real (sua ou buscada
   pelo agente).
4. **Phase 3 — Geração de HTML:** se houver foto a buscar, o agente pesquisa
   opções livres de direitos e alinhadas ao tema do slide e à identidade da
   marca, ajusta (crop/tint) e só então gera
   `conteudos/<YYYY-MM-DD>-<slug>/carousel.html`, já com painel lateral de
   edição.
5. **Phase 4 — Revisão e edição:** abra o HTML no navegador, edite textos no
   painel lateral, clique em **Baixar HTML** e substitua o arquivo no carrossel.
6. **Phase 5 — Exportação:** rode o exportador (ou diga "pode exportar" para
   o agente). O Playwright gera os PNGs 1080×1350 em
   `conteudos/<YYYY-MM-DD>-<slug>/slides/`.

### Exportar manualmente

```bash
python export_carousel.py conteudos/2026-05-14-tema-do-carrossel --slides 7
```

## Estrutura

```
brand-kit.json                 # criado na primeira execução (gitignored)
conteudos/                     # carrosséis gerados (gitignored)
  2026-05-13-7-erros-de-copy/
    carousel.html
    slides/
      slide_1.png
      ...
export_carousel.py             # exportador HTML -> PNG (Playwright)
requirements.txt
skills/instagram-carousel/
  SKILL.md                     # orquestrador do fluxo
  references/
    brand-kit.md
    images.md
    photo-sourcing.md
    design-system.md
    edit-panel.md
    export.md
```

As regras técnicas de design e exportação ficam intactas em `references/` — o
orquestrador adiciona o fluxo de trabalho por cima sem alterar nenhuma
instrução crítica.

## Notas

- `brand-kit.json` e o conteúdo de `conteudos/` ficam fora do versionamento
  (ver `.gitignore`) — são dados locais de cada usuário/projeto.
