import minescript as m

# ==================================================
#
#
# MineScript Command Sheet (Draft)
#
#
# ==================================================

# ==================================================
# ITEM GIVE　アイテム付与
# ==================================================

# ダイヤピッケル
# 効率V + 幸運III
# m.execute('give @p diamond_pickaxe[enchantments={"minecraft:efficiency":5,"minecraft:fortune":3}] 1')


# m.execute('give @p minecraft:fishing_rod[enchantments={"minecraft:luck_of_the_sea":3,"minecraft:lure":3,"minecraft:unbreaking":3,"minecraft:mending":1}] 1')
# m.execute('give @p minecraft:fishing_rod[enchantments={"minecraft:luck_of_the_sea":3,"minecraft:lure":3,"minecraft:unbreaking":3,"minecraft:mending":1},custom_name=\'{"text":"最強の釣り竿"}\'] 1')

# ==================================================
# CAKE MATERIALS　ケーキ材料
# ==================================================

# Cake 材料
# m.execute("give @a milk_bucket 3")
# m.execute("give @a sugar 2")
# m.execute("give @a egg 1")
# m.execute("give @a wheat 3")


# ==================================================
# 
# DISPLAY / BLOCK
#
# ==================================================

# ==================================================
# 文字入り看板
# ==================================================

# 2行目に「テスト」を表示
# m.execute('setblock ~ ~ ~ minecraft:pale_oak_sign{front_text:{messages:["","テスト","",""],color:"black",has_glowing_text:0b}}')

# 看板削除
# 半径5ブロック以内の pale_oak_sign を air に置き換え
# m.execute('fill ~-5 ~-5 ~-5 ~5 ~5 ~5 air replace minecraft:pale_oak_sign')

# ==================================================
# フル装備＋腕ありアーマースタンド
# ==================================================

# m.execute('summon minecraft:armor_stand ~ ~ ~ {ShowArms:true,equipment:{head:{id:"player_head",Count:1,components:{profile:{name:"crocadooo"}}},chest:{id:"netherite_chestplate",Count:1},legs:{id:"netherite_leggings",Count:1},feet:{id:"netherite_boots",Count:1}}}')

# アーマースタンド削除
# 半径5ブロック以内の armor_stand を削除
# m.execute('kill @e[type=minecraft:armor_stand,distance=..5]')

# ==================================================
# プレイヤーヘッド
# ==================================================

# crocadooo のスキン
# m.execute('setblock ~ ~ ~ minecraft:player_head[rotation=0]{profile:"crocadooo"}')

# プレイヤーヘッド削除
# 半径5ブロック以内の player_head を air に置き換え
# m.execute('fill ~-5 ~-5 ~-5 ~5 ~5 ~5 air replace minecraft:player_head')

# ==================================================
# プレイヤーヘッド（巨大表示）
# ==================================================

# item_display を使用
# m.execute('summon minecraft:item_display ~ ~ ~ {item:{id:"minecraft:player_head",Count:1b,components:{"minecraft:profile":{name:"crocadooo"}}},billboard:"fixed",transformation:{scale:[6f,6f,1f]},Tags:["big_player_head"]}')

# 巨大プレイヤーヘッド削除（item_display）
# big_player_head タグ付きのみ削除
# m.execute('kill @e[type=minecraft:item_display,tag=big_player_head,distance=..5]')

# ==================================================
#
# ENTITY
# 
# ==================================================


# ==================================================
# 弱いスケルトン
# ==================================================

# Skeleton (north)
# 座標: x+1 z-5
#
# NoAI → 動かない
# PersistenceRequired → 消えない
# Health:2 → ワンパン調整

# m.execute("summon minecraft:skeleton ~1 ~ ~-5 {NoAI:1b,PersistenceRequired:1b,Health:2f}")


# ==================================================
# 商品指定の村人
# ==================================================
# https://minecraft-blog.net/summon-villager-command-generator/

# 村人
# スノーボール販売
# 1エメラルド → 1スノーボール
#
# Silent → 声なし
# Invulnerable → 無敵
# NoAI → 動かない

# m.execute('/summon villager ~-1 ~ ~-5 {"VillagerData":{"level":5,"profession":"farmer","type":"plains"},"Silent":true,"Invulnerable":true,"NoAI":true,"Offers":{"Recipes":[{"buy":{"id":"emerald","count":1},"sell":{"id":"snowball","count":1},"maxUses":9999}]}}')


# ==================================================
#
# Rule
# 
# ==================================================


# ==================================================
# WORLD SETTINGS　ワールド設定
# ==================================================

# 難易度をピースフルに
# m.execute("difficulty peaceful")

# 難易度をノーマル
# m.execute("difficulty normal")


# ==================================================
# GAMEMODE　ゲームモード
# ==================================================

# アドベンチャーモード
# m.execute("gamemode adventure")

# クリエイティブ
# m.execute("gamemode creative")


# ==================================================
# TIME / WEATHER　時間・天候
# ==================================================

# 時間を昼
# m.execute("time set day")

# 夜
# m.execute("time set night")

# 天気を晴れ
# m.execute("weather clear")

# 雨
# m.execute("weather rain")

# 雷
# m.execute("weather thunder")


# ==================================================
# GAMERULE　ゲームルール設定
# ==================================================

# Mobが自然スポーンしなくなる
# m.execute("gamerule doMobSpawning false")

# Mobがアイテムをドロップしなくなる
# m.execute("gamerule doMobLoot false")

# ブロック破壊時のドロップを停止
# m.execute("gamerule doTileDrops false")

# 火の延焼を無効化
# m.execute("gamerule doFireTick false")

# 昼夜サイクル停止
# m.execute("gamerule doDaylightCycle false")

# 天候変化停止
# m.execute("gamerule doWeatherCycle false")

# コマンド実行ログをチャットに出さない
# m.execute("gamerule sendCommandFeedback false")
# 1.21.11
# m.execute("gamerule send_command_feedback false") 

# プレイヤー死亡メッセージを非表示
# m.execute("gamerule showDeathMessages false")

# 水中ダメージ無効
# m.execute("gamerule drowningDamage false")

# 落下ダメージ無効
# m.execute("gamerule fallDamage false")

# 火ダメージ無効
# m.execute("gamerule fireDamage false")

# インベントリ保持
# m.execute("gamerule keepInventory true")

# 即時リスポーン
# m.execute("gamerule doImmediateRespawn true")


# ==================================================
# CLEANUP　ワールドのエンティティ整理
# ==================================================

# プレイヤー以外のエンティティ削除
# Mob / Item / ArmorStand 等すべて消える
# m.execute("kill @e[type=!minecraft:player]")
# kill @e[type=!minecraft:player,distance=..50]

# 落ちているアイテム全削除
# m.execute("kill @e[type==minecraft:item]")
# kill @e[type=minecraft:item,distance=..20]

# 村人だけ削除
# m.execute("kill @e[type=minecraft:villager]")


# ==================================================
# PLAYER EFFECT　プレイヤー能力
# ==================================================

# 暗視
# m.execute("effect give @a night_vision infinite 255 true")

# 最大体力2倍
# m.execute("attribute @a minecraft:generic.max_health base set 40")

# 回復
# m.execute("effect give @a minecraft:instant_health 1 10 true")

# 空腹回復
# m.execute("effect give @a saturation 1 10 true")

# ==================================================
# DEBUG　デバッグ
# ==================================================

# 全プレイヤーの座標表示
# m.execute("data get entity @p Pos")

# import time
# while True:
#     m.execute('effect give @a minecraft:night_vision 5 0 true')
#     time.sleep(3)

# スコアボード一覧
# m.execute("scoreboard objectives list")

# ボスバー一覧
# m.execute("bossbar list")
