import minescript as m

'''
X + : East
Z + : South
'''

px, py, pz = map(int, m.player_position())

BLOCK_TYPE = "minecraft:blue_concrete"
LENGTH = 300

SEARCH_UP = 12
SEARCH_DOWN = 60  # 海底まで届かせる

# 「ちゃんとした地面」だけ
GROUND_BLOCKS = {
    "minecraft:dirt",
    # "minecraft:grass_block",
    "minecraft:grass_block[snowy=false]",
    "minecraft:grass_block[snowy=true]",
    "minecraft:coarse_dirt",
    "minecraft:podzol",
    "minecraft:mycelium",
    "minecraft:rooted_dirt",

    "minecraft:sand",
    "minecraft:red_sand",
    "minecraft:gravel",

    "minecraft:stone",
    "minecraft:andesite",
    "minecraft:diorite",
    "minecraft:granite",
    "minecraft:deepslate",
    "minecraft:tuff",
    "minecraft:calcite",
}

current_y = py

for i in range(LENGTH):
    x = px + i
    z = pz

    for y in range(current_y + SEARCH_UP, current_y - SEARCH_DOWN - 1, -1):
        block = m.getblock(x, y, z)

        # ★ 地面以外はすべて無視
        if block not in GROUND_BLOCKS:
            continue

        m.execute(f"setblock {x} {y} {z} {BLOCK_TYPE}")
        current_y = y
        break

m.echo("✅ 水・装飾を完全回避して一本道を生成しました")
