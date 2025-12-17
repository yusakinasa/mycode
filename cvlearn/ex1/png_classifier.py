import os
import shutil

raw_val = "raw_data/val"
val_dir = "data/val"
os.makedirs(os.path.join(val_dir, "cat"), exist_ok=True)
os.makedirs(os.path.join(val_dir, "dog"), exist_ok=True)

for fname in os.listdir(raw_val):
    if fname.startswith("cat"):
        shutil.copy(os.path.join(raw_val, fname), os.path.join(val_dir, "cat"))
    elif fname.startswith("dog"):
        shutil.copy(os.path.join(raw_val, fname), os.path.join(val_dir, "dog"))
