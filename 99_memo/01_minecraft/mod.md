# MOD一覧

## 🧰 基本＆前提系

### Fabric API

- Fabric MODの土台となる必須ライブラリ
- 操作：なし

### Fabric Language Kotlin

- Kotlin製MODを動かすための言語サポート
- 操作：なし

### Mod Menu

- ゲーム内でMOD一覧・設定画面を開ける
- 操作
  - `Esc → Mod Menu`

### Cloth Config v20

### YetAnotherConfigLib (YACL)

### Placeholder API

### libIPN

### MaLiLib

- MODの設定画面や内部処理を支えるライブラリ群
- 操作：なし（裏方）

---

## 🚀 軽量化・最適化系

※ 入れるだけで効果あり。基本ノータッチ。

### Sodium

- 描画処理を最適化してFPSを大幅向上
- 操作
  - `設定 → ビデオ設定（Sodium専用UI）`

### Lithium

- ゲーム内部処理（CPU負荷）を軽減
- 操作：なし

### FerriteCore

- メモリ使用量を削減
- 操作：なし

### EntityCulling

- 見えないエンティティを描画しない
- 操作：なし

### More Culling

- ブロック単位の描画最適化を追加
- 操作：なし

### BadOptimizations

- 細かい無駄処理をまとめて最適化
- 操作：なし

### ImmediatelyFast

- 描画・UI周りの即時処理を高速化
- 操作：なし

### Concurrent Chunk Management Engine（C2ME）

- チャンク処理を並列化して高速化
- 操作：なし
- ※低スペックPCでは相性注意（重く感じた場合はこのMODを外すだけでOK）

### ModernFix

- 起動・ロード・メモリ周りを総合的に改善
- 操作：なし

### ServerCore

- サーバー・マルチプレイ向け最適化
- 操作：なし

### Very Many Players

- 多人数プレイ時の処理最適化
- 操作：なし

### ScalableLux

- 光源・明るさ計算を改善
- 操作：Mod Menuから設定可能（基本不要）

---

## 📦 QoL（快適プレイ）系

※ 使わなくてもOK。必要なときだけ使う。

### Inventory Profiles Next

- インベントリ整理・装備管理
- 操作
  - `R`：インベントリ自動整理
  - `Mod Menu → 設定` で細かくカスタム可

### Item Scroller

- スクロールでアイテム操作を高速化
- 操作
  - `Shift + マウスホイール` など（設定変更可）

### Tweakeroo

- 建築・操作補助（正確設置など）
- 操作
  - `X + C`：設定画面
  - 機能は手動でONにしない限り無効（初期状態ではすべてOFF）

### TweakerMore

- Tweakerooの追加・拡張設定
- 操作
  - Tweakeroo設定画面から一緒に管理

---

## 🗺️ ナビゲーション・表示系

### Xaero’s Minimap

- 画面左上にミニマップ表示
- 操作
  - `Y`：設定画面が開く
  - `B`：Waypoint追加

### Xaero’s World Map

- フルスクリーンの全体マップ
- 操作
  - `M`：ワールドマップ表示

### XaeroZoomout

- マップのズームアウト強化
- 操作
  - マップ表示中にスクロール

### Map Link

- ミニマップとワールドマップの情報連携
- 操作：なし（自動）

---

## 🎨 見た目・便利拡張系

### Iris

- シェーダー対応MOD（OptiFine代替）
- 操作
  - `ビデオ設定 → シェーダー`
  - `O`：背景が透明なシェーダーパックメニューが開く
  - `K`：シェーダーのオンとオフが切り替わる
  - `R`：現在アクティブなシェーダーパックがリロードされる
  - これらのショートカットキーは、操作設定のキー割り当てから変更可能
- ※ シェーダーを使わなければ軽い

#### シェーダー

### Capes

- プレイヤーにケープを表示
- 操作
  - Mod MenuからON/OFF（対応サーバーのみ）

### Zoomify

- ズーム機能追加
- 操作
  - `C`（デフォルト・変更可）

### No Chat Reports

- チャット報告機能を無効化
- 操作：なし

## その他

### Minescript

- Pythonが使えるクライアントMod

### Continuity

- ガラスやブロックの見た目を自然につなげる描画改善
- 操作：なし

### Simple Voice Chat

- 操作
  - `V`：ボイスチャットメニューを開く
  - `M`：ミュート/ミュート解除を切り替える
  - ※ゲームのキー設定で変更も可能。

### Advancement Info

- 進捗を分かりやすくする