#!/usr/bin/env python3
"""Rename page-bundle image assets whose filename contains a space, and
rewrite the markdown links that reference them.

Why: Hugo's Resources.GetMatch() matches against literal filenames, but
markdown image links percent-encode spaces (%20). "image 1.png" on disk
vs "image%201.png" in the link never matches, so Blowfish's render hook
(themes/blowfish/layouts/_default/_markup/render-image.html) falls back to
an unprocessed <img>, skipping the .Resize()/srcset pipeline that normalizes
every other image to a consistent display width. Result: images with
spaces in their filename render at their raw native pixel size instead of
the site's standard width, producing wildly inconsistent sizes article to
article.

Fix: strip spaces from the asset filename (collision-safe within each page
bundle) and update every markdown reference to match, so all images take
the same Resources.GetMatch → Resize → srcset path.

Usage:
    python3 scripts/fix_image_spaces.py --dry-run     # preview only
    python3 scripts/fix_image_spaces.py                # apply (uses git mv)
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTENT_DOCS = REPO_ROOT / "content" / "docs"
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}


def sanitize(name):
    stem_ext = name.rsplit(".", 1)
    stem, ext = (stem_ext[0], "." + stem_ext[1]) if len(stem_ext) == 2 else (name, "")
    return re.sub(r"\s+", "", stem) + ext


def unique_target(desired, taken):
    if desired not in taken:
        return desired
    stem_ext = desired.rsplit(".", 1)
    stem, ext = (stem_ext[0], "." + stem_ext[1]) if len(stem_ext) == 2 else (desired, "")
    n = 2
    while f"{stem}-{n}{ext}" in taken:
        n += 1
    return f"{stem}-{n}{ext}"


def find_bundles():
    """Yield (dir, [Path,...]) for every content/docs directory that has
    image files with a space in their basename."""
    if not CONTENT_DOCS.is_dir():
        return
    dirs = {}
    for p in CONTENT_DOCS.rglob("*"):
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS and " " in p.name:
            dirs.setdefault(p.parent, []).append(p)
    for d, files in sorted(dirs.items()):
        yield d, sorted(files)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="Preview renames and link rewrites without changing anything")
    args = ap.parse_args()

    total_files = 0
    total_pages = 0

    for bundle_dir, files in find_bundles():
        existing_names = {f.name for f in bundle_dir.iterdir() if f.is_file()}
        rename_map = {}
        taken = set(existing_names)
        for f in files:
            new_name = sanitize(f.name)
            if new_name == f.name:
                continue
            new_name = unique_target(new_name, taken - {f.name})
            taken.add(new_name)
            rename_map[f.name] = new_name

        if not rename_map:
            continue

        md_files = list(bundle_dir.glob("*.md"))
        rel_dir = bundle_dir.relative_to(REPO_ROOT)
        print(f"\n{rel_dir}")
        for old, new in rename_map.items():
            print(f"  {old!r} -> {new!r}")

        if args.dry_run:
            for md in md_files:
                text = md.read_text(encoding="utf-8")
                touched = [old for old in rename_map if old in text or old.replace(" ", "%20") in text]
                if touched:
                    print(f"  would update links in {md.relative_to(REPO_ROOT)}: {touched}")
            total_files += len(rename_map)
            total_pages += 1
            continue

        for old, new in rename_map.items():
            old_path = bundle_dir / old
            new_path = bundle_dir / new
            result = subprocess.run(["git", "mv", str(old_path), str(new_path)], cwd=REPO_ROOT, capture_output=True, text=True)
            if result.returncode != 0:
                old_path.rename(new_path)

        for md in md_files:
            text = md.read_text(encoding="utf-8")
            original = text
            for old, new in rename_map.items():
                text = text.replace(old.replace(" ", "%20"), new)
                text = text.replace(old, new)
            if text != original:
                md.write_text(text, encoding="utf-8")
                print(f"  updated links in {md.relative_to(REPO_ROOT)}")

        total_files += len(rename_map)
        total_pages += 1

    verb = "Would rename" if args.dry_run else "Renamed"
    print(f"\n{verb} {total_files} files across {total_pages} pages.")
    if args.dry_run:
        print("Run without --dry-run to apply.")


if __name__ == "__main__":
    main()
