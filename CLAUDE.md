# 火加減手帖 — プロジェクトガイド（Claude Code用）

地方の小商い向けメディア「火加減手帖（Hikagen Techo）」の静的サイト。
このファイルのルールを常に守ること。記事は一次情報を武器に、GEO（AI検索引用）最適化で書く。

## 最重要：個人特定防止ルール（絶対厳守）
出力（HTML本文・Schema・コメント・コミットメッセージ含む）に、以下を**絶対に含めない**：
- 実際の店名・屋号、個人名、共同経営者の身体的特徴など個人を特定し得る情報
- 市区町村以下の所在地、都道府県名
- 正確な売上・経費・利益の実数字
- 実店舗のSNSアカウントや実店舗HPのURL
代わりに、必ず**ぼかし表現**を使う：
- 地域 →「人口5万人未満の地方都市」
- 規模 →「年商800〜1,000万円規模」
- 変化は率や時間で →「45分→5分（約89%削減）」のように
- 共同経営者 →「料理担当のパートナー」「共同経営者」のみ。関係性・性別・名前・外見は一切出さない。
迷ったら特定情報は出さない。新規ルールが必要になったらこのファイルに追記する。

## 著者・媒体
- 著者ペンネーム：**HANABI**（肩書き「地方で小商いを仕組み化する人」）
- 媒体：火加減手帖 / Hikagen Techo / https://hikagen-techo.com/
- キャッチコピー：地方の小さな飲食店が、仕組みで勝つ。
- Person JSON-LD：`@id` = `https://hikagen-techo.com/#person`、`url` = `https://hikagen-techo.com/about/` で全ページ統一。
- サイト名「火加減手帖」は WebSite schema の `name` / `<title>` / ヘッダー・フッターに使う。`Person.name` は必ず **HANABI**（混同しない）。
- `sameAs` は付けない（店舗SNS・屋号など外部リンクを出さないプライバシー方針）。

## 技術構成
- 静的 HTML/CSS/JS のみ。ビルド工程なし。Cloudflare がアセットを配信（assets root = リポジトリ直下 `./`）。
- GitHub（main ブランチ）への push で Cloudflare が自動デプロイ。
- push は内容を確認のうえ、ユーザー承認後に行う。

## デプロイ運用（Cloudflare）
- `wrangler deploy`（Workers向け）は使わない（`wrangler.toml` が無い・自動デプロイと競合の恐れ）。
- push 後 2〜3 分経っても本番に反映されない場合は、空コミットで再トリガーする：
  `git commit --allow-empty -m "chore: trigger deploy" && git push origin main`
- HTML は Cloudflare エッジでキャッシュされる（`cf-cache-status: HIT`）。反映確認・トラブル時は Cloudflare ダッシュボード → Caching → Purge Everything。
- **「Block AI bots」は必ず OFF のまま**。GEO戦略上、AIクローラー（GPTBot / OAI-SearchBot / ClaudeBot / PerplexityBot 等）のアクセスを遮断してはいけない。

## ディレクトリ / URL 設計
- 共通CSS：`/css/style.css`（全ページがこれを `<link rel="stylesheet" href="/css/style.css">` で参照）
- プロフィール：`/about/index.html`
- カテゴリと slug：記事は `<category>/<slug>/index.html`、URL は末尾スラッシュ
  - keiei（経営のリアル） / shikumi（仕組み化） / review（正直レビュー） / money（個人事業主のお金） / kaigyo（開業・独立）
- 記事の雛形：`article-template.html`（リポジトリには push しない作業用テンプレ）。新記事はこれを基に作る。

## 記事テンプレート構造（8要素）
1. タイトル（結論を含む） 2. 冒頭の結論ファースト 3. 筆者の状況・前提（一次情報の担保）
4. 本文（体験談＋具体的数字） 5. 使用ツールの自然な紹介 6. まとめ
7. FAQ（3〜5問） 8. Schema マークアップ

## GEO 6ルール（全記事）
1. 冒頭に結論（`.lede`） 2. 具体的な数字を入れる（`.stat`） 3. 末尾にFAQ 3〜5問
4. 構造化データを埋める 5. 公開日・更新日を明記 6. 一次情報（「私が実際に〜」）を前面に

## 構造化データ（JSON-LD）
- 全記事に必ず：**Person**（`@id` = `https://hikagen-techo.com/#person` で共通）、**Article**、**FAQPage**、**BreadcrumbList**
- レビュー記事は **Review**（itemReviewed + reviewRating）も追加
- **FAQPage の Q&A 文面は、本文の `.faq` の文面と完全一致させる**（不一致は不可）
- カテゴリ一覧ページ（keiei / shikumi / review / money / kaigyo の各 index.html）には **CollectionPage + BreadcrumbList** を `@graph` で設置する（実装済み）。
- トップページには **WebSite**（`@id` = `https://hikagen-techo.com/#website`）+ **Person** を `@graph` で設置（実装済み）。新たに Organization schema は不要（個人事業主のため Person が publisher）。

## 文章方針
- 結論ファースト。一次情報を前面に。曖昧表現より具体的な数字。
- 「おすすめ◯選」「徹底比較」などの比較記事は作らない。「私が実際に選んだ理由／使った感想」の一次情報記事のみ。
- 良い点だけでなく正直な弱点も書く（信頼の核）。

## OGP / SNS シェア
- `og:image` は全21記事に実装済み（1200×630 PNG、`/ogp/<cat>-<slug>.png`）。
- `twitter:card` は全記事 `summary_large_image` に設定済み。
- 生成スクリプト：`generate_ogp.py`（Pillow + Noto Sans JP）。新記事追加時は「新記事公開時の必須作業」手順5を参照。
- **Playfair Display は日本語グリフを持たない**。OGP画像の日本語テキストは必ず Noto Sans JP で描画すること（generate_ogp.py はこの設定で実装済み）。

## デザイントークン（style.css に定義済み・勝手に変えない）
- 色：ベース #FAFAF8 / 文字 #2D2D2D / アクセント(オリーブ) #6B7F5E / サブ #F5F5F3
- フォント：見出し Playfair Display + Noto Sans JP / 本文 Noto Sans JP / 装飾 DM Sans / 等幅 DM Mono
- 写真は使わない（個人特定防止）

## 収益化
- ASP：A8.net / もしもアフィリエイト / バリューコマース。実際に使ったもの・使ったことがあるものだけ紹介。
- CTA リンクは計測リンクに差し替える前提。`rel="sponsored nofollow noopener"` を付与。
- 無料サービス（例：Airレジ）は売り込まず、連携する有料ツール（会計ソフト等）の記事へ送客する。

## アフィリエイト提案ルール（記事執筆時）
- 記事を書くとき・編集するときに、本文中で言及しているツール・商品・サービスがアフィリエイト提携できそうな場合は**必ずユーザーに提案する**。
- 提案の基準：実際に使っている／使ったことがある一次情報として登場するもの（比較記事・憶測でのリンクは不可）。
- 提案の形式：「〇〇（記事名・箇所）で××（ツール・商品名）に触れています。アフィリエイトリンクを探して追加できますが、どうしますか？」と一言添える。
- 既存リンク一覧はメモリ（`ref_affiliate_links.md`）で管理。提案前にそちらを確認し、実装済みのものは重複提案しない。

## アフィリエイトリンクの実装ルール
- 商用外部リンクはすべて `rel="sponsored nofollow noopener" target="_blank"`。
- ASP（A8.net / もしも）が発行したリンクコードは**改変しない**：
  - トラッキング URL（先頭 `//` や `&` パラメータを含む）はそのまま使う。`&` → `&amp;` 変換・URL 再エンコードをしない。
  - もしもの計測ピクセル `<img ... i.moshimo.com/af/i/impression ...>` は `<a>` の直後に必ず置く。
  - `referrerpolicy` / `attributionsrc` 等の計測属性を削除しない。
  - 自分で付け足してよい属性は `sponsored` / `noopener` / `target="_blank"` のみ。
- もしも「どこでもリンク」の「リンク先URL」には**広告主サイトの URL** を入れる（自サイト `hikagen-techo.com` の URL は絶対に入れない）。
- 既存の収益リンク：
  - `/review/moneyforward/` … もしも「マネーフォワード クラウド登録プロモーション」(p_id=888) / 飛び先 `biz.moneyforward.com/accounting/`
  - `/review/airregi/` … Airレジ（提携・計測リンク実装は別途対応）

## アフィリエイト / 広告表示ルール（ステマ規制対応）
- `rel="sponsored"` を含む外部リンクを1つでも持つ記事には、記事ヘッダー（`</header>` 直後）かつ本文の前に `<aside class="pr-notice">` を必ず設置する。
- 文言は無条件・明瞭に：「PR 本記事はアフィリエイト広告を含みます。実際に自分の店で使ったツール・サービスのみを、対価の有無にかかわらず正直に評価しています。」
- 「〜する場合があります」等の条件付き表現は使わない（断定形）。
- アフィリエイトリンクが無いページ（about / privacy / contact / disclaimer / disclosure / カテゴリ一覧 / トップ）には PR表記を付けない。
- `.pr-notice` / `.pr-notice__tag` の CSS は `css/style.css` に 1か所だけ定義（重複定義しない）。

## GEO土台チェック（初期設定・随時確認）
- **robots.txt**（`/robots.txt`）で `User-agent: * / Allow: /` が維持されているか確認。AIクローラー（GPTBot / OAI-SearchBot / ClaudeBot / PerplexityBot / Google-Extended / Amazonbot）を個別に Disallow していないか。
- **Cloudflare ダッシュボード** → Security → Bots で「Block AI Bots」が OFF のまま保たれているか定期確認。
- **Crawler Hints（IndexNow）** → Cloudflare → Caching → Configuration → Crawler Hints を ON（設定済み）。新記事公開時に Bing へ自動通知される。
- **Bing Webmaster Tools** に `sitemap.xml` を提出する（ChatGPT検索はBingインデックスを参照するため、GEO目的ではGoogleより優先度高）（提出済み・処理完了後はインデックス状況を定期確認）。
- **Google Search Console** に `sitemap.xml` を提出する（登録済み）。
- 上記4点は一度設定すれば基本的に変わらないが、Cloudflareのアップデートで設定が変わる場合があるため月1回確認推奨。

## 公開前チェック（新規・更新記事で必ず実行）
- 各 JSON-LD が正しくパースできる
- 見える FAQ 件数 = FAQPage Schema の Question 件数（かつ文面一致）
- HTML タグの開閉が揃っている
- 個人特定情報（店名・地名・実数字・個人名・実URL）が混入していない
- `/css/style.css` への参照が先頭スラッシュ付きで入っている
- アフィリエイトリンクを含む記事に `<aside class="pr-notice">` が記事ヘッダー直後にあるか

## 新記事公開時の必須作業（記事HTMLと同時に必ず更新）
記事ファイルを作成したら、以下を**必ずセットで更新してからpush**する：
1. **カテゴリ一覧ページ** `<category>/index.html` の `<nav class="related__list">` に `<a class="related__item">` を追記
2. **トップページ** `index.html` の `<div class="art-list">` に `<a class="art">` を**先頭に**追記し、既存の連番を1ずつ繰り下げる（新しい記事が常に上＝小さい番号になるよう、末尾ではなく先頭に挿入する）
3. **sitemap.xml** に `<url>` エントリを追加
これを怠ると直リンクではアクセスできてもサイト内の一覧に載らない。
4. **このCLAUDE.md** の「公開済み記事一覧」テーブルにも行を追加し、日付を更新する
5. **OGP画像の生成と og:image タグの追加**（必須）：
   - リポジトリ直下で `py generate_ogp.py` を実行 → `/ogp/<cat>-<slug>.png` が生成される
   - 続けて `py add_ogp_tags.py` を実行 → 新記事の HTML に og:image / twitter:card タグが自動挿入される
   - 生成された PNG と更新された HTML を git add してから push する

## 作業ログ運用（オプション・新規提案）
- 大きな作業の完了後は `docs/worklog/YYYY-MM-DD-{topic}.md` に以下を残し、main に push する（Claude.ai側との情報共有用）：
  - 実装内容のサマリ
  - 設計判断の理由
  - 次回への申し送り

## 既存ファイル（構造・トーンの参照元）
- `css/style.css` … 全コンポーネントのスタイル
- `about/index.html` … プロフィール記事の完成形
- `shikumi/gas-order/index.html` … コード公開記事の完成形
- `review/airregi/index.html` … 正直レビュー記事の完成形
新記事はこれらのトーンと構造に合わせる。

## 公開済み記事一覧（最終更新：2026-05-31）
| カテゴリ | slug | タイトル |
|---|---|---|
| keiei | nebuke | 大手と価格で戦わない——弁当屋が原価率35%・800円台の値付けにたどり着くまで |
| keiei | staff-saiyou | 弁当屋が8人雇って3人辞めた話 |
| keiei | hitori-unui | 弁当屋2店舗をほぼ1人で3年回している |
| shikumi | yoyaku-kanri | 予約経路5つ・集約先ひとつ——製造漏れをゼロにした予約管理の仕組み |
| shikumi | seisan-shiji | ホワイトボードと電卓をやめた日——生産指示のデジタル化 |
| shikumi | gas-order | GASで注文管理を自動化したら毎日30分が5分になった話【コード公開】 |
| review | airregi-erabu | SquareとAirレジ、深く比較しなかった私がAirレジを選んだ理由と3年後の結論 |
| review | moneyforward | 弥生会計からマネーフォワード クラウド会計に乗り換えた理由と2年使った感想 |
| review | airregi | 開業時にレジをAirレジにした理由と2年使った正直な感想 |
| money | invoice | 消費税・インボイスに個人事業主として向き合った話 |
| money | keihi-kanri | 弁当屋の経費管理は「9割自動・手入力月30分」 |
| money | aoiro-shinkoku | 税理士なしで青色申告を2年やりきった弁当屋 |
| kaigyo | yatte-okeba | 開業前にやっておけばよかったこと——3年後の正直な後悔リスト |
| kaigyo | bukken-sagashi | 物件探し3年・内覧30件——立地選びで一番重視したのは駐車場だった |
| kaigyo | tetsuzuki | 飲食店の開業手続きを全部やった |
| kaigyo | sogyoshikin | 弁当屋が2回借りた創業資金の話 |
| shikumi | genka-kanri | 調味料をこっそり測るところから始めた——弁当屋の原価計算、どんぶりから抜け出すまで |
| money | hoken-nenkin | サラリーマンから個人事業主になった1年目、税金で車を売った話 |
| review | jigyo-card | 事業用カードを2枚に絞った理由——コストコカードとPayPayカードで仕入れと日常払いを完全分離 |
| review | food-processor | フードプロセッサーで仕込みが1時間から10分に——ティファールからクイジナートに買い替えた弁当屋の正直レビュー |
| review | alexa | 弁当屋がAlexaを2店舗に置いている理由——タイマー・計算・トランシーバーまで、調理現場で使い続けている正直な感想 |
