from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
SRC = HERE / "assets" / "raw" / "slide-photo-optionB.jpg"
DEST = HERE / "assets" / "edited" / "slide-photo.jpg"

img = Image.open(SRC)
w, h = img.size  # 5212x3475 landscape, worker roughly centered horizontally

target_ratio = 4 / 5  # width / height
new_w = int(h * target_ratio)  # crop width for a 4:5 frame at full height
left = (w - new_w) // 2  # centered — worker is already near-centered horizontally
crop = img.crop((left, 0, left + new_w, h))

crop.save(DEST, quality=92)
print(f"Saved {DEST} {crop.size}")
