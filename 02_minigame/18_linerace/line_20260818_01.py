# ============================================================
# LINERACE COURSE GENERATOR
# Version : v0.2.00
#
# Minecraft Java Edition + Minescript
#
# Features
#   ・5レーン直線コース
#   ・地形追従
#   ・getblocklist() による高速地面探索
#   ・同一高度区間は fill
#   ・生成途中保存
#   ・途中から再開可能
#
# Command
#   set
#
# Data Directory
#   minescript/data/linerace/
#
# Author : crocado
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

# 1回に処理する距離
SLICE_LENGTH = 50

# 何ブロックごとに保存するか
SAVE_INTERVAL = 100

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

# 地面として扱うブロック
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

# 前回Yからの探索範囲
SEARCH_UP = 6
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
# BLOCK TYPE NORMALIZATION
# ============================================================

def normalize_block(block):
    """
    minecraft:grass_block[snowy=false]
    ↓
    minecraft:grass_block
    """

    if not isinstance(block, str):
        return ""

    return block.split("[", 1)[0]


# ============================================================
# GROUND CHECK
# ============================================================

def is_ground(block):
    return normalize_block(block) in GROUND_BLOCKS


# ============================================================
# INITIALIZE
# ============================================================

def create_initial_state():

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
            "start": [sx, py, sz],
            "last_y": py,
            "prev_y": py,
            "color": COLORS[i]
        })

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

    state = {
        "current_length": 0,
        "lanes": lanes,
        "start_pos": [px, py, pz]
    }

    save_state(state)

    return state


# ============================================================
# LOAD / INITIALIZE
# ============================================================

def load_state():

    if os.path.exists(STATE_FILE):

        with open(
            STATE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    return create_initial_state()


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
# GET SEARCH Y VALUES
# ============================================================

def make_search_ys(last_y):

    """
    前回Yを中心に探索する。

    例:
        last_y = 70

        76
        75
        ...
        70
        ...
        50
    """

    return list(
        range(
            last_y + SEARCH_UP,
            last_y - SEARCH_DOWN - 1,
            -1
        )
    )


# ============================================================
# FIND GROUND FOR ALL LANES
# ============================================================

def find_ground_all_lanes(lanes, distance):
    """
    5レーンの地面をまとめて探索。

    getblocklist() を使って、
    各レーン × 各Y のブロックを一括取得する。
    """

    positions = []
    candidates = []

    # --------------------------------------------------------
    # 探索座標を作る
    # --------------------------------------------------------

    for lane_index, lane in enumerate(lanes):

        sx, sy, sz = lane["start"]

        x = sx + FX * distance
        z = sz + FZ * distance

        search_ys = make_search_ys(
            lane["last_y"]
        )

        lane_candidates = []

        for y in search_ys:

            positions.append([
                x,
                y,
                z
            ])

            lane_candidates.append(y)

        candidates.append(lane_candidates)

    # --------------------------------------------------------
    # 一括取得
    # --------------------------------------------------------

    blocks = m.getblocklist(positions)

    # --------------------------------------------------------
    # 各レーンの地面を決定
    # --------------------------------------------------------

    results = []

    index = 0

    for lane_index, lane in enumerate(lanes):

        found_y = None

        for y in candidates[lane_index]:

            block = blocks[index]

            index += 1

            if is_ground(block):

                found_y = y

                break

        # ----------------------------------------------------
        # 見つからなかった場合
        # ----------------------------------------------------

        if found_y is None:

            found_y = lane["last_y"]

        results.append(found_y)

    return results


# ============================================================
# SET BLOCK
# ============================================================

def set_lane_block(lane, distance, ground_y):

    sx, sy, sz = lane["start"]

    x = sx + FX * distance
    z = sz + FZ * distance

    block = f"minecraft:{lane['color']}_wool"

    m.execute(
        f"setblock {x} {ground_y} {z} {block}"
    )


# ============================================================
# FILL RANGE
# ============================================================

def fill_lane_range(
    lane,
    start_distance,
    end_distance,
    ground_y
):

    if end_distance < start_distance:
        return

    sx, sy, sz = lane["start"]

    x1 = sx + FX * start_distance
    z1 = sz + FZ * start_distance

    x2 = sx + FX * end_distance
    z2 = sz + FZ * end_distance

    block = f"minecraft:{lane['color']}_wool"

    # --------------------------------------------------------
    # Z方向
    # --------------------------------------------------------

    if FX == 0:

        min_x = x1
        max_x = x1

        min_z = min(z1, z2)
        max_z = max(z1, z2)

    # --------------------------------------------------------
    # X方向
    # --------------------------------------------------------

    else:

        min_x = min(x1, x2)
        max_x = max(x1, x2)

        min_z = z1
        max_z = z1

    # --------------------------------------------------------
    # 1ブロック
    # --------------------------------------------------------

    if start_distance == end_distance:

        m.execute(
            f"setblock "
            f"{x1} {ground_y} {z1} "
            f"{block}"
        )

        return

    # --------------------------------------------------------
    # fill
    # --------------------------------------------------------

    m.execute(
        f"fill "
        f"{min_x} {ground_y} {min_z} "
        f"{max_x} {ground_y} {max_z} "
        f"{block}"
    )


# ============================================================
# GENERATE ONE SLICE
# ============================================================

def generate_slice(
    lanes,
    start_distance,
    end_distance
):

    # --------------------------------------------------------
    # 地形高さを保存
    #
    # heights[lane_index][distance]
    # --------------------------------------------------------

    heights = [
        {}
        for _ in range(LINE_COUNT)
    ]

    # --------------------------------------------------------
    # 地形探索
    # --------------------------------------------------------

    for distance in range(
        start_distance,
        end_distance
    ):

        ground_ys = find_ground_all_lanes(
            lanes,
            distance
        )

        for i, ground_y in enumerate(ground_ys):

            heights[i][distance] = ground_y

    # --------------------------------------------------------
    # 各レーンを配置
    # --------------------------------------------------------

    for lane_index, lane in enumerate(lanes):

        lane_heights = heights[lane_index]

        if not lane_heights:
            continue

        # ----------------------------------------------------
        # 現在のfill区間
        # ----------------------------------------------------

        fill_start = None
        fill_y = None

        # ----------------------------------------------------
        # 高さごとに処理
        # ----------------------------------------------------

        for distance in range(
            start_distance,
            end_distance
        ):

            ground_y = lane_heights[distance]

            # -----------------------------------------------
            # 初回
            # -----------------------------------------------

            if fill_start is None:

                fill_start = distance
                fill_y = ground_y

                continue

            # -----------------------------------------------
            # 高さが同じ
            # -----------------------------------------------

            if ground_y == fill_y:

                continue

            # -----------------------------------------------
            # 高さが変わった
            # -----------------------------------------------

            fill_lane_range(
                lane,
                fill_start,
                distance - 1,
                fill_y
            )

            fill_start = distance
            fill_y = ground_y

        # ----------------------------------------------------
        # 最後
        # ----------------------------------------------------

        if fill_start is not None:

            fill_lane_range(
                lane,
                fill_start,
                end_distance - 1,
                fill_y
            )

        # ----------------------------------------------------
        # Y履歴更新
        # ----------------------------------------------------

        last_distance = end_distance - 1

        last_y = lane_heights[last_distance]

        if last_distance > start_distance:

            prev_y = lane_heights[
                last_distance - 1
            ]

        else:

            prev_y = lane["last_y"]

        lane["prev_y"] = prev_y
        lane["last_y"] = last_y


# ============================================================
# COURSE GENERATION
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

    total_start = time.time()

    m.echo(
        f"LineRace course start: "
        f"{current}/{TOTAL_LENGTH}"
    )

    # --------------------------------------------------------
    # Generate
    # --------------------------------------------------------

    while current < TOTAL_LENGTH:

        end_distance = min(
            current + SLICE_LENGTH,
            TOTAL_LENGTH
        )

        start_time = time.time()

        generate_slice(
            lanes,
            current,
            end_distance
        )

        elapsed = round(
            time.time() - start_time,
            3
        )

        # ----------------------------------------------------
        # State
        # ----------------------------------------------------

        current = end_distance

        state["current_length"] = current
        state["lanes"] = lanes

        # ----------------------------------------------------
        # Log
        # ----------------------------------------------------

        time_log[
            f"{current - SLICE_LENGTH}-{current}"
        ] = elapsed

        # ----------------------------------------------------
        # Save
        # ----------------------------------------------------

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

        total_elapsed = round(
            time.time() - total_start,
            2
        )

        m.echo(
            f"{current}/{TOTAL_LENGTH} "
            f"| slice {elapsed}s "
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
    # 進捗削除
    # --------------------------------------------------------

    if os.path.exists(STATE_FILE):

        os.remove(STATE_FILE)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    if len(sys.argv) < 2:

        m.echo("Usage: set")

        sys.exit()

    command = sys.argv[1]

    if command == "set":

        generate_course()

    else:

        m.echo(
            f"Unknown command: {command}"
        )