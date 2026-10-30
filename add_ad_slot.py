"""全記事の下に広告枠を入れる（ad_slot.html の中身を、全記事にそろえて書き込む）。

使い方: py add_ad_slot.py
- 広告の中身は ad_slot.html だけで管理する。ASP のリンクコードはそこに改変せず貼る
- 各記事の「あわせて読みたい」（<nav class="related"）の直前に <!-- ad-slot:start --> 〜 <!-- ad-slot:end --> を置き、毎回その間を書き換える
- ad_slot.html が空（コメントだけ）のときは、印だけ置いて何も表示しない
- PR 表示（pr-notice）の無い記事には、記事ヘッダーの直後に PR 表示を自動で付ける（<!-- pr-notice:auto --> の印つき）。
  中身を空に戻すと、自動で付けた PR 表示だけを外す。記事にもともとある PR 表示には触らない
"""
import glob
import io
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

CATS = ["kaigyo", "keiei", "money", "review", "shikumi"]
START, END = "<!-- ad-slot:start -->", "<!-- ad-slot:end -->"
PR_START, PR_END = "<!-- pr-notice:auto:start -->", "<!-- pr-notice:auto:end -->"
# ad_slot.html には実際に使っている物だけを載せる前提の文言（CLAUDE.md「アフィリエイト / 広告表示ルール」）
PR_TEXT = "本記事はアフィリエイト広告を含みます。実際に自分の店で使ったツール・サービスのみを、対価の有無にかかわらず正直に評価しています。"


def load_ad():
    s = io.open("ad_slot.html", encoding="utf-8").read()
    return re.sub(r"<!--.*?-->", "", s, flags=re.S).strip()


def apply(path, ad):
    raw = io.open(path, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in raw else "\n"
    s = raw.replace("\r\n", "\n")

    # 広告枠
    if ad:
        items = "\n".join("        " + l for l in ad.split("\n") if l.strip())
        block = (f"    {START}\n    <aside class=\"ad-slot\" aria-label=\"広告\">\n"
                 f"      <p class=\"ad-slot__label\">PR・この店で実際に使っている道具</p>\n"
                 f"      <ul class=\"ad-slot__list\">\n{items}\n      </ul>\n    </aside>\n    {END}")
    else:
        block = f"    {START}\n    {END}"
    if START in s:
        s = re.sub(r"    " + re.escape(START) + r".*?" + re.escape(END), lambda m: block, s, flags=re.S)
    else:
        i = s.find('    <nav class="related"')
        if i < 0:
            i = s.find("</article>")
        if i < 0:
            return "skip"
        s = s[:i] + block + "\n\n" + s[i:]

    # PR 表示（自動で付けた分だけを出し入れする）
    # 入れたときの形（"\n\n  " + 印〜印）をそのまま外すので、何度動かしても空行は増えない
    s = re.sub(r"\n\n  " + re.escape(PR_START) + r".*?" + re.escape(PR_END), "", s, flags=re.S)
    if ad and 'class="pr-notice"' not in s:
        art = s.find('<article class="article">')
        h = s.find("  </header>", art)
        if art < 0 or h < 0:
            return "no-header"
        h += len("  </header>")
        pr = (f"\n\n  {PR_START}\n  <aside class=\"pr-notice\" role=\"note\" aria-label=\"広告に関する表示\">\n"
              f"    <span class=\"pr-notice__tag\">PR</span>\n    <span>{PR_TEXT}</span>\n  </aside>\n  {PR_END}")
        s = s[:h] + pr + s[h:]

    out = s.replace("\n", nl)
    if out != raw:
        io.open(path, "w", encoding="utf-8", newline="").write(out)
        return "updated"
    return "same"


def main():
    ad = load_ad()
    res = {}
    for c in CATS:
        for p in sorted(glob.glob(f"{c}/*/index.html")):
            r = apply(p, ad)
            res.setdefault(r, []).append(p)
    for k, v in res.items():
        print(k, len(v))
        if k not in ("updated", "same"):
            print("  ", v)


if __name__ == "__main__":
    main()
