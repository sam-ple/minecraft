import minescript as m
import json, os, math, sys

BASE_DIR = "minescript"
os.makedirs(BASE_DIR, exist_ok=True)
LANES_FILE = f"{BASE_DIR}/linerace_lanes.json"

LINE_COUNT = 5
BLOCK_SPACING = 2

COURSE_LENGTH = 100      # 本番は2000に変更
TIME_LIMIT = 900
TOLERANCE = 1.2

# 前進方向（南向き）
FX, FZ = 0, 1
RX, RZ = 1, 0   # レーン横方向

COLORS = ["white","orange","light_blue","lime","yellow"]

GROUND_BLOCKS = {
    "minecraft:dirt",
    "minecraft:grass_block[snowy=false]",
    "minecraft:grass_block[snowy=true]",
    "minecraft:sand","minecraft:gravel",
    "minecraft:stone","minecraft:andesite",
    "minecraft:diorite","minecraft:granite"
}

SEARCH_UP = 12
SEARCH_DOWN = 60


def find_ground(x, sy, z):
    for y in range(sy + SEARCH_UP, sy - SEARCH_DOWN, -1):
        if m.getblock(x, y+1, z) in GROUND_BLOCKS:
            return y
    return None


# ===============================
# set（レーン生成）
# ===============================
def cmd_set():

    px, py, pz = map(math.floor, m.player_position())
    lanes = []

    for i in range(LINE_COUNT):
        offset = i * BLOCK_SPACING
        sx = px + RX * offset
        sz = pz + RZ * offset

        lanes.append({
            "player": "",      # ← 手動でJSON編集
            "start": [sx, py, sz],
            "color": COLORS[i]
        })

    # コース生成（地面追従）
    for d in range(COURSE_LENGTH):
        for lane in lanes:

            sx, sy, sz = lane["start"]
            x = sx + FX*d
            z = sz + FZ*d

            ground_y = find_ground(x, sy, z)
            if ground_y is None:
                continue

            block = f"minecraft:{lane['color']}_wool"
            m.execute(f"setblock {x} {ground_y+1} {z} {block}")

    data = {
        "lanes": lanes,
        "tolerance": TOLERANCE,
        "course_length": COURSE_LENGTH,
        "time_limit": TIME_LIMIT
    }

    with open(LANES_FILE, "w") as f:
        json.dump(data, f, indent=2)

    m.echo("SET complete. Edit JSON and write player names.")


# ===============================
# set2（プレイヤーヘッド設置）
# ===============================
def cmd_set2():

    if not os.path.exists(LANES_FILE):
        m.echo("JSON not found. Run set first.")
        return

    with open(LANES_FILE) as f:
        data = json.load(f)

    lanes = data["lanes"]

    for lane in lanes:
        player = lane["player"]
        if not player:
            continue

        sx, sy, sz = lane["start"]

        # スタート地点の「後ろ」に設置
        back_x = sx - FX
        back_z = sz - FZ

        # player_head設置（rotation=0で正面を向ける）
        m.execute(
            f'setblock {back_x} {sy+1} {back_z} '
            f'minecraft:player_head[rotation=8]{{profile:"{player}"}} replace'
        )

    m.echo("Player heads placed.")


# ===============================
# 実行分岐
# ===============================
if __name__ == "__main__":

    if len(sys.argv) < 2:
        m.echo("Usage: arg=set or arg=set2")
        sys.exit()

    arg = sys.argv[1]

    if arg == "set":
        cmd_set()

    elif arg == "set2":
        cmd_set2()

    else:
        m.echo("Unknown argument.")
