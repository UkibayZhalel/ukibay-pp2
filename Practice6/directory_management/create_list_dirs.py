

import os
import glob

# ── 1. Create nested directory structure ──────────────────
print("=" * 45)
print("CREATE NESTED DIRECTORIES")
print("=" * 45)

dirs = [
    "myproject/src/utils",
    "myproject/src/models",
    "myproject/tests",
    "myproject/data/raw",
    "myproject/data/processed",
]
for d in dirs:
    os.makedirs(d, exist_ok=True)
    print(f"  Created: {d}")

# Seed some dummy files
seed_files = {
    "myproject/src/main.py": "# entry point\n",
    "myproject/src/utils/helpers.py": "# helpers\n",
    "myproject/src/models/user.py": "# user model\n",
    "myproject/tests/test_main.py": "# tests\n",
    "myproject/data/raw/data.csv": "id,value\n1,100\n",
    "myproject/data/raw/notes.txt": "raw notes\n",
}
for path, content in seed_files.items():
    with open(path, "w") as f:
        f.write(content)

# ── 2. List files and folders (os.listdir) ────────────────
print("\n" + "=" * 45)
print("LIST TOP-LEVEL CONTENTS  (os.listdir)")
print("=" * 45)
for entry in sorted(os.listdir("myproject")):
    full = os.path.join("myproject", entry)
    kind = "DIR " if os.path.isdir(full) else "FILE"
    print(f"  [{kind}] {entry}")

# ── 3. Walk full tree ────────────────────────────────────
print("\n" + "=" * 45)
print("FULL TREE WALK  (os.walk)")
print("=" * 45)
for root, sub_dirs, files in os.walk("myproject"):
    depth  = root.replace("myproject", "").count(os.sep)
    indent = "  " * depth
    print(f"{indent}{os.path.basename(root)}/")
    for fname in sorted(files):
        print(f"  {indent}{fname}")

# ── 4. Find files by extension (glob) ─────────────────────
print("\n" + "=" * 45)
print("FIND FILES BY EXTENSION  (glob)")
print("=" * 45)
for ext in ("*.py", "*.csv", "*.txt"):
    matches = glob.glob(f"myproject/**/{ext}", recursive=True)
    print(f"  {ext:8} → {len(matches)} file(s)")
    for m in sorted(matches):
        print(f"           {m}")

# Cleanup
import shutil
shutil.rmtree("myproject")
print("\nDone — myproject/ removed.")
