import minescript as m

'''
X + : East
Z + : South
'''

px, py, pz = map(int, m.player_position())

BLOCK_TYPE = "minecraft:blue_concrete"
LENGTH = 300

SEARCH_UP = 8
SEARCH_DOWN = 30

# 一本道として「採用する地面」だけ
GROUND_BLOCKS = {
    "minecraft:dirt",
    "minecraft:grass_block",
    "minecraft:coarse_dirt",
    "minecraft:podzol",
    "minecraft:mycelium",

    "minecraft:sand",
    "minecraft:red_sand",
    "minecraft:gravel",

    "minecraft:stone",
    "minecraft:andesite",
    "minecraft:diorite",
    "minecraft:granite",
    "minecraft:deepslate",
}

current_y = py

for i in range(LENGTH):
    x = px + i
    z = pz

    for y in range(current_y + SEARCH_UP, current_y - SEARCH_DOWN - 1, -1):
        block = m.getblock(x, y, z)

        if block not in GROUND_BLOCKS:
            continue

        # 上が空気 or 水（海底OK）
        if m.getblock(x, y + 1, z) not in ("minecraft:air", "minecraft:water"):
            continue

        # 下は必ず実体
        if m.getblock(x, y - 1, z) == "minecraft:air":
            continue

        m.execute(f"setblock {x} {y} {z} {BLOCK_TYPE}")
        current_y = y
        break

m.echo(f"✅ 地面限定で一本道を {LENGTH} ブロック作成しました")
