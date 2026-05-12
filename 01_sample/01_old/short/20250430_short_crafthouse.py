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

# ブロック定義マップ
block_map = {
    "O": "oak_log",
    "C": "cobblestone",
    "P": "oak_planks",
    "G": "glass",
    "S": "oak_stairs",
    "D": "oak_door",
    "T": "wall_torch",
    " ": None  # 空白はブロックなし
}

# 建物の各層の2Dレイアウト（上から順に5層）
layers = [
    [  # y + 0
        " OOOOO ",
        " OCCCO ",
        " OCPCO ",
        " OCCCO ",
        " OCPCO ",
        " OCCCO ",
        " OOOOO "
    ],
    [  # y + 1
        " OOOOO ",
        " OGGGO ",
        " OGPGO ",
        " OGGGO ",
        " OGPGO ",
        " OGGGO ",
        " OOOOO "
    ],
    [  # y + 2
        " OOOOO ",
        " OPDPO ",
        " ODPDO ",
        " DPPPD ",
        " ODPDO ",
        " OPDPO ",
        " OOOOO "
    ],
    [  # y + 3
        " OOOOO ",
        " OPGPO ",
        " OGGGO ",
        " OPGPO ",
        " OGGGO ",
        " OPGPO ",
        " OOOOO "
    ],
    [  # y + 4
        " OOOOO ",
        " OCCCO ",
        " OCPCO ",
        " OCCCO ",
        " OCPCO ",
        " OCCCO ",
        " OOOOO "
    ]
]

# ブロック配置処理
for dy, layer in enumerate(layers):
    for dz, row in enumerate(layer):
        for dx, char in enumerate(row):
            block = block_map.get(char)
            if block:
                bx = x + dx - 3  # 中心揃え
                by = y + dy
                bz = z + dz - 3
                execute(f"/setblock {bx} {by} {bz} minecraft:{block}")

# トーチ設置（南向き）
execute(f"/setblock {x} {y + 1} {z + 3} minecraft:wall_torch[facing=south]")
