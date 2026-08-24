# ============================================================
# LINERACE COURSE GENERATOR
# Version : v0.3.00
#
# Minecraft Java Edition + Minescript
#
# Features
#   ・5レーン直線コース
#   ・地形追従
#   ・崖 / 坂 / 段差対応
#   ・各レーン独立地形判定
#   ・最上面の床ブロックをウールに置換
#   ・雪がある場合は雪をウールに置換
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

# 何ブロックごとに進捗保存
SAVE_INTERVAL = 50

# ============================================================
# 進行方向
#
# 現在:
#   Z+
#
# X方向にしたい場合:
#   FX, FZ = 1, 0
# ============================================================

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
# SURFACE SETTINGS
# ============================================================

# ============================================================
# 「床」として扱うブロック
#
# 上から下へ探索して、
# 最初にこの中のブロックを見つけた場所を
# 「その地点の床」とする。
#
# 例:
#
#   snow
#   grass_block
#   dirt
#
# → snow を床として採用
#
#   grass_block
#   dirt
#   dirt
#
# → grass_block を床として採用
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

# 前回Yより上を探索
SEARCH_UP = 8

# 前回Yより下を探索
SEARCH_DOWN = 20


# ============================================================
# DATA DIRECTORY
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
# BLOCK NORMALIZE
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
    指定X/Z地点の最上面を探す。

    前回のY付近から上→下へ探索する。

    最初に見つかった
    SURFACE_BLOCKS
    が、その地点の床。

    雪があれば雪を優先する。
    """

    # ========================================================
    # まず前回Yの近くを探索
    # ========================================================

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

        if is_surface(block):

            return y

    # ========================================================
    # 見つからない
    # ========================================================

    return None


# ============================================================
# CREATE INITIAL STATE
# ============================================================

def create_state():

    px, py, pz = map(
        math.floor,
        m.player_position()
    )

    lanes = []

    # ========================================================
    # 5レーン作成
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
    # lanes.json
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
    # progress
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

    sx, sy, sz = lane["start"]

    # ========================================================
    # 現在のX/Z
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
    # 最上面を探索
    # ========================================================

    surface_y = find_surface(
        x,
        lane["last_y"],
        z
    )

    # ========================================================
    # 見つからなかった
    # ========================================================

    if surface_y is None:

        m.echo(
            f"GROUND NOT FOUND "
            f"lane={lane['color']} "
            f"x={x} "
            f"z={z} "
            f"last_y={lane['last_y']}"
        )

        return False

    # ========================================================
    # ウール
    # ========================================================

    wool = (
        f"minecraft:"
        f"{lane['color']}"
        f"_wool"
    )

    # ========================================================
    # 最上面をウールに置換
    # ========================================================

    m.execute(
        f"setblock "
        f"{x} "
        f"{surface_y} "
        f"{z} "
        f"{wool}"
    )

    # ========================================================
    # 次回探索用Y
    # ========================================================

    lane["last_y"] = surface_y

    return True


# ============================================================
# GENERATE COURSE
# ============================================================

def generate_course():

    # ========================================================
    # State
    # ========================================================

    state = load_state()

    current = (
        state["current_length"]
    )

    lanes = (
        state["lanes"]
    )

    # ========================================================
    # Time Log
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
    # START
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
        # 5レーン生成
        # ====================================================

        for lane_index, lane in enumerate(
            lanes
        ):

            success = generate_block(
                lane,
                current
            )

            if not success:

                # --------------------------------------------
                # エラー時保存
                # --------------------------------------------

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
        # 次へ
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
                f"| "
                f"{elapsed}s "
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
    # Progress削除
    # ========================================================

    if os.path.exists(
        STATE_FILE
    ):

        os.remove(
            STATE_FILE
        )


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
            f"Unknown command: "
            f"{command}"
        )