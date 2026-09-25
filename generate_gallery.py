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
                "slides": count_slides(html),
                "html_path": html_path,
                "rel_link": html_path.relative_to(ROOT).as_posix(),
                "thumb_name": f"{project_dir.name}__{slug_dir.name}.png".replace(" ", "_").replace("&", "and"),
            })
    items.sort(key=lambda x: (x["project"], x["date"]), reverse=False)
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
    by_project = {}
    for it in items:
        by_project.setdefault(it["project"], []).append(it)
    for proj_items in by_project.values():
        proj_items.sort(key=lambda x: x["date"], reverse=True)

    sections = []
    for project, proj_items in sorted(by_project.items()):
        brand = proj_items[0]["brand"]
        cards = []
        for it in proj_items:
            cards.append(f"""
        <a class="card" href="{it['rel_link']}" title="Abrir carrossel">
          <div class="thumb-wrap">
            <img class="thumb" src="{it['thumb_rel']}" alt="{it['title']}" loading="lazy">
            <span class="badge">{it['slides']} slides</span>
          </div>
          <div class="card-body">
            <span class="card-title">{it['title']}</span>
            <span class="card-date">{it['date']}</span>
          </div>
        </a>""")
        sections.append(f"""
    <section class="project" style="--brand: {brand['primary']};">
      <h2>{brand['name']}</h2>
      <div class="grid">{''.join(cards)}
      </div>
    </section>""")

    total = len(items)
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Galeria de Carrosseis</title>
<style>
  :root {{ color-scheme: light; }}
  * {{ box-sizing: border-box; }}
  body {{
    margin:0; padding:32px 40px 64px; background:#f2f1ee;
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
    color:#1a1a1a;
  }}
  h1 {{ font-size:26px; margin:0 0 4px; }}
  .sub {{ color:#777; font-size:14px; margin:0 0 36px; }}
  .project {{ margin-bottom:44px; }}
  .project h2 {{
    font-size:16px; text-transform:uppercase; letter-spacing:1px;
    color:var(--brand); border-bottom:2px solid var(--brand);
    display:inline-block; padding-bottom:6px; margin-bottom:20px;
  }}
  .grid {{
    display:grid; grid-template-columns:repeat(auto-fill, minmax(190px, 1fr));
    gap:20px;
  }}
  .card {{
    display:flex; flex-direction:column; text-decoration:none; color:inherit;
    background:#fff; border-radius:14px; overflow:hidden;
    box-shadow:0 2px 10px rgba(0,0,0,0.06); transition:transform .15s ease, box-shadow .15s ease;
  }}
  .card:hover {{ transform:translateY(-3px); box-shadow:0 10px 24px rgba(0,0,0,0.12); }}
  .thumb-wrap {{ position:relative; width:100%; aspect-ratio:4/5; background:#eee; }}
  .thumb {{ width:100%; height:100%; object-fit:cover; display:block; }}
  .badge {{
    position:absolute; bottom:8px; right:8px; background:rgba(0,0,0,0.55);
    color:#fff; font-size:10px; padding:3px 8px; border-radius:20px; letter-spacing:0.3px;
  }}
  .card-body {{ padding:10px 12px 14px; display:flex; flex-direction:column; gap:2px; }}
  .card-title {{ font-size:13px; font-weight:600; line-height:1.3; }}
  .card-date {{ font-size:11px; color:#999; }}
</style>
</head>
<body>
  <h1>Galeria de Carrosseis</h1>
  <p class="sub">{total} carrosseis · clique em qualquer capa pra abrir o carrossel completo</p>
  {''.join(sections)}
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
