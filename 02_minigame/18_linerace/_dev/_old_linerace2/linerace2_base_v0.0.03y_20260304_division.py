import minescript as m
import json, os, math, sys, time

# ===============================
# 設定（ここを変更）
# ===============================

TOTAL_LENGTH = 2000        # 総延長
SEGMENT_LENGTH = 200       # 分割長
LINE_COUNT = 5
BLOCK_SPACING = 2

FX, FZ = 0, 1              # 南向き
RX, RZ = 1, 0

COLORS = ["white","orange","light_blue","lime","yellow"]

BASE_DIR = "minescript"
os.makedirs(BASE_DIR, exist_ok=True)

STATE_FILE = f"{BASE_DIR}/linerace_progress.json"

GROUND_BLOCKS = {
    "minecraft:dirt",
    "minecraft:grass_block[snowy=false]",
    "minecraft:grass_block[snowy=true]",
    "minecraft:sand","minecraft:gravel",
    "minecraft:stone","minecraft:andesite",
    "minecraft:diorite","minecraft:granite"
}

SEARCH_UP = 6
SEARCH_DOWN = 20


# ===============================
# 地面探索（軽量版）
# ===============================
def find_ground(x, last_y, z):

    # ±3のみ（高速化）
    for dy in range(3, -4, -1):
        y = last_y + dy
        if m.getblock(x, y+1, z) in GROUND_BLOCKS:
            return y

    # 保険探索（狭め）
    for dy in range(SEARCH_UP, -SEARCH_DOWN-1, -1):
        y = last_y + dy
        if m.getblock(x, y+1, z) in GROUND_BLOCKS:
            return y

    return last_y


# ===============================
# 初期化 or 再開ロード
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

    state = {
        "current_length": 0,
        "lanes": lanes
    }

    return state


# ===============================
# セグメント実行
# ===============================
def run():

    state = load_or_init()
    current_length = state["current_length"]
    lanes = state["lanes"]

    while current_length < TOTAL_LENGTH:

        segment_end = min(current_length + SEGMENT_LENGTH, TOTAL_LENGTH)

        # ===== forceload 範囲 =====
        base_x, base_y, base_z = lanes[0]["start"]

        start_x = base_x + FX * current_length
        start_z = base_z + FZ * current_length
        end_x   = base_x + FX * segment_end
        end_z   = base_z + FZ * segment_end

        cx1 = (start_x - 16) // 16
        cz1 = (start_z - 16) // 16
        cx2 = (end_x + LINE_COUNT*BLOCK_SPACING + 16) // 16
        cz2 = (end_z + LINE_COUNT*BLOCK_SPACING + 16) // 16

        m.execute(f"forceload add {cx1} {cz1} {cx2} {cz2}")
        m.echo(f"Segment {current_length} → {segment_end}")

        # ===== 描画 =====
        for d in range(current_length, segment_end):

            for i, lane in enumerate(lanes):

                sx, sy, sz = lane["start"]
                x = sx + FX*d
                z = sz + FZ*d

                last_y = lane["last_y"]
                ground_y = find_ground(x, last_y, z)

                block = f"minecraft:{COLORS[i]}_wool"
                m.execute(f"setblock {x} {ground_y+1} {z} {block}")

                lane["last_y"] = ground_y

        # ===== 進捗保存 =====
        current_length = segment_end
        state["current_length"] = current_length

        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)

        # ===== forceload解除 =====
        m.execute(f"forceload remove {cx1} {cz1} {cx2} {cz2}")

        time.sleep(0.1)  # TPS回復

    m.echo("COURSE COMPLETE.")
    os.remove(STATE_FILE)


# ===============================
# 実行
# ===============================
if __name__ == "__main__":
    run()
