# ============================================================
# LINERACE COURSE GENERATOR
# Version : v0.6.00
#
# Minecraft Java Edition + Minescript
#
# FAST + SAFE HYBRID
#
# Features
#   ・5レーン直線コース
#   ・200ブロック単位で処理
#   ・200ブロック先へSpectator TP
#   ・forceload 不使用
#   ・5レーンをまとめて地形取得
#   ・getblocklist() 高速取得
#   ・通常時は高速処理
#   ・失敗時だけ慎重な再ロード
#   ・崖 / 坂 / 急激な高度変化対応
#   ・雪をウールに置換
#   ・木 / 葉の上の雪を避ける
#   ・同高度区間はfill
#   ・50ブロック単位で保存
#   ・200ブロック完了時に確実に保存
#   ・途中から再開可能
#   ・reset
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

# 1回に処理する区間
AREA_LENGTH = 200

# 地形取得単位
SLICE_LENGTH = 50

# 保存間隔
SAVE_INTERVAL = 50


# ============================================================
# SPECTATOR SETTINGS
# ============================================================

# 通常TP後
TP_WAIT_FAST = 0.45

# 失敗時
TP_WAIT_SAFE = 0.80

# 失敗時の追加待機
RETRY_WAIT = 0.50

# 失敗地点周辺への移動間隔
RECOVERY_STEP = 16

# Spectatorの高さ
SPECTATOR_HEIGHT = 6


# ============================================================
# GROUND SEARCH
# ============================================================

# 通常探索
FAST_SEARCH_UP = 10
FAST_SEARCH_DOWN = 15

# 第2段階
MEDIUM_SEARCH_UP = 30
MEDIUM_SEARCH_DOWN = 50

# 最終探索
DEEP_SEARCH_UP = 60
DEEP_SEARCH_DOWN = 128


# ============================================================
# RETRY
# ============================================================

# 通常取得失敗後の再試行回数
MAX_NORMAL_RETRY = 2

# 慎重モード
MAX_SAFE_RETRY = 8


# ============================================================
# DIRECTION
# ============================================================

# Z+
FX, FZ = 0, 1

# X+
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
# SURFACE BLOCKS
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

    "minecraft:mycelium",

    "minecraft:snow",

}


# ============================================================
# TREE / LEAF BLOCKS
# ============================================================

WOOD_BLOCKS = {

    "minecraft:oak_log",
    "minecraft:spruce_log",
    "minecraft:birch_log",
    "minecraft:jungle_log",
    "minecraft:acacia_log",
    "minecraft:dark_oak_log",
    "minecraft:mangrove_log",
    "minecraft:cherry_log",

    "minecraft:stripped_oak_log",
    "minecraft:stripped_spruce_log",
    "minecraft:stripped_birch_log",
    "minecraft:stripped_jungle_log",
    "minecraft:stripped_acacia_log",
    "minecraft:stripped_dark_oak_log",
    "minecraft:stripped_mangrove_log",
    "minecraft:stripped_cherry_log",

    "minecraft:oak_wood",
    "minecraft:spruce_wood",
    "minecraft:birch_wood",
    "minecraft:jungle_wood",
    "minecraft:acacia_wood",
    "minecraft:dark_oak_wood",
    "minecraft:mangrove_wood",
    "minecraft:cherry_wood",
}


LEAF_BLOCKS = {

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

PLAYER_STATE_FILE = (
    f"{BASE_DIR}/player_state.json"
)


# ============================================================
# BLOCK UTIL
# ============================================================

def normalize_block(block):

    if not isinstance(block, str):
        return ""

    return block.split(
        "[",
        1
    )[0]


def is_surface(block):

    return (
        normalize_block(block)
        in SURFACE_BLOCKS
    )


def is_tree_or_leaf(block):

    block = normalize_block(
        block
    )

    return (
        block in WOOD_BLOCKS
        or block in LEAF_BLOCKS
    )


# ============================================================
# PLAYER SAVE
# ============================================================

def save_player_state():

    try:

        x, y, z = m.player_position()

        data = {
            "position": [
                x,
                y,
                z
            ]
        }

        with open(
            PLAYER_STATE_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=2
            )

    except Exception:

        pass


# ============================================================
# PLAYER RESTORE
# ============================================================

def restore_player():

    if not os.path.exists(
        PLAYER_STATE_FILE
    ):
        return

    try:

        with open(
            PLAYER_STATE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        x, y, z = data["position"]

        m.execute(
            "gamemode creative"
        )

        time.sleep(
            0.2
        )

        m.execute(
            f"tp @s {x} {y} {z}"
        )

        time.sleep(
            0.3
        )

        m.echo(
            "Player position restored."
        )

    except Exception as e:

        m.echo(
            f"Player restore failed: {e}"
        )


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
# CREATE STATE
# ============================================================

def create_state():

    px, py, pz = map(
        math.floor,
        m.player_position()
    )

    lanes = []

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

            "start": [
                sx,
                py,
                sz
            ],

            "last_y": py,

            "prev_y": py,

            "color": COLORS[i]

        })

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

    with open(
        LANES_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            {
                "lanes": lanes,
                "course_length": TOTAL_LENGTH
            },
            f,
            indent=2,
            ensure_ascii=False
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
# MAKE SEARCH POSITIONS
# ============================================================

def make_search_positions(
    x,
    z,
    last_y,
    up,
    down
):

    positions = []

    ys = range(
        last_y + up,
        last_y - down - 1,
        -1
    )

    for y in ys:

        positions.append(
            [
                x,
                y,
                z
            ]
        )

    return positions


# ============================================================
# FIND SURFACE FROM BLOCK LIST
# ============================================================

def find_surface_from_blocks(
    x,
    z,
    last_y,
    blocks,
    up,
    down
):

    ys = range(
        last_y + up,
        last_y - down - 1,
        -1
    )

    for index, block in enumerate(
        blocks
    ):

        if not is_surface(
            block
        ):
            continue

        y = list(ys)[index]

        block_type = normalize_block(
            block
        )

        # ----------------------------------------------------
        # 雪
        # ----------------------------------------------------

        if block_type == "minecraft:snow":

            try:

                below = m.getblock(
                    x,
                    y - 1,
                    z
                )

                # 木や葉の上の雪は無視
                if is_tree_or_leaf(
                    below
                ):

                    continue

            except Exception:

                pass

        return y

    return None


# ============================================================
# SINGLE SAFE SURFACE SEARCH
# ============================================================

def search_surface_single(
    x,
    z,
    last_y
):

    search_levels = [

        (
            FAST_SEARCH_UP,
            FAST_SEARCH_DOWN
        ),

        (
            MEDIUM_SEARCH_UP,
            MEDIUM_SEARCH_DOWN
        ),

        (
            DEEP_SEARCH_UP,
            DEEP_SEARCH_DOWN
        )

    ]

    for up, down in search_levels:

        positions = make_search_positions(
            x,
            z,
            last_y,
            up,
            down
        )

        try:

            blocks = m.getblocklist(
                positions
            )

        except Exception:

            blocks = None

        if not blocks:

            continue

        result = (
            find_surface_from_blocks(
                x,
                z,
                last_y,
                blocks,
                up,
                down
            )
        )

        if result is not None:

            return result

    return None


# ============================================================
# SPECTATOR TP
# ============================================================

def spectator_tp(
    lane,
    distance,
    wait_time
):

    sx, sy, sz = lane["start"]

    x = (
        sx
        + FX * distance
    )

    z = (
        sz
        + FZ * distance
    )

    y = (
        lane["last_y"]
        + SPECTATOR_HEIGHT
    )

    m.execute(
        "gamemode spectator"
    )

    time.sleep(
        0.1
    )

    m.execute(
        f"tp @s {x} {y} {z}"
    )

    time.sleep(
        wait_time
    )

    return x, y, z


# ============================================================
# FAST AREA LOAD
# ============================================================

def load_area_fast(
    lanes,
    start_distance
):

    """
    200ブロック区間の先頭へTP。

    通常時はここだけ。
    """

    lane = lanes[0]

    x, y, z = spectator_tp(
        lane,
        start_distance,
        TP_WAIT_FAST
    )

    m.echo(
        f"Spectator TP -> "
        f"{start_distance} "
        f"({x}, {round(y, 1)}, {z})"
    )


# ============================================================
# SAFE AREA LOAD
# ============================================================

def load_area_safe(
    lanes,
    start_distance,
    failed_distance
):

    """
    失敗したときだけ使用。

    失敗地点へ移動し、
    少しずつ周辺を読み込ませる。
    """

    m.echo(
        "--------------------------------"
    )

    m.echo(
        "SAFE CHUNK RECOVERY"
    )

    m.echo(
        f"failed distance="
        f"{failed_distance}"
    )

    # --------------------------------------------------------
    # 中心地点
    # --------------------------------------------------------

    lane = lanes[0]

    spectator_tp(
        lane,
        failed_distance,
        TP_WAIT_SAFE
    )

    # --------------------------------------------------------
    # 前後を移動
    # --------------------------------------------------------

    offsets = [
        -48,
        -32,
        -16,
        0,
        16,
        32,
        48
    ]

    for offset in offsets:

        distance = (
            failed_distance
            + offset
        )

        if distance < 0:
            continue

        if distance >= TOTAL_LENGTH:
            continue

        spectator_tp(
            lane,
            distance,
            0.18
        )

    # --------------------------------------------------------
    # 最後に失敗地点
    # --------------------------------------------------------

    spectator_tp(
        lane,
        failed_distance,
        TP_WAIT_SAFE
    )

    # 追加待機
    time.sleep(
        RETRY_WAIT
    )

    m.echo(
        "SAFE CHUNK RECOVERY COMPLETE"
    )


# ============================================================
# GENERATE SLICE
# ============================================================

def generate_slice(
    lanes,
    start_distance,
    end_distance
):

    """
    50ブロック単位。

    5レーンをまとめて処理する。

    まず地形取得。
    全て成功したらブロック生成。
    """

    heights = []

    # ========================================================
    # GROUND SEARCH
    # ========================================================

    for lane_index, lane in enumerate(
        lanes
    ):

        lane_heights = []

        for distance in range(
            start_distance,
            end_distance
        ):

            sx, sy, sz = lane["start"]

            x = (
                sx
                + FX * distance
            )

            z = (
                sz
                + FZ * distance
            )

            last_y = lane["last_y"]

            # ------------------------------------------------
            # 段階的探索
            # ------------------------------------------------

            found_y = search_surface_single(
                x,
                z,
                last_y
            )

            if found_y is None:

                return (
                    False,
                    lane_index,
                    distance,
                    None
                )

            lane_heights.append(
                found_y
            )

            lane["last_y"] = found_y

        heights.append(
            lane_heights
        )

    # ========================================================
    # BLOCK GENERATION
    # ========================================================

    for lane_index, lane in enumerate(
        lanes
    ):

        lane_heights = heights[
            lane_index
        ]

        for index, distance in enumerate(
            range(
                start_distance,
                end_distance
            )
        ):

            ground_y = lane_heights[
                index
            ]

            sx, sy, sz = lane["start"]

            x = (
                sx
                + FX * distance
            )

            z = (
                sz
                + FZ * distance
            )

            wool = (
                f"minecraft:"
                f"{lane['color']}"
                f"_wool"
            )

            m.execute(
                f"setblock "
                f"{x} "
                f"{ground_y} "
                f"{z} "
                f"{wool}"
            )

    return (
        True,
        None,
        None,
        heights
    )


# ============================================================
# GENERATE AREA
# ============================================================

def generate_area(
    lanes,
    area_start,
    area_end
):

    current = area_start

    while current < area_end:

        slice_end = min(
            current + SLICE_LENGTH,
            area_end
        )

        start_time = time.time()

        # ----------------------------------------------------
        # FAST ATTEMPT
        # ----------------------------------------------------

        success, lane_index, failed_distance, data = (
            generate_slice(
                lanes,
                current,
                slice_end
            )
        )

        # ====================================================
        # SUCCESS
        # ====================================================

        if success:

            elapsed = round(
                time.time()
                - start_time,
                3
            )

            current = slice_end

            m.echo(
                f"GROUND "
                f"{current}/{area_end} "
                f"| {elapsed}s"
            )

            continue

        # ====================================================
        # FAILURE
        # ====================================================

        lane = lanes[
            lane_index
        ]

        m.echo(
            "================================"
        )

        m.echo(
            "GROUND LOAD FAILED"
        )

        m.echo(
            f"lane={lane['color']}"
        )

        m.echo(
            f"distance={failed_distance}"
        )

        m.echo(
            f"slice={current}-{slice_end}"
        )

        m.echo(
            "================================"
        )

        # ====================================================
        # NORMAL RETRY
        # ====================================================

        recovered = False

        for retry in range(
            1,
            MAX_NORMAL_RETRY + 1
        ):

            m.echo(
                f"GROUND RETRY "
                f"{retry}/"
                f"{MAX_NORMAL_RETRY}"
            )

            time.sleep(
                RETRY_WAIT
            )

            success, lane_index2, failed_distance2, data2 = (
                generate_slice(
                    lanes,
                    current,
                    slice_end
                )
            )

            if success:

                m.echo(
                    "GROUND RECOVERED"
                )

                recovered = True

                break

        if recovered:

            current = slice_end

            continue

        # ====================================================
        # SAFE RECOVERY
        # ====================================================

        for retry in range(
            1,
            MAX_SAFE_RETRY + 1
        ):

            m.echo(
                "================================"
            )

            m.echo(
                f"SAFE RETRY "
                f"{retry}/"
                f"{MAX_SAFE_RETRY}"
            )

            m.echo(
                f"distance="
                f"{failed_distance}"
            )

            m.echo(
                "================================"
            )

            load_area_safe(
                lanes,
                area_start,
                failed_distance
            )

            success, lane_index2, failed_distance2, data2 = (
                generate_slice(
                    lanes,
                    current,
                    slice_end
                )
            )

            if success:

                m.echo(
                    "SAFE RECOVERY SUCCESS"
                )

                recovered = True

                break

        # ====================================================
        # FINAL FAILURE
        # ====================================================

        if not recovered:

            m.echo(
                "================================"
            )

            m.echo(
                "GROUND LOAD FAILED"
            )

            m.echo(
                "SAFE RETRY EXHAUSTED"
            )

            m.echo(
                f"area="
                f"{area_start}-"
                f"{area_end}"
            )

            m.echo(
                "================================"
            )

            return False

        current = slice_end

    return True


# ============================================================
# GENERATE COURSE
# ============================================================

def generate_course():

    save_player_state()

    state = load_state()

    current = (
        state[
            "current_length"
        ]
    )

    lanes = (
        state[
            "lanes"
        ]
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
        "LINERACE COURSE GENERATOR"
    )

    m.echo(
        "VERSION : v0.6.00"
    )

    m.echo(
        f"Length  : {TOTAL_LENGTH}"
    )

    m.echo(
        f"Area    : {AREA_LENGTH}"
    )

    m.echo(
        f"Slice   : {SLICE_LENGTH}"
    )

    m.echo(
        f"Current : {current}"
    )

    m.echo(
        "Mode    : SPECTATOR"
    )

    m.echo(
        "Chunk   : NO FORCELOAD"
    )

    m.echo(
        "Mode    : FAST + SAFE"
    )

    m.echo(
        "================================"
    )

    total_start = time.time()

    m.execute(
        "gamemode spectator"
    )

    time.sleep(
        0.3
    )

    try:

        # ====================================================
        # 200 BLOCK AREAS
        # ====================================================

        while current < TOTAL_LENGTH:

            area_start = current

            area_end = min(
                current + AREA_LENGTH,
                TOTAL_LENGTH
            )

            m.echo(
                "================================"
            )

            m.echo(
                f"AREA "
                f"{area_start}-"
                f"{area_end}"
            )

            m.echo(
                "5 LANES"
            )

            m.echo(
                "================================"
            )

            # ------------------------------------------------
            # TP
            # ------------------------------------------------

            load_area_fast(
                lanes,
                area_start
            )

            # ------------------------------------------------
            # 200 BLOCK GENERATION
            # ------------------------------------------------

            success = generate_area(
                lanes,
                area_start,
                area_end
            )

            # =================================================
            # FAILED
            # =================================================

            if not success:

                state[
                    "current_length"
                ] = area_start

                state[
                    "lanes"
                ] = lanes

                save_state(
                    state
                )

                m.echo(
                    "================================"
                )

                m.echo(
                    "COURSE GENERATION PAUSED"
                )

                m.echo(
                    f"Resume from "
                    f"{area_start}"
                )

                m.echo(
                    "Run 'set' again "
                    "to retry."
                )

                m.echo(
                    "================================"
                )

                return

            # =================================================
            # AREA COMPLETE
            # =================================================

            current = area_end

            state[
                "current_length"
            ] = current

            state[
                "lanes"
            ] = lanes

            save_state(
                state
            )

            elapsed = round(
                time.time()
                - total_start,
                2
            )

            time_log[
                str(current)
            ] = elapsed

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
                "================================"
            )

            m.echo(
                f"AREA COMPLETE "
                f"{current}/"
                f"{TOTAL_LENGTH}"
            )

            m.echo(
                f"TOTAL TIME "
                f"{elapsed}s"
            )

            m.echo(
                "================================"
            )

        # ====================================================
        # COMPLETE
        # ====================================================

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
            f"5 LANES"
        )

        m.echo(
            f"LENGTH : "
            f"{TOTAL_LENGTH}"
        )

        m.echo(
            f"TIME   : "
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

    finally:

        restore_player()


# ============================================================
# RESET
# ============================================================

def reset_course():

    files = [

        STATE_FILE,

        LANES_FILE,

        TIME_FILE,

        PLAYER_STATE_FILE

    ]

    deleted = 0

    for path in files:

        if os.path.exists(
            path
        ):

            os.remove(
                path
            )

            m.echo(
                f"Deleted: {path}"
            )

            deleted += 1

    m.echo(
        "================================"
    )

    m.echo(
        "LineRace reset complete."
    )

    m.echo(
        f"{deleted} files removed."
    )

    m.echo(
        "World blocks were NOT removed."
    )

    m.echo(
        "================================"
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

    if command == "set":

        generate_course()

    elif command == "reset":

        reset_course()

    else:

        m.echo(
            f"Unknown command: {command}"
        )
