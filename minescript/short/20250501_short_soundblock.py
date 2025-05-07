import time
import minescript
from minescript import execute, echo

# プレイヤーの現在位置を取得
x, y, z = map(int, minescript.player_position())
execute(f"/tp @p {x} {y} {z} 0")  
execute(f"/setblock {x} {y} {z} minecraft:white_wool")

# プレイヤー位置調整
base_y = 0
base_z = 0
execute(f"/tp @p {x} {y + base_y + 1} {z + base_z}")

# 音階に対応するブロックとピッチのリスト
notes = [
    ("red_wool",       0.70),  # ド
    ("orange_wool",    0.79),  # レ
    ("yellow_wool",    0.89),  # ミ
    ("green_wool",     0.94),  # ファ
    ("light_blue_wool",1.05),  # ソ
    ("blue_wool",      1.18),  # ラ
    ("purple_wool",    1.33),  # シ
    # ("white_wool",   1.41),  # ド（高）←必要なら追加
]

by = y
bz = z - 3

for i, (block, pitch) in enumerate(notes):
    bx = x - 3 + i
    execute(f"/setblock {bx} {by} {bz} minecraft:{block}")
    execute(f"playsound minecraft:block.note_block.bell master @a ~ ~ ~ 1 {pitch} 1")
    time.sleep(0.5)
