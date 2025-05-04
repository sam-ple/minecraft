import time
import minescript
from minescript import execute

# プレイヤーの現在位置を取得し整列
x, y, z = map(int, minescript.player_position())
execute(f"/tp @p {x} {y} {z} 0 180")

# 基準位置にガラスとテレポート
base_y = 5
base_z = 5
execute(f"/setblock {x} {y+base_y} {z+base_z} minecraft:glass")
execute(f"/tp @p {x} {y+base_y+1} {z+base_z} 0 -90")

# 簡易 setblock ヘルパー
def setblock(x, y, z, block):
    execute(f"/setblock {x} {y} {z} minecraft:{block}")

# 7x7エリアにブロックを設置する関数
def fill_plane(y, z_range, x_range, block_map):
    for dz, bz in enumerate(range(*z_range)):
        for dx, bx in enumerate(range(*x_range)):
            block = block_map[dz][dx]
            setblock(bx, y, bz, block)

# --- 地面（丸石で埋める） ---
block_map_ground = [["cobblestone"] * 7 for _ in range(7)]
fill_plane(y - 1, (z - 3, z + 4), (x - 3, x + 4), block_map_ground)

time.sleep(2)

# --- 1段上（建物の床や壁） ---
block_map_layer1 = [
    ["air", "air",       "air",       "air",       "air",       "air",       "air"],
    ["air", "oak_log",   "cobblestone", "cobblestone", "cobblestone", "oak_log",   "air"],
    ["air", "cobblestone", "oak_planks", "oak_planks", "oak_planks", "cobblestone", "air"],
    ["air", "cobblestone", "oak_planks", "oak_planks", "oak_planks", "cobblestone", "air"],
    ["air", "cobblestone", "oak_planks", "oak_planks", "oak_planks", "cobblestone", "air"],
    ["air", "oak_log",   "cobblestone", "cobblestone", "cobblestone", "oak_log",   "air"],
    ["air", "air",       "air",       "oak_stairs", "air",       "air",       "air"],
]
fill_plane(y, (z - 3, z + 4), (x - 3, x + 4), block_map_layer1)

time.sleep(2)
