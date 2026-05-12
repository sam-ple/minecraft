import minescript as m

'''
X + : East
Z + : South
'''

# -------------------------------------------------
# プレイヤー位置
# -------------------------------------------------
px, py, pz = map(int, m.player_position())

# -------------------------------------------------
# 設定
# -------------------------------------------------
BLOCK_TYPE = "minecraft:blue_concrete"
LENGTH = 300

SEARCH_UP = 8
SEARCH_DOWN = 20

# 地面として「使わない」ブロック
IGNORE_BLOCKS = {
    "minecraft:air",
    "minecraft:grass",
    "minecraft:tall_grass",
    "minecraft:fern",
    "minecraft:large_fern",

    # 雪
    "minecraft:snow",
    "minecraft:snow_block",

    # 葉
    "minecraft:oak_leaves",
    "minecraft:birch_leaves",
    "minecraft:spruce_leaves",
    "minecraft:jungle_leaves",
    "minecraft:acacia_leaves",
    "minecraft:dark_oak_leaves",

    # 木
    "minecraft:oak_log",
    "minecraft:birch_log",
    "minecraft:spruce_log",
}

# -------------------------------------------------
# 初期Y
# -------------------------------------------------
current_y = py

# -------------------------------------------------
# メイン処理
# -------------------------------------------------
for i in range(LENGTH):
    x = px + i
    z = pz

    found = False

    # 前回Yを中心に上下探索
    for y in range(current_y + SEARCH_UP, current_y - SEARCH_DOWN - 1, -1):
        block = m.getblock(x, y, z)

        if block in IGNORE_BLOCKS:
            continue

        block_above = m.getblock(x, y + 1, z)
        block_below = m.getblock(x, y - 1, z)

        # 一本道として採用する「地面」条件
        if (
            block_below != "minecraft:air" and
            block_above in ("minecraft:air", "minecraft:water")
        ):
            m.execute(f"setblock {x} {y} {z} {BLOCK_TYPE}")
            current_y = y   # 見つかった時だけ更新
            found = True
            break

    # ❗ 未検出でも何もしない（スキップして次へ）
    # → 谷・海溝・大穴を自然に飛ばす

# -------------------------------------------------
# 完了
# -------------------------------------------------
m.echo(f"✅ 一本道を {LENGTH} ブロック生成しました（未検出地点は自動スキップ）")
