#!/usr/bin/env python3
"""Local web UI for scripts/import_notion.py.

Run it, then open the printed URL in a browser:

    python3 scripts/import_notion_ui.py

It lets you pick a Notion export folder (auto-detected on the Desktop),
preview the parsed title/date, choose (or type) a destination folder under
content/docs, adjust tags/series, and run the import — all without touching
the command line for each new page.

Everything runs locally (127.0.0.1) with no external dependencies.
"""
import glob
import importlib.util
import io
import json
import webbrowser
import zipfile
from contextlib import redirect_stdout
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTENT_DOCS = REPO_ROOT / "content" / "docs"

spec = importlib.util.spec_from_file_location("import_notion", Path(__file__).resolve().parent / "import_notion.py")
importer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(importer)


def extract_zip(zip_path):
    """Extract a zip next to itself (idempotent: reuse the folder if already extracted)."""
    target_dir = zip_path.with_suffix("")
    if not target_dir.exists():
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(target_dir)
    return target_dir


def expand_to_page_dirs(d):
    """Notion's export is double-zipped: an outer '<uuid>_ExportBlock-<uuid>.zip'
    wraps one or more inner 'ExportBlock-<uuid>-Part-N.zip', each of which finally
    holds the real '<title>.md' + asset folder. Recursively unzip until we hit
    folders that directly contain a .md file (one per exported page)."""
    if list(d.glob("*.md")):
        return [d]
    pages = []
    for z in sorted(d.glob("*.zip")):
        pages.extend(expand_to_page_dirs(extract_zip(z)))
    return pages


def find_export_dirs():
    """Auto-detect and auto-extract Notion export zips/folders on the Desktop,
    returning page-ready directories (each directly containing a .md file)."""
    desktop = Path.home() / "Desktop"
    if not desktop.is_dir():
        return []

    seen = set()
    candidates = []

    def add(p):
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            candidates.append(p)

    for p in desktop.glob("*"):
        if p.is_dir() and "ExportBlock" in p.name:
            for page_dir in expand_to_page_dirs(p):
                add(page_dir)
        elif p.is_file() and p.suffix == ".zip" and "ExportBlock" in p.name:
            for page_dir in expand_to_page_dirs(extract_zip(p)):
                add(page_dir)

    candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return [str(p) for p in candidates]


def find_section_dirs():
    """All existing directories under content/docs, as relative 'docs/...' paths, for autocomplete."""
    if not CONTENT_DOCS.is_dir():
        return []
    dirs = set()
    for p in CONTENT_DOCS.rglob("*"):
        if p.is_dir():
            rel = p.relative_to(REPO_ROOT)
            dirs.add(str(rel))
    return sorted(dirs)


def guess_title(exported_title):
    import re
    m = re.match(r"^([A-Za-z]+)(\d+)\.(.*)$", exported_title)
    if m:
        letters, digits, rest = m.groups()
        return f"{letters} {digits}. {rest}"
    return exported_title


def guess_tags(exported_title):
    import re
    m = re.match(r"^([A-Za-z]+)\d*", exported_title)
    prefix = m.group(1) if m else ""
    tags = []
    if prefix:
        tags.append(prefix)
    tags.append("Docs")
    return tags


PAGE = """<!doctype html>
<html lang="zh">
<head>
<meta charset="utf-8">
<title>Notion → Hugo 导入</title>
<style>
  :root { color-scheme: light dark; }
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; max-width: 760px; margin: 40px auto; padding: 0 20px; line-height: 1.5; }
  h1 { font-size: 1.4rem; }
  fieldset { border: 1px solid #8884; border-radius: 8px; padding: 16px 20px; margin-bottom: 20px; }
  legend { font-weight: 600; padding: 0 6px; }
  label { display: block; font-size: 0.85rem; opacity: 0.75; margin: 12px 0 4px; }
  input[type=text], select { width: 100%; box-sizing: border-box; padding: 8px 10px; font-size: 0.95rem; border-radius: 6px; border: 1px solid #8886; background: transparent; color: inherit; }
  .row { display: flex; gap: 12px; }
  .row > div { flex: 1; }
  .hint { font-size: 0.8rem; opacity: 0.6; margin-top: 4px; }
  button { font-size: 0.95rem; padding: 10px 18px; border-radius: 6px; border: none; background: #2563eb; color: white; cursor: pointer; }
  button:hover { background: #1d4ed8; }
  button.secondary { background: #6b7280; }
  #log { white-space: pre-wrap; background: #0001; border-radius: 8px; padding: 14px; font-family: ui-monospace, monospace; font-size: 0.85rem; margin-top: 16px; display: none; }
  #log.show { display: block; }
  #log.error { background: #ef444422; }
  .checkbox-row { display: flex; align-items: center; gap: 8px; margin-top: 14px; }
  .checkbox-row input { width: auto; }
  .warn { color: #d97706; font-size: 0.85rem; margin-top: 6px; display: none; }
  .warn.show { display: block; }
  .autocomplete-wrap { position: relative; }
  .suggestions-list { display: none; position: absolute; top: 100%; left: 0; margin-top: 4px; min-width: 100%; width: max-content; max-width: 90vw; max-height: 280px; overflow-y: auto; background: Canvas; color: CanvasText; border: 1px solid #8886; border-radius: 8px; box-shadow: 0 8px 24px #0003; z-index: 30; }
  .suggestions-list.show { display: block; }
  .suggestions-list .item { padding: 8px 14px; font-size: 0.85rem; cursor: pointer; white-space: nowrap; }
  .suggestions-list .item:hover, .suggestions-list .item.active { background: #2563eb22; }
</style>
</head>
<body>
<h1>Notion 导出 → Hugo 页面导入</h1>

<fieldset>
  <legend>1. 选择 Notion 导出文件夹</legend>
  <label for="export_dir">导出文件夹路径</label>
  <select id="export_select"></select>
  <input type="text" id="export_dir" placeholder="~/Desktop/ExportBlock-xxxx-Part-1" style="margin-top:8px;">
  <div class="hint">下拉框自动列出了 Desktop 上检测到的 ExportBlock-* 文件夹（按修改时间排序）；也可以直接手动输入路径。</div>
  <button type="button" class="secondary" id="preview_btn" style="margin-top:12px;">解析预览</button>
</fieldset>

<fieldset>
  <legend>2. 目标位置</legend>
  <label for="parent_dir">目标目录（相对仓库根目录，如 content/docs/UofT/26W/Circuit Analysis）</label>
  <div class="autocomplete-wrap">
    <input type="text" id="parent_dir" placeholder="content/docs/UofT/..." autocomplete="off">
    <div id="parent_suggestions" class="suggestions-list"></div>
  </div>
  <label for="folder_name">页面文件夹名（如 CA6.Laplace）</label>
  <input type="text" id="folder_name" placeholder="CA6.Laplace">
  <div class="hint" id="dest_preview"></div>
  <div class="warn" id="exists_warn">⚠️ 该目录已存在，可能包含已导入的页面，继续将覆盖其中的 index.md 和同名图片。</div>
</fieldset>

<fieldset>
  <legend>3. 元信息</legend>
  <label for="title">标题</label>
  <input type="text" id="title">
  <label for="tags">标签（逗号分隔）</label>
  <input type="text" id="tags">
  <label for="series">系列（可选）</label>
  <input type="text" id="series">
  <div class="checkbox-row">
    <input type="checkbox" id="clean">
    <label style="margin:0;" for="clean">导入成功后删除源导出文件夹</label>
  </div>
</fieldset>

<button type="button" id="import_btn">执行导入</button>
<span id="overwrite_confirm_wrap" style="display:none; margin-left:12px;">
  <label class="checkbox-row" style="display:inline-flex; margin:0;">
    <input type="checkbox" id="overwrite_confirm"> 我确认要覆盖已存在的目标目录
  </label>
</span>

<div id="log"></div>

<script>
const $ = id => document.getElementById(id);
let sectionDirs = [];

async function loadOptions() {
  const r = await fetch('/api/options');
  const data = await r.json();
  const sel = $('export_select');
  sel.innerHTML = '<option value="">-- 从 Desktop 检测到的导出文件夹中选择 --</option>' +
    data.export_dirs.map(d => `<option value="${d}">${d}</option>`).join('');
  sectionDirs = data.section_dirs;
}

function escapeHtml(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function renderParentSuggestions(list) {
  const box = $('parent_suggestions');
  if (!list.length) {
    box.className = 'suggestions-list';
    box.innerHTML = '';
    return;
  }
  box.innerHTML = list.map(d => `<div class="item" data-value="${escapeHtml(d)}">${escapeHtml(d)}</div>`).join('');
  box.className = 'suggestions-list show';
}

function filterParentDir() {
  const q = $('parent_dir').value.trim().toLowerCase();
  const matches = q
    ? sectionDirs.filter(d => d.toLowerCase().includes(q)).slice(0, 40)
    : sectionDirs.slice(0, 40);
  renderParentSuggestions(matches);
}

$('parent_dir').addEventListener('input', () => { filterParentDir(); updateDestPreview(); });
$('parent_dir').addEventListener('focus', filterParentDir);
$('parent_suggestions').addEventListener('click', e => {
  const item = e.target.closest('.item');
  if (!item) return;
  $('parent_dir').value = item.dataset.value;
  renderParentSuggestions([]);
  updateDestPreview();
});
document.addEventListener('click', e => {
  if (!e.target.closest('.autocomplete-wrap')) renderParentSuggestions([]);
});

$('export_select').addEventListener('change', e => {
  if (e.target.value) {
    $('export_dir').value = e.target.value;
    doPreview();
  }
});

async function doPreview() {
  const export_dir = $('export_dir').value.trim();
  if (!export_dir) { return; }
  const log = $('log');
  log.className = 'show';
  log.textContent = '解析中…';
  const r = await fetch('/api/preview?export_dir=' + encodeURIComponent(export_dir));
  const data = await r.json();
  if (data.error) {
    log.className = 'show error';
    log.textContent = '解析失败：' + data.error;
    return;
  }
  log.className = '';
  log.textContent = '';
  $('title').value = data.title;
  $('tags').value = data.tags.join(', ');
  if (!$('folder_name').value) {
    $('folder_name').value = data.exported_title.replace(/\\s+/g, '');
  }
  updateDestPreview();
}

async function updateDestPreview() {
  const parent = $('parent_dir').value.trim().replace(/\\/+$/, '');
  const folder = $('folder_name').value.trim();
  const previewEl = $('dest_preview');
  const warnEl = $('exists_warn');
  if (!parent || !folder) { previewEl.textContent = ''; warnEl.className = 'warn'; return; }
  const dest = parent + '/' + folder;
  previewEl.textContent = '将写入：' + dest + '/index.md';
  const r = await fetch('/api/check_dest?dest_dir=' + encodeURIComponent(dest));
  const data = await r.json();
  warnEl.className = data.exists ? 'warn show' : 'warn';
  $('overwrite_confirm_wrap').style.display = data.exists ? 'inline' : 'none';
}

$('preview_btn').addEventListener('click', doPreview);
$('parent_dir').addEventListener('input', updateDestPreview);
$('folder_name').addEventListener('input', updateDestPreview);

$('import_btn').addEventListener('click', async () => {
  const parent = $('parent_dir').value.trim();
  const folder = $('folder_name').value.trim();
  const exportDir = $('export_dir').value.trim();
  const log = $('log');
  if (!exportDir || !parent || !folder || !$('title').value.trim()) {
    log.className = 'show error';
    log.textContent = '请先填写导出文件夹、目标目录、文件夹名和标题。';
    return;
  }
  const destExists = $('exists_warn').className.includes('show');
  if (destExists && !$('overwrite_confirm').checked) {
    log.className = 'show error';
    log.textContent = '目标目录已存在，请勾选"我确认要覆盖已存在的目标目录"后再试一次。';
    return;
  }
  log.className = 'show';
  log.textContent = '导入中…';
  const payload = {
    export_dir: exportDir,
    dest_dir: parent + '/' + folder,
    title: $('title').value.trim(),
    tags: $('tags').value.split(',').map(s => s.trim()).filter(Boolean),
    series: $('series').value.trim(),
    clean: $('clean').checked,
  };
  const r = await fetch('/api/import', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload),
  });
  const data = await r.json();
  log.className = data.ok ? 'show' : 'show error';
  log.textContent = data.log;
});

loadOptions();
</script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def _json(self, obj, status=200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            body = PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if parsed.path == "/api/options":
            self._json({
                "export_dirs": find_export_dirs(),
                "section_dirs": find_section_dirs(),
            })
            return

        if parsed.path == "/api/preview":
            qs = parse_qs(parsed.query)
            export_dir = Path(qs.get("export_dir", [""])[0]).expanduser()
            try:
                if not export_dir.is_dir():
                    raise ValueError(f"不是一个目录：{export_dir}")
                md_files = sorted(export_dir.glob("*.md"))
                if not md_files:
                    raise ValueError(f"文件夹里没有找到 .md 文件：{export_dir}")
                if len(md_files) > 1:
                    raise ValueError(f"文件夹里有不止一个 .md 文件：{[f.name for f in md_files]}")
                text = md_files[0].read_text(encoding="utf-8")
                m = importer.TITLE_RE.search(text)
                if not m:
                    raise ValueError("在导出文件里没找到 '# 标题' 行")
                exported_title = m.group(1)
                created = importer.parse_created(text)
                self._json({
                    "exported_title": exported_title,
                    "title": guess_title(exported_title),
                    "tags": guess_tags(exported_title),
                    "created": created.strftime("%Y-%m-%d") if created else None,
                })
            except Exception as e:
                self._json({"error": str(e)})
            return

        if parsed.path == "/api/check_dest":
            qs = parse_qs(parsed.query)
            dest = REPO_ROOT / qs.get("dest_dir", [""])[0]
            self._json({"exists": dest.is_dir() and any(dest.iterdir())})
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        if self.path != "/api/import":
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw.decode("utf-8"))
            export_dir = Path(payload["export_dir"]).expanduser()
            dest_dir = REPO_ROOT / payload["dest_dir"]
            tags = payload.get("tags") or ["Docs"]
            title = payload.get("title") or None
            series = payload.get("series") or None
            clean = bool(payload.get("clean"))

            buf = io.StringIO()
            with redirect_stdout(buf):
                run_import(export_dir, dest_dir, tags, title, series, clean)
            self._json({"ok": True, "log": buf.getvalue()})
        except SystemExit as e:
            self._json({"ok": False, "log": str(e)})
        except Exception as e:
            self._json({"ok": False, "log": f"导入失败：{e}"})


def run_import(export_dir, dest_dir, tags, title, series, clean):
    """Mirrors import_notion.main()'s body, parameterized instead of argv-driven."""
    if not export_dir.is_dir():
        raise SystemExit(f"Not a directory: {export_dir}")

    md_files = sorted(export_dir.glob("*.md"))
    if not md_files:
        raise SystemExit(f"No .md file found in {export_dir}")
    if len(md_files) > 1:
        raise SystemExit(f"Expected exactly one .md file in {export_dir}, found {len(md_files)}")
    md_path = md_files[0]

    text = md_path.read_text(encoding="utf-8")

    title_match = importer.TITLE_RE.search(text)
    if not title_match:
        raise SystemExit("Could not find a top-level '# Title' line in the export")
    exported_title = title_match.group(1)
    final_title = title or exported_title

    created = importer.parse_created(text)
    from datetime import datetime
    date = created or datetime.fromtimestamp(md_path.stat().st_mtime)

    asset_dirname = exported_title
    asset_dir = export_dir / asset_dirname
    if not asset_dir.is_dir():
        subdirs = [d for d in export_dir.iterdir() if d.is_dir()]
        asset_dir = subdirs[0] if len(subdirs) == 1 else None

    body = importer.strip_meta_lines(text)
    if asset_dir is not None:
        body = importer.rewrite_image_links(body, asset_dir.name)
    body = importer.escape_math_asterisks(body)
    body = importer.collapse_math_blank_lines(body)

    last_edit = f"{date.month}/{date.day}/{date.strftime('%y')}"

    tags_yaml = "[" + ", ".join(f'"{t}"' for t in tags) + "]"
    front_matter_lines = [
        "---",
        f'title: "{final_title}"',
        f"date: {date.strftime('%Y-%m-%d')}",
        f"tags: {tags_yaml}",
    ]
    if series:
        front_matter_lines.append(f'series: ["{series}"]')
    front_matter_lines += ["math: mathjax", "---", "", f"> Last Edit: {last_edit}", "", ""]

    final_text = "\n".join(front_matter_lines) + body

    dest_dir.mkdir(parents=True, exist_ok=True)
    (dest_dir / "index.md").write_text(final_text, encoding="utf-8")

    copied = []
    if asset_dir is not None:
        import shutil
        for f in asset_dir.iterdir():
            if f.is_file():
                shutil.copy2(f, dest_dir / f.name)
                copied.append(f.name)

    print(f"标题：{final_title}")
    print(f"日期：{date.strftime('%Y-%m-%d')}（Last Edit: {last_edit}）")
    print(f"写入：{dest_dir.relative_to(REPO_ROOT)}/index.md")
    print(f"图片：拷贝 {len(copied)} 个 -> {dest_dir.relative_to(REPO_ROOT)}")
    for name in copied:
        print(f"  - {name}")

    if clean:
        import shutil
        shutil.rmtree(export_dir)
        print(f"已删除源导出文件夹：{export_dir}")
    else:
        print(f"\n（源导出文件夹保留在 {export_dir}，勾选“导入后删除”可自动清理）")


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8799)
    ap.add_argument("--no-browser", action="store_true")
    args = ap.parse_args()

    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    url = f"http://127.0.0.1:{args.port}/"
    print(f"Notion 导入 UI 已启动：{url}")
    print("按 Ctrl+C 停止")
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
