#!/usr/bin/env python3
# リポジトリ内の index.html を走査して sitemap.xml を自動生成する
import os, re, datetime

DOMAIN = "https://hikagen-techo.com"
# Actions では GITHUB_WORKSPACE、ローカルでは scripts から2つ上をリポジトリ直下とみなす
ROOT = os.environ.get("GITHUB_WORKSPACE") or os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
JST = datetime.timezone(datetime.timedelta(hours=9))
TODAY = datetime.datetime.now(JST).date().isoformat()

def find_pages(root):
    pages = []
    for dirpath, dirnames, filenames in os.walk(root):
        # ドット始まり(.git/.github等)と node_modules は走査対象から除外
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "node_modules"]
        if "index.html" in filenames:
            rel = os.path.relpath(dirpath, root)
            url = "/" if rel == "." else "/" + rel.replace(os.sep, "/") + "/"
            pages.append((url, os.path.join(dirpath, "index.html")))
    return pages

def get_lastmod(path):
    try:
        with open(path, encoding="utf-8") as f:
            html = f.read()
    except Exception:
        return None
    # <time datetime="2026-05-26"> から日付を拾い、最新（＝更新日）を採用
    dates = re.findall(r'datetime="(\d{4}-\d{2}-\d{2})', html)
    return max(dates) if dates else None

def main():
    pages = sorted(find_pages(ROOT), key=lambda x: (x[0] != "/", x[0]))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, path in pages:
        lastmod = get_lastmod(path) or TODAY
        lines.append(f"  <url><loc>{DOMAIN}{url}</loc><lastmod>{lastmod}</lastmod></url>")
    lines.append("</urlset>")
    out_path = os.path.join(ROOT, "sitemap.xml")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"✅ {out_path} を生成: {len(pages)} URL")

if __name__ == "__main__":
    main()
