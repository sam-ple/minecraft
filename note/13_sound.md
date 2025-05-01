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
