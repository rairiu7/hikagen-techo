"""全記事の「まとめ」の後（著者ボックスの前）に、SNSで共有するボタンを入れる。

使い方: py add_share.py
- 各記事の <!-- 著者ボックス --> の直前に <!-- share:start --> 〜 <!-- share:end --> を置き、毎回その間を書き換える
- 記事のURLと題名は og:url・og:title から取る
- 各SNSの共有用のURLへ飛ぶ、ただのリンクにしている（外部のスクリプトを読み込まないので、読者の情報を外に渡さない）
"""
import glob
import html
import io
import os
import re
from urllib.parse import quote

os.chdir(os.path.dirname(os.path.abspath(__file__)))

CATS = ["kaigyo", "keiei", "money", "review", "shikumi"]
START, END = "<!-- share:start -->", "<!-- share:end -->"
MARK = "    <!-- 著者ボックス -->"


def block(url, title):
    u, t = quote(url, safe=""), quote(title, safe="")
    links = [
        ("x", "X", f"https://x.com/intent/post?text={t}&amp;url={u}"),
        ("line", "LINE", f"https://social-plugins.line.me/lineit/share?url={u}"),
        ("facebook", "Facebook", f"https://www.facebook.com/sharer/sharer.php?u={u}"),
        ("hatena", "はてブ", "https://b.hatena.ne.jp/entry/s/" + url.split("://", 1)[1]),
        ("threads", "Threads", f"https://www.threads.net/intent/post?text={t}%20{u}"),
    ]
    a = "\n".join(f'        <a class="share__btn share__btn--{k}" href="{h}" target="_blank" rel="noopener nofollow">{n}</a>'
                  for k, n, h in links)
    return (f"    {START}\n    <aside class=\"share\" aria-label=\"この記事を共有する\">\n"
            f"      <p class=\"share__label\">役に立ったら、共有してもらえるとうれしいです</p>\n"
            f"      <div class=\"share__list\">\n{a}\n      </div>\n    </aside>\n    {END}\n\n")


def main():
    res = {}
    for c in CATS:
        for p in sorted(glob.glob(f"{c}/*/index.html")):
            raw = io.open(p, encoding="utf-8", newline="").read()
            nl = "\r\n" if "\r\n" in raw else "\n"
            s = raw.replace("\r\n", "\n")
            mu = re.search(r'<meta property="og:url" content="([^"]+)"', s)
            mt = re.search(r'<meta property="og:title" content="([^"]+)"', s)
            if not mu or not mt:
                res.setdefault("no-og", []).append(p)
                continue
            title = html.unescape(mt.group(1)).split("｜火加減手帖")[0]
            b = block(mu.group(1), title)
            if START in s:
                s = re.sub(r"    " + re.escape(START) + r".*?" + re.escape(END) + r"\n\n", lambda m: b, s, flags=re.S)
            elif MARK in s:
                s = s.replace(MARK, b + MARK, 1)
            else:
                res.setdefault("no-mark", []).append(p)
                continue
            out = s.replace("\n", nl)
            r = "same" if out == raw else "updated"
            if r == "updated":
                io.open(p, "w", encoding="utf-8", newline="").write(out)
            res.setdefault(r, []).append(p)
    for k, v in res.items():
        print(k, len(v))
        if k not in ("updated", "same"):
            print("  ", v)


if __name__ == "__main__":
    main()
