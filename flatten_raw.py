# flatten_raw.py
import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "raw_frames")
SUB = os.path.join(RAW, "training_images")
IMAGE_EXT = (".jpg", ".jpeg", ".png", ".bmp", ".webp")

moved = 0
for root, _, files in os.walk(RAW):
    if root == RAW:
        continue
    for name in files:
        if not name.lower().endswith(IMAGE_EXT):
            continue
        src = os.path.join(root, name)
        dst = os.path.join(RAW, name)
        if os.path.exists(dst):
            stem, ext = os.path.splitext(name)
            dst = os.path.join(RAW, f"{os.path.basename(root)}_{stem}{ext}")
        shutil.move(src, dst)
        moved += 1

print(f"Moved {moved} images into raw_frames/")