"""
OGP画像生成スクリプト（1200×630）
火加減手帖 — 記事別og:image PNG を /ogp/ ディレクトリに出力する
"""
from PIL import Image, ImageDraw, ImageFont
import os, re
from pathlib import Path

# --- デザイントークン ---
BG      = "#FAFAF8"
ACCENT  = "#6B7F5E"
TEXT    = "#2D2D2D"
WHITE   = "#FFFFFF"
MUTED   = "#7A7A72"
LINE    = "#E5E5E0"

W, H    = 1200, 630
PAD     = 80

FONT_JP = r"C:\Windows\Fonts\NotoSansJP-VF.ttf"

CATEGORY_LABELS = {
    "keiei":   "経営のリアル",
    "shikumi": "仕組み化",
    "review":  "正直レビュー",
    "money":   "個人事業主のお金",
    "kaigyo":  "開業・独立",
}

def font(size):
    return ImageFont.truetype(FONT_JP, size)

def wrap_jp(text, fnt, max_w, draw):
    """文字単位で折り返す（日本語対応）"""
    lines, cur = [], ""
    for ch in text:
        test = cur + ch
        w = draw.textbbox((0, 0), test, font=fnt)[2]
        if w > max_w and cur:
            lines.append(cur)
            cur = ch
        else:
            cur = test
    if cur:
        lines.append(cur)
    return lines

def fit_title(title, draw, max_w, max_lines=3):
    """フォントサイズを自動調整して最大3行に収める"""
    for size in (52, 44, 36, 30):
        fnt = font(size)
        lines = wrap_jp(title, fnt, max_w, draw)
        if len(lines) <= max_lines:
            return fnt, lines
    # それでも収まらなければ3行で切る
    fnt = font(30)
    lines = wrap_jp(title, fnt, max_w, draw)
    lines = lines[:max_lines]
    lines[-1] = lines[-1][:-1] + "…"
    return fnt, lines

def extract_title(html_path):
    content = Path(html_path).read_text(encoding="utf-8")
    m = re.search(r'<meta property="og:title" content="([^"]+)"', content)
    if m:
        return re.sub(r'｜火加減手帖$', '', m.group(1)).strip()
    m = re.search(r'<title>([^<]+)</title>', content)
    if m:
        return re.sub(r'｜火加減手帖$', '', m.group(1)).strip()
    return "火加減手帖"

def generate(title, cat_label, out_path):
    img  = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # 左アクセントバー
    draw.rectangle([(0, 0), (10, H)], fill=ACCENT)

    # カテゴリバッジ
    f_cat  = font(26)
    cb     = draw.textbbox((0, 0), cat_label, font=f_cat)
    cw, ch = cb[2] - cb[0] + 40, cb[3] - cb[1] + 16
    cx, cy = PAD + 10, PAD
    draw.rounded_rectangle([(cx, cy), (cx + cw, cy + ch)], radius=6, fill=ACCENT)
    draw.text((cx + 20, cy + 8), cat_label, font=f_cat, fill=WHITE)

    # タイトル
    max_title_w = W - PAD * 2 - 20
    f_title, lines = fit_title(title, draw, max_title_w)
    ty = cy + ch + 36
    line_h = draw.textbbox((0, 0), "あ", font=f_title)[3] + 14
    for line in lines:
        draw.text((PAD + 10, ty), line, font=f_title, fill=TEXT)
        ty += line_h

    # 区切り線
    draw.line([(PAD + 10, H - PAD - 18), (W - PAD, H - PAD - 18)], fill=LINE, width=1)

    # サイト名（右下）
    f_site = font(30)
    f_en   = font(20)
    sj = "火加減手帖"
    se = "Hikagen Techo"
    sjb = draw.textbbox((0, 0), sj, font=f_site)
    seb = draw.textbbox((0, 0), se, font=f_en)
    draw.text((W - PAD - (sjb[2] - sjb[0]), H - PAD + 2), sj, font=f_site, fill=ACCENT)
    draw.text((W - PAD - (seb[2] - seb[0]), H - PAD + 36), se, font=f_en, fill=MUTED)

    img.save(out_path, "PNG", optimize=True)
    print(f"  OK  {Path(out_path).name}")

# --- メイン処理 ---
ROOT    = Path(r"C:\Users\user\Documents\hikagen-techo")
OGP_DIR = ROOT / "ogp"
OGP_DIR.mkdir(exist_ok=True)

# サンプル1枚だけ生成（確認用）
SAMPLE_ONLY = False  # True にすると1枚だけ

articles = []
for cat in ["keiei", "shikumi", "review", "money", "kaigyo"]:
    for item in sorted((ROOT / cat).iterdir()):
        idx = item / "index.html"
        if item.is_dir() and idx.exists():
            articles.append((cat, idx))

if SAMPLE_ONLY:
    articles = articles[:1]

print(f"生成対象: {len(articles)} 記事")
for cat, html_path in articles:
    title     = extract_title(html_path)
    cat_label = CATEGORY_LABELS.get(cat, "火加減手帖")
    slug      = html_path.parent.name
    out       = OGP_DIR / f"{cat}-{slug}.png"
    generate(title, cat_label, str(out))

# 共通デフォルト画像
generate("地方の小さな飲食店が、仕組みで勝つ。", "火加減手帖", str(OGP_DIR / "default.png"))

print(f"\n完了: {OGP_DIR}")
