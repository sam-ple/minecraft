# ============================================================
# LINERACE COURSE GENERATOR
# Version : v0.4.00
#
# Minecraft Java Edition + Minescript
#
# Features
#   ・5レーン直線コース生成
#   ・各レーン独立の地形追従
#   ・崖 / 坂 / 段差対応
#   ・地形の最上面をウールに置換
#   ・雪があれば雪自体をウールに置換
#   ・途中保存
#   ・途中から再開可能
#   ・resetで生成状態をリセット
#
# Commands
#   set   : コース生成 / 途中から再開
#   reset : 生成状態をリセット
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

# 何ブロックごとに保存するか
SAVE_INTERVAL = 50


# ============================================================
# DIRECTION
# ============================================================

# 進行方向
# Z+
FX, FZ = 0, 1

# 横方向
RX, RZ = 1, 0


# ============================================================
# LANE COLORS
# ============================================================

COLORS = [
    "white",
    "orange",
    "light_blue",
    "lime",
    "yellow"
]


# ============================================================
# SURFACE BLOCKS
# ============================================================

# 「床」として認識するブロック
#
# その地点で上から探索し、
# 最初に見つかったものを床とする。
#
# snowも含めているため、
#
#   snow
#   grass_block
#   dirt
#
# の場合は snow をウールに置換する。
#
# ============================================================

SURFACE_BLOCKS = {

    "minecraft:dirt",

    "minecraft:grass_block",

    "minecraft:sand",

    "minecraft:red_sand",

    "minecraft:gravel",

    "minecraft:stone",

    "minecraft:andesite",

    "minecraft:diorite",

    "minecraft:granite",

    "minecraft:podzol",

    "minecraft:coarse_dirt",

    "minecraft:mossy_cobblestone",

    "minecraft:dirt_path",

    # 雪
    "minecraft:snow",
}


# ============================================================
# SEARCH SETTINGS
# ============================================================

# 通常探索
#
# 前回の高さの近くをまず探索する。
# 普通の地形ならここで見つかるので高速。
#
FAST_SEARCH_UP = 8
FAST_SEARCH_DOWN = 8


# ============================================================
# FALLBACK SEARCH
# ============================================================

# 通常探索で見つからなかった場合の
# 広範囲探索。
#
# 大きな崖や急激な地形変化に対応する。
#
FALLBACK_SEARCH_UP = 30
FALLBACK_SEARCH_DOWN = 120


# ============================================================
# DATA DIRECTORY
# ============================================================

BASE_DIR = "minescript/data/linerace"

os.makedirs(
    BASE_DIR,
    exist_ok=True
)


LANES_FILE = (
    f"{BASE_DIR}/lanes.json"
)

STATE_FILE = (
    f"{BASE_DIR}/progress.json"
)

TIME_FILE = (
    f"{BASE_DIR}/timelog.json"
)


# ============================================================
# BLOCK UTIL
# ============================================================

def normalize_block(block):
    """
    ブロック状態を除去する。

    例:

    minecraft:grass_block[snowy=false]

    ↓

    minecraft:grass_block
    """

    if not isinstance(block, str):
        return ""

    return block.split(
        "[",
        1
    )[0]


# ============================================================
# SURFACE CHECK
# ============================================================

def is_surface(block):

    return (
        normalize_block(block)
        in SURFACE_BLOCKS
    )


# ============================================================
# FIND SURFACE
# ============================================================

def find_surface(
    x,
    last_y,
    z
):
    """
    指定したX/Z地点の床を探す。

    1.
        前回Y周辺を高速探索

    2.
        見つからなければ広範囲探索

    最初に見つかったSURFACE_BLOCKSを
    その地点の床とする。
    """

    # ========================================================
    # 1. FAST SEARCH
    # ========================================================

    for dy in range(
        FAST_SEARCH_UP,
        -FAST_SEARCH_DOWN - 1,
        -1
    ):

        y = last_y + dy

        block = m.getblock(
            x,
            y,
            z
        )

        if is_surface(block):

            return y


    # ========================================================
    # 2. FALLBACK SEARCH
    # ========================================================

    for dy in range(
        FALLBACK_SEARCH_UP,
        -FALLBACK_SEARCH_DOWN - 1,
        -1
    ):

        y = last_y + dy

        block = m.getblock(
            x,
            y,
            z
        )

        if is_surface(block):

            return y


    # ========================================================
    # 3. NOT FOUND
    # ========================================================

    return None


# ============================================================
# CREATE INITIAL STATE
# ============================================================

def create_state():

    # 現在のプレイヤー位置
    px, py, pz = map(
        math.floor,
        m.player_position()
    )


    lanes = []


    # ========================================================
    # CREATE 5 LANES
    # ========================================================

    for i in range(
        LINE_COUNT
    ):

        offset = (
            i
            * BLOCK_SPACING
        )

        sx = (
            px
            + RX * offset
        )

        sz = (
            pz
            + RZ * offset
        )

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


    # ========================================================
    # SAVE LANES
    # ========================================================

    lane_data = {

        "lanes": lanes,

        "course_length":
            TOTAL_LENGTH

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


    # ========================================================
    # INITIAL STATE
    # ========================================================

    state = {

        "current_length": 0,

        "lanes": lanes,

        "start_pos": [
            px,
            py,
            pz
        ]

    }


    save_state(
        state
    )


    return state


# ============================================================
# LOAD STATE
# ============================================================

def load_state():

    if os.path.exists(
        STATE_FILE
    ):

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

def save_state(
    state
):

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

def generate_block(
    lane,
    distance
):
    """
    1レーンの1地点を生成する。
    """

    sx, sy, sz = lane["start"]


    # ========================================================
    # X/Z
    # ========================================================

    x = (
        sx
        + FX * distance
    )

    z = (
        sz
        + FZ * distance
    )


    # ========================================================
    # FIND SURFACE
    # ========================================================

    surface_y = find_surface(
        x,
        lane["last_y"],
        z
    )


    # ========================================================
    # NOT FOUND
    # ========================================================

    if surface_y is None:

        m.echo(
            "GROUND NOT FOUND "
            f"lane={lane['color']} "
            f"x={x} "
            f"z={z} "
            f"last_y={lane['last_y']}"
        )

        return False


    # ========================================================
    # WOOL
    # ========================================================

    wool = (
        f"minecraft:"
        f"{lane['color']}"
        f"_wool"
    )


    # ========================================================
    # REPLACE TOP SURFACE
    # ========================================================

    m.execute(
        f"setblock "
        f"{x} "
        f"{surface_y} "
        f"{z} "
        f"{wool}"
    )


    # ========================================================
    # UPDATE LAST Y
    # ========================================================

    lane["last_y"] = surface_y


    return True


# ============================================================
# GENERATE COURSE
# ============================================================

def generate_course():

    # ========================================================
    # LOAD
    # ========================================================

    state = load_state()

    current = (
        state["current_length"]
    )

    lanes = (
        state["lanes"]
    )


    # ========================================================
    # TIME LOG
    # ========================================================

    if os.path.exists(
        TIME_FILE
    ):

        with open(
            TIME_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            time_log = json.load(f)

    else:

        time_log = {}


    # ========================================================
    # HEADER
    # ========================================================

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
        f"Current: {current}"
    )

    m.echo(
        "================================"
    )


    total_start = time.time()


    # ========================================================
    # MAIN LOOP
    # ========================================================

    while current < TOTAL_LENGTH:

        slice_start = time.time()


        # ====================================================
        # 5 LANES
        # ====================================================

        for lane in lanes:

            success = generate_block(
                lane,
                current
            )


            # =================================================
            # GENERATION ERROR
            # =================================================

            if not success:

                state[
                    "current_length"
                ] = current

                state[
                    "lanes"
                ] = lanes

                save_state(
                    state
                )

                m.echo(
                    "Generation stopped."
                )

                return


        # ====================================================
        # NEXT DISTANCE
        # ====================================================

        current += 1


        state[
            "current_length"
        ] = current

        state[
            "lanes"
        ] = lanes


        # ====================================================
        # SAVE
        # ====================================================

        if (
            current
            % SAVE_INTERVAL
            == 0
            or current
            >= TOTAL_LENGTH
        ):

            elapsed = round(
                time.time()
                - slice_start,
                3
            )

            total_elapsed = round(
                time.time()
                - total_start,
                2
            )


            time_log[
                str(current)
            ] = elapsed


            save_state(
                state
            )


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
                f"{current}/"
                f"{TOTAL_LENGTH} "
                f"| {elapsed}s "
                f"| total "
                f"{total_elapsed}s"
            )


    # ========================================================
    # COMPLETE
    # ========================================================

    total_elapsed = round(
        time.time()
        - total_start,
        2
    )


    m.echo(
        "================================"
    )

    m.echo(
        "COURSE COMPLETE"
    )

    m.echo(
        f"Length : {TOTAL_LENGTH}"
    )

    m.echo(
        f"Time   : {total_elapsed}s"
    )

    m.echo(
        "================================"
    )


    # ========================================================
    # DELETE PROGRESS
    # ========================================================

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
    """
    生成状態を完全にリセット。

    lanes.json
    progress.json
    timelog.json

    を削除する。

    ワールド上のウールは削除しない。
    """

    files = [
        STATE_FILE,
        LANES_FILE,
        TIME_FILE
    ]


    deleted = 0


    for file in files:

        if os.path.exists(
            file
        ):

            os.remove(
                file
            )

            m.echo(
                f"Deleted: {file}"
            )

            deleted += 1


    if deleted == 0:

        m.echo(
            "Nothing to reset."
        )

    else:

        m.echo(
            "LineRace reset complete."
        )

        m.echo(
            "Run 'set' to start again."
        )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    if len(sys.argv) < 2:

        m.echo(
            "Usage:"
        )

        m.echo(
            "  set"
        )

        m.echo(
            "  reset"
        )

        sys.exit()


    command = sys.argv[1]


    # ========================================================
    # SET
    # ========================================================

    if command == "set":

        generate_course()


    # ========================================================
    # RESET
    # ========================================================

    elif command == "reset":

        reset_course()


    # ========================================================
    # UNKNOWN
    # ========================================================

    else:

        m.echo(
            f"Unknown command: {command}"
        )