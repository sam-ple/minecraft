## 🎵 ブロック設置音（`/playsound` 用）

| 材質 | サウンドID | 説明 |
|------|-------------|------|
| 石系 | `block.stone.place` | 石や石レンガなど |
| 木材系 | `block.wood.place` | 原木や木材ブロック |
| 土系 | `block.grass.place` | 土、草ブロック |
| 砂系 | `block.sand.place` | 砂、赤い砂 |
| ガラス系 | `block.glass.place` | ガラス、ガラス板 |
| 金属系 | `block.metal.place` | 鉄ブロック、金ブロックなど |
| 雪系 | `block.snow.place` | 雪ブロック、雪層 |
| スライム | `block.slime.place` | スライムブロック |
| ラダー | `block.ladder.place` | はしご |
| ピストン | `block.piston.place` | ピストン、粘着ピストン | ([ALL MINECRAFT 1.9 PLAYSOUNDS FILE NAMES! - Minecraft Forum](https://www.minecraftforum.net/forums/minecraft-java-edition/recent-updates-and-snapshots/2555112-all-minecraft-1-9-playsounds-file-names?utm_source=chatgpt.com))

## 🧚 アレイ（Allay）の鳴き声

| 状態 | サウンドID | 説明 |
|------|-------------|------|
| アイテム所持中のアイドル音 | `entity.allay.idle_with_item` | アイテムを持っているときの待機音 |
| アイテム未所持のアイドル音 | `entity.allay.idle_without_item` | アイテムを持っていないときの待機音 |
| ダメージを受けたとき | `entity.allay.hurt` | ダメージを受けた際の鳴き声 |
| 死亡時 | `entity.allay.death` | 死亡時の鳴き声 | ([Category:Allay sounds - Minecraft Wiki](https://minecraft.fandom.com/wiki/Category%3AAllay_sounds?utm_source=chatgpt.com))

## 🐐 ヤギの角笛（Goat Horn）の音

| 名前 | サウンドID |
|------|-------------|
| Ponder | `item.goat_horn.sound.0` |
| Sing | `item.goat_horn.sound.1` |
| Seek | `item.goat_horn.sound.2` |
| Feel | `item.goat_horn.sound.3` |
| Admire | `item.goat_horn.sound.4` |
| Call | `item.goat_horn.sound.5` |
| Yearn | `item.goat_horn.sound.6` |
| Dream | `item.goat_horn.sound.7` | ([Goat horn sound effect name in skript - skUnity Forums](https://forums.skunity.com/threads/goat-horn-sound-effect-name-in-skript.19142/?utm_source=chatgpt.com), [ALL MINECRAFT 1.9 PLAYSOUNDS FILE NAMES! - Minecraft Forum](https://www.minecraftforum.net/forums/minecraft-java-edition/recent-updates-and-snapshots/2555112-all-minecraft-1-9-playsounds-file-names?utm_source=chatgpt.com))

## 📌 `/playsound` コマンドの使用例

```mcfunction
/playsound minecraft:block.wood.place master @p ~ ~ ~ 1 1 1
```

- `master` はサウンドカテゴリ（例：`master`、`music`、`record`、`weather`、`block`、`hostile`、`neutral`、`player`、`ambient`、`voice`）を指定。
- 最後の3つの数値は、音量、ピッチ、最小再生距離を指定。

* * *

## 🎵 **音階の仕組み**

```mcfunction
/playsound minecraft:block.note_block.harp master @p ~ ~ ~ <音量> <ピッチ>
```
- `/playsound` コマンドで「ドレミファソラシド」や半音（#）、音階（通常・低音・高音）を再現するには、主に **`note.harp`** などのサウンドと **ピッチ指定** を使用。

| 音名         | 半音番号（0〜24） | ピッチ値     | 備考     |
| ---------- | ---------- | -------- | ------ |
| ド          | 0          | 0.5      | 最低音    |
| ド♯ / レ♭    | 1          | 0.529732 | 半音上    |
| レ          | 2          | 0.561231 |        |
| レ♯ / ミ♭    | 3          | 0.594604 |        |
| ミ          | 4          | 0.629961 |        |
| ファ         | 5          | 0.667420 |        |
| ファ♯ / ソ♭   | 6          | 0.707107 |        |
| ソ          | 7          | 0.749154 |        |
| ソ♯ / ラ♭    | 8          | 0.793701 |        |
| ラ          | 9          | 0.840896 |        |
| ラ♯ / シ♭    | 10         | 0.890899 |        |
| シ          | 11         | 0.943874 |        |
| ド（1オクターブ上） | 12         | 1.0      | 標準の「ド」 |
| 〜          | ...        | ...      |        |
| 2オクターブ上    | 24         | 2.0      | 最高音    |

### 🔈 **例：実際のコマンド**

#### 🔹 通常の「ドレミファソラシド」

```mcfunction
/playsound minecraft:block.note_block.harp master @p ~ ~ ~ 1.0 1.0  # ド（中央）
/playsound minecraft:block.note_block.harp master @p ~ ~ ~ 1.0 1.122462  # レ
/playsound minecraft:block.note_block.harp master @p ~ ~ ~ 1.0 1.259921  # ミ
/playsound minecraft:block.note_block.harp master @p ~ ~ ~ 1.0 1.334840  # ファ
/playsound minecraft:block.note_block.harp master @p ~ ~ ~ 1.0 1.498307  # ソ
/playsound minecraft:block.note_block.harp master @p ~ ~ ~ 1.0 1.587401  # ラ
/playsound minecraft:block.note_block.harp master @p ~ ~ ~ 1.0 1.781797  # シ
/playsound minecraft:block.note_block.harp master @p ~ ~ ~ 1.0 2.0       # ド（上）
```

### 📉 **下の音域（低音）**

上記ピッチを **0.5〜1.0** に合わせると、1オクターブ下の音階になる。

```mcfunction
/playsound minecraft:block.note_block.harp master @p ~ ~ ~ 1.0 0.5  # 低いド
```

### 📈 **上の音域（高音）**

上記ピッチを **1.0〜2.0** に合わせると、1オクターブ上の音階になる。

```mcfunction
/playsound minecraft:block.note_block.harp master @p ~ ~ ~ 1.0 2.0  # 高いド
```

### 🎼 **楽器の種類**

| 楽器名（サウンド名）                   | 音色          |
| ---------------------------- | ----------- |
| `block.note_block.harp`      | デフォルト（ピアノ風） |
| `block.note_block.bass`      | ベース音        |
| `block.note_block.snare`     | スネアドラム      |
| `block.note_block.pling`     | シンセ風        |
| `block.note_block.xylophone` | 木琴          |
| `block.note_block.flute`     | フルート        |
| `block.note_block.bell`      | 鐘           |

- `note_block` はブロックの下に何があるかで楽器が変わる。
