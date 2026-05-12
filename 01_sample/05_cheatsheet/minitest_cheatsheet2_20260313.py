import minescript as m
import time

# ==================================================
#
#
# MineScript Command Sheet 2 (Draft)
#
#
# ==================================================


# ==================================================
#
# EXECUTE
#
# ==================================================

# while True:
#     m.execute("execute as @a at @s if block ~ ~-1 ~ minecraft:gold_block run summon minecraft:skeleton ^ ^ ^2")
#     time.sleep(1)


# ==================================================
# PLAYER INVENTORY　プレイヤー所持品検知
# ==================================================

# インベントリ全体を検索
# snowball を持っているプレイヤー
# while True:
#     m.execute('execute as @a if entity @s[nbt={Inventory:[{id:"minecraft:snowball"}]}] run say I have a snowball!')
#     time.sleep(1)

# m.execute("\\killlog -1")

# 手に持っているアイテムのみ検索
# メインハンドの snowball
# while True:
#     m.execute('execute as @a if entity @s[nbt={SelectedItem:{id:"minecraft:snowball"}}] run say holding snowball!')
#     time.sleep(1)

# ==================================================
# ARMOR STAND　攻撃検知
# ==================================================

# アーマースタンド召喚（攻撃検知用）
# m.execute('summon minecraft:armor_stand ~ ~ ~ {ShowArms:1b,Tags:["attack_test"]}')

# アーマースタンド攻撃検知
# while True:
#     m.execute('execute as @e[type=minecraft:armor_stand,tag=attack_test] on attacker run say attacked!')
#     time.sleep(1)

# アーマースタンド削除
# m.execute('kill @e[type=minecraft:armor_stand,tag=attack_test]')

# ==================================================
# ARMOR STAND　タグ指定攻撃検知
# ==================================================

# player1タグ付きアーマースタンド召喚
# m.execute('summon minecraft:armor_stand ~ ~ ~ {ShowArms:1b,Tags:["player1"]}')

# player1タグだけ攻撃検知
# while True:
#     m.execute('execute as @e[type=minecraft:armor_stand,tag=player1] on attacker run say attacked!')
#     time.sleep(1)

# player1タグアーマースタンド削除
# m.execute('kill @e[type=minecraft:armor_stand,tag=player1]')

# ==================================================
# INTERACTION ENTITY　クリック検知
# ==================================================

# # interaction entity 召喚 （クリック検知用）F3+Bで当たり判定表示
# m.execute('summon minecraft:interaction ~ ~ ~ {width:1f,height:1f,Tags:["click_test"]}')

# while True:
#     # 右クリック検知
#     m.execute('execute as @e[type=minecraft:interaction,tag=click_test] on target run say clicked!')
    
#     # 左クリック検知
#     m.execute('execute as @e[type=minecraft:interaction,tag=click_test] on attacker run say attacked!')
    
#     # リセット
#     m.execute('data remove entity @e[type=minecraft:interaction,tag=click_test] interaction')
    
#     time.sleep(0.1)

# interaction entity 削除
# m.execute("kill @e[type=minecraft:interaction,tag=click_test]")

# ==================================================
# ADVANCEMENT DETECT　進捗検知
# ==================================================

# Cake レシピ開放検知
# 条件：milk bucket / sugar / wheat / egg を初取得
# m.execute('execute as @a[advancements={minecraft:recipes/food/cake=true}] run say cake recipe unlocked!')

# レシピ検知リセット
# m.execute('advancement revoke @a only minecraft:recipes/food/cake')

# ダイヤ進捗検知
# while True:
#     m.execute('execute as @a[advancements={minecraft:story/mine_diamond=true}] run say diamond!')
#     time.sleep(1)

# ダイヤ進捗リセット
# m.execute('advancement revoke @a only minecraft:story/mine_diamond')


# ==================================================
#
# SCOREBOARD
#
# ==================================================

# ==================================================
# SCOREBOARD　CRAFT DETECT　クラフト検知
# ==================================================

# Cake クラフト検知用スコア作成
# m.execute('scoreboard objectives add craft_cake minecraft.crafted:minecraft.cake')
# m.execute('scoreboard objectives setdisplay sidebar craft_cake')

# Cake クラフト検知
# while True:
#     m.execute('execute as @a[scores={craft_cake=1..}] run say cake crafted!')
#     m.execute('scoreboard players set @a craft_cake 0')
#     time.sleep(1)

# クラフトカウントリセット
# m.execute('scoreboard players set @a craft_cake 0')

# scoreboard 削除
# m.execute('scoreboard objectives remove craft_cake')

# scoreboard 値リセット
# m.execute('scoreboard players reset @a craft_cake')


# ==================================================
# SCOREBOARD　MINING DETECT　採掘検知
# ==================================================

# スコア作成
# m.execute("scoreboard objectives add mine_diamond minecraft.mined:minecraft.diamond_ore")
# m.execute("scoreboard objectives setdisplay sidebar mine_diamond")

# ダイヤ採掘検知
# while True:
#     m.execute("execute as @a[scores={mine_diamond=1..}] run say mined diamond!")
#     m.execute("scoreboard players set @a mine_diamond 0")
#     time.sleep(1)

# リセット
# m.execute("scoreboard players set @a mine_diamond 0")

# 削除
# m.execute("scoreboard objectives remove mine_diamond")


# ==================================================
# SCOREBOARD　ITEM USE DETECT　右クリック検知
# ==================================================

# スコア作成
# m.execute("scoreboard objectives add use_stick minecraft.used:minecraft.stick")
# m.execute("scoreboard objectives setdisplay sidebar use_stick")

# 棒右クリック検知
# while True:
#     m.execute("execute as @a[scores={use_stick=1..}] run say used stick!")
#     m.execute("scoreboard players set @a use_stick 0")
#     time.sleep(1)

# リセット
# m.execute("scoreboard players set @a use_stick 0")

# 削除
# m.execute("scoreboard objectives remove use_stick")


# ==================================================
# SCOREBOARD　COMBAT DETECT　攻撃検知
# ==================================================

# スコア作成
# m.execute("scoreboard objectives add damage minecraft.damage_dealt")
# m.execute("scoreboard objectives setdisplay sidebar damage")

# 攻撃ダメージ検知
# while True:
#     m.execute("execute as @a[scores={damage=1..}] run say attacked!")
#     m.execute("scoreboard players set @a damage 0")
#     time.sleep(1)

# リセット
# m.execute("scoreboard players set @a damage 0")

# 削除
# m.execute("scoreboard objectives remove damage")


# ==================================================
# SCOREBOARD　PLAYER ACTION DETECT　プレイヤー行動
# ==================================================

# スコア作成
# m.execute("scoreboard objectives add sneak_time minecraft.custom:minecraft.sneak_time")
# m.execute("scoreboard objectives setdisplay sidebar sneak_time")

# スニーク検知
# while True:
#     m.execute("execute as @a[scores={sneak_time=1..}] run say sneaking!")
#     m.execute("scoreboard players set @a sneak_time 0")
#     time.sleep(1)

# リセット
# m.execute("scoreboard players set @a sneak_time 0")

# 削除
# m.execute("scoreboard objectives remove sneak_time")


# スコア作成
# m.execute("scoreboard objectives add jump minecraft.custom:minecraft.jump")
# m.execute("scoreboard objectives setdisplay sidebar jump")

# ジャンプ検知
# while True:
#     m.execute("scoreboard players set @a jump 0")
#     time.sleep(1)

# リセット
# m.execute("scoreboard players set @a jump 0")

# 削除
# m.execute("scoreboard objectives remove jump")


# ==================================================
# SCOREBOARD　BLOCK PLACE DETECT　ブロック設置
# ==================================================

# スコア作成
# m.execute("scoreboard objectives add place_stone minecraft.used:minecraft.stone")
# m.execute("scoreboard objectives setdisplay sidebar place_stone")

# 石設置検知
# while True:
#     m.execute("scoreboard players set @a place_stone 0")
#     time.sleep(1)

# リセット
# m.execute("scoreboard players set @a place_stone 0")

# 削除
# m.execute("scoreboard objectives remove place_stone")
