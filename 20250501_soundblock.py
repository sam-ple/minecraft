import time
import minescript
from minescript import execute, echo

# プレイヤーの位置取得＆初期セット
x, y, z = map(int, minescript.player_position())
execute(f"/tp @p {x} {y} {z} 0")
execute(f"/setblock {x} {y} {z} minecraft:white_wool")
execute(f"/tp @p {x} {y+1} {z}")

# 音階とピッチ（ドレミファソラシド）
notes = [
    ("red_wool",    0.70, "block.note_block.bell"),
    ("orange_wool", 0.79, "block.note_block.bell"),
    ("yellow_wool", 0.89, "block.note_block.bell"),
    ("green_wool",  0.94, "block.note_block.bell"),
    ("light_blue_wool", 1.05, "block.note_block.bell"),
    ("blue_wool",   1.18, "block.note_block.bell"),
    ("purple_wool", 1.33, "block.note_block.bell"),
]

# ブロックを並べて音を鳴らす
def play_sequence(forward=True, place=True, sound=True):
    seq = notes if forward else reversed(notes)
    offset = -3
    for i, (block, pitch, snd) in enumerate(seq):
        bx = x + (offset + i if forward else 3 - i)
        execute(f"/setblock {bx} {y} {z - 3} minecraft:{block if place else 'air'}")
        if sound:
            execute(f"/playsound minecraft:{snd} master @a ~ ~ ~ 1 {pitch} 1")
        time.sleep(0.5)

# 置きながら鳴らす
play_sequence(forward=True, place=True, sound=True)
# 逆再生
play_sequence(forward=False, place=False, sound=True)

# ブロック音の種類（置く・壊す）
block_sounds = [
    ("red_wool",    "block.stone.place", "block.stone.break"),
    ("orange_wool", "block.wood.place",  "block.wood.break"),
    ("yellow_wool", "block.grass.place", "block.grass.break"),
    ("green_wool",  "block.sand.place",  "block.sand.break"),
    ("light_blue_wool", "block.glass.place", "block.glass.break"),
    ("blue_wool",   "block.metal.place", "block.metal.break"),
    ("purple_wool", "block.snow.place",  "block.snow.break"),
]

# 効果音付きで配置と破壊
def place_and_break_blocks():
    for i, (block, place_snd, break_snd) in enumerate(block_sounds):
        bx = x - 3 + i
        execute(f"/setblock {bx} {y} {z - 3} minecraft:{block}")
        execute(f"/playsound minecraft:{place_snd} master @p ~ ~ ~ 1 1 1")
        time.sleep(0.5)

    for i, (block, place_snd, break_snd) in reversed(list(enumerate(block_sounds))):
        bx = x - 3 + i
        execute(f"/setblock {bx} {y} {z - 3} minecraft:air")
        execute(f"/playsound minecraft:{break_snd} master @p ~ ~ ~ 1 1 1")
        time.sleep(0.5)

place_and_break_blocks()
