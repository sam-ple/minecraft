## 1. **プレイヤー関連コマンド**

### 👥 プレイヤー管理
- `/gamemode <モード> [プレイヤー]`  
  ゲームモードを変更（例：`/gamemode creative @p`）

- `/tp <ターゲット> <X> <Y> <Z>`  
  指定した座標へテレポート（例：`/tp @p 100 64 -100`）

- `/tp <ターゲット1> <ターゲット2>`  
  1人のプレイヤーを別のプレイヤーにテレポート（例：`/tp @p @a[distance=5]`）

- `/effect <ターゲット> minecraft:<効果> [秒数] [強さ]`  
  プレイヤーに効果を付与（例：`/effect @p minecraft:speed 30 1`）

- `/give <プレイヤー> <アイテム> [数]`  
  アイテムをプレイヤーに与える（例：`/give @p minecraft:diamond 64`）

- `/spawnpoint <プレイヤー> [X] [Y] [Z]`  
  プレイヤーのスポーンポイントを設定（例：`/spawnpoint @p 100 64 -100`）

- `/setworldspawn [X] [Y] [Z]`  
  ワールドのスポーン地点を設定

### 🧳 アイテム管理
- `/clear <プレイヤー> [アイテム]`  
  プレイヤーのインベントリからアイテムを削除（例：`/clear @p minecraft:stone`）

- `/give @p minecraft:music_disc_13`  
  プレイヤーに音楽ディスクを与える（例：`/give @p minecraft:music_disc_13`）

- `/replaceitem entity <プレイヤー> slot.<スロット> <アイテム>`  
  プレイヤーのインベントリ内のアイテムを置き換える

## 2. **ワールド関連コマンド**

### 🌍 ワールド管理
- `/time set <時間>`  
  時間を設定（例：`/time set day`）

- `/weather <種類>`  
  天気を変更（例：`/weather clear`）

- `/difficulty <難易度>`  
  ゲームの難易度を変更（例：`/difficulty easy`）

- `/gamerule <ルール> <値>`  
  ゲームルールを設定（例：`/gamerule keepInventory true`）

- `/summon <エンティティ> [X] [Y] [Z]`  
  エンティティ（モブやブロックなど）を召喚（例：`/summon minecraft:zombie`）

- `/setblock <X> <Y> <Z> <ブロック>`  
  座標にブロックを配置（例：`/setblock 100 64 -100 minecraft:stone`）

- `/fill <X1> <Y1> <Z1> <X2> <Y2> <Z2> <ブロック>`  
  指定範囲をブロックで埋める（例：`/fill 10 64 10 20 70 20 minecraft:stone`）

- `/clone <X1> <Y1> <Z1> <X2> <Y2> <Z2> <X> <Y> <Z>`  
  範囲を別の位置にクローン（例：`/clone 10 64 10 20 70 20 50 64 50`）

- `/worldborder set <サイズ>`  
  ワールドの境界サイズを設定（例：`/worldborder set 500`）

## 3. **エンティティ・モブ関連コマンド**

### 🧟‍♂️ モブ・エンティティ管理
- `/summon <モブ> [X] [Y] [Z]`  
  モブを召喚（例：`/summon minecraft:zombie`）

- `/kill <ターゲット>`  
  ターゲットを殺す（例：`/kill @e[type=minecraft:zombie]`）

- `/tp <ターゲット1> <ターゲット2>`  
  モブまたはプレイヤーをテレポート（例：`/tp @e[type=minecraft:sheep] @p`）

- `/scoreboard players add <プレイヤー> <スコアボード名> <スコア>`  
  スコアボードのスコアを追加（例：`/scoreboard players add @p killCount 1`）

- `/data get entity <エンティティ>`  
  エンティティのデータを表示（例：`/data get entity @e[type=zombie]`）

## 4. **コマンドブロック・レッドストーン関連**

### 🔲 コマンドブロック
- `/setblock <X> <Y> <Z> minecraft:command_block`  
  指定位置にコマンドブロックを配置（例：`/setblock 100 64 -100 minecraft:command_block`）

- `/trigger <スコアボード名>.set <値>`  
  トリガーによるアクション（例：`/trigger health.set 100`）

## 5. **特殊コマンド・その他**

### 🌍 ワールドエディット・管理
- `/locate <構造物>`  
  特定の構造物を探す（例：`/locate village`）

- `/execute <ターゲット> <X> <Y> <Z> <コマンド>`  
  指定位置またはターゲットでコマンドを実行（例：`/execute @p ~ ~ ~ /say Hello`）

- `/advancement revoke <ターゲット> from <アドバンスメント名>`  
  アドバンスメントを取り消す（例：`/advancement revoke @p from minecraft:story/root`）

- `/playsound <サウンドID> [ターゲット] [X] [Y] [Z]`  
  サウンドを再生（例：`/playsound minecraft:ambient.cave music @p`）

- `/tag <ターゲット> add <タグ>`  
  エンティティにタグを追加（例：`/tag @e add Boss`）

### 🔨 その他便利なコマンド
- `/recipe give <プレイヤー> <レシピ>`  
  特定のクラフトレシピをプレイヤーに与える（例：`/recipe give @p minecraft:diamond_sword`）

- `/ban <プレイヤー>`  
  プレイヤーをワールドからバン（例：`/ban player123`）

- `/pardon <プレイヤー>`  
  プレイヤーのバンを解除（例：`/pardon player123`）

- `/whitelist add <プレイヤー>`  
  ホワイトリストにプレイヤーを追加（例：`/whitelist add player123`）
