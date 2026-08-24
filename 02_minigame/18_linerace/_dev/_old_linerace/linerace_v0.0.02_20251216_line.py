import minescript as m

'''
座標の向きメモ
Xが増える → 東 (East)
Xが減る → 西 (West)
Zが増える → 南 (South)
Zが減る → 北 (North)
'''

# -------------------------------------------------
# プレイヤーの現在位置
# -------------------------------------------------
px, py, pz = map(int, m.player_position())

# -------------------------------------------------
# 設定
# -------------------------------------------------
BLOCK_TYPE = "minecraft:blue_concrete"
LENGTH = 300

# 探索範囲（前回Yを基準）
SEARCH_UP = 5
SEARCH_DOWN = 10

# 地面として扱わないブロック
IGNORE_BLOCKS = {
    "minecraft:air",
    "minecraft:grass",
    "minecraft:tall_grass",
    "minecraft:fern",
    "minecraft:large_fern",
    "minecraft:oak_leaves",
    "minecraft:birch_leaves",
    "minecraft:spruce_leaves",
    "minecraft:jungle_leaves",
    "minecraft:acacia_leaves",
    "minecraft:dark_oak_leaves",
    "minecraft:oak_log",
    "minecraft:birch_log",
    "minecraft:spruce_log",
}

# -------------------------------------------------
# 初期Y（今いる位置）
# -------------------------------------------------
current_y = py

# -------------------------------------------------
# メイン処理
# -------------------------------------------------
for i in range(LENGTH):
    x = px + i
    z = pz

    found = False

    # 前回のYを中心に上下だけ探す
    for y in range(current_y + SEARCH_UP, current_y - SEARCH_DOWN - 1, -1):
        block = m.getblock(x, y, z)

        if block not in IGNORE_BLOCKS:
            m.execute(f"setblock {x} {y} {z} {BLOCK_TYPE}")
            current_y = y  # 次回の基準Yにする
            found = True
            break

    if not found:
        m.echo(f"⚠ 地面が見つからない: x={x}")

# -------------------------------------------------
# 完了
# -------------------------------------------------
m.echo(f"✅ 高速モードで {LENGTH} ブロックの一本道を作成しました")
