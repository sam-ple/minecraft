# ============================================================
# LINERACE COURSE GENERATOR
# Version : v0.2.20
#
# Minecraft Java Edition + Minescript
#
# Features
#   ・5レーン直線コース
#   ・1レーンずつ生成
#   ・200ブロック単位で区切って生成
#   ・区間ごとにプレイヤーを次地点へTP
#   ・地形追従
#   ・getblocklist() による高速地面探索
#   ・一番上の床を取得
#   ・地面上の雪はウール化
#   ・木の葉などの上の雪は無視
#   ・同一高度区間は fill
#   ・生成途中保存
#   ・途中から再開可能
#   ・reset による完全リセット
#
# Commands
#   set
#   reset
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

BLOCK_SPACING = 2

TOTAL_LENGTH = 1000

# ------------------------------------------------------------
# ★ 安定性重視
# 200ブロックごとに区切る
# ------------------------------------------------------------

CHUNK_LENGTH = 200

# 地形探索の細かい単位
SLICE_LENGTH = 50

# ------------------------------------------------------------
# TP設定
# ------------------------------------------------------------

TP_AFTER_SEGMENT = True

# TP時に少し手前へ
TP_OFFSET = 10

# プレイヤーを地面から何ブロック上に置くか
TP_HEIGHT = 3

# ------------------------------------------------------------
# 進行方向
# Z+
# ------------------------------------------------------------

FX, FZ = 0, 1

# 横方向
RX, RZ = 1, 0


# ============================================================
# COLORS
# ============================================================

COLORS = [
    "white",
    "orange",
    "light_blue",
    "lime",
    "yellow"
]


# ============================================================
# SURFACE SETTINGS
# ============================================================

SURFACE_SEARCH_UP = 8
SURFACE_SEARCH_DOWN = 20


# ============================================================
# NORMAL GROUND
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
    "minecraft:dirt_path",
    "minecraft:mycelium",
}


# ============================================================
# SNOW
# ============================================================

SNOW_BLOCKS = {
    "minecraft:snow",
    "minecraft:snow_block",
}


# ============================================================
# BLOCKS THAT SHOULD BE IGNORED
#
# 木の上など
# ============================================================

IGNORE_BLOCKS = {
    "minecraft:oak_leaves",
    "minecraft:spruce_leaves",
    "minecraft:birch_leaves",
    "minecraft:jungle_leaves",
    "minecraft:acacia_leaves",
    "minecraft:dark_oak_leaves",
    "minecraft:mangrove_leaves",
    "minecraft:cherry_leaves",
    "minecraft:azalea_leaves",
    "minecraft:flowering_azalea_leaves",

    "minecraft:oak_log",
    "minecraft:spruce_log",
    "minecraft:birch_log",
    "minecraft:jungle_log",
    "minecraft:acacia_log",
    "minecraft:dark_oak_log",
    "minecraft:mangrove_log",
    "minecraft:cherry_log",

    "minecraft:oak_wood",
    "minecraft:spruce_wood",
    "minecraft:birch_wood",
    "minecraft:jungle_wood",
    "minecraft:acacia_wood",
    "minecraft:dark_oak_wood",
    "minecraft:mangrove_wood",
    "minecraft:cherry_wood",
}


# ============================================================
# DATA
# ============================================================

BASE_DIR = "minescript/data/linerace"

os.makedirs(
    BASE_DIR,
    exist_ok=True
)

LANES_FILE = f"{BASE_DIR}/lanes.json"
STATE_FILE = f"{BASE_DIR}/progress.json"
TIME_FILE = f"{BASE_DIR}/timelog.json"


# ============================================================
# BLOCK NORMALIZATION
# ============================================================

def normalize_block(block):

    if not isinstance(block, str):
        return ""

    return block.split("[", 1)[0]


# ============================================================
# BLOCK CHECK
# ============================================================

def is_ground(block):

    return (
        normalize_block(block)
        in GROUND_BLOCKS
    )


def is_snow(block):

    return (
        normalize_block(block)
        in SNOW_BLOCKS
    )


def is_ignored(block):

    return (
        normalize_block(block)
        in IGNORE_BLOCKS
    )


# ============================================================
# INITIAL STATE
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
            "start": [
                sx,
                py,
                sz
            ],
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
        "current_lane": 0,
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
# SEARCH Y
# ============================================================

def make_search_ys(last_y):

    return list(
        range(
            last_y + SURFACE_SEARCH_UP,
            last_y - SURFACE_SEARCH_DOWN - 1,
            -1
        )
    )


# ============================================================
# FIND SURFACE
# ============================================================

def find_surface(
    blocks,
    search_ys
):

    # --------------------------------------------------------
    # 上から順番に見る
    # --------------------------------------------------------

    for index, block in enumerate(blocks):

        block_name = normalize_block(block)

        # ----------------------------------------------------
        # 雪
        #
        # 雪の場合は、その下が通常の地面か確認する
        # ----------------------------------------------------

        if is_snow(block):

            if index + 1 < len(blocks):

                below = normalize_block(
                    blocks[index + 1]
                )

                # 地面上の雪
                if below in GROUND_BLOCKS:

                    return search_ys[index]

                # 木の葉などの上の雪
                if below in IGNORE_BLOCKS:

                    continue

        # ----------------------------------------------------
        # 通常の地面
        # ----------------------------------------------------

        if is_ground(block):

            return search_ys[index]

        # ----------------------------------------------------
        # 木・葉など
        #
        # ここでは無視してさらに下を探す
        # ----------------------------------------------------

        if is_ignored(block):

            continue

    return None


# ============================================================
# GENERATE HEIGHTS
# ============================================================

def generate_lane_heights_fast(
    lane,
    start_distance,
    end_distance
):

    sx, sy, sz = lane["start"]

    heights = {}

    current_y = lane["last_y"]

    for distance in range(
        start_distance,
        end_distance
    ):

        x = sx + FX * distance
        z = sz + FZ * distance

        search_ys = make_search_ys(
            current_y
        )

        positions = [
            [x, y, z]
            for y in search_ys
        ]

        blocks = m.getblocklist(
            positions
        )

        found_y = find_surface(
            blocks,
            search_ys
        )

        if found_y is None:

            m.echo(
                f"WARNING "
                f"lane={lane['color']} "
                f"x={x} "
                f"z={z} "
                f"last_y={current_y}"
            )

            found_y = current_y

        heights[distance] = found_y

        current_y = found_y

    return heights


# ============================================================
# SET BLOCK
# ============================================================

def set_lane_block(
    lane,
    distance,
    ground_y
):

    sx, sy, sz = lane["start"]

    x = sx + FX * distance
    z = sz + FZ * distance

    block = (
        f"minecraft:{lane['color']}_wool"
    )

    m.execute(
        f"setblock "
        f"{x} {ground_y} {z} "
        f"{block}"
    )


# ============================================================
# FILL
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

    block = (
        f"minecraft:{lane['color']}_wool"
    )

    # --------------------------------------------------------
    # 1 block
    # --------------------------------------------------------

    if start_distance == end_distance:

        set_lane_block(
            lane,
            start_distance,
            ground_y
        )

        return

    # --------------------------------------------------------
    # Z direction
    # --------------------------------------------------------

    if FX == 0:

        min_x = x1
        max_x = x1

        min_z = min(
            z1,
            z2
        )

        max_z = max(
            z1,
            z2
        )

    else:

        min_x = min(
            x1,
            x2
        )

        max_x = max(
            x1,
            x2
        )

        min_z = z1
        max_z = z1

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
# APPLY
# ============================================================

def apply_lane_heights(
    lane,
    heights,
    start_distance,
    end_distance
):

    if not heights:
        return

    fill_start = None
    fill_y = None

    for distance in range(
        start_distance,
        end_distance
    ):

        ground_y = heights[distance]

        if fill_start is None:

            fill_start = distance
            fill_y = ground_y

            continue

        if ground_y == fill_y:

            continue

        fill_lane_range(
            lane,
            fill_start,
            distance - 1,
            fill_y
        )

        fill_start = distance
        fill_y = ground_y

    if fill_start is not None:

        fill_lane_range(
            lane,
            fill_start,
            end_distance - 1,
            fill_y
        )

    last_distance = end_distance - 1

    lane["last_y"] = (
        heights[last_distance]
    )

    if last_distance > start_distance:

        lane["prev_y"] = (
            heights[last_distance - 1]
        )


# ============================================================
# FIND TP Y
# ============================================================

def find_tp_y(
    lane,
    distance
):

    sx, sy, sz = lane["start"]

    x = sx + FX * distance
    z = sz + FZ * distance

    search_ys = make_search_ys(
        lane["last_y"]
    )

    positions = [
        [x, y, z]
        for y in search_ys
    ]

    blocks = m.getblocklist(
        positions
    )

    found = find_surface(
        blocks,
        search_ys
    )

    if found is None:

        return lane["last_y"]

    return found


# ============================================================
# TP PLAYER
# ============================================================

def teleport_to_next_area(
    lane,
    distance
):

    if not TP_AFTER_SEGMENT:
        return

    target_distance = max(
        0,
        distance - TP_OFFSET
    )

    y = find_tp_y(
        lane,
        target_distance
    )

    sx, sy, sz = lane["start"]

    x = sx + FX * target_distance
    z = sz + FZ * target_distance

    tp_y = y + TP_HEIGHT

    m.execute(
        f"tp @s "
        f"{x} {tp_y} {z}"
    )

    m.echo(
        f"TP -> "
        f"{x} {tp_y} {z}"
    )

    # --------------------------------------------------------
    # チャンク読み込み待ち
    # --------------------------------------------------------

    time.sleep(0.5)


# ============================================================
# GENERATE ONE SEGMENT
# ============================================================

def generate_segment(
    lane,
    start_distance,
    end_distance
):

    current = start_distance

    while current < end_distance:

        slice_end = min(
            current + SLICE_LENGTH,
            end_distance
        )

        heights = (
            generate_lane_heights_fast(
                lane,
                current,
                slice_end
            )
        )

        apply_lane_heights(
            lane,
            heights,
            current,
            slice_end
        )

        current = slice_end


# ============================================================
# GENERATE ONE LANE
# ============================================================

def generate_one_lane(
    lane_index,
    lane
):

    m.echo(
        "--------------------------------"
    )

    m.echo(
        f"LANE "
        f"{lane_index + 1}/{LINE_COUNT} "
        f"{lane['color']}"
    )

    current = 0

    total_start = time.time()

    while current < TOTAL_LENGTH:

        end_distance = min(
            current + CHUNK_LENGTH,
            TOTAL_LENGTH
        )

        m.echo(
            f"SEGMENT "
            f"{current}-{end_distance}"
        )

        segment_start = time.time()

        # ----------------------------------------------------
        # 200 block generation
        # ----------------------------------------------------

        generate_segment(
            lane,
            current,
            end_distance
        )

        elapsed = round(
            time.time() - segment_start,
            2
        )

        current = end_distance

        m.echo(
            f"{lane['color']} "
            f"{current}/{TOTAL_LENGTH} "
            f"| {elapsed}s"
        )

        # ----------------------------------------------------
        # 次の200へTP
        # ----------------------------------------------------

        if current < TOTAL_LENGTH:

            teleport_to_next_area(
                lane,
                current
            )

            # ------------------------------------------------
            # 少し待つ
            # ------------------------------------------------

            time.sleep(0.5)

    total_elapsed = round(
        time.time() - total_start,
        2
    )

    m.echo(
        f"LANE COMPLETE "
        f"{lane['color']} "
        f"| {total_elapsed}s"
    )


# ============================================================
# COURSE GENERATION
# ============================================================

def generate_course():

    state = load_state()

    current_lane = state.get(
        "current_lane",
        0
    )

    lanes = state["lanes"]

    if os.path.exists(TIME_FILE):

        with open(
            TIME_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            time_log = json.load(f)

    else:

        time_log = {}

    total_start = time.time()

    m.echo(
        "================================"
    )

    m.echo(
        "LineRace Course Generator"
    )

    m.echo(
        f"Length : {TOTAL_LENGTH}"
    )

    m.echo(
        f"Segment : {CHUNK_LENGTH}"
    )

    m.echo(
        f"Current Lane : "
        f"{current_lane + 1}/{LINE_COUNT}"
    )

    m.echo(
        "================================"
    )

    # ========================================================
    # ONE LANE AT A TIME
    # ========================================================

    for lane_index in range(
        current_lane,
        LINE_COUNT
    ):

        lane = lanes[lane_index]

        lane_start = time.time()

        generate_one_lane(
            lane_index,
            lane
        )

        lane_elapsed = round(
            time.time() - lane_start,
            2
        )

        # ----------------------------------------------------
        # Save
        # ----------------------------------------------------

        state["current_lane"] = (
            lane_index + 1
        )

        state["current_length"] = 0

        state["lanes"] = lanes

        save_state(state)

        time_log[
            f"lane_{lane_index + 1}"
        ] = lane_elapsed

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

    # ========================================================
    # COMPLETE
    # ========================================================

    total_elapsed = round(
        time.time() - total_start,
        2
    )

    m.echo(
        "================================"
    )

    m.echo(
        "COURSE COMPLETE"
    )

    m.echo(
        f"{LINE_COUNT} lanes"
    )

    m.echo(
        f"{TOTAL_LENGTH} blocks"
    )

    m.echo(
        f"TOTAL TIME : "
        f"{total_elapsed}s"
    )

    m.echo(
        "================================"
    )

    if os.path.exists(
        STATE_FILE
    ):

        os.remove(
            STATE_FILE
        )


# ============================================================
# RESET
# ============================================================

def reset_course():

    removed = 0

    for path in [
        STATE_FILE,
        LANES_FILE,
        TIME_FILE
    ]:

        if os.path.exists(path):

            os.remove(path)

            removed += 1

    m.echo(
        f"LineRace reset complete "
        f"({removed} files removed)"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    if len(sys.argv) < 2:

        m.echo(
            "Usage: set / reset"
        )

        sys.exit()

    command = sys.argv[1]

    if command == "set":

        generate_course()

    elif command == "reset":

        reset_course()

    else:

        m.echo(
            f"Unknown command: {command}"
        )