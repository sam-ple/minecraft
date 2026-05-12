import minescript
from minescript import execute
import time

# === プレイヤー位置 ===
x, y, z = map(int, minescript.player_position())

# 南向き
execute(f"/tp @p {x} {y} {z} 0 0")

# === ブロック定義 ===
block_map = {
    "_": None,
    "T": "target",
    "B": "barrier",
    "S": "sandstone",
    "G": "gold_block",
    "C": "white_stained_glass",
    "E": "emerald_block",
    "Q": "quartz_block",
    "D": "birch_trapdoor[facing=south,half=top,open=false]",

    "1": "sea_lantern","2": "sea_lantern","3": "sea_lantern",
    "4": "sea_lantern","5": "sea_lantern","6": "sea_lantern",
    "7": "sea_lantern","8": "sea_lantern","9": "sea_lantern",
    "10": "sea_lantern","11": "sea_lantern",
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
G	G	G	S	S	S	S	S	S	S	S	S	S	S	S	S	S	S	G	G	G
G	G	G	S	S	S	S	S	S	S	S	S	S	S	S	S	S	S	G	G	G
G	G	G	S	S	S	S	S	S	S	S	S	S	S	S	S	S	S	G	G	G
G	G	G	S	S	S	S	S	S	S	S	S	S	S	S	S	S	S	G	G	G
G	G	G	S	S	S	S	S	S	S	S	S	S	S	S	S	S	S	G	G	G
G	G	G	S	S	S	S	S	S	S	S	S	S	S	S	S	S	S	G	G	G
G	G	G	S	S	S	S	S	S	S	S	S	S	S	S	S	S	S	G	G	G
G	G	G	S	S	S	S	S	S	S	S	S	S	S	S	S	S	S	G	G	G
G	G	G	S	S	S	S	S	S	S	S	S	S	S	S	S	S	S	G	G	G
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
_	_	G	Q	Q	E	Q	D	Q	Q	E	Q	Q	D	Q	E	Q	Q	G	_	_
_	G	G	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	G	G	_
_	G	G	_	_	_	_	D	_	_	_	_	_	D	_	_	_	_	G	G	_
_	G	G	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	G	G	_
G	G	G	Q	D	Q	Q	D	Q	Q	D	Q	Q	D	Q	Q	D	Q	G	G	G
G	G	G	Q	_	Q	_	_	_	Q	_	Q	_	_	_	Q	_	Q	G	G	G
G	G	G	_	1	_	_	D	_	_	2	_	_	D	_	_	3	_	G	G	G
G	G	G	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	G	G	G
G	G	G	Q	D	Q	Q	D	Q	Q	D	Q	Q	D	Q	Q	D	Q	G	G	G
G	G	G	Q	_	Q	_	_	_	Q	_	Q	_	_	_	Q	_	Q	G	G	G
G	G	G	_	4	_	_	_	_	_	5	_	_	_	_	_	6	_	G	G	G
G	G	G	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	G	G	G
G	G	G	Q	Q	Q	D	Q	D	Q	D	Q	D	Q	D	Q	Q	Q	G	G	G
_	G	G	Q	Q	Q	_	Q	_	Q	_	Q	_	Q	_	Q	Q	Q	G	G	_
_	G	G	G	Q	Q	7	Q	8	Q	9	Q	10	Q	11	Q	Q	G	G	G	_
_	_	G	G	G	_	_	_	_	_	_	_	_	_	_	_	G	G	G	_	_
_	_	_	_	_	G	G	G	G	G	G	G	G	G	G	G	_	_	_	_	_
"""

# ==============================
# 手前（そのまま）
# ==============================
# ==============================
# レイヤー（手前）
# ==============================
layer_front_text = """
_	_	_	_	_	_	_	_	B	C	C	C	B	_	_	_	_	_	_	_	_
_	_	_	_	_	_	B	B	C	_	_	_	C	B	B	_	_	_	_	_	_
_	_	_	_	B	B	B	B	C	_	_	_	C	B	B	B	B	_	_	_	_
_	_	_	B	B	B	B	B	B	C	C	C	B	B	B	B	B	B	_	_	_
_	_	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	_	_
_	_	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	_	_
_	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	_
_	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	_
_	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	_
B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B
B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B
B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B
B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B
B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B
B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B
B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B
B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B
B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B
_	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	_
_	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	_
_	_	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	B	_	_
_	_	_	_	_	B	B	B	B	B	B	B	B	B	B	B	_	_	_	_	_
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
for dz, layer in enumerate(layers):
    for dy, row in enumerate(layer):
        for dx, char in enumerate(row):

            block = block_map.get(char)
            if block is None:
                continue

            width = len(layer[0])
            bx = x + dx - width // 2
            by = y + (len(layer) - 1 - dy)
            bz = z + (len(layers) - dz)

            execute(f"/setblock {bx} {by} {bz} minecraft:{block}")

    time.sleep(0.3)
