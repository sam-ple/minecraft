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

cmd("tp @p ~ ~ ~ 180 0")

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

# ベッド
cmd(f"setblock {pos(-4,0,-5)} minecraft:red_bed[facing=south,part=foot]")
cmd(f"setblock {pos(-4,0,-4)} minecraft:red_bed[facing=south,part=head]")

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

# スケルトン
cmd(f"summon minecraft:skeleton {pos(-2,0,-5)} {{NoAI:1b,PersistenceRequired:1b,Health:2f,Rotation:{ROT}}}")

# 看板
cmd(f'setblock {pos(-1,0,-5)} minecraft:oak_sign[rotation=0]{{front_text:{{messages:["","crocadooo","",""]}}}}')

# 作業台
cmd(f"setblock {pos(0,0,-5)} minecraft:crafting_table")

# 動物
cmd(f"summon minecraft:parrot {pos(1,0,-5)} {{NoAI:1b,Silent:1b,Rotation:{ROT}}}")
cmd(f"summon minecraft:armadillo {pos(2,0,-5)} {{NoAI:1b,Silent:1b,Rotation:{ROT}}}")
cmd(f"summon minecraft:wolf {pos(3,0,-5)} {{NoAI:1b,Silent:1b}}")

# ==================================================
# アーマースタンド（ベッド横）
# ==================================================

HEAD_NAME = "crocadooo"

# ダイヤ装備
cmd((f'/summon minecraft:armor_stand {pos(-6,0,-5)} '
              f'{{ShowArms:true,NoGravity:true,PersistenceRequired:true,'
              f'equipment:{{'
              f'head:{{id:"player_head",Count:1,components:{{profile:{{name:"{HEAD_NAME}"}}}}}},'
              f'chest:{{id:"diamond_chestplate",Count:1}},'
              f'legs:{{id:"diamond_leggings",Count:1}},'
              f'feet:{{id:"diamond_boots",Count:1}}'
              f'}}}}'))

# ネザライト装備
cmd((f'/summon minecraft:armor_stand {pos(-8,0,-5)} '
              f'{{ShowArms:true,NoGravity:true,PersistenceRequired:true,'
              f'equipment:{{'
              f'head:{{id:"player_head",Count:1,components:{{profile:{{name:"{HEAD_NAME}"}}}}}},'
              f'chest:{{id:"netherite_chestplate",Count:1}},'
              f'legs:{{id:"netherite_leggings",Count:1}},'
              f'feet:{{id:"netherite_boots",Count:1}}'
              f'}}}}'))


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
    'diamond_pickaxe[enchantments={"minecraft:efficiency":5,"minecraft:fortune":3}] 1',
    'minecraft:fishing_rod[enchantments={"minecraft:luck_of_the_sea":3,"minecraft:lure":3,"minecraft:unbreaking":3,"minecraft:mending":1}] 1',
    "minecraft:emerald 64",
    "minecraft:bone 64",
    "minecraft:glow_ink_sac 64",
    "minecraft:copper_ingot 64",
    "minecraft:iron_ingot 64",
    "minecraft:amethyst_shard 64",
    "minecraft:feather 64",
    "minecraft:stick 64",
    "minecraft:suspicious_sand 64",
]

for item in items:
    cmd(f"give @a {item}")
