"""Regenerate content-map.html from the current content/ directory.

Usage:
    python scripts/generate_content_map.py

Run this any time content/ changes and you want the visualization
(content-map.html, in the project root) to reflect the latest state.
It embeds a full snapshot of content/ as JSON, so the page itself
never auto-updates -- rerunning this script is what refreshes it.
"""
import os
import re
import json

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(ROOT_DIR, "content")
OUTPUT_HTML = os.path.join(ROOT_DIR, "content-map.html")
TEMPLATE_HTML = os.path.join(os.path.dirname(os.path.abspath(__file__)), "content_map_template.html")
DATA_PLACEHOLDER = "__DATA_JSON__"


def parse_frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
    fm = {}
    if not m:
        return fm, text
    block = m.group(1)
    body = text[m.end():]
    title_m = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', block, re.MULTILINE)
    date_m = re.search(r'^date:\s*["\']?(.*?)["\']?\s*$', block, re.MULTILINE)
    desc_m = re.search(r'^description:\s*["\']?(.*?)["\']?\s*$', block, re.MULTILINE)
    draft_m = re.search(r'^draft:\s*(true|false)\s*$', block, re.MULTILINE)
    tags_m = re.search(r'^tags:\s*\[(.*?)\]\s*$', block, re.MULTILINE)
    if title_m:
        fm['title'] = title_m.group(1).strip()
    if date_m:
        fm['date'] = date_m.group(1).strip()
    if desc_m:
        fm['description'] = desc_m.group(1).strip()
    if draft_m:
        fm['draft'] = draft_m.group(1) == 'true'
    if tags_m:
        tags = [t.strip().strip('"').strip("'") for t in tags_m.group(1).split(',') if t.strip()]
        fm['tags'] = tags
    return fm, body


def word_count(body):
    text = re.sub(r'```.*?```', '', body, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '', text)
    cjk = re.findall(r'[一-鿿]', text)
    words = re.findall(r'[A-Za-z0-9_]+', text)
    return len(cjk) + len(words)


def build_tree(path):
    name = os.path.basename(path)
    node = {"name": name, "type": "dir", "children": [], "files": []}
    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        return node

    dirs, files = [], []
    for e in entries:
        full = os.path.join(path, e)
        (dirs if os.path.isdir(full) else files).append(full)

    page_info = None
    assets = []
    for f in files:
        base = os.path.basename(f)
        if base in ("index.md", "_index.md"):
            try:
                with open(f, encoding="utf-8") as fh:
                    text = fh.read()
                fm, body = parse_frontmatter(text)
                page_info = {
                    "file": base,
                    "title": fm.get("title", name),
                    "date": fm.get("date"),
                    "description": fm.get("description", ""),
                    "draft": fm.get("draft", False),
                    "tags": fm.get("tags", []),
                    "words": word_count(body),
                }
            except Exception as ex:
                page_info = {"file": base, "title": name, "error": str(ex)}
        else:
            ext = os.path.splitext(base)[1].lower().lstrip('.')
            assets.append({"name": base, "ext": ext})

    node["page"] = page_info
    node["assets"] = assets
    for d in dirs:
        node["children"].append(build_tree(d))
    return node


def main():
    tree = build_tree(CONTENT_DIR)
    tree["name"] = "content"
    data_json = json.dumps(tree, ensure_ascii=False)

    with open(TEMPLATE_HTML, encoding="utf-8") as f:
        tmpl = f.read()

    if DATA_PLACEHOLDER not in tmpl:
        raise SystemExit(f"Template is missing the {DATA_PLACEHOLDER} placeholder: {TEMPLATE_HTML}")

    out = tmpl.replace(DATA_PLACEHOLDER, data_json)
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(out)

    print(f"Wrote {OUTPUT_HTML} ({len(out):,} bytes)")


if __name__ == "__main__":
    main()
