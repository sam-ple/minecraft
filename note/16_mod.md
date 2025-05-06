# MOD

## ✅ 【MODローダー比較】Forge / NeoForge / Fabric

| 特徴          | Forge                         | NeoForge                  | Fabric                         |
| ----------- | ----------------------------- | ------------------------- | ------------------------------ |
| 開発開始        | 2011年                         | 2023年（Forgeからの派生）         | 2018年                          |
| 互換性         | MOD数最多（安定）                    | Forgeの改良版。MOD数はこれから。      | 軽量で高速。Mod数も増加中。                |
| パフォーマンス     | やや重め                          | Forgeより軽量化・並列処理など改善       | 非常に軽量、高速起動                     |
| 独自機能        | 多くのMODがForge前提で作られている         | LoomやGradleの改善、Mod構築のしやすさ | クリーンなAPI、頻繁な更新、Snapshot対応が早い   |
| Modding API | Forge独自API                    | 改良版Forge API              | Fabric API（別途導入）               |
| メイン対象       | 安定重視・大型Mod（例：IndustrialCraft） | 新しいForge代替として注目           | 軽量・小規模～中規模Mod、Snapshot対応Mod開発者 |

> NeoForgeは、Forge開発者と意見が割れた一部の開発者が2023年に立ち上げた新プロジェクトです。Forgeと互換性はありませんが、同様の仕組みでよりモダンな作りを目指しています。

---

## 🧰 【Fabricで入れておくと便利なMOD】

Fabricは軽量ですが、そのままだとForgeにある便利機能が不足しています。以下のModはFabric導入環境でよく使われる定番Mod。

### 🔧 基本環境・依存MOD

| MOD名                 | 概要                                     |
| -------------------- | -------------------------------------- |
| **Fabric API**       | Fabric用Modの共通ライブラリ。必須。                 |
| **Mod Menu**         | インゲームで導入Modの一覧や詳細を確認できるGUI。Fabricでは定番。 |
| **Cloth Config API** | Modの設定画面用のAPI。多くのModが依存。               |
| **Architectury API** | Fabric・Forge両対応ModのためのAPI。依存Modあり。     |

### 🖥 UI / メニュー拡張系

| MOD名                          | 概要                          |
| ----------------------------- | --------------------------- |
| **Sodium**                    | パフォーマンス向上系。OptiFine代替として人気。 |
| **Iris**                      | Sodiumと組み合わせ可能なシェーダーMod。    |
| **REI（Roughly Enough Items）** | アイテム一覧とレシピ表示。JEIのFabric版。   |
| **Inventory Profiles Next**   | インベントリ整理、並び替えなど便利操作。        |
| **Continuity**                | 隣接テクスチャ表示（ガラスがつながるなど）を改善。   |
| **BetterF3**                  | F3画面をカスタマイズ可能にするMod。        |

### 🧪 開発者・便利機能

| MOD名                     | 概要                              |
| ------------------------ | ------------------------------- |
| **MiniHUD**              | F3より詳しい情報を画面にオーバーレイ表示（ブロック情報など） |
| **WorldEdit for Fabric** | 建築補助。範囲選択してコマンドで操作。             |
| **Debugify**             | バグ修正Mod。バニラの既知バグにパッチを当てる。       |

---

## 🔄 Fabric使用時の注意点

* **OptiFine** はFabricと非互換。代わりに **Sodium + Iris + EntityCulling** を使うと快適。
* FabricとForgeのMODは**互換性がありません**（同時には使えない）。
* **Quilt**というFabricの後継的ローダーも存在しますが、現時点ではFabricの方がMod数は多い。

---

必要であれば、Mod Menuなどの導入方法（導入手順やダウンロードURL）もお手伝いします。
特定のジャンル（建築補助、UI改善、技術系）でおすすめModを知りたいですか？
