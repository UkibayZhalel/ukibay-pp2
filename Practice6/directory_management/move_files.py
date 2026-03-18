"""
Directory Management - Moving and Copying Files Between Directories
Demonstrates shutil.move, shutil.copy, and shutil.copytree.
"""

import os
import shutil

# ── Setup ─────────────────────────────────────────────────
os.makedirs("inbox",        exist_ok=True)
os.makedirs("processed",    exist_ok=True)
os.makedirs("archive",      exist_ok=True)
os.makedirs("reports/2024", exist_ok=True)

sample_files = ["invoice_001.pdf", "invoice_002.pdf", "summary.txt", "notes.txt"]
for fname in sample_files:
    with open(f"inbox/{fname}", "w") as f:
        f.write(f"Content of {fname}\n")

def show_dir(path):
    files = sorted(os.listdir(path)) if os.path.exists(path) else []
    print(f"  {path:20} → {files if files else '(empty)'}")

# ── 1. Copy files between directories ─────────────────────
print("=" * 50)
print("COPY FILES  (shutil.copy)")
print("=" * 50)
for fname in ["invoice_001.pdf", "invoice_002.pdf"]:
    shutil.copy(f"inbox/{fname}", f"processed/{fname}")
    print(f"  Copied: inbox/{fname} → processed/")

print("\nAfter copy:")
show_dir("inbox")
show_dir("processed")

# ── 2. Move files between directories ─────────────────────
print("\n" + "=" * 50)
print("MOVE FILES  (shutil.move)")
print("=" * 50)
for fname in ["summary.txt", "notes.txt"]:
    shutil.move(f"inbox/{fname}", f"archive/{fname}")
    print(f"  Moved:  inbox/{fname} → archive/")

print("\nAfter move:")
show_dir("inbox")
show_dir("archive")

# ── 3. Move entire folder ──────────────────────────────────
print("\n" + "=" * 50)
print("MOVE ENTIRE DIRECTORY  (shutil.move)")
print("=" * 50)
shutil.move("processed", "reports/2024/processed")
print("  Moved: processed/ → reports/2024/processed/")
show_dir("reports/2024")

# ── 4. Copy entire directory tree ─────────────────────────
print("\n" + "=" * 50)
print("COPY DIRECTORY TREE  (shutil.copytree)")
print("=" * 50)
shutil.copytree("archive", "archive_backup")
print("  Copied: archive/ → archive_backup/")
show_dir("archive_backup")

# Cleanup
for d in ("inbox", "processed", "archive", "archive_backup", "reports"):
    shutil.rmtree(d, ignore_errors=True)
print("\nDone — all temp directories removed.")
