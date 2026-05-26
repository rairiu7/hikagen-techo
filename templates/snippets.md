# コピペ用スニペット集

記事作成時にコピーして使うHTMLブロックのリファレンスです。

---

## (A) PR表記ブロック

**挿入位置：** 記事ヘッダー（タイトル・日付）の直下、`.post-body` の先頭（`.lede` より前）

アフィリエイトリンクを含む記事には必ず入れること。スクロールせずに「PR」が見える位置に置く。

```html
<aside class="pr-notice" role="note">
  <span class="pr-notice__label">PR</span>
  <p class="pr-notice__text">
    本記事にはアフィリエイト広告（プロモーション）を含みます。
    紹介しているサービスはすべて、筆者が実際に使用した・使用中のものです。
    詳しくは<a href="/disclosure/">運営方針</a>をご覧ください。
  </p>
</aside>
```

---

## (B) アフィリエイトリンク記法

`href` 内の `XXXXXX` は、各ASPで発行された計測リンクIDに差し替えること。

### インラインリンク（文中に埋め込む）

```html
<a href="https://px.a8.net/svt/ejp?a8mat=XXXXXX" rel="sponsored noopener" target="_blank">サービス名</a>
```

### CTAボタン（記事末尾やCTAボックス内）

```html
<a href="https://px.a8.net/svt/ejp?a8mat=XXXXXX" rel="sponsored noopener" target="_blank" class="aff-btn">○○を無料で試す</a>
```

### もしもアフィリエイト

```html
<!-- インライン -->
<a href="https://af.moshimo.com/af/c/click?a_id=XXXXXX&p_id=XXXXXX" rel="sponsored noopener" target="_blank">サービス名</a>

<!-- CTAボタン -->
<a href="https://af.moshimo.com/af/c/click?a_id=XXXXXX&p_id=XXXXXX" rel="sponsored noopener" target="_blank" class="aff-btn">○○を無料で試す</a>
```

### 属性ルール

| 属性 | 値 | 理由 |
|---|---|---|
| `rel` | `sponsored noopener` | 収益リンクには必須（景品表示法・Google方針）。`target="_blank"` 時の `noopener` は必須 |
| `target` | `_blank` | 外部サービスへの誘導のため別タブ推奨 |
| `class` | `aff-btn`（CTAの場合のみ） | スタイル適用 |

> **注意：** 無料サービス（Airレジ等）の公式リンクに `rel="sponsored"` を付ける場合でも、A8.net / もしもの計測リンク以外は `nofollow` を追加する（例：`rel="sponsored nofollow noopener"`）。
