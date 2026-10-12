import random
import shutil
from pathlib import Path

# Settings: all paths are relative to this script's folder, so it works from anywhere.
BASE = Path(__file__).resolve().parent
IMG_DIR = BASE / "images"
LBL_DIR = BASE / "labels"
VAL_FRACTION = 0.2
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")

# Collect images from both train and val folders. A dict keyed by filename means a
# file present in both folders is stored once, which removes the duplicates.
# Train is scanned first so the train copy is the one kept.
images = {}      # filename -> path of the copy we keep
extra_copies = []  # duplicate paths to delete later
for sub in ("train", "val"):
    folder = IMG_DIR / sub
    if not folder.is_dir():
        continue
    for path in folder.iterdir():
        name = path.name
        if name.lower().endswith(IMAGE_EXTS):
            if name in images:
                extra_copies.append(path)
            else:
                images[name] = path

# Pair each image with its label (same name, .txt). Images with no label are
# warned about and skipped, so unlabeled data doesn't silently end up in training.
pairs = []  # (image filename, label filename)
for name in sorted(images):
    label = Path(name).stem + ".txt"
    if (LBL_DIR / label).is_file():
        pairs.append((name, label))
    else:
        print(f"WARNING: no label file for image '{name}' - skipping it")

# Shuffle and split: the first ~20% become val, the rest train.
# The fixed seed makes the shuffle repeatable; change or remove it for a new split.
random.seed(42)
random.shuffle(pairs)
n_val = max(1, round(len(pairs) * VAL_FRACTION)) if pairs else 0
splits = {"val": pairs[:n_val], "train": pairs[n_val:]}

# Delete the duplicate copies so no image can end up in both train and val.
for path in extra_copies:
    path.unlink()

# Create the four target folders (no error if they already exist).
for kind in (IMG_DIR, LBL_DIR):
    for sub in ("train", "val"):
        (kind / sub).mkdir(parents=True, exist_ok=True)

# Move each image and its label into its split's folder.
for sub, items in splits.items():
    for img_name, lbl_name in items:
        img_dst = IMG_DIR / sub / img_name
        if images[img_name].resolve() != img_dst.resolve():
            shutil.move(images[img_name], img_dst)
        shutil.move(LBL_DIR / lbl_name, LBL_DIR / sub / lbl_name)

print(f"Done: {len(splits['train'])} train, {len(splits['val'])} val, "
      f"{len(extra_copies)} duplicate(s) removed.")
