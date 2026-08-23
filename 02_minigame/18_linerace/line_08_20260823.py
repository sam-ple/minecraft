# ============================================================
# LINERACE COURSE GENERATOR
# Version : v0.5.00
#
# Minecraft Java Edition + Minescript
#
# Features
#   ・5レーンを200ブロック単位でまとめて生成
#   ・0-200 → 200-400 → 400-600 ... の順番
#   ・各200区間の開始時に1回だけTP
#   ・Spectator方式
#   ・forceload不使用
#   ・TP後に十分待機
#   ・getblocklist()による高速地形探索
#   ・5レーン分をまとめて地形取得
#   ・雪は地面の場合のみウール化
#   ・木や葉の上の雪は無視
#   ・GROUND NOT FOUND時は自動リトライ
#   ・途中保存
#   ・途中から再開可能
#   ・resetで状態リセット
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

# レーン間隔
BLOCK_SPACING = 2

# コース全長
TOTAL_LENGTH = 1000

# ------------------------------------------------------------
# 200ブロック単位
# ------------------------------------------------------------

AREA_LENGTH = 200

# ------------------------------------------------------------
# getblocklistでまとめて取得する単位
# ------------------------------------------------------------

SLICE_LENGTH = 50

# ------------------------------------------------------------
# 状態保存
# ------------------------------------------------------------

SAVE_INTERVAL = 50


# ============================================================
# SPECTATOR SETTINGS
# ============================================================

# 200ブロック区間の開始地点へTPした後の待機
TP_WAIT = 1.0

# 地面からどの程度上にいるか
SPECTATOR_HEIGHT = 5


# ============================================================
# RETRY SETTINGS
# ============================================================

# GROUND NOT FOUND時のリトライ回数
GROUND_RETRY_COUNT = 3

# リトライ前待機
GROUND_RETRY_WAIT = 0.5


# ============================================================
# DIRECTION
# ============================================================

# Z+
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
# SURFACE BLOCKS
# ============================================================

SURFACE_BLOCKS = {

    "minecraft:snow",

    "minecraft:grass_block",

    "minecraft:dirt",

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
PLAYER_STATE_FILE = f"{BASE_DIR}/player_state.json"


# ============================================================
# BLOCK NORMALIZATION
# ============================================================

def normalize_block(block):

    if not isinstance(block, str):
        return ""

    return block.split(
        "[",
        1
    )[0]


# ============================================================
# BLOCK CHECK
# ============================================================

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
# SAVE PLAYER POSITION
# ============================================================

def save_player_position():

    try:

        x, y, z = m.player_position()

        with open(
            PLAYER_STATE_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                {
                    "position": [
                        x,
                        y,
                        z
                    ]
                },
                f,
                indent=2
            )

    except Exception:

        pass


# ============================================================
# RESTORE PLAYER
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

            state = json.load(f)

        x, y, z = state["position"]

        m.execute(
            "gamemode creative"
        )

        time.sleep(0.2)

        m.execute(
            f"tp @s {x} {y} {z}"
        )

        time.sleep(0.5)

        m.echo(
            "Player position restored."
        )

    except Exception as e:

        m.echo(
            f"Player restore failed: {e}"
        )


# ============================================================
# CREATE INITIAL STATE
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

    state = {

        # 現在の200区間
        "current_area": 0,

        # 現在の距離
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
# MAKE SEARCH Y
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

def find_surface_safe(
    x,
    z,
    search_ys,
    blocks
):

    for index, block in enumerate(
        blocks
    ):

        if not is_surface(block):

            continue

        y = search_ys[index]

        block_type = normalize_block(
            block
        )

        # ----------------------------------------------------
        # 通常の地面
        # ----------------------------------------------------

        if block_type != "minecraft:snow":

            return y

        # ----------------------------------------------------
        # 雪の場合
        # ----------------------------------------------------

        try:

            below = m.getblock(
                x,
                y - 1,
                z
            )

            if is_tree_or_leaf(
                below
            ):

                continue

        except Exception:

            pass

        return y

    return None


# ============================================================
# GET ONE LANE HEIGHTS
# ============================================================

def generate_lane_heights(
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

        x = (
            sx
            + FX * distance
        )

        z = (
            sz
            + FZ * distance
        )

        search_ys = make_search_ys(
            current_y
        )

        positions = [
            [
                x,
                y,
                z
            ]
            for y in search_ys
        ]

        blocks = m.getblocklist(
            positions
        )

        found_y = find_surface_safe(
            x,
            z,
            search_ys,
            blocks
        )

        if found_y is None:

            return None, distance

        heights[distance] = found_y

        current_y = found_y

    return heights, None


# ============================================================
# GENERATE ALL LANES IN SLICE
# ============================================================

def generate_slice(
    lanes,
    start_distance,
    end_distance
):

    """
    5レーンを同じ区間で処理。

    white
    orange
    light_blue
    lime
    yellow

    の順番。
    """

    results = []

    for lane_index, lane in enumerate(
        lanes
    ):

        m.echo(
            f"Terrain "
            f"{lane['color']} "
            f"{start_distance}-"
            f"{end_distance}"
        )

        heights, failed_distance = (
            generate_lane_heights(
                lane,
                start_distance,
                end_distance
            )
        )

        if heights is None:

            m.echo(
                "GROUND NOT FOUND "
                f"lane={lane['color']} "
                f"distance={failed_distance} "
                f"last_y={lane['last_y']}"
            )

            return None

        results.append(
            (
                lane,
                heights
            )
        )

    return results


# ============================================================
# APPLY ONE LANE
# ============================================================

def apply_lane(
    lane,
    heights,
    start_distance,
    end_distance
):

    sx, sy, sz = lane["start"]

    wool = (
        f"minecraft:"
        f"{lane['color']}"
        f"_wool"
    )

    fill_start = None
    fill_y = None

    for distance in range(
        start_distance,
        end_distance
    ):

        y = heights[distance]

        if fill_start is None:

            fill_start = distance
            fill_y = y

            continue

        if y == fill_y:

            continue

        fill_range(
            lane,
            fill_start,
            distance - 1,
            fill_y,
            wool
        )

        fill_start = distance
        fill_y = y

    if fill_start is not None:

        fill_range(
            lane,
            fill_start,
            end_distance - 1,
            fill_y,
            wool
        )

    lane["last_y"] = (
        heights[end_distance - 1]
    )

    if (
        end_distance
        - start_distance
        >= 2
    ):

        lane["prev_y"] = (
            heights[end_distance - 2]
        )


# ============================================================
# FILL RANGE
# ============================================================

def fill_range(
    lane,
    start_distance,
    end_distance,
    y,
    wool
):

    if (
        end_distance
        < start_distance
    ):

        return

    sx, sy, sz = lane["start"]

    x1 = (
        sx
        + FX * start_distance
    )

    z1 = (
        sz
        + FZ * start_distance
    )

    x2 = (
        sx
        + FX * end_distance
    )

    z2 = (
        sz
        + FZ * end_distance
    )

    # --------------------------------------------------------
    # 1ブロック
    # --------------------------------------------------------

    if (
        start_distance
        == end_distance
    ):

        m.execute(
            f"setblock "
            f"{x1} {y} {z1} "
            f"{wool}"
        )

        return

    # --------------------------------------------------------
    # Z方向
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

    m.execute(
        f"fill "
        f"{min_x} {y} {min_z} "
        f"{max_x} {y} {max_z} "
        f"{wool}"
    )


# ============================================================
# TP TO AREA
# ============================================================

def move_to_area(
    lanes,
    distance
):

    """
    5レーンの中央付近へ移動。

    200区間につき1回だけTPする。
    """

    lane = lanes[0]

    sx, sy, sz = lane["start"]

    x = (
        sx
        + FX * distance
    )

    z = (
        sz
        + FZ * distance
    )

    # 5レーンの中央
    center_offset = (
        (LINE_COUNT - 1)
        * BLOCK_SPACING
        / 2
    )

    x += RX * center_offset
    z += RZ * center_offset

    # --------------------------------------------------------
    # Spectator
    # --------------------------------------------------------

    m.execute(
        "gamemode spectator"
    )

    time.sleep(0.15)

    # --------------------------------------------------------
    # 前回Y付近
    # --------------------------------------------------------

    y = (
        lane["last_y"]
        + SPECTATOR_HEIGHT
    )

    m.execute(
        f"tp @s {x} {y} {z}"
    )

    # --------------------------------------------------------
    # 重要
    #
    # TP直後はチャンクロード待ち
    # --------------------------------------------------------

    time.sleep(
        TP_WAIT
    )


# ============================================================
# PRELOAD AREA
# ============================================================

def preload_area(
    lanes,
    start_distance,
    end_distance
):

    """
    200区間を一度Spectatorで読み込ませる。

    ただしTPは開始地点だけ。

    実際の地形取得は
    getblocklist()で行う。
    """

    move_to_area(
        lanes,
        start_distance
    )

    # --------------------------------------------------------
    # 区間中央
    #
    # 200ブロック先まで完全に読み込めていない
    # 可能性があるので中央付近へ一度移動。
    # --------------------------------------------------------

    middle = (
        start_distance
        + (
            end_distance
            - start_distance
        )
        // 2
    )

    move_to_area(
        lanes,
        middle
    )

    time.sleep(
        0.3
    )

    # --------------------------------------------------------
    # 区間終端付近
    # --------------------------------------------------------

    if end_distance < TOTAL_LENGTH:

        move_to_area(
            lanes,
            end_distance - 1
        )

        time.sleep(
            0.3
        )


# ============================================================
# GENERATE AREA
# ============================================================

def generate_area(
    state,
    start_distance,
    end_distance
):

    lanes = state["lanes"]

    # ========================================================
    # PRELOAD
    # ========================================================

    m.echo(
        f"PRELOAD "
        f"{start_distance}-"
        f"{end_distance}"
    )

    preload_area(
        lanes,
        start_distance,
        end_distance
    )

    # ========================================================
    # GENERATION
    # ========================================================

    current = start_distance

    while current < end_distance:

        slice_end = min(
            current + SLICE_LENGTH,
            end_distance
        )

        success = False

        # ----------------------------------------------------
        # RETRY
        # ----------------------------------------------------

        for retry in range(
            GROUND_RETRY_COUNT
        ):

            if retry > 0:

                m.echo(
                    f"Retry "
                    f"{retry}/"
                    f"{GROUND_RETRY_COUNT}"
                )

                # 失敗地点へ戻る
                move_to_area(
                    lanes,
                    current
                )

                time.sleep(
                    GROUND_RETRY_WAIT
                )

            # ------------------------------------------------
            # 地形取得
            # ------------------------------------------------

            result = generate_slice(
                lanes,
                current,
                slice_end
            )

            if result is not None:

                # --------------------------------------------
                # 5レーン描画
                # --------------------------------------------

                for lane, heights in result:

                    apply_lane(
                        lane,
                        heights,
                        current,
                        slice_end
                    )

                success = True

                break

        # ----------------------------------------------------
        # 完全失敗
        # ----------------------------------------------------

        if not success:

            m.echo(
                "================================"
            )

            m.echo(
                "GENERATION STOPPED"
            )

            m.echo(
                f"distance={current}"
            )

            m.echo(
                "GROUND LOAD FAILED"
            )

            m.echo(
                "================================"
            )

            return False

        # ----------------------------------------------------
        # 進行
        # ----------------------------------------------------

        current = slice_end

        state[
            "current_length"
        ] = current

        state[
            "lanes"
        ] = lanes

        # ----------------------------------------------------
        # 保存
        # ----------------------------------------------------

        if (
            current % SAVE_INTERVAL == 0
            or current == end_distance
        ):

            save_state(
                state
            )

        m.echo(
            f"GENERATED "
            f"{current}/"
            f"{end_distance}"
        )

    return True


# ============================================================
# GENERATE COURSE
# ============================================================

def generate_course():

    # --------------------------------------------------------
    # プレイヤー位置保存
    # --------------------------------------------------------

    save_player_position()

    # --------------------------------------------------------
    # State
    # --------------------------------------------------------

    state = load_state()

    current = (
        state.get(
            "current_length",
            0
        )
    )

    lanes = state["lanes"]

    # --------------------------------------------------------
    # Time log
    # --------------------------------------------------------

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

    total_start = time.time()

    # --------------------------------------------------------
    # Spectator
    # --------------------------------------------------------

    m.execute(
        "gamemode spectator"
    )

    time.sleep(
        0.3
    )

    # ========================================================
    # HEADER
    # ========================================================

    m.echo(
        "================================"
    )

    m.echo(
        "LineRace Generator v0.5.00"
    )

    m.echo(
        f"Length : {TOTAL_LENGTH}"
    )

    m.echo(
        f"Area   : {AREA_LENGTH}"
    )

    m.echo(
        "Mode   : SPECTATOR"
    )

    m.echo(
        "Chunk  : PLAYER LOAD"
    )

    m.echo(
        "Method : getblocklist()"
    )

    m.echo(
        "================================"
    )

    try:

        # ====================================================
        # 200 BLOCK AREA LOOP
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
                "white -> orange -> "
                "light_blue -> lime -> yellow"
            )

            m.echo(
                "================================"
            )

            area_start_time = time.time()

            # ------------------------------------------------
            # 5レーンをこの200区間で生成
            # ------------------------------------------------

            success = generate_area(
                state,
                area_start,
                area_end
            )

            # ------------------------------------------------
            # 失敗
            # ------------------------------------------------

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
                    "================================"
                )

                return

            # ------------------------------------------------
            # 200完了
            # ------------------------------------------------

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

            area_time = round(
                time.time()
                - area_start_time,
                2
            )

            total_time = round(
                time.time()
                - total_start,
                2
            )

            time_log[
                str(current)
            ] = area_time

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
                f"AREA TIME : "
                f"{area_time}s"
            )

            m.echo(
                f"TOTAL TIME : "
                f"{total_time}s"
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
            f"5 lanes"
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

        # ----------------------------------------------------
        # Progress削除
        # ----------------------------------------------------

        if os.path.exists(
            STATE_FILE
        ):

            os.remove(
                STATE_FILE
            )

    finally:

        # ----------------------------------------------------
        # プレイヤー復帰
        # ----------------------------------------------------

        restore_player()


# ============================================================
# RESET
# ============================================================

def reset_course():

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

            deleted += 1

            m.echo(
                f"Deleted: {file}"
            )

    m.echo(
        f"LineRace reset complete "
        f"({deleted} files)"
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
