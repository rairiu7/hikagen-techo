"""PCの左右の空いている場所に広告の列を入れる（画面の広いPCだけに出す。スマホでは出さない）。

使い方: py add_side.py
- 左の列＝今の店の厨房機器（side_left.html）、右の列＝記事の下の広告枠と同じ中身（ad_slot.html）
- 各記事の </main> の直前に <!-- side:start --> 〜 <!-- side:end --> を置き、毎回その間を書き換える
- 記事の幅は変えない。CSS は css/style.css の .side-rail（幅の広い画面だけ position: fixed で左右に出す）
- 両方の中身が空（コメントだけ）なら印だけ置いて何も出さない
- 列はPR表示（pr-notice）のある記事にだけ出す。add_ad_slot.py の後に動かす
"""
import glob
import io
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

CATS = ["kaigyo", "keiei", "money", "review", "shikumi"]
START, END = "<!-- side:start -->", "<!-- side:end -->"


def load(name):
    s = io.open(name, encoding="utf-8").read()
    return re.sub(r"<!--.*?-->", "", s, flags=re.S).strip()


def rail(side, label, items):
    if not items:
        return ""
    li = "\n".join("        " + l for l in items.split("\n") if l.strip())
    # 外側の aside は記事の高さいっぱいに伸ばし、内側の箱だけを画面について来させる（フッターに重ならない）
    return (f'  <aside class="side-rail side-rail--{side}" aria-label="広告">\n'
            f'    <div class="side-rail__box">\n'
            f'      <p class="side-rail__label">{label}</p>\n'
            f'      <ul class="side-rail__list">\n{li}\n      </ul>\n    </div>\n  </aside>\n')


def main():
    left = load("side_left.html")
    right = re.sub(r'class="ad-slot__', 'class="side-rail__', load("ad_slot.html"))
    res = {}
    for c in CATS:
        for p in sorted(glob.glob(f"{c}/*/index.html")):
            raw = io.open(p, encoding="utf-8", newline="").read()
            nl = "\r\n" if "\r\n" in raw else "\n"
            s = raw.replace("\r\n", "\n")
            inner = ""
            if 'class="pr-notice"' in s:
                inner = rail("left", "PR・今の店の厨房機器", left) + rail("right", "PR・この店で実際に使っている道具", right)
            block = f"  {START}\n{inner}  {END}\n"
            if START in s:
                s = re.sub(r"  " + re.escape(START) + r".*?" + re.escape(END) + r"\n", lambda m: block, s, flags=re.S)
            elif "</main>" in s:
                s = s.replace("</main>", block + "</main>", 1)
            else:
                res.setdefault("skip", []).append(p)
                continue
            out = s.replace("\n", nl)
            r = "same" if out == raw else "updated"
            if r == "updated":
                io.open(p, "w", encoding="utf-8", newline="").write(out)
            res.setdefault(r, []).append(p)
    for k, v in res.items():
        print(k, len(v))
        if k == "skip":
            print("  ", v)


if __name__ == "__main__":
    main()
