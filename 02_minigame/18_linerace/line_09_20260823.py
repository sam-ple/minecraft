# ============================================================
# LINERACE COURSE GENERATOR
# Version : v0.5.01
#
# Minecraft Java Edition + Minescript
#
# Features
#   ・5レーン直線コース生成
#   ・200ブロック単位で処理
#   ・200ブロック内で5レーンをまとめて生成
#   ・200ブロックごとにSpectator移動
#   ・forceload 不使用
#   ・tp後にロード待機
#   ・区間内をSpectatorで先行移動してチャンクをロード
#   ・getblocklist() による高速地面探索
#   ・50ブロック単位で地形取得
#   ・GROUND NOT FOUND 自動リトライ
#   ・崖 / 坂 / 段差対応
#   ・雪はウールに置換
#   ・木や葉の上の雪は地面として扱わない
#   ・5レーンそれぞれ独立した高さ追従
#   ・途中保存
#   ・途中から再開可能
#   ・resetで生成状態をリセット
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

# コース長
TOTAL_LENGTH = 1000

# ============================================================
# AREA
# ============================================================

# 200ブロックごとに区切る
AREA_LENGTH = 200

# 地形取得単位
GROUND_SLICE = 50


# ============================================================
# SPECTATOR SETTINGS
# ============================================================

# 200ブロック区間内を先に移動する間隔
LOAD_STEP = 32

# TP直後の待機
TP_WAIT = 0.45

# 区間内を移動した後の待機
LOAD_WAIT = 0.15

# GROUND NOT FOUND時の追加待機
RETRY_WAIT = 0.35

# 最大リトライ回数
GROUND_RETRY = 3

# 地面からの高さ
SPECTATOR_HEIGHT = 5


# ============================================================
# DIRECTION
# ============================================================

# 進行方向
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

    # 雪
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
# SEARCH SETTINGS
# ============================================================

FAST_SEARCH_UP = 12
FAST_SEARCH_DOWN = 12

FALLBACK_SEARCH_UP = 40
FALLBACK_SEARCH_DOWN = 128


# ============================================================
# DATA
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

PLAYER_STATE_FILE = (
    f"{BASE_DIR}/player_state.json"
)


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

    block = normalize_block(block)

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

    except Exception as e:

        m.echo(
            f"Player position save failed: {e}"
        )


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
# LANE POSITION
# ============================================================

def lane_position(
    lane,
    distance
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

    return x, z


# ============================================================
# SPECTATOR TP
# ============================================================

def spectator_tp(
    lane,
    distance,
    wait=True
):

    x, z = lane_position(
        lane,
        distance
    )

    y = (
        lane["last_y"]
        + SPECTATOR_HEIGHT
    )

    m.execute(
        "gamemode spectator"
    )

    time.sleep(
        0.08
    )

    m.execute(
        f"tp @s {x} {y} {z}"
    )

    if wait:

        time.sleep(
            TP_WAIT
        )

    return x, y, z


# ============================================================
# PRELOAD AREA
# ============================================================

def preload_area(
    lanes,
    start_distance,
    end_distance
):

    """
    200ブロック区間をSpectatorで先に走査する。

    5レーンの中央付近を移動する。
    レーン間隔は最大8ブロック程度なので、
    1本を通れば周囲のチャンクも読み込まれる。
    """

    lane = lanes[0]

    m.echo(
        f"Preload "
        f"{start_distance}-"
        f"{end_distance}"
    )


    distance = start_distance


    while distance < end_distance:

        spectator_tp(
            lane,
            distance,
            wait=False
        )

        time.sleep(
            LOAD_WAIT
        )

        distance += LOAD_STEP


    # 最後の地点
    spectator_tp(
        lane,
        end_distance - 1,
        wait=True
    )


    m.echo(
        "Chunk preload complete."
    )


# ============================================================
# SEARCH Y LIST
# ============================================================

def make_search_ys(
    last_y
):

    return list(
        range(
            last_y
            + FAST_SEARCH_UP,

            last_y
            - FAST_SEARCH_DOWN
            - 1,

            -1
        )
    )


# ============================================================
# GET SURFACE FROM BLOCK LIST
# ============================================================

def find_surface_from_blocks(
    x,
    z,
    last_y,
    blocks
):

    # ========================================================
    # FAST SEARCH
    # ========================================================

    search_ys = make_search_ys(
        last_y
    )

    limit = min(
        len(search_ys),
        len(blocks)
    )


    for i in range(
        limit
    ):

        block = blocks[i]

        if not is_surface(block):
            continue

        y = search_ys[i]

        # ----------------------------------------------------
        # 雪
        # ----------------------------------------------------

        if normalize_block(block) == "minecraft:snow":

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


    # ========================================================
    # FALLBACK
    # ========================================================

    fallback_ys = list(
        range(
            last_y
            + FALLBACK_SEARCH_UP,

            last_y
            - FALLBACK_SEARCH_DOWN
            - 1,

            -1
        )
    )


    positions = [
        [
            x,
            y,
            z
        ]
        for y in fallback_ys
    ]


    try:

        fallback_blocks = m.getblocklist(
            positions
        )

    except Exception:

        return None


    limit = min(
        len(fallback_ys),
        len(fallback_blocks)
    )


    for i in range(
        limit
    ):

        block = fallback_blocks[i]

        if not is_surface(block):
            continue

        y = fallback_ys[i]

        if normalize_block(block) == "minecraft:snow":

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
# GENERATE HEIGHTS FOR ONE LANE
# ============================================================

def generate_lane_heights(
    lane,
    start_distance,
    end_distance
):

    """
    1レーン分の50ブロックを
    getblocklist()でまとめて探索。
    """

    heights = {}

    current_y = lane["last_y"]


    for distance in range(
        start_distance,
        end_distance
    ):

        x, z = lane_position(
            lane,
            distance
        )

        # ----------------------------------------------------
        # FAST SEARCH用のY
        # ----------------------------------------------------

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


        try:

            blocks = m.getblocklist(
                positions
            )

        except Exception as e:

            m.echo(
                f"getblocklist failed "
                f"lane={lane['color']} "
                f"distance={distance} "
                f"error={e}"
            )

            return None


        surface_y = (
            find_surface_from_blocks(
                x,
                z,
                current_y,
                blocks
            )
        )


        # ----------------------------------------------------
        # 見つからない
        # ----------------------------------------------------

        if surface_y is None:

            return None


        heights[distance] = (
            surface_y
        )

        current_y = surface_y


    return heights


# ============================================================
# RETRY GROUND
# ============================================================

def generate_lane_heights_retry(
    lane,
    start_distance,
    end_distance
):

    """
    GROUND NOT FOUND対策。

    失敗したらその地点まで
    Spectatorで移動してロードを促す。
    """

    for attempt in range(
        GROUND_RETRY + 1
    ):

        result = generate_lane_heights(
            lane,
            start_distance,
            end_distance
        )

        if result is not None:

            return result


        if attempt >= GROUND_RETRY:

            return None


        # ----------------------------------------------------
        # リトライ前に区間中央へ移動
        # ----------------------------------------------------

        retry_distance = (
            start_distance
            + min(
                25,
                end_distance
                - start_distance
                - 1
            )
        )


        m.echo(
            f"Ground retry "
            f"{attempt + 1}/"
            f"{GROUND_RETRY}"
        )


        spectator_tp(
            lane,
            retry_distance,
            wait=True
        )


        time.sleep(
            RETRY_WAIT
        )


    return None


# ============================================================
# SET WOOL
# ============================================================

def set_wool(
    lane,
    distance,
    y
):

    x, z = lane_position(
        lane,
        distance
    )

    wool = (
        f"minecraft:"
        f"{lane['color']}"
        f"_wool"
    )

    m.execute(
        f"setblock "
        f"{x} {y} {z} "
        f"{wool}"
    )


# ============================================================
# APPLY HEIGHTS
# ============================================================

def apply_heights(
    lane,
    heights,
    start_distance,
    end_distance
):

    """
    同じ高さが連続する部分は
    fillでまとめて生成する。
    """

    if not heights:

        return


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


        # ----------------------------------------------------
        # 高さが変わった
        # ----------------------------------------------------

        fill_lane_range(
            lane,
            fill_start,
            distance - 1,
            fill_y
        )


        fill_start = distance

        fill_y = y


    # --------------------------------------------------------
    # 最後
    # --------------------------------------------------------

    if fill_start is not None:

        fill_lane_range(
            lane,
            fill_start,
            end_distance - 1,
            fill_y
        )


    last_distance = (
        end_distance - 1
    )


    lane["last_y"] = (
        heights[last_distance]
    )


# ============================================================
# FILL LANE
# ============================================================

def fill_lane_range(
    lane,
    start_distance,
    end_distance,
    y
):

    if (
        end_distance
        < start_distance
    ):

        return


    x1, z1 = lane_position(
        lane,
        start_distance
    )

    x2, z2 = lane_position(
        lane,
        end_distance
    )


    wool = (
        f"minecraft:"
        f"{lane['color']}"
        f"_wool"
    )


    # ========================================================
    # Z+
    # ========================================================

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


    # ========================================================
    # SET
    # ========================================================

    if start_distance == end_distance:

        set_wool(
            lane,
            start_distance,
            y
        )

        return


    m.execute(
        f"fill "
        f"{min_x} {y} {min_z} "
        f"{max_x} {y} {max_z} "
        f"{wool}"
    )


# ============================================================
# GENERATE ONE 50 BLOCK SLICE
# ============================================================

def generate_slice(
    lane,
    start_distance,
    end_distance
):

    heights = (
        generate_lane_heights_retry(
            lane,
            start_distance,
            end_distance
        )
    )


    if heights is None:

        m.echo(
            "GROUND NOT FOUND "
            f"lane={lane['color']} "
            f"distance={start_distance}"
        )

        return False


    apply_heights(
        lane,
        heights,
        start_distance,
        end_distance
    )


    return True


# ============================================================
# GENERATE 200 BLOCK AREA
# ============================================================

def generate_area(
    lanes,
    start_distance,
    end_distance
):

    m.echo(
        "================================"
    )

    m.echo(
        f"AREA "
        f"{start_distance}-"
        f"{end_distance}"
    )

    m.echo(
        "5 LANES"
    )

    m.echo(
        "================================"
    )


    area_start = time.time()


    current = start_distance


    while current < end_distance:

        slice_end = min(
            current + GROUND_SLICE,
            end_distance
        )


        slice_start = time.time()


        # ====================================================
        # 5 LANES
        # ====================================================

        for lane in lanes:

            success = generate_slice(
                lane,
                current,
                slice_end
            )


            if not success:

                m.echo(
                    "================================"
                )

                m.echo(
                    "GROUND LOAD FAILED"
                )

                m.echo(
                    f"AREA "
                    f"{start_distance}-"
                    f"{end_distance}"
                )

                m.echo(
                    "================================"
                )

                return False


        # ====================================================
        # PROGRESS
        # ====================================================

        current = slice_end


        elapsed = round(
            time.time()
            - slice_start,
            3
        )


        m.echo(
            f"GROUND "
            f"{current}/"
            f"{end_distance} "
            f"| {elapsed}s"
        )


    area_elapsed = round(
        time.time()
        - area_start,
        2
    )


    m.echo(
        f"AREA COMPLETE "
        f"| {area_elapsed}s"
    )


    return True


# ============================================================
# GENERATE COURSE
# ============================================================

def generate_course():

    save_player_position()


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
        "LINERACE COURSE GENERATOR"
    )

    m.echo(
        "VERSION : v0.5.01"
    )

    m.echo(
        f"Length  : {TOTAL_LENGTH}"
    )

    m.echo(
        f"Area    : {AREA_LENGTH}"
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
        "================================"
    )


    total_start = time.time()


    # ========================================================
    # SPECTATOR
    # ========================================================

    m.execute(
        "gamemode spectator"
    )

    time.sleep(
        0.3
    )


    try:

        # ====================================================
        # AREA LOOP
        # ====================================================

        while current < TOTAL_LENGTH:

            area_end = min(
                current + AREA_LENGTH,
                TOTAL_LENGTH
            )


            # =================================================
            # PRELOAD
            # =================================================

            m.echo(
                "================================"
            )

            m.echo(
                f"PRELOAD "
                f"{current}-"
                f"{area_end}"
            )

            m.echo(
                "================================"
            )


            preload_area(
                lanes,
                current,
                area_end
            )


            # =================================================
            # GENERATE
            # =================================================

            success = generate_area(
                lanes,
                current,
                area_end
            )


            # =================================================
            # FAILED
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
                    "================================"
                )

                m.echo(
                    "COURSE GENERATION PAUSED"
                )

                m.echo(
                    f"Resume from "
                    f"{current}"
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


            area_elapsed = round(
                time.time()
                - total_start,
                2
            )


            time_log[
                str(current)
            ] = area_elapsed


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
                f"{area_elapsed}s"
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
            f"Length : {TOTAL_LENGTH}"
        )

        m.echo(
            f"Lanes  : {LINE_COUNT}"
        )

        m.echo(
            f"Time   : {total_elapsed}s"
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


    if command == "set":

        generate_course()


    elif command == "reset":

        reset_course()


    else:

        m.echo(
            f"Unknown command: {command}"
        )
