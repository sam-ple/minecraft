## モブの色違い（Color Variants）

| モブ名 | 英語名 | コマンドID | 色違いの特徴 |
|---|---|---|---|
| 羊 | Sheep | `minecraft:sheep` | 羊は様々な色の毛を持つことができる。`/summon minecraft:sheep ~ ~ ~ {Color:15}`で色を指定。 |
| 馬 | Horse | `minecraft:horse` | 馬には複数の色（茶色、黒、白、斑点など）が存在。`/summon minecraft:horse ~ ~ ~ {Variant:0}`で指定。 |
| ウーパールーパー | Axolotl | `minecraft:axolotl` | ウーパールーパーは複数の色（ピンク、黄色、青など）がある。`/summon minecraft:axolotl ~ ~ ~ {Variant:0}`で色を指定。 |
| パンダ | Panda | `minecraft:panda` | パンダの模様はランダムで決まる。`/summon minecraft:panda ~ ~ ~ {MainGene:0,HiddenGene:0}`で遺伝子を指定。 |
| ロバ | Donkey | `minecraft:donkey` | ロバにもいくつかの色のバリエーション（灰色、白など）がある。 |

- ニワトリ
- 牛
- 豚

## 向き

| ブロック名 | コマンドID | 設置向きのオプション（書き方例） | 説明 |
|---|---|---|---|
| オークのドア | `minecraft:oak_door` | `/setblock ~ ~ ~ minecraft:oak_door[facing=north]` | ドアを北向きに設置。 |

## 🎯 ドロッパー（Dropper）の向き

### 向き指定の例

| 向き | facing値 | コマンド例 |
|------|----------|------------|
| 上（上向きに発射） | `up` | `/setblock ~ ~ ~ minecraft:dropper[facing=up]` |
| 下（下向きに発射） | `down` | `/setblock ~ ~ ~ minecraft:dropper[facing=down]` |
| 北 | `north` | `/setblock ~ ~ ~ minecraft:dropper[facing=north]` |
| 南 | `south` | `/setblock ~ ~ ~ minecraft:dropper[facing=south]` |
| 西 | `west` | `/setblock ~ ~ ~ minecraft:dropper[facing=west]` |
| 東 | `east` | `/setblock ~ ~ ~ minecraft:dropper[facing=east]` |

※ **ディスペンサー（dispenser）** も同様に `facing` プロパティで向き指定できます。

## 🔌 レッドストーン関連の向き付きブロック例

### ✅ 1. ピストン（piston / sticky_piston）

```mcfunction
/setblock ~ ~ ~ minecraft:sticky_piston[facing=up]
```

### ✅ 2. オブザーバー（observer）

```mcfunction
/setblock ~ ~ ~ minecraft:observer[facing=south]
```

- オブザーバーは「**観察する方向**＝face方向」にブロックの変化を感知します。

### ✅ 3. リピーター（repeater）

```mcfunction
/setblock ~ ~ ~ minecraft:repeater[facing=north, delay=3]
```

- `delay` で信号遅延のティック数（1〜4）も指定可能。

## 🪜 階段ブロックの設置向きまとめ（`minecraft:oak_stairs` など）

### `facing`（向き）+ `half`（位置）の組み合わせ一覧

| 向き | `facing` | 下付き階段（`half=bottom`） | 上付き階段（`half=top`） |
|------|----------|------------------------------|---------------------------|
| 南向き | `south` | `/setblock ~ ~ ~ minecraft:oak_stairs[facing=south,half=bottom]` | `/setblock ~ ~ ~ minecraft:oak_stairs[facing=south,half=top]` |
| 北向き | `north` | `/setblock ~ ~ ~ minecraft:oak_stairs[facing=north,half=bottom]` | `/setblock ~ ~ ~ minecraft:oak_stairs[facing=north,half=top]` |
| 東向き | `east` | `/setblock ~ ~ ~ minecraft:oak_stairs[facing=east,half=bottom]` | `/setblock ~ ~ ~ minecraft:oak_stairs[facing=east,half=top]` |
| 西向き | `west` | `/setblock ~ ~ ~ minecraft:oak_stairs[facing=west,half=bottom]` | `/setblock ~ ~ ~ minecraft:oak_stairs[facing=west,half=top]` |

## 🔄 その他のプロパティ

- `shape`：コーナー階段の形状（自動適用 or 明示指定可）
  - `straight`, `inner_left`, `inner_right`, `outer_left`, `outer_right`
  - 例：`minecraft:oak_stairs[facing=south,half=bottom,shape=outer_left]`

## ✅ よく使うパターン

```mcfunction
/setblock ~ ~ ~ minecraft:oak_stairs[facing=east,half=top,shape=inner_right]
```

→ 東向き・上付き・内側右カーブの階段。


## 🏇 **ジョッキー（ライダー）などの特殊召喚の例**

### 1. 🐓 **チキンジョッキー**（ゾンビがニワトリに乗る）

```mcfunction
/summon minecraft:zombie ~ ~ ~ {IsBaby:1b,Passengers:[{id:"minecraft:chicken"}]}
```

- `IsBaby:1b` で子供のゾンビに。
- `Passengers` に乗るエンティティを指定することでライダーに。

---

### 2. 🐷 **クリーパーに乗ったスケルトン**（カスタムライダー）

```mcfunction
/summon minecraft:creeper ~ ~ ~ {Passengers:[{id:"minecraft:skeleton"}]}
```

- スケルトンがクリーパーに乗った「カスタムジョッキー」になります。

---

### 3. 🦴 **スケルトンホースライダー**（イベントで見かける組み合わせ）

```mcfunction
/summon minecraft:skeleton_horse ~ ~ ~ {Passengers:[{id:"minecraft:skeleton"}]}
```

※イベント時に自然発生するパターンを模倣できます。

---

### 4. 🐴 **複数段重ねのジョッキー**（マトリョーシカ召喚）

```mcfunction
/summon minecraft:chicken ~ ~ ~ {
  Passengers:[
    {
      id:"minecraft:zombie",
      IsBaby:1b,
      Passengers:[
        {
          id:"minecraft:skeleton"
        }
      ]
    }
  ]
}
```

- スケルトン → 子供ゾンビ → ニワトリ に乗っている、3重ジョッキー。

---

## 🔧 使えるカスタム要素（よく使うNBTタグ）

| タグ名 | 説明 | 例 |
|--------|------|-----|
| `CustomName` | 名前をつける | `{CustomName:'"ボスゾンビ"'}` |
| `Health` | 体力設定 | `{Health:100.0f}` |
| `ArmorItems` | 防具を装備 | `{ArmorItems:[{},{},{},{id:"minecraft:diamond_helmet",Count:1b}]}` |
| `HandItems` | 武器を持たせる | `{HandItems:[{id:"minecraft:diamond_sword",Count:1b},{}]}` |
| `NoAI:1b` | 動かないモブ | `{NoAI:1b}` |
