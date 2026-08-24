import minescript as m
import math

# ======================
# 設定
# ======================
LENGTH = 200
BLOCK = "minecraft:white_wool"

SEARCH_UP = 12
SEARCH_DOWN = 60

GROUND_BLOCKS = {
    "minecraft:dirt",
    "minecraft:grass_block[snowy=false]",
    "minecraft:grass_block[snowy=true]",
    "minecraft:coarse_dirt",
    "minecraft:sand",
    "minecraft:gravel",
    "minecraft:stone",
    "minecraft:andesite",
    "minecraft:diorite",
    "minecraft:granite",
}

# GROUND_BLOCKS = {
#     "minecraft:dirt",                 # 普通の土
#     "minecraft:coarse_dirt",          # 粗い土
#     "minecraft:grass_block[snowy=false]",  # 草ブロック（雪なし）
#     "minecraft:grass_block[snowy=true]",   # 草ブロック（雪あり）
#     "minecraft:grass_path",           # 草道（村の道）
#     "minecraft:sand",                 # 砂
#     "minecraft:gravel",               # 砂利
#     "minecraft:stone",                # 石
#     "minecraft:andesite",             # 安山岩
#     "minecraft:diorite",              # 閃緑岩
#     "minecraft:granite",              # 花崗岩
#     "minecraft:mycelium",             # 菌糸ブロック（キノコ島）
#     "minecraft:podzol",               # ポドゾル（土質の森）
#     "minecraft:clay",                 # 粘土
#     "minecraft:snow_block",           # 雪ブロック（固まった雪）
#     "minecraft:soul_sand",            # ソウルサンド（ネザー）
#     "minecraft:soul_soil",            # ソウルソイル（ネザー）
# }

# ======================
# 地面探索
# ======================
def find_ground(x, sy, z):
    for y in range(sy + SEARCH_UP, sy - SEARCH_DOWN, -1):
        if m.getblock(x, y, z) in GROUND_BLOCKS:
            return y
    return None

# ======================
# メイン
# ======================
px, py, pz = map(math.floor, m.player_position())

# South固定（+Z方向）
for d in range(LENGTH):

    x = px
    z = pz + d

    ground_y = find_ground(x, py, z)
    if ground_y is None:
        continue

    m.execute(f"setblock {x} {ground_y} {z} {BLOCK}")

m.echo("South ground-follow line created.")

# /kill @e[type=item,nbt={Item:{id:"minecraft:white_wool"}}]
# /execute as @a at @s run kill @e[type=item,nbt={Item:{id:"minecraft:white_wool"}},distance=..10]
# /execute as @e[type=item] if data entity @s Item{id:"minecraft:white_wool"} run kill @s
