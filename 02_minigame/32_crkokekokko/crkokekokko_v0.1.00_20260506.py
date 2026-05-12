import minescript as m
import time
import os
import sys
import random
import json
import threading

# ============================================================
# DATA DIRECTORY
# ============================================================

BASE_DIR = "minescript/data/cr"
os.makedirs(BASE_DIR, exist_ok=True)

BLOCK_POS = f"{BASE_DIR}/pos.json"

# ============================================================
# FIELD FLATTEN
# ============================================================

def flatten_area():

    x_min, x_max = x-25, x+25
    z_min, z_max = z-25, z+25

    # 地面生成
    m.execute(
        f"fill {x_min} {y-1} {z_min} {x_max} {y-1} {z_max} minecraft:quartz_block"
    )

    # 空間クリア／建築スペース確保（高さ30ブロック分を空気化）
    m.execute(f"fill {x-25} {y} {z-25} {x+25} {y+10} {z+25} minecraft:air")
    m.execute(f"fill {x-25} {y+10} {z-25} {x+25} {y+20} {z+25} minecraft:air")
    m.execute(f"fill {x-25} {y+20} {z-25} {x+25} {y+30} {z+25} minecraft:air")

# ============================================================
# 
# ============================================================

# === プレイヤー位置 ===
x, y, z = map(int, m.player_position())

# 南向き
m.execute(f"/tp @p {x} {y} {z} 0 0")

# === ブロック定義 ===
block_map = {
    "_": None,
    "T": "target",
    "X": "barrier",
    "S": "sandstone",
    "G": "gold_block",
    "C": "white_stained_glass",
    "E": "diamond_block",
    "Q": "quartz_block",
    "D": "pale_oak_trapdoor[facing=south,half=top,open=false]",
    "H": "pale_oak_slab",
    "B": "sea_lantern",
    "B1": "sea_lantern",

    "1": "red_concrete",
    "2": "orange_concrete",
    "3": "yellow_concrete",
    "4": "lime_concrete",
    "5": "green_concrete",
    "6": "cyan_concrete",
    "7": "light_blue_concrete",
    "8": "blue_concrete",
    "9": "purple_concrete",
    "10": "magenta_concrete",
    "11": "pink_concrete",
}

def parse_layer(text):
    lines = []
    for line in text.strip().split("\n"):
        row = [c for c in line.split("\t") if c != ""]
        if row:
            lines.append(row)
    return lines

# ==============================
# レイヤー（奥）
# ==============================
layer_back_text = """
_	_	_	_	_	_	_	_	G	G	G	G	G	_	_	_	_	_	_	_	_
_	_	_	_	_	_	G	G	S	T	T	T	S	G	G	_	_	_	_	_	_
_	_	_	_	G	G	S	S	S	S	S	S	S	S	S	G	G	_	_	_	_
_	_	_	G	S	S	S	S	S	S	S	S	S	S	S	S	S	G	_	_	_
_	_	G	S	S	S	S	S	S	S	S	S	S	S	S	S	S	S	G	_	_
_	_	G	S	S	S	S	S	S	S	S	S	S	S	S	S	S	S	G	_	_
_	G	G	S	S	S	S	S	S	S	S	S	S	S	S	S	S	S	G	G	_
_	G	G	S	S	S	S	S	S	S	S	S	S	S	S	S	S	S	G	G	_
_	G	G	S	S	S	S	S	S	S	S	S	S	S	S	S	S	S	G	G	_
G	G	G	S	B1	S	S	S	S	S	B1	S	S	S	S	S	B1	S	G	G	G
G	G	G	S	S	S	S	S	S	S	S	S	S	S	S	S	S	S	G	G	G
G	G	G	S	S	S	S	S	S	S	S	S	S	S	S	S	S	S	G	G	G
G	G	G	S	S	S	S	S	S	S	S	S	S	S	S	S	S	S	G	G	G
G	G	G	S	B1	S	S	S	S	S	B1	S	S	S	S	S	B1	S	G	G	G
G	G	G	S	S	S	S	S	S	S	S	S	S	S	S	S	S	S	G	G	G
G	G	G	S	S	S	S	S	S	S	S	S	S	S	S	S	S	S	G	G	G
G	G	G	S	S	S	S	S	S	S	S	S	S	S	S	S	S	S	G	G	G
G	G	G	S	S	S	B1	S	B1	S	B1	S	B1	S	B1	S	S	S	G	G	G
_	G	G	S	S	S	S	S	S	S	S	S	S	S	S	S	S	S	G	G	_
_	G	G	G	S	S	S	S	S	S	S	S	S	S	S	S	S	G	G	G	_
_	_	G	G	G	S	S	S	S	S	S	S	S	S	S	S	G	G	G	_	_
_	_	_	_	_	G	G	G	G	G	G	G	G	G	G	G	_	_	_	_	_
"""

# ==============================
# 真ん中
# ==============================
layer_middle_text = """
_	_	_	_	_	_	_	_	G	G	G	G	G	_	_	_	_	_	_	_	_
_	_	_	_	_	_	G	G	_	_	_	_	_	G	G	_	_	_	_	_	_
_	_	_	_	G	G	_	_	_	_	_	_	_	_	_	G	G	_	_	_	_
_	_	_	G	_	_	_	_	_	_	_	_	_	_	_	_	_	G	_	_	_
_	_	G	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	G	_	_
_	_	G	Q	Q	E	Q	D	Q	Q	Q	Q	Q	D	Q	E	Q	Q	G	_	_
_	G	G	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	G	G	_
_	G	G	_	_	_	_	H	_	_	_	_	_	H	_	_	_	_	G	G	_
_	G	G	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	G	G	_
G	G	G	Q	B	Q	Q	D	Q	Q	B	Q	Q	D	Q	Q	B	Q	G	G	G
G	G	G	Q	_	Q	_	_	_	Q	_	Q	_	_	_	Q	_	Q	G	G	G
G	G	G	_	1	_	_	H	_	_	2	_	_	H	_	_	3	_	G	G	G
G	G	G	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	G	G	G
G	G	G	Q	B	Q	Q	D	Q	Q	B	Q	Q	D	Q	Q	B	Q	G	G	G
G	G	G	Q	_	Q	_	_	_	Q	_	Q	_	_	_	Q	_	Q	G	G	G
G	G	G	_	4	_	_	_	_	_	5	_	_	_	_	_	6	_	G	G	G
G	G	G	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	G	G	G
G	G	G	Q	Q	Q	B	Q	B	Q	B	Q	B	Q	B	Q	Q	Q	G	G	G
_	G	G	Q	Q	Q	_	Q	_	Q	_	Q	_	Q	_	Q	Q	Q	G	G	_
_	G	G	G	Q	Q	7	Q	8	Q	9	Q	10	Q	11	Q	Q	G	G	G	_
_	_	G	G	G	Q	Q	Q	Q	Q	Q	Q	Q	Q	Q	Q	G	G	G	_	_
_	_	_	_	_	G	G	G	G	G	G	G	G	G	G	G	_	_	_	_	_
"""

# ==============================
# レイヤー（手前）
# ==============================
layer_front_text = """
_	_	_	_	_	_	_	_	G	G	G	G	G	_	_	_	_	_	_	_	_
_	_	_	_	_	_	G	G	C	_	_	_	C	G	G	_	_	_	_	_	_
_	_	_	_	G	G	X	X	C	_	_	_	C	X	X	G	G	_	_	_	_
_	_	_	G	X	X	X	X	X	C	C	C	X	X	X	X	X	G	_	_	_
_	_	G	X	X	X	X	X	X	X	X	X	X	X	X	X	X	X	G	_	_
_	_	G	X	X	X	X	X	X	X	X	X	X	X	X	X	X	X	G	_	_
_	G	G	X	X	X	X	X	X	X	X	X	X	X	X	X	X	X	G	G	_
_	G	G	X	X	X	X	X	X	X	X	X	X	X	X	X	X	X	G	G	_
_	G	G	X	X	X	X	X	X	X	X	X	X	X	X	X	X	X	G	G	_
G	G	G	X	X	X	X	X	X	X	X	X	X	X	X	X	X	X	G	G	G
G	G	G	X	X	X	X	X	X	X	X	X	X	X	X	X	X	X	G	G	G
G	G	G	X	X	X	X	X	X	X	X	X	X	X	X	X	X	X	G	G	G
G	G	G	X	X	X	X	X	X	X	X	X	X	X	X	X	X	X	G	G	G
G	G	G	X	X	X	X	X	X	X	X	X	X	X	X	X	X	X	G	G	G
G	G	G	X	X	X	X	X	X	X	X	X	X	X	X	X	X	X	G	G	G
G	G	G	X	X	X	X	X	X	X	X	X	X	X	X	X	X	X	G	G	G
G	G	G	X	X	X	X	X	X	X	X	X	X	X	X	X	X	X	G	G	G
G	G	G	X	X	X	X	X	X	X	X	X	X	X	X	X	X	X	G	G	G
_	G	G	X	X	X	X	X	X	X	X	X	X	X	X	X	X	X	G	G	_
_	G	G	G	X	X	X	X	X	X	X	X	X	X	X	X	X	G	G	G	_
_	_	G	G	G	X	X	X	X	X	X	X	X	X	X	X	G	G	G	_	_
_	_	_	_	_	G	G	G	G	G	G	G	G	G	G	G	_	_	_	_	_
"""

# ==============================
# パース
# ==============================
layer_back = parse_layer(layer_back_text)
layer_middle = parse_layer(layer_middle_text)
layer_front = parse_layer(layer_front_text)

layers = [layer_back, layer_middle, layer_front]

# ==============================
# 描画
# ==============================

D_POS = []
B_POS = []

def build_layers():
    global D_POS, B_POS
    D_POS = []
    B_POS = []

    for dz, layer in enumerate(layers):
        for dy, row in enumerate(layer):
            for dx, char in enumerate(row):

                block = block_map.get(char)
                if block is None:
                    continue

                width = len(layer[0])
                bx = x + dx - width // 2
                by = y + (len(layer) - 1 - dy)
                bz = z + (len(layers) - dz) + 15

                if char == "D":
                    D_POS.append([bx, by, bz])

                if char == "B":
                    B_POS.append([bx, by, bz])

                m.execute(f"/setblock {bx} {by} {bz} minecraft:{block}")

    with open(BLOCK_POS, "w") as f:
        json.dump({"D": D_POS, "B": B_POS}, f)

CONCRETE_RESULT = {
    "red_concrete": ("RED", "red"),
    "orange_concrete": ("ORANGE", "gold"),
    "yellow_concrete": ("YELLOW", "yellow"),
    "lime_concrete": ("LIME", "green"),
    "green_concrete": ("GREEN", "dark_green"),
    "cyan_concrete": ("CYAN", "aqua"),
    "light_blue_concrete": ("LIGHT BLUE", "blue"),
    "blue_concrete": ("BLUE", "dark_blue"),
    "purple_concrete": ("PURPLE", "dark_purple"),
    "magenta_concrete": ("MAGENTA", "light_purple"),
    "pink_concrete": ("PINK", "light_purple"),
}

# ==============================
# 
# ==============================
def game():
    while True:
        # ヒヨコ発光
        m.execute('execute as @e[type=chicken] run effect give @s glowing 1 0 true')

        # コンクリ判定（全色対応）
        for block, (message, color) in CONCRETE_RESULT.items():

            # 踏んだ瞬間
            m.execute(
                f'execute as @e[type=chicken,tag=!done] at @s '
                f'if block ~ ~-1 ~ minecraft:{block} '
                f'run tag @s add done'
            )

            # 表示＋演出（まだのやつだけ）
            m.execute(
                f'execute as @e[type=chicken,tag=done,tag=!shown] at @s run title @a title '
                f'{{"text":"{message}","color":"{color}","bold":true}}'
            )

            # 🔊 音
            m.execute(
                'execute as @e[type=chicken,tag=done,tag=!shown] at @s '
                'run playsound minecraft:entity.firework_rocket.launch master @a ~ ~ ~ 1 1'
            )

            # 🎆 花火
            m.execute(
                'execute as @e[type=chicken,tag=done,tag=!shown] at @s '
                'run summon firework_rocket ~ ~1 ~ {LifeTime:20,FireworksItem:{id:"minecraft:firework_rocket",Count:1,tag:{Fireworks:{Explosions:[{Type:1,Colors:[I;16711680],FadeColors:[I;16776960]}]}}}}'
            )

            # 表示済み
            m.execute(
                'execute as @e[type=chicken,tag=done,tag=!shown] run tag @s add shown'
            )

        # エメラルド判定
        # ① 今踏んでる → on タグ
        m.execute('execute as @e[type=chicken] at @s if block ~ ~-1 ~ minecraft:diamond_block run tag @s add on')

        # ② 離れたら on を消す
        m.execute('execute as @e[type=chicken] at @s unless block ~ ~-1 ~ minecraft:diamond_block run tag @s remove on')

        # ③ 新しく踏んだ瞬間だけ発射
        m.execute('execute as @e[type=chicken,tag=on,tag=!was_on] at @s run summon egg ~ ~2 ~')

        # ④ 状態保存
        m.execute('execute as @e[type=chicken,tag=on] run tag @s add was_on')
        m.execute('execute as @e[type=chicken,tag=!on] run tag @s remove was_on')

        time.sleep(0.1)


# ==============================
# ブロックの位置データを読み込む
# ==============================

def load_positions():
    with open(BLOCK_POS, "r") as f:
        data = json.load(f)
    return data["D"], data["B"]

# ==============================
# トラップドアの開閉をランダム化
# ==============================
def randomize_trapdoors():
    # positions = load_d_positions()
    d_positions, _ = load_positions()

    for (bx, by, bz) in d_positions:
        open_flag = random.choice([True, False])

        state = "true" if open_flag else "false"

        m.execute(
            f'execute unless block {bx} {by} {bz} birch_trapdoor[facing=south,half=top,open={state}] '
            f'run setblock {bx} {by} {bz} birch_trapdoor[facing=south,half=top,open={state}]'
        )

def trapdoor_loop():
    while True:
        randomize_trapdoors()
        # time.sleep(0.5)
        time.sleep(random.uniform(0.6, 0.8))

# ==============================
# Bブロックの移動
# ==============================

def move_b_blocks():
    _, b_positions = load_positions()

    while True:
        for (bx, by, bz) in b_positions:
            if random.random() < 0.3:
                # m.execute(f"setblock {bx} {by} {bz} air")
                m.execute(
                    f'execute unless block {bx} {by} {bz} air '
                    f'run setblock {bx} {by} {bz} air'
                )
            else:
                # m.execute(f"setblock {bx} {by} {bz} sea_lantern")
                m.execute(
                    f'execute unless block {bx} {by} {bz} sea_lantern '
                    f'run setblock {bx} {by} {bz} sea_lantern'
                )

        time.sleep(0.5)

# ==============================
# メイン
# ==============================
def main():

    arg = sys.argv[1] if len(sys.argv) > 1 else "flat"

    if arg == "flat":
        flatten_area()
        return

    if arg == "set":
        build_layers()
        return

    if arg == "start":
        if not os.path.exists(BLOCK_POS):
            build_layers()

        m.execute('title @a title {"text":"START","color":"gold"}')
        m.execute('playsound minecraft:block.note_block.pling master @a ~ ~ ~ 1 1')

        threading.Thread(target=trapdoor_loop, daemon=True).start()
        threading.Thread(target=move_b_blocks, daemon=True).start()

        # randomize_trapdoors()
        game()
        return

main()
