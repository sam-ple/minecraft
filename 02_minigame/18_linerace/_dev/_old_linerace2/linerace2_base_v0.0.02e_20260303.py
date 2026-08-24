import minescript as m
import json, os, math, sys
import time

BASE_DIR = "minescript"
os.makedirs(BASE_DIR, exist_ok=True)
LANES_FILE = f"{BASE_DIR}/linerace_lanes.json"

LINE_COUNT = 5
BLOCK_SPACING = 2

COURSE_LENGTH = 2000
TIME_LIMIT = 900
TOLERANCE = 1.2

# 前進方向（南向き）
FX, FZ = 0, 1
RX, RZ = 1, 0

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


# ===============================
# 前回y基準探索（高速安定版）
# ===============================
def find_ground_simple_fixed(x, last_y, z):

    # ① 近距離探索（±4）
    for dy in range(4, -5, -1):
        y = last_y + dy
        if m.getblock(x, y+1, z) in GROUND_BLOCKS:
            return y

    # ② 通常範囲探索
    for dy in range(SEARCH_UP, -SEARCH_DOWN-1, -1):
        y = last_y + dy
        if m.getblock(x, y+1, z) in GROUND_BLOCKS:
            return y

    return last_y


# ===============================
# set（ログ付き高速版）
# ===============================
def cmd_set():

    start_time = time.time()

    px, py, pz = map(math.floor, m.player_position())
    lanes = []

    # レーン初期化
    for i in range(LINE_COUNT):
        offset = i * BLOCK_SPACING
        sx = px + RX * offset
        sz = pz + RZ * offset
        lanes.append({
            "player": "",
            "start": [sx, py, sz],
            "color": COLORS[i],
            "last_y": py
        })

    # ===== チャンク事前読み込み =====
    chunk_start_x = (px - 32) // 16
    chunk_start_z = (pz - 32) // 16
    chunk_end_x = (px + FX * COURSE_LENGTH + RX * (LINE_COUNT-1) + 32) // 16
    chunk_end_z = (pz + FZ * COURSE_LENGTH + RZ * (LINE_COUNT-1) + 32) // 16

    m.execute(f"forceload add {chunk_start_x} {chunk_start_z} {chunk_end_x} {chunk_end_z}")
    m.echo(f"Chunks loaded: ({chunk_start_x},{chunk_start_z}) to ({chunk_end_x},{chunk_end_z})")

    # ===== コース生成 =====
    for d in range(COURSE_LENGTH):

        # 100ブロックごとにログ表示
        if d % 100 == 0 and d != 0:
            elapsed = time.time() - start_time
            bps = d / elapsed if elapsed > 0 else 0
            m.echo(f"Progress: {d}/{COURSE_LENGTH}  Time: {elapsed:.2f}s  Speed: {bps:.1f} blocks/sec")

        for lane in lanes:
            sx, sy, sz = lane["start"]
            x = sx + FX*d
            z = sz + FZ*d

            last_y = lane["last_y"]
            ground_y = find_ground_simple_fixed(x, last_y, z)

            block = f"minecraft:{lane['color']}_wool"
            m.execute(f"setblock {x} {ground_y+1} {z} {block}")

            lane["last_y"] = ground_y

    # JSON保存（last_y除外）
    data = {
        "lanes": [{k: v for k, v in lane.items() if k != "last_y"} for lane in lanes],
        "tolerance": TOLERANCE,
        "course_length": COURSE_LENGTH,
        "time_limit": TIME_LIMIT
    }

    with open(LANES_FILE, "w") as f:
        json.dump(data, f, indent=2)

    total_time = time.time() - start_time
    m.echo(f"SET_FAST complete. Total time: {total_time:.2f}s")


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

        back_x = sx - FX
        back_z = sz - FZ

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
