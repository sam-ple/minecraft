import minescript as m
import math
import time

# ==================================================
# 基本設定
# ==================================================

def cmd(c):
    m.execute(c)

p = m.player()
px, py, pz = p.position

x = math.floor(px)
y = math.floor(py)
z = math.floor(pz)

# 相対座標 → 絶対座標変換
def pos(dx=0, dy=0, dz=0):
    return f"{x+dx} {y+dy} {z+dz}"

# ==================================================
# 初期設定
# ==================================================

cmd("gamerule spawnMonsters false")
cmd("difficulty easy")
cmd("time set night")
cmd("clear @a")

cmd("tp @p ~ ~ ~ 180 0") #north

# ==================================================
# 床整地
# ==================================================

cmd(f"fill {pos(-25,-1,-25)} {pos(25,-1,25)} minecraft:grass_block")

# 空間クリア（まとめて1発でOK）
cmd(f"fill {pos(-25,0,-25)} {pos(25,9,25)} minecraft:air")
cmd(f"fill {pos(-25,10,-25)} {pos(25,20,25)} minecraft:air")

# ==================================================
# 上段エンティティ（Z -5 ライン）
# ==================================================

ROT = "[0f,0f]"

HEAD_NAME = "crocadooo"

# アーマースタンド（鉄装備）
cmd((f'/summon minecraft:armor_stand {pos(-14,0,-5)} '
     f'{{ShowArms:true,NoGravity:true,PersistenceRequired:true,'
     f'equipment:{{'
    #  f'weapon.mainhand:{{id:"iron_hoe",Count:1}},'
     f'head:{{id:"player_head",Count:1,components:{{profile:{{name:"{HEAD_NAME}"}}}}}},'
     f'chest:{{id:"iron_chestplate",Count:1}},'
     f'legs:{{id:"iron_leggings",Count:1}},'
     f'feet:{{id:"iron_boots",Count:1}}'
     f'}}}}'))

# アーマースタンド（ダイヤ装備）
cmd((f'/summon minecraft:armor_stand {pos(-13,0,-5)} '
     f'{{ShowArms:true,NoGravity:true,PersistenceRequired:true,'
     f'equipment:{{'
    #  f'weapon.mainhand:{{id:"diamond_hoe",Count:1}},'
     f'head:{{id:"wither_skeleton_skull",Count:1}},'
     f'chest:{{id:"diamond_chestplate",Count:1}},'
     f'legs:{{id:"diamond_leggings",Count:1}},'
     f'feet:{{id:"diamond_boots",Count:1}}'
     f'}}}}'))

# アーマースタンド（ネザライト装備）
cmd((f'/summon minecraft:armor_stand {pos(-12,0,-5)} '
     f'{{ShowArms:1b,NoGravity:1b,PersistenceRequired:1b,'
     f'equipment:{{'
    #  f'weapon.mainhand:{{id:"minecraft:netherite_pickaxe",Count:1}},'
     f'head:{{id:"minecraft:netherite_helmet",Count:1}},'
     f'chest:{{id:"minecraft:netherite_chestplate",Count:1}},'
     f'legs:{{id:"minecraft:netherite_leggings",Count:1}},'
     f'feet:{{id:"minecraft:netherite_boots",Count:1}}'
     f'}}}}'))


# ------------------------------
# 模様入り本棚
cmd(f"setblock {pos(-10,0,-5)} minecraft:chiseled_bookshelf")

# ------------------------------
# エンチャントテーブル
cmd(f"setblock {pos(-9,0,-5)} minecraft:enchanting_table")

# ------------------------------
# 醸造台
cmd(f"setblock {pos(-8,0,-5)} minecraft:brewing_stand")

# ------------------------------
# 溶鉱炉
cmd(f"setblock {pos(-7,0,-5)} minecraft:blast_furnace[facing=south]")

# ------------------------------
# ダブルチェスト
# 左
cmd(f"setblock {pos(-6,0,-5)} minecraft:chest[facing=south,type=right]")
# 右
cmd(f"setblock {pos(-5,0,-5)} minecraft:chest[facing=south,type=left]")

# 中身投入（左側にまとめて入れると両方に反映される）
cmd((f'/data merge block {pos(-6,0,-5)} '
     f'{{Items:['

     # 基本素材
     f'{{Slot:0b,id:"minecraft:cobblestone",Count:64b}},'
     f'{{Slot:1b,id:"minecraft:iron_ingot",Count:64b}},'

     # ツール・装備
     f'{{Slot:2b,id:"minecraft:stone_pickaxe",Count:1b}},'
     f'{{Slot:3b,id:"minecraft:shield",Count:1b}},'
     f'{{Slot:4b,id:"minecraft:bow",Count:1b}},'
     f'{{Slot:5b,id:"minecraft:arrow",Count:64b}},'
     f'{{Slot:6b,id:"minecraft:trident",Count:1b}},'

     # ブロック系
     f'{{Slot:7b,id:"minecraft:obsidian",Count:64b}},'
     f'{{Slot:8b,id:"minecraft:crying_obsidian",Count:64b}},'

     # レア系
     f'{{Slot:9b,id:"minecraft:diamond",Count:64b}},'
     f'{{Slot:10b,id:"minecraft:dried_ghast",Count:1b}},'
     f'{{Slot:11b,id:"minecraft:sniffer_egg",Count:1b}},'
     f'{{Slot:12b,id:"minecraft:wheat_seeds",Count:64b}},'
     f'{{Slot:13b,id:"minecraft:blaze_rod",Count:64b}},'
     f'{{Slot:14b,id:"minecraft:dragon_egg",Count:1b}},'
     f'{{Slot:15b,id:"minecraft:dragon_breath",Count:64b}},'
     f'{{Slot:16b,id:"minecraft:elytra",Count:1b}},'
     f'{{Slot:17b,id:"minecraft:pumpkin",Count:64b}}'

     f']}}'))

# ------------------------------
# ベッド
cmd(f"setblock {pos(-4,0,-5)} minecraft:red_bed[facing=south,part=foot]")
cmd(f"setblock {pos(-4,0,-4)} minecraft:red_bed[facing=south,part=head]")

# ------------------------------
# 村人
cmd((f"""
summon villager {pos(-3,0,-5)} {{
 VillagerData:{{level:5,profession:"farmer",type:"plains"}},
 Silent:1b,Invulnerable:1b,NoAI:1b,
 Offers:{{Recipes:[
  {{buy:{{id:"emerald",count:1}},sell:{{id:"snowball",count:1}},maxUses:9999}}
 ]}}
}}
""").replace("\n",""))

# ------------------------------
# スケルトン
cmd(f"summon minecraft:skeleton {pos(-2,0,-5)} {{NoAI:1b,PersistenceRequired:1b,Health:2f,Rotation:{ROT}}}")

# ------------------------------
# 看板
cmd(f'setblock {pos(-1,0,-5)} minecraft:oak_sign[rotation=0]{{front_text:{{messages:["","crocadooo","",""]}}}}')

# ------------------------------
# 作業台
cmd(f"setblock {pos(0,0,-5)} minecraft:crafting_table")

# ------------------------------
# 動物
cmd(f"summon minecraft:parrot {pos(1,0,-5)} {{NoAI:1b,Silent:1b,Rotation:{ROT}}}")
cmd(f"summon minecraft:armadillo {pos(2,0,-5)} {{NoAI:1b,Silent:1b,Rotation:{ROT}}}")
cmd(f"summon minecraft:allay {pos(3,0,-5)} "
    f'{{Silent:1b,NoGravity:1b,PersistenceRequired:1b}}')

# ------------------------------
# 金ブロックを踏んだら怪しげな砂が出る仕掛け
cmd(f"setblock {pos(10,-1,-5)} minecraft:gold_block")
cmd((f'setblock {pos(10,-2,-5)} minecraft:repeating_command_block'
     f'{{auto:1b,Command:"execute as @a at @s if block ~ ~-1 ~ minecraft:gold_block run setblock {pos(10,0,-7)} minecraft:suspicious_sand"}}'))

# ------------------------------
# TP装置

# # 見た目ブロック
# cmd(f"setblock {pos(11,0,-5)} minecraft:stone")
# cmd(f"setblock {pos(11,1,-5)} minecraft:oak_wall_sign[facing=south]{{front_text:{{messages:['\"TP\"','\"押す\"','\"\"','\"\"']}}}}")

# # ボタン
# cmd(f"setblock {pos(11,0,-4)} minecraft:stone_button[facing=south]")

# # コマンドブロック（地下）
# cmd((f'setblock {pos(11,-1,-5)} minecraft:command_block'
#      f'{{Command:"tp @s {pos(0,1,0)}"}}'))

# /gamerule commandBlockOutput true

# コマンドブロック
# cmd((f'setblock {pos(11,-1,-5)} minecraft:command_block'
#      f'{{Command:"tp @p {pos(0,1,0)}",auto:0b}}'))
cmd(f"setblock {pos(11,-1,-5)} minecraft:command_block{{Command:\"tp @p {pos(0,1,0)}\"}}")

# その上にブロック
cmd(f"setblock {pos(11,0,-5)} minecraft:stone")

# そのブロックにボタン
cmd(f"setblock {pos(11,0,-4)} minecraft:stone_button[facing=south]")


# ------------------------------
# 看板クリック
# 看板設置
cmd(f"setblock {pos(12,0,-5)} minecraft:oak_sign")
# データ付与
cmd(f'data merge block {pos(12,0,-5)} '
    '{"front_text":{"messages":['
    '"{\\"text\\":\\"ダイヤGET\\",\\"clickEvent\\":{\\"action\\":\\"run_command\\",\\"value\\":\\"give @s minecraft:diamond 1\\"}}"'
    ',"","",""]}}')

# ==================================================
# コンパス＋スニークで帰還
# ==================================================

# スコアボード
cmd("scoreboard objectives add isSneaking minecraft.custom:minecraft.sneak_time")

# ▼ TP処理（コンパス持ち＋しゃがみ）
tp_cmd = (
    f'execute as @a[nbt={{SelectedItem:{{id:"minecraft:compass"}}}}] '
    f'if score @s isSneaking matches 1.. '
    f'run tp @s {pos(0,1,0)}'
).replace('"', '\\"')

cmd((f'setblock {pos(0,-2,0)} minecraft:repeating_command_block'
     f'{{auto:1b,Command:"{tp_cmd}"}}'))

# ▼ スコアリセット（超重要）
reset_cmd = 'scoreboard players set @a isSneaking 0'.replace('"', '\\"')

cmd((f'setblock {pos(1,-2,0)} minecraft:repeating_command_block'
     f'{{auto:1b,Command:"{reset_cmd}"}}'))

# ==================================================
# 水・溶岩エリア
# ==================================================

# 水（まとめてfill）
cmd(f"fill {pos(-5,-1,0)} {pos(-2,-1,1)} minecraft:water")

# 溶岩
cmd(f"fill {pos(2,-1,0)} {pos(2,-1,1)} minecraft:lava")

# 生物
cmd(f"summon minecraft:axolotl {pos(-3,-1,0)} {{NoAI:1b}}")
cmd(f"summon minecraft:tadpole {pos(-5,-1,1)} {{NoAI:1b}}")

# ==================================================
# ネザーゲート
# ==================================================

BASE_X, BASE_Y, BASE_Z = 5, -1, -5

for dy in range(5):
    for dx in range(4):
        block = "minecraft:obsidian" if dx in [0,3] or dy in [0,4] else "minecraft:air"
        cmd(f"setblock {pos(BASE_X+dx, BASE_Y+dy, BASE_Z)} {block}")

# 点火
cmd(f"setblock {pos(BASE_X+1, BASE_Y+1, BASE_Z)} minecraft:fire")

# ==================================================
# アイテム配布
# ==================================================

items = [
#    'diamond_pickaxe[enchantments={"minecraft:efficiency":5,"minecraft:fortune":3}] 1',
    'minecraft:fishing_rod[enchantments={"minecraft:luck_of_the_sea":3,"minecraft:lure":3,"minecraft:unbreaking":3,"minecraft:mending":1}] 1',
    "minecraft:emerald 64",
    "minecraft:bone 64",
    "minecraft:glow_ink_sac 64",
    "minecraft:copper_ingot 64",
#    "minecraft:amethyst_shard 64",
    "minecraft:feather 64",
    "minecraft:stick 64",
    "minecraft:suspicious_sand 64",
    "minecraft:compass 1"
]

for item in items:
    cmd(f"give @a {item}")


# ==================================================
# オオカミ横一列
# ==================================================

WOLF_VARIANTS = [
    "pale","woods","ashen","black","chestnut","rusty",
    "spotted","striped","snowy","classic","big","grumpy"
]

base_x = -11
z_line = -10

for i, variant in enumerate(WOLF_VARIANTS):
    cmd(f"summon minecraft:wolf {pos(base_x+i,0,z_line)} "
        f'{{NoAI:1b,Sitting:1b,Silent:1b,CollarColor:14b,'
        f'variant:"minecraft:{variant}",sound_variant:"minecraft:{variant}"}}')

# -----------------------------------
# 骨チェスト
cmd(f"setblock {pos(-12,0,-10)} minecraft:chest[facing=south]")
cmd((f'/data merge block {pos(-12,0,-10)} '
     f'{{Items:['
     f'{{Slot:0b,id:"minecraft:bone",Count:64b}},'
     f'{{Slot:1b,id:"minecraft:bone",Count:64b}},'
     f'{{Slot:2b,id:"minecraft:bone",Count:64b}},'
     f'{{Slot:3b,id:"minecraft:bone",Count:64b}},'
     f'{{Slot:4b,id:"minecraft:bone",Count:64b}},'
     f'{{Slot:5b,id:"minecraft:bone",Count:64b}},'
     f'{{Slot:6b,id:"minecraft:bone",Count:64b}},'
     f'{{Slot:7b,id:"minecraft:bone",Count:64b}}'
     f']}}'))

# ==================================================
# 猫横一列
# ==================================================

CAT_VARIANTS = [
    "tabby","black","red","siamese","british_shorthair",
    "calico","persian","ragdoll","white","jellie","all_black"
]

base_x = -11
z_line = -14

for i, variant in enumerate(CAT_VARIANTS):
    cmd(f"summon minecraft:cat {pos(base_x+i,0,z_line)} "
        f'{{NoAI:1b,Sitting:1b,Silent:1b,variant:"minecraft:{variant}"}}')

# -----------------------------------
# 魚チェスト
cmd(f"setblock {pos(-12,0,-14)} minecraft:chest[facing=south]")

cmd((f'/data merge block {pos(-12,0,-14)} '
     f'{{Items:['
     f'{{Slot:0b,id:"minecraft:cod",Count:64b}},'
     f'{{Slot:1b,id:"minecraft:cod",Count:64b}},'
     f'{{Slot:2b,id:"minecraft:salmon",Count:64b}},'
     f'{{Slot:3b,id:"minecraft:salmon",Count:64b}}'
     f']}}'))

# ==================================================
# カエル横一列
# ==================================================

FROG_VARIANTS = ["temperate","warm","cold"]

base_x = -11
z_line = -18

for i, variant in enumerate(FROG_VARIANTS):
    cmd(f"summon minecraft:frog {pos(base_x+i,0,z_line)} "
        f'{{NoAI:1b,Silent:1b,variant:"minecraft:{variant}"}}')

# -----------------------------------
# リードチェスト
cmd(f"setblock {pos(-12,0,-18)} minecraft:chest[facing=south]")

cmd((f'/data merge block {pos(-12,0,-18)} '
     f'{{Items:['
     f'{{Slot:0b,id:"minecraft:lead",Count:64b}},'
     f'{{Slot:1b,id:"minecraft:lead",Count:64b}},'
     f'{{Slot:2b,id:"minecraft:lead",Count:64b}},'
     f']}}'))
