import time
import minescript
from minescript import execute

# execute("/playsound minecraft:music.credits record @p")

# プレイヤーの現在位置を取得し整列
x, y, z = map(int, minescript.player_position())
# execute(f"/tp @p {x} {y} {z} 180 0")

# 基準位置にガラスとテレポート
base_y = 10
base_z = 5
execute(f"/setblock {x} {y+base_y} {z+base_z} minecraft:glass")
execute(f"/tp @p {x} {y+base_y+1} {z+base_z} 180 0")

# ブロック定義マップ（番号と色を正しくマッピング）
block_map = {
    0: "white_concrete_powder",
    1: "orange_concrete_powder",
    2: "magenta_concrete_powder",
    3: "light_blue_concrete_powder",
    4: "yellow_concrete_powder",
    5: "lime_concrete_powder",
    6: "pink_concrete_powder",
    7: "gray_concrete_powder",
    8: "light_gray_concrete_powder",
    9: "cyan_concrete_powder",
    10: "purple_concrete_powder",
    11: "blue_concrete_powder",
    12: "brown_concrete_powder",
    13: "green_concrete_powder",
    14: "red_concrete_powder",
    15: "black_concrete_powder",
    16: "air"
}

# キャラクター画像データ
creeper_colors = [
    [5, 13, 5, 5, 0, 5, 5, 13],
    [13, 5, 5, 5, 13, 5, 5, 0],
    [5, 15, 15, 5, 13, 15, 15, 0],
    [5, 15, 15, 5, 5, 15, 15, 5],
    [5, 5, 5, 15, 15, 0, 13, 5],
    [5, 13, 15, 15, 15, 15, 5, 5],
    [0, 13, 15, 15, 15, 15, 5, 13],
    [5, 5, 15, 5, 5, 15, 13, 5]
]

zombie_colors = [
    [13, 13, 13, 13, 13, 13, 13, 13],
    [13, 13, 13, 13, 5, 5, 13, 13],
    [13, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 13, 5, 5, 5],
    [5, 15, 15, 5, 5, 15, 15, 5],
    [5, 5, 5, 13, 13, 5, 5, 13],
    [5, 5, 13, 5, 5, 13, 5, 13],
    [13, 13, 13, 13, 13, 13, 5, 13]
]

skeleton_colors = [
    [7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 8, 8, 7, 7],
    [7, 8, 8, 8, 8, 8, 8, 7],
    [8, 8, 8, 8, 7, 8, 8, 8],
    [8, 15, 15, 8, 8, 15, 15, 8],
    [8, 8, 8, 7, 7, 8, 8, 7],
    [8, 15, 15, 15, 15, 15, 15, 7],
    [7, 7, 7, 7, 7, 7, 7, 7]
]

sheep_colors = [
    [8, 8, 8, 8, 8, 8, 8, 8],
    [8, 0, 0, 0, 0, 0, 0, 8],
    [8, 12, 12, 12, 12, 12, 12, 8],
    [8, 15, 0, 12, 12, 0, 15, 8],
    [8, 12, 12, 12, 12, 12, 12, 8],
    [8, 0, 12, 6, 6, 12, 0, 8],
    [8, 0, 12, 6, 6, 12, 0, 8],
    [8, 8, 8, 8, 8, 8, 8, 8]
]

mooshroom_colors = [
    [14, 14, 14, 8, 8, 7, 7, 14],
    [14, 14, 14, 8, 8, 8, 14, 14],
    [15, 15, 14, 8, 8, 14, 15, 15],
    [15, 15, 14, 8, 14, 14, 15, 15],
    [14, 14, 14, 14, 14, 14, 14, 14],
    [14, 12, 0, 0, 0, 0, 12, 14],
    [14, 0, 15, 7, 7 ,15, 0, 14],
    [14, 0, 14, 7, 7, 14, 0, 14]
]

fox_colors = [
    [8, 8, 0, 0, 0, 0, 8, 8],
    [8, 7, 0, 0, 0, 0, 7, 8],
    [12, 12, 12, 12, 12, 12, 12, 12],
    [12, 12, 12, 12, 12, 12, 12, 12],
    [12, 12, 12, 12, 12, 12, 12, 12],
    [15, 0, 12, 12, 12, 12, 0, 15],
    [12, 12, 8, 15, 15, 8, 12, 12],
    [8, 8, 0, 0, 0, 0, 8, 8]
]

# 配置関数
def draw_art(start_x, start_y, start_z, art):
    for dy, row in enumerate(art):
        for dx, val in enumerate(row):
            block = block_map.get(val)
            if block:
                bx = start_x + dx -3
                by = start_y
                bz = start_z + dy -10  
                execute(f"/setblock {bx} {by} {bz} minecraft:{block}")
                # 効果音を鳴らす
                execute("playsound minecraft:block.amethyst_block.chime master @p ~ ~ ~ 1 1")
                
                time.sleep(0.1)

# 描画
draw_art(x, y + 10, z, creeper_colors)
time.sleep(1)
draw_art(x, y + 10, z, zombie_colors)
time.sleep(1)
draw_art(x, y + 10, z, skeleton_colors)
time.sleep(1)
draw_art(x, y + 10, z, sheep_colors)
time.sleep(1)
draw_art(x, y + 10, z, mooshroom_colors)
time.sleep(1)
draw_art(x, y + 10, z, fox_colors)
time.sleep(1)

