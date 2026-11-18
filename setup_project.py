# setup_project.py
import os

BASE = os.path.dirname(os.path.abspath(__file__))

FOLDERS = [
    "raw_frames",
    "labeled/images",
    "labeled/labels",
    "baja-dataset/images/train",
    "baja-dataset/images/val",
    "baja-dataset/labels/train",
    "baja-dataset/labels/val",
]

for folder in FOLDERS:
    path = os.path.join(BASE, folder)
    if os.path.isfile(path):
        print(f"WARNING: '{folder}' exists as a file. Rename or delete it, then rerun.")
        continue
    os.makedirs(path, exist_ok=True)
    print(f"OK: {folder}")

data_yaml = os.path.join(BASE, "baja-dataset", "data.yaml")
if not os.path.exists(data_yaml):
    with open(data_yaml, "w") as f:
        f.write(
            "path: baja-dataset\n"
            "train: images/train\n"
            "val: images/val\n"
            "names:\n"
            "  0: cone\n"
            "  1: vehicle\n"
        )
    print("OK: created baja-dataset/data.yaml")

print("\nProject structure is ready.")