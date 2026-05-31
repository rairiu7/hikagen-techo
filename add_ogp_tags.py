"""全記事に og:image タグを一括追加するスクリプト"""
from pathlib import Path

ROOT     = Path(r"C:\Users\user\Documents\hikagen-techo")
CATS     = ["keiei", "shikumi", "review", "money", "kaigyo"]
BASE_URL = "https://hikagen-techo.com/ogp"

OLD = '<meta property="og:locale" content="ja_JP">\n<meta name="twitter:card" content="summary">'

updated, skipped = [], []

for cat in CATS:
    for item in sorted((ROOT / cat).iterdir()):
        idx = item / "index.html"
        if not (item.is_dir() and idx.exists()):
            continue
        slug    = item.name
        img_url = f"{BASE_URL}/{cat}-{slug}.png"
        content = idx.read_text(encoding="utf-8")

        if "og:image" in content:
            skipped.append(f"{cat}/{slug}")
            continue

        new_block = (
            f'<meta property="og:locale" content="ja_JP">\n'
            f'<meta property="og:image" content="{img_url}">\n'
            f'<meta property="og:image:width" content="1200">\n'
            f'<meta property="og:image:height" content="630">\n'
            f'<meta name="twitter:card" content="summary_large_image">\n'
            f'<meta name="twitter:image" content="{img_url}">'
        )

        if OLD not in content:
            print(f"WARN: pattern not found in {cat}/{slug}")
            skipped.append(f"{cat}/{slug} (pattern missing)")
            continue

        content = content.replace(OLD, new_block)
        idx.write_text(content, encoding="utf-8")
        updated.append(f"{cat}/{slug}")

print(f"\nUpdated: {len(updated)}")
for u in updated:
    print(f"  {u}")
print(f"\nSkipped: {skipped}")
