"""Gera galeria.html na raiz da pasta, listando todos os carrosseis de todos
os projetos (qualquer pasta com conteudos/<data>-<slug>/carousel.html).

Uso:
    python generate_gallery.py

Roda toda vez que um carrossel novo for criado/editado, pra manter a galeria
atualizada. Gera uma miniatura (slide 1) de cada carrossel em
.gallery-cache/ (fora do git) e um card clicavel que abre o carousel.html
original.
"""
import asyncio
import json
import re
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent
CACHE_DIR = ROOT / ".gallery-cache"
CACHE_DIR.mkdir(exist_ok=True)

THUMB_W, THUMB_H, THUMB_SCALE = 420, 525, 1.2


def humanize_slug(slug: str) -> str:
    # remove prefixo de data YYYY-MM-DD-
    m = re.match(r"^\d{4}-\d{2}-\d{2}-(.+)$", slug)
    rest = m.group(1) if m else slug
    words = rest.replace("-", " ").replace("_", " ").split()
    return " ".join(w.capitalize() for w in words)


def extract_date(slug: str) -> str:
    m = re.match(r"^(\d{4}-\d{2}-\d{2})-", slug)
    return m.group(1) if m else ""


def count_slides(html: str) -> int:
    # Slide markup changed across skill versions (ig-slide class vs plain
    # divs), but every slide always carries at least one data-edit-id
    # attribute prefixed "slideN-" — the highest N is a reliable proxy.
    nums = [int(n) for n in re.findall(r'data-edit-id="slide(\d+)-', html)]
    return max(nums) if nums else html.count('class="ig-slide"')


def load_brand(project_dir: Path) -> dict:
    bk = project_dir / "brand-kit.json"
    if bk.exists():
        try:
            data = json.loads(bk.read_text(encoding="utf-8"))
            return {
                "name": data.get("brand_name", project_dir.name),
                "primary": data.get("derived", {}).get("BRAND_PRIMARY", "#333333"),
                "light_bg": data.get("derived", {}).get("LIGHT_BG", "#F4F0E7"),
            }
        except Exception:
            pass
    return {"name": project_dir.name, "primary": "#333333", "light_bg": "#F4F0E7"}


def creation_ts(html_path: Path, slug: str) -> float:
    # Prefer the date encoded in the folder slug (that's the carousel's real
    # "creation day" from the skill's naming convention) combined with the
    # file's own timestamp for same-day ordering; fall back to mtime/ctime
    # alone if the slug has no date prefix.
    stat = html_path.stat()
    fs_ts = getattr(stat, "st_ctime", stat.st_mtime)
    date_str = extract_date(slug)
    if not date_str:
        return fs_ts
    try:
        import datetime
        day_start = datetime.datetime.strptime(date_str, "%Y-%m-%d").timestamp()
    except ValueError:
        return fs_ts
    # keep the slug's calendar day, but use the file's time-of-day for
    # ordering carousels created on the same date
    frac_of_day = fs_ts % 86400
    return day_start + frac_of_day


def discover_carousels():
    items = []
    for project_dir in sorted(ROOT.iterdir()):
        if not project_dir.is_dir() or project_dir.name.startswith("."):
            continue
        conteudos = project_dir / "conteudos"
        if not conteudos.exists():
            continue
        brand = load_brand(project_dir)
        for slug_dir in sorted(conteudos.iterdir()):
            html_path = slug_dir / "carousel.html"
            if not html_path.exists():
                continue
            html = html_path.read_text(encoding="utf-8", errors="ignore")
            items.append({
                "project": project_dir.name,
                "brand": brand,
                "slug": slug_dir.name,
                "title": humanize_slug(slug_dir.name),
                "date": extract_date(slug_dir.name),
                "ts": creation_ts(html_path, slug_dir.name),
                "slides": count_slides(html),
                "html_path": html_path,
                "rel_link": html_path.relative_to(ROOT).as_posix(),
                "thumb_name": f"{project_dir.name}__{slug_dir.name}.png".replace(" ", "_").replace("&", "and"),
            })
    items.sort(key=lambda x: x["ts"], reverse=True)
    return items


async def render_thumb(html_path: Path, out_path: Path):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": THUMB_W, "height": THUMB_H},
            device_scale_factor=THUMB_SCALE,
        )
        await page.set_content(html_path.read_text(encoding="utf-8"), wait_until="networkidle")
        await page.wait_for_timeout(900)
        await page.evaluate("""() => {
            const vp = document.querySelector('.ig-viewport') || document.querySelector('.carousel-viewport');
            if (!vp) return;
            document.body.innerHTML = '';
            document.body.appendChild(vp);
            document.body.style.cssText = 'padding:0;margin:0;display:block;overflow:hidden;background:#000;';
            vp.style.cssText = 'position:relative;width:420px;height:525px;overflow:hidden;background:#000;';
            const track = document.querySelector('.ig-track') || document.querySelector('.carousel-track');
            if (track) track.style.transition = 'none';
        }""")
        await page.wait_for_timeout(200)
        await page.screenshot(path=str(out_path), clip={"x": 0, "y": 0, "width": THUMB_W, "height": THUMB_H})
        await browser.close()


async def ensure_thumbs(items, force=False):
    for it in items:
        out = CACHE_DIR / it["thumb_name"]
        if force or not out.exists() or out.stat().st_mtime < it["html_path"].stat().st_mtime:
            print("Gerando miniatura:", it["project"], "/", it["slug"])
            await render_thumb(it["html_path"], out)
        it["thumb_rel"] = out.relative_to(ROOT).as_posix()


def build_html(items) -> str:
    brands = {}
    for it in items:
        brands.setdefault(it["project"], it["brand"])

    data = []
    for it in items:
        data.append({
            "project": it["project"],
            "brand": it["brand"]["name"],
            "color": it["brand"]["primary"],
            "title": it["title"],
            "date": it["date"],
            "ts": it["ts"],
            "slides": it["slides"],
            "link": it["rel_link"],
            "thumb": it["thumb_rel"],
        })
    data_json = json.dumps(data, ensure_ascii=False)

    chips = "".join(
        f'<button class="chip" data-brand="{b["name"]}" style="--c:{b["primary"]}">{b["name"]} '
        f'<span class="chip-count">{sum(1 for it in items if it["brand"]["name"] == b["name"])}</span></button>'
        for b in brands.values()
    )

    total = len(items)
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Galeria de Carrosseis</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root {{
    color-scheme: light;
    --bg: #eeece6; --card-bg:#fff; --ink:#181818; --muted:#8a8580;
    --line:#e2ddd3; --accent:#181818;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin:0; padding:0 0 80px; background:var(--bg); color:var(--ink);
    font-family:'Inter',-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  }}
  .hero {{
    padding:48px 5vw 28px; background:
      radial-gradient(circle at 15% 0%, #ffffff 0%, transparent 55%),
      radial-gradient(circle at 90% 100%, #ffffff80 0%, transparent 50%), var(--bg);
    border-bottom:1px solid var(--line);
  }}
  h1 {{ font-size:clamp(28px,4vw,42px); margin:0 0 6px; font-weight:800; letter-spacing:-1px; }}
  .sub {{ color:var(--muted); font-size:14.5px; margin:0 0 24px; }}
  .chips {{ display:flex; flex-wrap:wrap; gap:8px; }}
  .chip {{
    all:unset; cursor:pointer; display:inline-flex; align-items:center; gap:6px;
    font-size:12.5px; font-weight:600; padding:7px 14px; border-radius:20px;
    background:#fff; border:1.5px solid var(--line); color:var(--ink);
    transition:all .15s ease;
  }}
  .chip:before {{ content:""; width:8px; height:8px; border-radius:50%; background:var(--c); display:inline-block; }}
  .chip:hover {{ border-color:var(--c); }}
  .chip.active {{ background:var(--c); border-color:var(--c); color:#fff; }}
  .chip.active:before {{ background:#fff; }}
  .chip-count {{ opacity:.6; font-weight:500; }}

  .toolbar {{
    position:sticky; top:0; z-index:20; background:var(--bg)ee; backdrop-filter:blur(8px);
    display:flex; flex-wrap:wrap; align-items:center; gap:12px;
    padding:16px 5vw; border-bottom:1px solid var(--line);
  }}
  .search {{
    flex:1; min-width:180px; position:relative;
  }}
  .search input {{
    width:100%; font:inherit; font-size:14px; padding:10px 14px 10px 36px;
    border-radius:10px; border:1.5px solid var(--line); background:#fff; color:var(--ink);
  }}
  .search input:focus {{ outline:2px solid #181818; outline-offset:-1px; }}
  .search::before {{
    content:"⌕"; position:absolute; left:12px; top:50%; transform:translateY(-50%);
    color:var(--muted); font-size:16px;
  }}
  select {{
    font:inherit; font-size:13.5px; padding:9px 12px; border-radius:10px;
    border:1.5px solid var(--line); background:#fff; color:var(--ink); cursor:pointer;
  }}
  .view-toggle {{ display:flex; background:#fff; border:1.5px solid var(--line); border-radius:10px; overflow:hidden; }}
  .view-toggle button {{
    all:unset; cursor:pointer; font-size:13px; font-weight:600; padding:9px 16px;
    color:var(--muted);
  }}
  .view-toggle button.active {{ background:var(--ink); color:#fff; }}

  main {{ padding:36px 5vw 0; }}
  .count-line {{ font-size:12.5px; color:var(--muted); margin:0 0 20px; }}

  /* ---- client view ---- */
  .project {{ margin-bottom:48px; }}
  .project h2 {{
    display:flex; align-items:center; gap:10px;
    font-size:15px; text-transform:uppercase; letter-spacing:1.2px; font-weight:700;
    color:var(--ink); margin:0 0 18px;
  }}
  .project h2 .dot {{ width:10px; height:10px; border-radius:50%; background:var(--brand); }}
  .project h2 .n {{ color:var(--muted); font-weight:500; text-transform:none; letter-spacing:0; }}
  .grid {{
    display:grid; grid-template-columns:repeat(auto-fill, minmax(200px, 1fr));
    gap:22px;
  }}
  .card {{
    display:flex; flex-direction:column; text-decoration:none; color:inherit;
    background:var(--card-bg); border-radius:16px; overflow:hidden;
    box-shadow:0 1px 3px rgba(0,0,0,0.06); transition:transform .2s cubic-bezier(.2,.8,.2,1), box-shadow .2s ease;
    border-top:4px solid var(--c, #181818);
  }}
  .card:hover {{ transform:translateY(-5px); box-shadow:0 16px 32px rgba(0,0,0,0.14); }}
  .thumb-wrap {{ position:relative; width:100%; aspect-ratio:4/5; background:#e9e6df; overflow:hidden; }}
  .thumb {{ width:100%; height:100%; object-fit:cover; display:block; transition:transform .4s ease; }}
  .card:hover .thumb {{ transform:scale(1.06); }}
  .badge {{
    position:absolute; bottom:9px; right:9px; background:rgba(0,0,0,0.6);
    color:#fff; font-size:10px; font-weight:600; padding:4px 9px; border-radius:20px; letter-spacing:0.3px;
    backdrop-filter:blur(2px);
  }}
  .card-body {{ padding:12px 14px 15px; display:flex; flex-direction:column; gap:3px; }}
  .card-title {{ font-size:13.5px; font-weight:700; line-height:1.32; }}
  .card-date {{ font-size:11.5px; color:var(--muted); }}

  /* ---- timeline view ---- */
  .timeline {{ position:relative; max-width:760px; margin:0 auto; }}
  .month-group {{ margin-bottom:8px; }}
  .month-label {{
    position:sticky; top:70px; z-index:5;
    font-size:13px; font-weight:700; text-transform:uppercase; letter-spacing:1px;
    color:var(--ink); background:var(--bg); display:inline-block; padding:4px 0 14px;
  }}
  .t-row {{
    display:grid; grid-template-columns:56px 1fr; gap:16px; position:relative; padding-bottom:22px;
  }}
  .t-row::before {{
    content:""; position:absolute; left:27px; top:44px; bottom:-4px; width:2px; background:var(--line);
  }}
  .t-row:last-child::before {{ display:none; }}
  .t-day {{
    display:flex; flex-direction:column; align-items:center; justify-content:center;
    width:56px; height:56px; border-radius:50%; background:#fff; border:2px solid var(--line);
    font-weight:700; z-index:1;
  }}
  .t-day .num {{ font-size:17px; line-height:1; }}
  .t-day .mon {{ font-size:9px; text-transform:uppercase; color:var(--muted); letter-spacing:.5px; }}
  .t-card {{
    display:flex; gap:14px; text-decoration:none; color:inherit; background:#fff;
    border-radius:14px; padding:10px; box-shadow:0 1px 3px rgba(0,0,0,0.06);
    border-left:4px solid var(--c,#181818); transition:transform .15s ease, box-shadow .15s ease;
  }}
  .t-card:hover {{ transform:translateX(4px); box-shadow:0 10px 24px rgba(0,0,0,0.12); }}
  .t-thumb {{ width:64px; height:80px; border-radius:8px; object-fit:cover; flex:none; background:#eee; }}
  .t-info {{ display:flex; flex-direction:column; gap:5px; justify-content:center; min-width:0; }}
  .t-title {{ font-size:14px; font-weight:700; line-height:1.3; }}
  .t-meta {{ display:flex; align-items:center; gap:8px; font-size:11.5px; color:var(--muted); }}
  .t-brand {{
    display:inline-flex; align-items:center; gap:5px; font-weight:600; color:var(--ink);
  }}
  .t-brand::before {{ content:""; width:7px; height:7px; border-radius:50%; background:var(--c,#181818); }}

  .empty {{ text-align:center; padding:60px 20px; color:var(--muted); font-size:14px; }}

  @media (max-width:640px) {{
    .toolbar {{ position:static; }}
    .t-row {{ grid-template-columns:44px 1fr; }}
    .t-day {{ width:44px; height:44px; }}
    .t-day .num {{ font-size:14px; }}
  }}
</style>
</head>
<body>
  <div class="hero">
    <h1>Galeria de Carrosseis</h1>
    <p class="sub">{total} carrosseis no total · clique em qualquer capa pra abrir o carrossel completo</p>
    <div class="chips" id="chips">{chips}</div>
  </div>

  <div class="toolbar">
    <div class="search">
      <input id="q" type="text" placeholder="Buscar por titulo...">
    </div>
    <select id="sort">
      <option value="new">Mais recentes</option>
      <option value="old">Mais antigos</option>
      <option value="title">Titulo (A-Z)</option>
      <option value="client">Cliente</option>
    </select>
    <div class="view-toggle">
      <button data-view="client" class="active">Por cliente</button>
      <button data-view="timeline">Linha do tempo</button>
    </div>
  </div>

  <main>
    <p class="count-line" id="count-line"></p>
    <div id="output"></div>
  </main>

<script>
const DATA = {data_json};
const MONTHS = ["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"];
const MONTHS_FULL = ["Janeiro","Fevereiro","Marco","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"];
const WEEKDAYS = ["dom","seg","ter","qua","qui","sex","sab"];

let state = {{ view: "client", sort: "new", query: "", brand: null }};
try {{
  const saved = JSON.parse(localStorage.getItem("galeria-state") || "{{}}");
  if (saved.view) state.view = saved.view;
  if (saved.sort) state.sort = saved.sort;
}} catch (e) {{}}

function saveState() {{
  try {{ localStorage.setItem("galeria-state", JSON.stringify({{ view: state.view, sort: state.sort }})); }} catch (e) {{}}
}}

function fmtDate(ts) {{
  const d = new Date(ts * 1000);
  return `${{d.getDate()}} ${{MONTHS[d.getMonth()]}} ${{d.getFullYear()}}`;
}}

function escapeHtml(s) {{
  return s.replace(/[&<>"']/g, c => ({{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}}[c]));
}}

function getFiltered() {{
  let out = DATA.slice();
  if (state.brand) out = out.filter(it => it.brand === state.brand);
  if (state.query) {{
    const q = state.query.toLowerCase();
    out = out.filter(it => it.title.toLowerCase().includes(q) || it.brand.toLowerCase().includes(q));
  }}
  switch (state.sort) {{
    case "new": out.sort((a,b) => b.ts - a.ts); break;
    case "old": out.sort((a,b) => a.ts - b.ts); break;
    case "title": out.sort((a,b) => a.title.localeCompare(b.title)); break;
    case "client": out.sort((a,b) => a.brand.localeCompare(b.brand) || b.ts - a.ts); break;
  }}
  return out;
}}

function cardHtml(it) {{
  return `
    <a class="card" style="--c:${{it.color}}" href="${{it.link}}" title="Abrir carrossel">
      <div class="thumb-wrap">
        <img class="thumb" src="${{it.thumb}}" alt="${{escapeHtml(it.title)}}" loading="lazy">
        <span class="badge">${{it.slides}} slides</span>
      </div>
      <div class="card-body">
        <span class="card-title">${{escapeHtml(it.title)}}</span>
        <span class="card-date">${{fmtDate(it.ts)}} · ${{escapeHtml(it.brand)}}</span>
      </div>
    </a>`;
}}

function renderClientView(items) {{
  const byBrand = {{}};
  items.forEach(it => {{ (byBrand[it.brand] = byBrand[it.brand] || []).push(it); }});
  const order = state.sort === "client" ? Object.keys(byBrand).sort() :
    Object.keys(byBrand).sort((a,b) => Math.max(...byBrand[b].map(x=>x.ts)) - Math.max(...byBrand[a].map(x=>x.ts)));
  return order.map(brand => {{
    const list = byBrand[brand];
    const color = list[0].color;
    return `
    <section class="project" style="--brand:${{color}}">
      <h2><span class="dot"></span>${{escapeHtml(brand)}} <span class="n">(${{list.length}})</span></h2>
      <div class="grid">${{list.map(cardHtml).join("")}}</div>
    </section>`;
  }}).join("");
}}

function renderTimeline(items) {{
  const groups = [];
  let lastKey = null, group = null;
  items.forEach(it => {{
    const d = new Date(it.ts * 1000);
    const key = `${{d.getFullYear()}}-${{d.getMonth()}}`;
    if (key !== lastKey) {{
      group = {{ key, year: d.getFullYear(), month: d.getMonth(), items: [] }};
      groups.push(group);
      lastKey = key;
    }}
    group.items.push(it);
  }});
  return `<div class="timeline">` + groups.map(g => `
    <div class="month-group">
      <div class="month-label">${{MONTHS_FULL[g.month]}} ${{g.year}}</div>
      ${{g.items.map(it => {{
        const d = new Date(it.ts * 1000);
        return `
        <div class="t-row">
          <div class="t-day"><span class="num">${{d.getDate()}}</span><span class="mon">${{MONTHS[d.getMonth()]}}</span></div>
          <a class="t-card" style="--c:${{it.color}}" href="${{it.link}}" title="Abrir carrossel">
            <img class="t-thumb" src="${{it.thumb}}" alt="${{escapeHtml(it.title)}}" loading="lazy">
            <div class="t-info">
              <span class="t-title">${{escapeHtml(it.title)}}</span>
              <span class="t-meta">
                <span class="t-brand" style="--c:${{it.color}}">${{escapeHtml(it.brand)}}</span>
                · ${{it.slides}} slides · ${{WEEKDAYS[d.getDay()]}}
              </span>
            </div>
          </a>
        </div>`;
      }}).join("")}}
    </div>`).join("") + `</div>`;
}}

function render() {{
  const items = getFiltered();
  const out = document.getElementById("output");
  const countLine = document.getElementById("count-line");
  countLine.textContent = items.length === DATA.length
    ? `Mostrando todos os ${{items.length}} carrosseis`
    : `${{items.length}} de ${{DATA.length}} carrosseis`;
  out.innerHTML = items.length === 0
    ? `<div class="empty">Nenhum carrossel encontrado.</div>`
    : (state.view === "timeline" ? renderTimeline(items) : renderClientView(items));

  document.querySelectorAll(".view-toggle button").forEach(b => b.classList.toggle("active", b.dataset.view === state.view));
  document.querySelectorAll(".chip").forEach(c => c.classList.toggle("active", c.dataset.brand === state.brand));
  document.getElementById("sort").value = state.sort;
}}

document.getElementById("q").addEventListener("input", e => {{ state.query = e.target.value; render(); }});
document.getElementById("sort").addEventListener("change", e => {{ state.sort = e.target.value; saveState(); render(); }});
document.querySelectorAll(".view-toggle button").forEach(b => {{
  b.addEventListener("click", () => {{ state.view = b.dataset.view; saveState(); render(); }});
}});
document.querySelectorAll(".chip").forEach(c => {{
  c.addEventListener("click", () => {{
    state.brand = state.brand === c.dataset.brand ? null : c.dataset.brand;
    render();
  }});
}});

render();
</script>
</body>
</html>
"""


async def main(force_thumbs=False):
    items = discover_carousels()
    await ensure_thumbs(items, force=force_thumbs)
    html = build_html(items)
    out = ROOT / "galeria.html"
    out.write_text(html, encoding="utf-8")
    print(f"Galeria gerada: {out} ({len(items)} carrosseis)")


if __name__ == "__main__":
    import sys
    asyncio.run(main(force_thumbs="--force" in sys.argv))
