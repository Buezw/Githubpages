#!/usr/bin/env python3
"""Import a single-page Notion "Export as Markdown & CSV" bundle into a
Hugo page bundle under content/docs, converting it to this site's format.

Usage:
    python3 scripts/import_notion.py <notion_export_dir> <dest_content_dir> \
        [--tags TAG [TAG ...]] [--series SERIES]

Example:
    python3 scripts/import_notion.py \
        ~/Desktop/ExportBlock-xxxx-Part-1 \
        "content/docs/UofT/26W/Circuit Analysis/CA6.Laplace" \
        --tags CA "Circuit Analysis" Docs
"""
import argparse
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

CREATED_RE = re.compile(r"^创建时间:\s*(.+?)\s*$", re.MULTILINE)
TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
IMG_RE = re.compile(r"(!\[[^\]]*\]\()([^)]+)(\))")


def parse_created(text):
    m = CREATED_RE.search(text)
    if not m:
        return None
    raw = m.group(1)
    for fmt in ("%d %B %Y %H:%M", "%d %B %Y"):
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue
    return None


def strip_meta_lines(text):
    text = TITLE_RE.sub("", text, count=1)
    text = CREATED_RE.sub("", text, count=1)
    return text.lstrip("\n")


def escape_math_asterisks(text):
    """A bare '*' inside $$...$$ or $...$ (e.g. Notion's p^* complex-conjugate
    notation) gets parsed by Markdown as italics/bold before KaTeX/MathJax ever
    sees it, silently breaking the equation. Escaping it as '\\*' makes
    Markdown emit a literal '*' instead, which the math renderer then sees."""
    def esc(m):
        return m.group(0).replace("*", r"\*")

    text = re.sub(r"\$\$.*?\$\$", esc, text, flags=re.DOTALL)
    text = re.sub(r"(?<!\$)\$(?!\$)[^\n$]+?\$(?!\$)", esc, text)
    return text


def collapse_math_blank_lines(text):
    """Notion sometimes exports a stray blank line right before the closing $$
    of a display-math block. Markdown treats a blank line as a paragraph
    break, so Goldmark never recognizes the block as math and prints the
    literal '$$ ... $$' as plain text instead of rendering an equation."""
    lines = text.split("\n")
    out = []
    in_math = False
    for line in lines:
        stripped = line.strip()
        if stripped == "$$":
            in_math = not in_math
            out.append(line)
            continue
        if in_math and stripped == "":
            continue
        out.append(line)
    return "\n".join(out)


def rewrite_image_links(text, asset_dirname):
    """Strip the Notion subfolder prefix from image links so they point
    at files sitting next to index.md (Hugo leaf bundle convention)."""
    prefix_variants = {asset_dirname, asset_dirname.replace(" ", "%20")}

    def repl(match):
        pre, path, post = match.groups()
        for prefix in prefix_variants:
            if path.startswith(prefix + "/"):
                path = path[len(prefix) + 1:]
                break
        return f"{pre}{path}{post}"

    return IMG_RE.sub(repl, text)


def sanitize_filename(name):
    stem_ext = name.rsplit(".", 1)
    stem, ext = (stem_ext[0], "." + stem_ext[1]) if len(stem_ext) == 2 else (name, "")
    return re.sub(r"\s+", "", stem) + ext


def build_rename_map(asset_dir):
    """Map on-disk filenames with spaces to a space-free, collision-safe name.

    Hugo's Resources.GetMatch() matches literal filenames, but markdown links
    percent-encode spaces (%20), so "image 1.png" never matches "image%201.png"
    in the link. Blowfish's render hook then falls back to an unprocessed
    <img>, skipping the .Resize()/srcset pipeline that normalizes every other
    image to a consistent display width -- the imported page ends up with
    wildly inconsistent image sizes. See scripts/fix_image_spaces.py, which
    applies this same fix retroactively across the whole site."""
    existing = {f.name for f in asset_dir.iterdir() if f.is_file()}
    taken = set(existing)
    rename_map = {}
    for name in sorted(existing):
        if " " not in name:
            continue
        new_name = sanitize_filename(name)
        if new_name in taken and new_name != name:
            stem_ext = new_name.rsplit(".", 1)
            stem, ext = (stem_ext[0], "." + stem_ext[1]) if len(stem_ext) == 2 else (new_name, "")
            n = 2
            while f"{stem}-{n}{ext}" in taken:
                n += 1
            new_name = f"{stem}-{n}{ext}"
        taken.add(new_name)
        rename_map[name] = new_name
    return rename_map


def apply_filename_renames(text, rename_map):
    def repl(match):
        pre, path, post = match.groups()
        decoded = path.replace("%20", " ")
        if decoded in rename_map:
            path = rename_map[decoded]
        return f"{pre}{path}{post}"

    return IMG_RE.sub(repl, text)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("export_dir", type=Path, help="Notion export folder (contains the .md file and image subfolder)")
    ap.add_argument("dest_dir", type=Path, help="Destination Hugo page bundle folder, e.g. content/docs/UofT/26W/Circuit Analysis/CA6.Laplace")
    ap.add_argument("--tags", nargs="+", default=["Docs"], help="Front matter tags (default: Docs)")
    ap.add_argument("--series", default=None, help="Optional front matter series value")
    ap.add_argument("--title", default=None, help="Override the front matter title (default: the exported H1)")
    ap.add_argument("--clean", action="store_true", help="Delete the source export_dir after a successful import")
    args = ap.parse_args()

    export_dir = args.export_dir.expanduser()
    if not export_dir.is_dir():
        sys.exit(f"Not a directory: {export_dir}")

    md_files = sorted(export_dir.glob("*.md"))
    if not md_files:
        sys.exit(f"No .md file found in {export_dir}")
    if len(md_files) > 1:
        sys.exit(f"Expected exactly one .md file in {export_dir}, found {len(md_files)}: {[f.name for f in md_files]}")
    md_path = md_files[0]

    text = md_path.read_text(encoding="utf-8")

    title_match = TITLE_RE.search(text)
    if not title_match:
        sys.exit("Could not find a top-level '# Title' line in the export")
    exported_title = title_match.group(1)
    title = args.title or exported_title

    created = parse_created(text)
    date = created or datetime.fromtimestamp(md_path.stat().st_mtime)

    # Notion suffixes the .md filename (and asset subfolder) with a hex hash;
    # the asset folder keeps the *bare* exported title as its name (no hash).
    asset_dirname = exported_title
    asset_dir = export_dir / asset_dirname
    if not asset_dir.is_dir():
        # fall back to whatever single subfolder exists, if any
        subdirs = [d for d in export_dir.iterdir() if d.is_dir()]
        asset_dir = subdirs[0] if len(subdirs) == 1 else None

    body = strip_meta_lines(text)
    rename_map = {}
    if asset_dir is not None:
        body = rewrite_image_links(body, asset_dir.name)
        rename_map = build_rename_map(asset_dir)
        if rename_map:
            body = apply_filename_renames(body, rename_map)
    body = escape_math_asterisks(body)
    body = collapse_math_blank_lines(body)

    last_edit = f"{date.month}/{date.day}/{date.strftime('%y')}"

    tags_yaml = "[" + ", ".join(f'"{t}"' for t in args.tags) + "]"
    front_matter_lines = [
        "---",
        f'title: "{title}"',
        f"date: {date.strftime('%Y-%m-%d')}",
        f"tags: {tags_yaml}",
    ]
    if args.series:
        front_matter_lines.append(f'series: ["{args.series}"]')
    front_matter_lines += ["math: mathjax", "---", "", f"> Last Edit: {last_edit}", "", ""]

    final_text = "\n".join(front_matter_lines) + body

    dest_dir = args.dest_dir
    dest_dir.mkdir(parents=True, exist_ok=True)
    (dest_dir / "index.md").write_text(final_text, encoding="utf-8")

    copied = []
    if asset_dir is not None:
        for f in asset_dir.iterdir():
            if f.is_file():
                dest_name = rename_map.get(f.name, f.name)
                shutil.copy2(f, dest_dir / dest_name)
                copied.append(dest_name)

    print(f"Title:   {title}")
    print(f"Date:    {date.strftime('%Y-%m-%d')} (Last Edit: {last_edit})")
    print(f"Wrote:   {dest_dir / 'index.md'}")
    print(f"Images:  {len(copied)} copied -> {dest_dir}")
    for name in copied:
        print(f"  - {name}")

    if args.clean:
        shutil.rmtree(export_dir)
        print(f"Removed source export dir: {export_dir}")
    else:
        print(f"\n(Source export left at {export_dir} - pass --clean to auto-delete it next time)")


if __name__ == "__main__":
    main()
