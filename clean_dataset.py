# clean_dataset.py
import hashlib
import os

import imagehash
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "raw_frames")
IMAGES = os.path.join(BASE, "labeled", "images")
LABELS = os.path.join(BASE, "labeled", "labels")


def file_hash(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def remove_exact_duplicates(folder):
    seen = {}
    removed = 0
    for name in sorted(os.listdir(folder)):
        path = os.path.join(folder, name)
        if not os.path.isfile(path):
            continue
        h = file_hash(path)
        if h in seen:
            os.remove(path)
            removed += 1
        else:
            seen[h] = name
    print(f"Removed {removed} exact duplicates from {folder}")


def remove_near_duplicates(folder, threshold=5):
    kept_hashes = []
    removed = 0
    for name in sorted(os.listdir(folder)):
        path = os.path.join(folder, name)
        try:
            with Image.open(path) as img:
                h = imagehash.phash(img)
        except Exception:
            print(f"Could not read {name}, skipping")
            continue
        if any(h - prev <= threshold for prev in kept_hashes):
            os.remove(path)
            removed += 1
        else:
            kept_hashes.append(h)
    print(f"Removed {removed} near-duplicates from {folder}")


def check_pairs(images_dir, labels_dir, remove_orphans=False):
    image_stems = {os.path.splitext(f)[0] for f in os.listdir(images_dir)}
    label_stems = {os.path.splitext(f)[0] for f in os.listdir(labels_dir)}

    missing_labels = image_stems - label_stems
    orphan_labels = label_stems - image_stems

    print(f"Images without labels: {len(missing_labels)}")
    print(f"Labels without images: {len(orphan_labels)}")

    if remove_orphans:
        for stem in orphan_labels:
            os.remove(os.path.join(labels_dir, stem + ".txt"))
        print("Orphan labels removed")
    return missing_labels


def check_labels(labels_dir, num_classes):
    problems = []
    for name in os.listdir(labels_dir):
        with open(os.path.join(labels_dir, name)) as f:
            for lineno, line in enumerate(f, 1):
                parts = line.split()
                if not parts:
                    continue
                if len(parts) != 5:
                    problems.append((name, lineno, "wrong number of fields"))
                    continue
                cls = int(float(parts[0]))
                coords = [float(x) for x in parts[1:]]
                if not (0 <= cls < num_classes):
                    problems.append((name, lineno, f"class {cls} out of range"))
                if any(not (0 <= c <= 1) for c in coords):
                    problems.append((name, lineno, "coordinate outside 0-1"))
    for p in problems:
        print(p)
    print(f"Found {len(problems)} problems")


if __name__ == "__main__":
    # Cleaning the raw frames (run this first)
    remove_exact_duplicates(RAW)
    remove_near_duplicates(RAW, threshold=5)

    # Checking labels (run after you've labeled and exported to labeled/)
    # check_pairs(IMAGES, LABELS, remove_orphans=True)
    # check_labels(LABELS, num_classes=2)