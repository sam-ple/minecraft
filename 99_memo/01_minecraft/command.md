# Minecraft コマンド (Java)

## 0. セレクター

- @p  
  - 最も近いプレイヤー
- @r  
  - ランダムのプレイヤー
- @a  
  - 全プレイヤー
- @s  
  - コマンド実行者
- @e  
  - 全エンティティ
- @e[type=Zombie]  
  - ゾンビだけ
- @e[tag=example]  
  - タグ付き
- @e[distance=..10]  
  - 半径10以内
- @e[sort=nearest,limit=1]  
  - 近い1体だけ
- @a[scores={targetPoints=1..}]  
  - スコアボード条件付き
- @p[name=Steve]  
  - 特定プレイヤー
- @e[limit=1,sort=furthest]  
  - 遠い1体だけ
- @a[tag=team_red]  
  - タグ付きチームプレイヤーだけ
- @e[type=item]  
  - 落ちているアイテムを操作

---

## 1. 基本コマンド

- /help [command]  
  - コマンドのヘルプを表示
- /give <player> <item> [count] [nbt]  
  - プレイヤーにアイテムを与える
- /tp <target> <destination>  
  - プレイヤーやエンティティをテレポート
- /teleport <target> <destination>  
  - /tp の別名
- /gamemode <mode> [player]  
  - ゲームモードを変更（サバイバル、クリエイティブ、アドベンチャー、スペクテイター）
- /effect <give|clear> <player> <effect> [seconds] [amplifier] [hideParticles]  
  - ステータス効果を付与・解除
- /summon <entity> [pos] [nbt]  
  - エンティティを召喚
- /kill [target]  
  - エンティティやプレイヤーを倒す
- /weather <clear|rain|thunder> [duration]  
  - 天気を変更
- /time <set|add|query> [value]  
  - 時間を操作
- /say <message>  
  - チャットメッセージを送信
- /tellraw <player> {"text":"<message>","color":"<color>"}  
  - black, dark_blue, dark_green, dark_aqua, dark_red, dark_purple, gold, gray, dark_gray, blue, green, aqua, red, light_purple, yellow, white
- /clear <player> [item] [data]  
  - プレイヤーのインベントリからアイテムを削除
- /enchant <player> <enchantment> [level]  
  - アイテムにエンチャント付与
- /item replace entity <player> <slot> with <item>  
  - 特定スロットにアイテムを直接入れる

---

## 2. 実行・条件付きコマンド

- /execute [as <entity>] [at <entity>] [store <...] <...] [if|unless <condition>] run <command>  
  - 条件やコンテキスト付きでコマンドを実行
- /execute positioned <x> <y> <z> run <command>  
  - 指定座標からコマンド実行
- /execute as <entity> run <command>  
  - エンティティ視点でコマンド実行

---

## 3. 位置・座標関連

- /locate <structure|biome> [name]  
  - 最寄りの構造物やバイオームを探す
- /setworldspawn [pos]  
  - ワールドのスポーン地点を設定
- /spawnpoint [player] [pos]  
  - プレイヤーのスポーン地点を設定

---

## 4. ブロック・環境操作

- /setblock <pos> <block> [destroy|keep|replace] [nbt]  
  - ブロックを設置
- /fill <from> <to> <block> [destroy|keep|replace|...] [nbt]  
  - 範囲内をブロックで埋める
- /clone <begin> <end> <destination> [maskMode] [cloneMode] [tileName]  
  - 範囲内のブロックをコピー
- /destroy <pos>  
  - 指定ブロックを破壊
- /setblock <pos> minecraft:air  
  - ブロック削除用

---

## 5. プレイヤー管理

- /ban <target> [reason]  
  - プレイヤーをBAN
- /pardon <target>  
  - BANを解除
- /op <player>  
  - オペレーター権限を付与
- /deop <player>  
  - オペレーター権限を剥奪
- /kick <player> [reason]  
  - プレイヤーをサーバーから追放
- /team add <team>  
  - チーム作成
- /team join <team> <player>  
  - チームにプレイヤーを追加
- /team remove <team>
- /team empty <team>
- /team list

---

## 6. ゲームルール

- /gamerule <ruleName> [value]  
  - ゲームルールを設定または確認
- /gamerule sendCommandFeedback false  
  - コマンド実行時のチャット通知を非表示
- /gamerule doDaylightCycle false  
  - 時間を固定
- /gamerule doMobSpawning false  
  - Mobが自然スポーンしない
- /gamerule doTileDrops false  
  - ブロック破壊時のドロップ停止
- /gamerule doFireTick false  
  - 火災を防ぐ
- /difficulty <peaceful|easy|normal|hard>  
  - 難易度を設定

---

## 7. エンティティデータ

- /data get|merge|remove <target> [path]  
  - エンティティやブロックのNBTデータを操作

---

## 8. スコアボード・ボスバー管理

### スコアボード

- /scoreboard objectives add <name> <type> [displayName]  
  - 新しいスコアボードを作成
- /scoreboard objectives remove <name>  
  - スコアボード削除
- /scoreboard objectives setdisplay <slot> <objective>  
  - スコアボードの表示位置を設定
- /scoreboard objectives list
  - 作成済みスコアボードの一覧を確認
- /scoreboard players reset <player> [objective]
  - プレイヤーのスコアをリセット
- /scoreboard players enable <player> <objective>
  - 反復トリガー用
- /scoreboard players disable <player> <objective>
  - trigger の使用を無効化
- /scoreboard players set <player> <objective> <value>  
  - プレイヤーのスコア設定
- /scoreboard players add <player> <objective> <value>  
  - スコア加算
- /scoreboard players list <player>  
  - プレイヤーのスコア一覧

### ボスバー

- /bossbar add <id> <name>  
  - ボスバー作成
- /bossbar set <id> value <数値>  
  - ボスバー進捗設定
- /bossbar set <id> max <数値>
  - ボスバーの最大値を設定
- /bossbar remove <id>  
  - ボスバー削除
- /bossbar set <id> players @a  
  - 表示対象プレイヤー設定
- /bossbar list
  - ボスバーの一覧を表示
- /bossbar set <id> name <text>
  - ボスバー名を動的に変更可能
- /bossbar set <id> color <color>
  - ボスバーの色を変更（red / green / blue / yellow / purple / white）
- /bossbar set <id> style <style>
  - バーのスタイル（progress / notched_6 / notched_10 / notched_12 / notched_20）

---

## 9. その他

- /title <player> <title|subtitle|actionbar|clear|reset> [text|times]  
  - タイトルを表示
- /playsound <sound> <source> <targets> [pos] [volume] [pitch] [minimumVolume]  
  - 音を再生
- /particle <name> [pos] [delta] [speed] [count] [force|normal] [player]  
  - パーティクルを生成
- /advancement <grant|revoke> <player> <advancement>  
  - 実績（アドバンスメント）を管理
- /function <name>  
  - コマンド関数を実行
- /loot  
  - 戦利品テーブルを操作

