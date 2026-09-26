import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW_DIR = HERE / "assets" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

URL = "https://images.unsplash.com/photo-1705579609022-a7a2266b6226?fm=jpg&q=80&w=1600&auto=format&fit=crop&ixlib=rb-4.1.0"
DEST = RAW_DIR / "slide1-photo-optionC.jpg"

req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
DEST.write_bytes(urllib.request.urlopen(req).read())
print(f"Downloaded {DEST} ({DEST.stat().st_size} bytes)")
