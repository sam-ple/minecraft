import time
import minescript
from minescript import execute, echo, player_position

x, y, z = map(int, minescript.player_position())
execute(f"/tp @p {x} {y} {z} 0 45")  # 南向きに向ける
x, y, z = int(x), int(y), int(z + 5)

# マップ定義（5層の3D）
map_layers = [
    [  # 表面（0層目）
        "GGGGGGGGGG",
        "GGGGGGGGGG",
        "GGGGGGGGGG",
        "GGGGGGGGGG",
        "GGGGGGGGGG",
        "GGGGGGGGGG",
        "GGGGGGGGGG",
        "GGGGGGGGGG",
        "GGGGGGGGGG",
        "GGGGGGGGGG",
    ],
    [  # 表面（1層目）
        "GGGGGGGGGG",
        "GGGGGGGGGG",
        "GGGYYYYGGG",
        "GGGYYYYGGG",
        "GGGGGGGGGG",
        "GGGGGGGGGG",
        "GGGGGGGGGG",
        "GGGGGGGGGG",
        "GGGGGGGGGG",
        "GGGGGGGGGG",
    ],
    [  # 中間（2層目）
        "GGGGGGGGGG",
        "GGGGGGGGGG",
        "GGGYYYYGGG",
        "GGGYYYYGGG",
        "GGGGRRGGGG",
        "GGGGRRGGGG",
        "GGGGGGGGGG",
        "GGGGGGGGGG",
        "GGGGGGGGGG",
        "GGGGGGGGGG",
    ],
    [  # 背面（3層目）
        "GGGWWWWGGG",
        "GGGBWWBGGG",
        "GGWYYYYWGG",
        "GWWYYYYWWG",
        "GWWWRRWWWG",
        "GWWWRRWWWG",
        "GGWWWWWWGG",
        "GGWWWWWWGG",
        "GGGYGGYGGG",
        "GGGYGGYGGG",
    ],
    [  # 背面（4層目）
        "GGGWWWWGGG",
        "GGGWWWWGGG",
        "GGWYYYYWGG",
        "GWWYYYYWWG",
        "GWWWRRWWWG",
        "GWWWRRWWWG",
        "GGWWWWWWGG",
        "GGWWWWWWGG",
        "GGGYGGYGGG",
        "GGGYGGYGGG",
    ],
]

# 色のパターン定義（複数バージョン）
color_patterns = [
    {
        "W": "white_wool", "B": "black_wool", "Y": "yellow_wool",
        "R": "red_wool", "G": "glass", "_": "air",
    },
    {
        "W": "white_wool", "B": "black_wool", "Y": "yellow_wool",
        "R": "red_wool", "G": "air", "_": "air",
    },
    {
        "W": "pink_wool", "B": "black_wool", "Y": "yellow_wool",
        "R": "red_wool", "G": "air", "_": "air",
    },
    {
        "W": "blue_wool", "B": "black_wool", "Y": "lime_wool",
        "R": "orange_wool", "G": "air", "_": "air",
    },
    {
        "W": "magenta_wool", "B": "gray_wool", "Y": "orange_wool",
        "R": "purple_wool", "G": "air", "_": "air",
    },
    {
        "W": "white_wool", "B": "black_wool", "Y": "yellow_wool",
        "R": "red_wool", "G": "glass", "_": "air",
    },
]

for i, map_color in enumerate(color_patterns):
    for dz, layer in enumerate(map_layers):
        for dy, row in enumerate(layer):
            for dx, char in enumerate(row):
                block = map_color.get(char)
                if block:
                    bx = x + dx - 5
                    by = y + 9 - dy - 10
                    bz = z + dz
                    execute(f"/setblock {bx} {by} {bz} minecraft:{block}")
    time.sleep(2.5)
