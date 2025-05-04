import time
import minescript
from minescript import execute, echo, player_position

x, y, z = map(int, player_position())
execute(f"/tp @p {x} {y} {z} 0 45")  # 南向きに向ける

# マップ定義（5層の3D）
map_layers = [
    [  # 表面（0層目）
        "__________",
        "__________",
        "__________",
        "__________",
        "__________",
        "__________",
        "__________",
        "__________",
        "__________",
        "__________",
    ],
    [  # 表面（1層目）
        "__________",
        "__________",
        "___YYYY___",
        "___YYYY___",
        "__________",
        "__________",
        "__________",
        "__________",
        "__________",
        "__________",
    ],
    [  # 中間（2層目）
        "__________",
        "__________",
        "___YYYY___",
        "___YYYY___",
        "____RR____",
        "____RR____",
        "__________",
        "__________",
        "__________",
        "__________",
    ],
    [  # 背面（3層目）
        "___WWWW___",
        "___BWWB___",
        "__WYYYYW__",
        "_WWYYYYWW_",
        "_WWWRRWWW_",
        "_WWWRRWWW_",
        "__WWWWWW__",
        "__WWWWWW__",
        "___Y__Y___",
        "___Y__Y___",
    ],
    [  # 背面（4層目）
        "___WWWW___",
        "___WWWW___",
        "__WYYYYW__",
        "_WWYYYYWW_",
        "_WWWRRWWW_",
        "_WWWRRWWW_",
        "__WWWWWW__",
        "__WWWWWW__",
        "___Y__Y___",
        "___Y__Y___",
    ],
]

# 色のパターン定義（複数バージョン）
color_patterns = [
    {
        "W": "white_wool", "B": "black_wool", "Y": "yellow_wool","R": "red_wool", "_": "glass",
    },
    {
        "W": "white_wool", "B": "black_wool", "Y": "yellow_wool","R": "red_wool", "_": "air",
    },
    {
        "W": "pink_wool", "B": "black_wool", "Y": "yellow_wool","R": "red_wool", "_": "air",
    },
    {
        "W": "blue_wool", "B": "black_wool", "Y": "lime_wool","R": "orange_wool", "_": "air",
    },
    {
        "W": "magenta_wool", "B": "gray_wool", "Y": "orange_wool","R": "purple_wool", "_": "air",
    },
    {
        "W": "white_wool", "B": "black_wool", "Y": "yellow_wool","R": "red_wool", "_": "glass",
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
