import minescript as m
import json, os, math, time

# ===============================
# 設定
# ===============================
TOTAL_LENGTH = 2000
SEGMENT_LENGTH = 200
TIME_SLICE = 100

LINE_COUNT = 5
BLOCK_SPACING = 2

FX, FZ = 0, 1
RX, RZ = 1, 0

COLORS = ["white","orange","light_blue","lime","yellow"]

BASE_DIR = "minescript/data/linerace"
os.makedirs(BASE_DIR, exist_ok=True)

STATE_FILE = f"{BASE_DIR}/progress.json"
TIME_FILE  = f"{BASE_DIR}/timelog.json"

GROUND_BLOCKS = {
    "minecraft:dirt",
    "minecraft:grass_block[snowy=false]",
    "minecraft:grass_block[snowy=true]",
    "minecraft:sand",
    "minecraft:gravel",
    "minecraft:stone",
    "minecraft:andesite",
    "minecraft:diorite",
    "minecraft:granite"
}

SEARCH_UP = 6
SEARCH_DOWN = 20

# ===============================
# 地面探索
# ===============================
def find_ground(x, last_y, z):
    for dy in range(3, -4, -1):
        y = last_y + dy
        if m.getblock(x, y+1, z) in GROUND_BLOCKS:
            return y
    for dy in range(SEARCH_UP, -SEARCH_DOWN-1, -1):
        y = last_y + dy
        if m.getblock(x, y+1, z) in GROUND_BLOCKS:
            return y
    return last_y

# ===============================
# 安全TP
# ===============================
def safe_tp(x, z, approx_y):
    y = approx_y
    for dy in range(10, -20, -1):
        check_y = approx_y + dy
        if m.getblock(x, check_y, z) in GROUND_BLOCKS:
            m.execute(f"tp @p {x} {check_y+2} {z}")
            return check_y+2
    m.execute(f"tp @p {x} {approx_y+5} {z}")
    return approx_y+5

# ===============================
# 初期化
# ===============================
def load_or_init():

    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)

    px, py, pz = map(math.floor, m.player_position())

    lanes = []

    for i in range(LINE_COUNT):
        offset = i * BLOCK_SPACING
        sx = px + RX * offset
        sz = pz + RZ * offset
        lanes.append({
            "start": [sx, py, sz],
            "last_y": py
        })

    return {
        "current_length": 0,
        "lanes": lanes
    }

# ===============================
# メイン
# ===============================
def run():

    state = load_or_init()
    current = state["current_length"]
    lanes = state["lanes"]

    if os.path.exists(TIME_FILE):
        with open(TIME_FILE) as f:
            time_log = json.load(f)
    else:
        time_log = {}

    while current < TOTAL_LENGTH:

        segment_end = min(current + SEGMENT_LENGTH, TOTAL_LENGTH)

        while current < segment_end:

            slice_end = min(current + TIME_SLICE, segment_end)

            slice_start_time = time.time()

            for d in range(current, slice_end):

                for i, lane in enumerate(lanes):

                    sx, sy, sz = lane["start"]

                    x = sx + FX*d
                    z = sz + FZ*d

                    ground_y = find_ground(x, lane["last_y"], z)

                    block = f"minecraft:{COLORS[i]}_wool"
                    m.execute(f"setblock {x} {ground_y+1} {z} {block}")

                    lane["last_y"] = ground_y

            elapsed = round(time.time() - slice_start_time, 3)
            time_log[f"{current}-{slice_end}"] = elapsed

            current = slice_end
            state["current_length"] = current

            with open(STATE_FILE, "w") as f:
                json.dump(state, f, indent=2)

            with open(TIME_FILE, "w") as f:
                json.dump(time_log, f, indent=2)

            m.echo(f"{current} / {TOTAL_LENGTH}  ({elapsed}s)")

        # ===== セグメント終点へTP =====
        base_x, base_y, base_z = lanes[0]["start"]
        tp_x = base_x + FX*current
        tp_z = base_z + FZ*current

        new_y = safe_tp(tp_x, tp_z, lanes[0]["last_y"])
        time.sleep(0.3)

    m.echo("COURSE COMPLETE")
    os.remove(STATE_FILE)

# ===============================
if __name__ == "__main__":
    run()
