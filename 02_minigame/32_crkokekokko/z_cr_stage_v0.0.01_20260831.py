import minescript as m
import os
import sys

# ============================================================
# CR STAGE GENERATOR
#
# Minecraft Java Edition + MineScript
#
# Version : v0.2.00
#
# ============================================================
#
# 役割
#
#   MineScript
#       ↓
#   ステージ生成専用
#
#   Skript
#       ↓
#   ゲーム稼働専用
#
# ============================================================
#
# COMMAND
#
#   python cr.py flat
#       → 地面を整地
#
#   python cr.py set
#       → ステージ生成
#
# ============================================================


# ============================================================
# プレイヤー位置
# ============================================================

x, y, z = map(int, m.player_position())


# ============================================================
# 実行地点を南向きにする
# ============================================================

m.execute(f"/tp @p {x} {y} {z} 0 0")


# ============================================================
# FIELD FLATTEN
# ============================================================

def flatten_area():

    x_min, x_max = x - 25, x + 25
    z_min, z_max = z - 25, z + 25

    # --------------------------------------------------------
    # 地面
    # --------------------------------------------------------

    m.execute(
        f"fill {x_min} {y-1} {z_min} "
        f"{x_max} {y-1} {z_max} "
        f"minecraft:quartz_block"
    )

    # --------------------------------------------------------
    # 空間クリア
    # --------------------------------------------------------

    m.execute(
        f"fill {x-25} {y} {z-25} "
        f"{x+25} {y+10} {z+25} "
        f"minecraft:air"
    )

    m.execute(
        f"fill {x-25} {y+10} {z-25} "
        f"{x+25} {y+20} {z+25} "
        f"minecraft:air"
    )

    m.execute(
        f"fill {x-25} {y+20} {z-25} "
        f"{x+25} {y+30} {z+25} "
        f"minecraft:air"
    )


# ============================================================
# BLOCK MAP
# ============================================================

block_map = {

    "_": None,

    "T": "target",
    "X": "barrier",
    "S": "sandstone",
    "G": "gold_block",
    "C": "white_stained_glass",
    "E": "diamond_block",
    "Q": "quartz_block",

    # --------------------------------------------------------
    # Trapdoor
    # --------------------------------------------------------

    "D": "pale_oak_trapdoor[facing=south,half=top,open=false]",

    "H": "pale_oak_slab",

    # --------------------------------------------------------
    # B
    # --------------------------------------------------------

    "B": "sea_lantern",
    "B1": "sea_lantern",

    # --------------------------------------------------------
    # Colors
    # --------------------------------------------------------

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


# ============================================================
# LAYER PARSER
# ============================================================

def parse_layer(text):

    lines = []

    for line in text.strip().split("\n"):

        row = [
            c
            for c in line.split("\t")
            if c != ""
        ]

        if row:
            lines.append(row)

    return lines


# ============================================================
# BACK
# ============================================================

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
G	G	G	S	S	S	S	S	S	S	S	S	S	S	S	S	G	G	G
G	G	G	S	B1	S	S	S	S	S	B1	S	S	S	S	S	B1	S	G	G	G
G	G	G	S	S	S	S	S	S	S	S	S	S	S	S	S	S	S	G	G	G
G	G	G	S	S	S	S	S	S	S	S	S	S	S	S	S	S	S	G	G	G
G	G	G	S	S	S	S	S	S	S	S	S	S	S	S	S	S	S	G	G	G
G	G	G	S	S	S	B1	S	B1	S	B1	S	B1	S	B1	S	S	S	G	G	G
_	G	G	S	S	S	S	S	S	S	S	S	S	S	S	S	S	S	G	G	_
_	G	G	G	S	S	S	S	S	S	S	S	S	S	S	G	G	G	_
_	_	G	G	G	S	S	S	S	S	S	S	S	G	G	G	_	_
_	_	_	_	_	G	G	G	G	G	G	G	G	G	G	G	_	_	_	_	_
"""


# ============================================================
# MIDDLE
# ============================================================

layer_middle_text = """
_	_	_	_	_	_	_	_	G	G	G	G	G	_	_	_	_	_	_	_	_
_	_	_	_	_	G	G	_	_	_	_	_	_	G	G	_	_	_	_	_	_
_	_	_	_	G	G	_	_	_	_	_	_	_	_	_	G	G	_	_	_	_
_	_	_	G	_	_	_	_	_	_	_	_	_	_	_	_	_	G	_	_	_
_	_	G	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	G	_	_
_	_	G	Q	Q	E	Q	D	Q	Q	Q	Q	Q	D	Q	E	Q	Q	G	_	_
_	G	G	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	G	G	_
_	G	G	_	_	_	_	H	_	_	_	_	_	H	_	_	_	_	G	G	_
_	G	G	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	G	G	_
G	G	G	Q	B	Q	Q	D	Q	Q	B	Q	Q	D	Q	Q	B	Q	G	G	G
G	G	G	Q	_	Q	_	_	_	Q	_	Q	_	_	Q	_	Q	G	G	G
G	G	G	_	1	_	_	H	_	_	2	_	_	H	_	_	3	_	G	G	G
G	G	G	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	G	G	G
G	G	G	Q	B	Q	Q	D	Q	Q	B	Q	Q	D	Q	Q	B	Q	G	G	G
G	G	G	Q	_	Q	_	_	_	Q	_	Q	_	_	_	Q	_	Q	G	G	G
G	G	G	_	4	_	_	_	_	_	5	_	_	_	_	_	6	_	G	G	G
G	G	G	_	_	_	_	_	_	_	_	_	_	_	_	_	_	G	G	G
G	G	G	Q	Q	Q	B	Q	B	Q	B	Q	B	Q	B	Q	Q	Q	G	G	G
_	G	G	Q	Q	Q	_	Q	_	Q	_	Q	_	Q	_	Q	Q	Q	G	G	_
_	G	G	G	Q	Q	7	Q	8	Q	9	Q	10	Q	11	Q	Q	G	G	G	_
_	_	G	G	G	Q	Q	Q	Q	Q	Q	Q	Q	Q	Q	Q	G	G	G	_	_
_	_	_	_	_	G	G	G	G	G	G	G	G	G	G	G	_	_	_	_	_
"""


# ============================================================
# FRONT
# ============================================================

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
G	G	G	X	X	X	X	X	X	X	X	X	X	X	X	X	G	G	G
G	G	G	X	X	X	X	X	X	X	X	X	X	X	X	X	G	G	G
G	G	G	X	X	X	X	X	X	X	X	X	X	X	X	X	G	G	G
G	G	G	X	X	X	X	X	X	X	X	X	X	X	X	X	G	G	G
G	G	G	X	X	X	X	X	X	X	X	X	X	X	X	X	G	G	G
G	G	G	X	X	X	X	X	X	X	X	X	X	X	X	X	G	G	G
G	G	G	X	X	X	X	X	X	X	X	X	X	X	X	X	G	G	G
G	G	G	X	X	X	X	X	X	X	X	X	X	X	X	X	G	G	G
G	G	G	X	X	X	X	X	X	X	X	X	X	X	X	X	G	G	G
_	G	G	X	X	X	X	X	X	X	X	X	X	X	X	X	G	G	_
_	G	G	G	X	X	X	X	X	X	X	X	X	X	X	G	G	G	_
_	_	G	G	G	X	X	X	X	X	X	X	X	X	G	G	G	_	_
_	_	_	_	_	G	G	G	G	G	G	G	G	G	G	G	_	_	_	_	_
"""


# ============================================================
# PARSE
# ============================================================

layer_back = parse_layer(layer_back_text)
layer_middle = parse_layer(layer_middle_text)
layer_front = parse_layer(layer_front_text)

layers = [
    layer_back,
    layer_middle,
    layer_front
]


# ============================================================
# MARKER削除
# ============================================================

def remove_markers():

    m.execute(
        'kill @e[type=marker,tag=cr_trapdoor]'
    )

    m.execute(
        'kill @e[type=marker,tag=cr_b]'
    )


# ============================================================
# BUILD
# ============================================================

def build_layers():

    # --------------------------------------------------------
    # 既存マーカー削除
    # --------------------------------------------------------

    remove_markers()

    # --------------------------------------------------------
    # ステージ生成
    # --------------------------------------------------------

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

                # ------------------------------------------------
                # ブロック配置
                # ------------------------------------------------

                m.execute(
                    f"/setblock {bx} {by} {bz} minecraft:{block}"
                )

                # ------------------------------------------------
                # Trapdoor位置をMarker登録
                # ------------------------------------------------

                if char == "D":

                    m.execute(
                        f'/summon marker {bx} {by} {bz} '
                        f'{{Tags:["cr_trapdoor"]}}'
                    )

                # ------------------------------------------------
                # B位置をMarker登録
                #
                # B と B1 の両方を対象
                # ------------------------------------------------

                if char == "B" or char == "B1":

                    m.execute(
                        f'/summon marker {bx} {by} {bz} '
                        f'{{Tags:["cr_b"]}}'
                    )


# ============================================================
# MAIN
# ============================================================

def main():

    arg = sys.argv[1] if len(sys.argv) > 1 else "flat"

    # --------------------------------------------------------
    # FLAT
    # --------------------------------------------------------

    if arg == "flat":

        flatten_area()

        return

    # --------------------------------------------------------
    # SET
    # --------------------------------------------------------

    if arg == "set":

        build_layers()

        return


main()