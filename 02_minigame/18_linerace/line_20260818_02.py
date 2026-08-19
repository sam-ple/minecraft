# ============================================================
# LINERACE COURSE GENERATOR
# Version : v0.2.01
#
# Minecraft Java Edition + Minescript
#
# Features
#   ・5レーン
#   ・地形完全追従
#   ・崖、坂、段差対応
#   ・各レーン独立地形判定
#   ・途中保存
#   ・途中から再開可能
#
# Command
#   set
#
# ============================================================

import minescript as m
import json
import os
import math
import sys
import time


# ============================================================
# COURSE SETTINGS
# ============================================================

LINE_COUNT = 5

# レーン間隔
BLOCK_SPACING = 2

# コース長
TOTAL_LENGTH = 1000

# 何ブロックごとに保存
SAVE_INTERVAL = 50

# 進行方向
# Z+
FX, FZ = 0, 1

# 横方向
RX, RZ = 1, 0

# レーンカラー
COLORS = [
    "white",
    "orange",
    "light_blue",
    "lime",
    "yellow"
]


# ============================================================
# GROUND SETTINGS
# ============================================================

GROUND_BLOCKS = {
    "minecraft:dirt",
    "minecraft:grass_block",
    "minecraft:sand",
    "minecraft:gravel",
    "minecraft:stone",
    "minecraft:andesite",
    "minecraft:diorite",
    "minecraft:granite",
    "minecraft:podzol",
    "minecraft:coarse_dirt",
    "minecraft:mossy_cobblestone",
    "minecraft:dirt_path",
}


# 前回Yから上に何ブロック探すか
SEARCH_UP = 6

# 前回Yから下に何ブロック探すか
SEARCH_DOWN = 20


# ============================================================
# DATA
# ============================================================

BASE_DIR = "minescript/data/linerace"

os.makedirs(BASE_DIR, exist_ok=True)

LANES_FILE = f"{BASE_DIR}/lanes.json"
STATE_FILE = f"{BASE_DIR}/progress.json"
TIME_FILE = f"{BASE_DIR}/timelog.json"


# ============================================================
# BLOCK NORMALIZE
# ============================================================

def normalize_block(block):

    if not isinstance(block, str):
        return ""

    # minecraft:grass_block[snowy=false]
    # ↓
    # minecraft:grass_block

    return block.split("[", 1)[0]


# ============================================================
# GROUND CHECK
# ============================================================

def is_ground(block):

    return normalize_block(block) in GROUND_BLOCKS


# ============================================================
# FIND GROUND
# ============================================================

def find_ground(x, last_y, z):

    # --------------------------------------------------------
    # まず前回Yの周辺を探す
    # --------------------------------------------------------

    for dy in range(
        3,
        -4,
        -1
    ):

        y = last_y + dy

        block = m.getblock(
            x,
            y,
            z
        )

        if is_ground(block):

            return y

    # --------------------------------------------------------
    # 広範囲探索
    # --------------------------------------------------------

    for dy in range(
        SEARCH_UP,
        -SEARCH_DOWN - 1,
        -1
    ):

        y = last_y + dy

        block = m.getblock(
            x,
            y,
            z
        )

        if is_ground(block):

            return y

    # --------------------------------------------------------
    # 地面が見つからなかった
    # --------------------------------------------------------

    return None


# ============================================================
# INITIALIZE
# ============================================================

def create_state():

    px, py, pz = map(
        math.floor,
        m.player_position()
    )

    lanes = []

    for i in range(LINE_COUNT):

        offset = i * BLOCK_SPACING

        sx = px + RX * offset
        sz = pz + RZ * offset

        lanes.append({
            "player": "",
            "start": [
                sx,
                py,
                sz
            ],
            "last_y": py,
            "color": COLORS[i]
        })

    # --------------------------------------------------------
    # lanes.json
    # --------------------------------------------------------

    lane_data = {
        "lanes": lanes,
        "course_length": TOTAL_LENGTH
    }

    with open(
        LANES_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            lane_data,
            f,
            indent=2,
            ensure_ascii=False
        )

    # --------------------------------------------------------
    # state
    # --------------------------------------------------------

    state = {
        "current_length": 0,
        "lanes": lanes,
        "start_pos": [
            px,
            py,
            pz
        ]
    }

    save_state(state)

    return state


# ============================================================
# LOAD STATE
# ============================================================

def load_state():

    if os.path.exists(STATE_FILE):

        with open(
            STATE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    return create_state()


# ============================================================
# SAVE STATE
# ============================================================

def save_state(state):

    with open(
        STATE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            state,
            f,
            indent=2,
            ensure_ascii=False
        )


# ============================================================
# GENERATE ONE BLOCK
# ============================================================

def generate_block(lane, distance):

    sx, sy, sz = lane["start"]

    # --------------------------------------------------------
    # 座標
    # --------------------------------------------------------

    x = sx + FX * distance
    z = sz + FZ * distance

    # --------------------------------------------------------
    # 地面探索
    # --------------------------------------------------------

    ground_y = find_ground(
        x,
        lane["last_y"],
        z
    )

    # --------------------------------------------------------
    # 地面が見つからなかった場合
    # --------------------------------------------------------

    if ground_y is None:

        m.echo(
            f"GROUND NOT FOUND "
            f"x={x} z={z} "
            f"last_y={lane['last_y']}"
        )

        return False

    # --------------------------------------------------------
    # ウール
    # --------------------------------------------------------

    block = f"minecraft:{lane['color']}_wool"

    # --------------------------------------------------------
    # 地面そのものを置換
    # --------------------------------------------------------

    m.execute(
        f"setblock "
        f"{x} {ground_y} {z} "
        f"{block}"
    )

    # --------------------------------------------------------
    # Y更新
    # --------------------------------------------------------

    lane["last_y"] = ground_y

    return True


# ============================================================
# GENERATE COURSE
# ============================================================

def generate_course():

    state = load_state()

    current = state["current_length"]

    lanes = state["lanes"]

    # --------------------------------------------------------
    # Time log
    # --------------------------------------------------------

    if os.path.exists(TIME_FILE):

        with open(
            TIME_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            time_log = json.load(f)

    else:

        time_log = {}

    # --------------------------------------------------------
    # Start
    # --------------------------------------------------------

    m.echo(
        f"LineRace START "
        f"{current}/{TOTAL_LENGTH}"
    )

    total_start = time.time()

    # ========================================================
    # MAIN
    # ========================================================

    while current < TOTAL_LENGTH:

        start_time = time.time()

        # ----------------------------------------------------
        # 5レーン
        # ----------------------------------------------------

        for lane_index, lane in enumerate(lanes):

            ok = generate_block(
                lane,
                current
            )

            if not ok:

                m.echo(
                    f"STOP "
                    f"lane={lane_index + 1} "
                    f"distance={current}"
                )

                state["lanes"] = lanes

                save_state(state)

                return

        # ----------------------------------------------------
        # 進行
        # ----------------------------------------------------

        current += 1

        state["current_length"] = current
        state["lanes"] = lanes

        # ----------------------------------------------------
        # 保存
        # ----------------------------------------------------

        if (
            current % SAVE_INTERVAL == 0
            or current >= TOTAL_LENGTH
        ):

            elapsed = round(
                time.time() - start_time,
                3
            )

            total_elapsed = round(
                time.time() - total_start,
                2
            )

            time_log[
                str(current)
            ] = elapsed

            save_state(state)

            with open(
                TIME_FILE,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    time_log,
                    f,
                    indent=2,
                    ensure_ascii=False
                )

            m.echo(
                f"{current}/{TOTAL_LENGTH} "
                f"| {elapsed}s "
                f"| total {total_elapsed}s"
            )

    # ========================================================
    # COMPLETE
    # ========================================================

    total_elapsed = round(
        time.time() - total_start,
        2
    )

    m.echo(
        f"COURSE COMPLETE "
        f"| {TOTAL_LENGTH} blocks "
        f"| {total_elapsed}s"
    )

    # --------------------------------------------------------
    # progress削除
    # --------------------------------------------------------

    if os.path.exists(STATE_FILE):

        os.remove(STATE_FILE)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    if len(sys.argv) < 2:

        m.echo(
            "Usage: set"
        )

        sys.exit()

    command = sys.argv[1]

    if command == "set":

        generate_course()

    else:

        m.echo(
            f"Unknown command: {command}"
        )