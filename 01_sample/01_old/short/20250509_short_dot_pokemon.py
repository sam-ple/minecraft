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
#    "_": "air",
    "_": "white_concrete_powder",
    "A": "white_concrete_powder",
    "B": "light_gray_concrete_powder",
    "C": "gray_concrete_powder",
    "D": "black_concrete_powder",
    "E": "brown_concrete_powder",
    "F": "red_concrete_powder",
    "G": "pink_concrete_powder",
    "H": "orange_concrete_powder",
    "I": "yellow_concrete_powder",
    "J": "purple_concrete_powder",
    "K": "magenta_concrete_powder",
    "L": "blue_concrete_powder",
    "M": "light_blue_concrete_powder",
    "N": "cyan_concrete_powder",
    "O": "green_concrete_powder",
    "P": "lime_concrete_powder"
}

# キャラクター画像データ
charmander_colors = [
    "_________________D___",
    "_____DDD________D_D__",
    "___DD___D_______D__D_",
    "__D______D______D__D_",
    "__D______D_____D____D",
    "_D________D____D____D",
    "_D________D____D____D",
    "D_________D_____D__D_",
    "D_________D_____D_D__",
    "_D_________D____D_D__",
    "__DD_______D___D__D__",
    "____DD______D_D__D___",
    "_____D_______D___D___",
    "_____D__________D____",
    "____D__________D_____",
    "____D_________D______",
    "_____DDDD____D_______",
    "_________D___D_______",
    "__________DDD________",
]

#squirtle
#charmander
#bulbasaur
#pikachu
#porygon
#eevee

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
                time.sleep(0.1)

# 描画
draw_art(x, y + 10, z, charmander_colors)
time.sleep(1)
