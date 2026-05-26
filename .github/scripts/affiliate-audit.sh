#!/usr/bin/env bash
# affiliate-audit.sh: アフィリエイトリンクを含むHTMLにPR表記(.pr-notice)があるか監査する
set -euo pipefail

FAILED=0
CHECKED=0
FLAGGED=0

# アフィリエイトドメインのパターン（hrefの値として検出）
AFF_PATTERN='href="[^"]*\b(px\.a8\.net|a8\.net/svt|af\.moshimo\.com)[^"]*"'

while IFS= read -r -d '' file; do
  CHECKED=$((CHECKED + 1))

  # アフィリエイトドメインのURLがhref属性に含まれるか確認
  if grep -qE "$AFF_PATTERN" "$file"; then
    # pr-notice クラスが存在するか確認（class="..." の値中にpr-noticeを含む）
    if ! grep -qE 'class="[^"]*pr-notice[^"]*"' "$file"; then
      echo "::error file=${file}::アフィリエイトリンク（a8.net / moshimo）を含みますが、PR表記ブロック（class=\"pr-notice\"）が見つかりません。記事冒頭にPR表記を追加してください。"
      FLAGGED=$((FLAGGED + 1))
      FAILED=1
    fi
  fi
done < <(find . \
  -name "*.html" \
  -not -path "./.git/*" \
  -not -path "./.github/*" \
  -print0)

echo "--- アフィリエイトPR表記 監査結果 ---"
echo "検査ファイル数: ${CHECKED}"
echo "違反ファイル数: ${FLAGGED}"

if [ "$FAILED" -eq 1 ]; then
  echo "::error::PR表記の欠落が ${FLAGGED} 件あります。上記ファイルの記事冒頭にPR表記ブロック（.pr-notice）を追加してください。"
  exit 1
fi

echo "✓ 全ファイルのPR表記チェック完了：問題なし"
