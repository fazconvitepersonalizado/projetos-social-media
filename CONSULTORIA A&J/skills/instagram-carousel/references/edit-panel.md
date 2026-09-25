# Edit Panel + Download HTML (Review step)

After generating the carousel HTML, the user wants to **open it in a browser, tweak text per slide in a side panel, and download the edited HTML** before the export step.

## Hard constraints (do not break)

1. The edit panel is purely additive. It MUST live **outside** `.ig-frame` and MUST NOT modify any rule from [[design-system.md]] or [[export.md]].
2. `.ig-frame` width stays at **420px** exactly. Do not change layout to make room for the panel — use `body { display:flex; gap:24px; }`.
3. Every editable text element keeps an attribute `data-edit-id="slide{N}-{role}"` (e.g. `slide1-headline`, `slide3-cta`). Use stable role names: `tag`, `headline`, `subhead`, `body`, `quote`, `cta`, `item-{i}-title`, `item-{i}-desc`, `step-{i}-title`, `step-{i}-desc`.
4. The panel script and panel DOM MUST be stripped from the downloaded file so the exporter sees a clean HTML.

## Where to inject

In the generated `carousel.html`:

- Add `<aside id="carousel-editor">…</aside>` as a sibling of `.ig-frame`, inside `<body>`.
- Add a single `<script id="carousel-editor-script">…</script>` at the end of `<body>` containing the build/wire/download logic below.
- Wrap `<body>` style as `display:flex; gap:24px; align-items:flex-start; padding:24px;` (only when the panel is present — the export script already overrides body styles, so this is fine).

## Required panel features

- Header with the carousel topic + a "Baixar HTML" button.
- One collapsible group per slide titled `Slide N — {type}` (Hero, Problem, Solution, etc).
- Inside each group, one `<textarea>` (auto-resize) per element with `data-edit-id`, labeled with the role name. Multi-line allowed.
- Live binding: typing in a textarea updates `textContent` of the matching element in real time.
- "Baixar HTML" produces a clean HTML file: clones `document.documentElement`, removes `#carousel-editor` and `#carousel-editor-script`, resets `body` inline style, then triggers a `Blob` download named `carousel.html`.

## Reference snippet (paste into the generated HTML, adjust ids)

```html
<aside id="carousel-editor" style="
  width:360px;max-height:90vh;overflow:auto;
  background:#fff;border:1px solid #e5e5e5;border-radius:14px;
  padding:18px;font-family:system-ui,sans-serif;font-size:13px;
  box-shadow:0 4px 24px rgba(0,0,0,0.06);position:sticky;top:24px;
">
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;">
    <strong style="font-size:14px;">Editar carrossel</strong>
    <button id="ce-download" style="
      background:#111;color:#fff;border:0;border-radius:8px;
      padding:8px 14px;font-weight:600;cursor:pointer;font-size:12px;">
      Baixar HTML
    </button>
  </div>
  <div id="ce-groups"></div>
  <p style="margin-top:14px;color:#888;font-size:11px;line-height:1.4;">
    O download remove o painel e gera um <code>carousel.html</code> limpo,
    pronto para exportar. Substitua o arquivo em
    <code>conteudos/&lt;data&gt;-&lt;slug&gt;/carousel.html</code>.
  </p>
</aside>

<script id="carousel-editor-script">
(function(){
  const SLIDE_LABELS = {
    1:"Hero",2:"Problem",3:"Solution",4:"Features",
    5:"Details",6:"How-to",7:"CTA"
  }; // override per sequence
  const groups = document.getElementById('ce-groups');
  const slides = {};
  document.querySelectorAll('[data-edit-id]').forEach(el => {
    const id = el.getAttribute('data-edit-id');
    const m = id.match(/^slide(\d+)-(.+)$/);
    if(!m) return;
    const n = +m[1];
    (slides[n] = slides[n] || []).push({id, role:m[2], el});
  });
  Object.keys(slides).sort((a,b)=>+a-+b).forEach(n => {
    const det = document.createElement('details');
    det.open = (+n <= 2);
    det.style.cssText = 'margin-bottom:8px;border:1px solid #eee;border-radius:8px;padding:8px 10px;';
    det.innerHTML = `<summary style="cursor:pointer;font-weight:600;">Slide ${n} — ${SLIDE_LABELS[n]||''}</summary>`;
    slides[n].forEach(({id, role, el}) => {
      const wrap = document.createElement('div');
      wrap.style.cssText = 'margin:8px 0;';
      const label = document.createElement('label');
      label.textContent = role;
      label.style.cssText = 'display:block;color:#666;font-size:11px;margin-bottom:4px;text-transform:uppercase;letter-spacing:1px;';
      const ta = document.createElement('textarea');
      ta.value = el.textContent.trim();
      ta.style.cssText = 'width:100%;min-height:48px;border:1px solid #ddd;border-radius:6px;padding:8px;font:inherit;resize:vertical;';
      ta.addEventListener('input', () => { el.textContent = ta.value; });
      wrap.append(label, ta);
      det.append(wrap);
    });
    groups.append(det);
  });
  document.getElementById('ce-download').addEventListener('click', () => {
    const clone = document.documentElement.cloneNode(true);
    clone.querySelector('#carousel-editor')?.remove();
    clone.querySelector('#carousel-editor-script')?.remove();
    const body = clone.querySelector('body');
    if (body) body.removeAttribute('style');
    const html = '<!doctype html>\n' + clone.outerHTML;
    const blob = new Blob([html], {type:'text/html'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'carousel.html';
    document.body.appendChild(a); a.click(); a.remove();
  });
})();
</script>
```

## Safety check before handoff to export

When the user says "pode exportar":

1. Confirm the **clean** `conteudos/<date>-<slug>/carousel.html` exists (no `#carousel-editor` element in it). If the file still has the panel, ask the user to download via the "Baixar HTML" button first, or strip it server-side before running the exporter.
2. The exporter from [[export.md]] runs against this clean file.
