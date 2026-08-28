# ============================================================
# LINERACE COURSE GENERATOR
# Version : v0.1.00
#
# Minecraft Java Edition + Minescript
#
# Features
#   ・5レーン直線コース
#   ・レーン本体は各色の羊毛
#   ・スタート地点に各色コンクリート
#   ・コンクリートにストーンボタンを設置
#   ・set0でスタート設備だけ設置
#   ・setでスタート設備設置後にレーン生成
#   ・200ブロック単位で処理
#   ・50ブロック単位で地形取得
#   ・getblocklist()による高速探索
#   ・失敗時のみgetblock()へフォールバック
#   ・さらに失敗した場合は広範囲探索
#   ・崖 / 坂 / 大きな段差対応
#   ・地形の高さに追従
#   ・地面の雪をウールに置換
#   ・木 / 葉の上の雪は無視
#   ・Spectator TPによるチャンクロード
#   ・200ブロックごとに自動保存
#   ・途中から再開可能
#   ・resetで生成状態をリセット
#   ・forceload不使用
#
# Commands
#   set
#   set0
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

# 1回に処理する区間
AREA_LENGTH = 200

# 地形取得単位
SLICE_LENGTH = 50


# ============================================================
# SPECTATOR / CHUNK LOAD
# ============================================================

TP_CENTER_OFFSET = 100

TP_WAIT = 1.0

GROUND_RETRY_COUNT = 5

GROUND_RETRY_WAIT = 0.25

FALLBACK_WAIT = 0.4

DEEP_FALLBACK_WAIT = 0.5

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

    "minecraft:stripped_oak_wood",
    "minecraft:stripped_spruce_wood",
    "minecraft:stripped_birch_wood",
    "minecraft:stripped_jungle_wood",
    "minecraft:stripped_acacia_wood",
    "minecraft:stripped_dark_oak_wood",
    "minecraft:stripped_mangrove_wood",
    "minecraft:stripped_cherry_wood",
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
FALLBACK_SEARCH_DOWN = 120

DEEP_SEARCH_UP = 80
DEEP_SEARCH_DOWN = 180


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

PLAYER_STATE_FILE = f"{BASE_DIR}/player_state.json"


# ============================================================
# BLOCK NORMALIZE
# ============================================================

def normalize_block(block):

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
# TREE CHECK
# ============================================================

def is_tree_or_leaf(block):

    block = normalize_block(block)

    return (
        block in WOOD_BLOCKS
        or block in LEAF_BLOCKS
    )


# ============================================================
# SAVE PLAYER
# ============================================================

def save_player_state():

    try:

        x, y, z = m.player_position()

        state = {
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
                state,
                f,
                indent=2
            )

    except Exception as e:

        m.echo(
            f"Player state save failed: {e}"
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

            state = json.load(f)

        x, y, z = state["position"]

        # ====================================================
        # 生成終了時はSURVIVAL
        # ====================================================

        m.execute(
            "gamemode survival"
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
# SEARCH Y LIST
# ============================================================

def make_search_ys(last_y):

    ys = []

    # 近傍

    for dy in range(
        FAST_SEARCH_UP,
        -FAST_SEARCH_DOWN - 1,
        -1
    ):

        ys.append(
            last_y + dy
        )


    # 上方向

    for dy in range(
        FAST_SEARCH_UP + 1,
        FALLBACK_SEARCH_UP + 1
    ):

        ys.append(
            last_y + dy
        )


    # 下方向

    for dy in range(
        FAST_SEARCH_DOWN + 1,
        FALLBACK_SEARCH_DOWN + 1
    ):

        ys.append(
            last_y - dy
        )

    return ys


# ============================================================
# FIND SURFACE FROM BLOCK LIST
# ============================================================

def find_surface_from_blocks(
    x,
    z,
    search_ys,
    blocks
):

    if blocks is None:
        return None

    if len(blocks) != len(
        search_ys
    ):
        return None


    for index, block in enumerate(
        blocks
    ):

        if not is_surface(block):
            continue


        y = search_ys[index]

        block_type = normalize_block(
            block
        )


        # ====================================================
        # 雪
        # ====================================================

        if block_type == (
            "minecraft:snow"
        ):

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
# GETBLOCKLIST
# ============================================================

def get_surface_with_getblocklist(
    x,
    z,
    last_y
):

    search_ys = make_search_ys(
        last_y
    )

    positions = []

    for y in search_ys:

        positions.append([
            x,
            y,
            z
        ])


    try:

        blocks = m.getblocklist(
            positions
        )

    except Exception:

        return None


    return find_surface_from_blocks(
        x,
        z,
        search_ys,
        blocks
    )


# ============================================================
# GETBLOCK FALLBACK
# ============================================================

def find_surface_fallback(
    x,
    z,
    last_y
):

    for dy in range(
        FALLBACK_SEARCH_UP,
        -FALLBACK_SEARCH_DOWN - 1,
        -1
    ):

        y = last_y + dy

        try:

            block = m.getblock(
                x,
                y,
                z
            )

        except Exception:

            continue


        if not is_surface(block):
            continue


        block_type = normalize_block(
            block
        )


        if block_type == (
            "minecraft:snow"
        ):

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
# DEEP FALLBACK
# ============================================================

def find_surface_deep(
    x,
    z,
    last_y
):

    for dy in range(
        DEEP_SEARCH_UP,
        -DEEP_SEARCH_DOWN - 1,
        -1
    ):

        y = last_y + dy

        try:

            block = m.getblock(
                x,
                y,
                z
            )

        except Exception:

            continue


        if not is_surface(block):
            continue


        block_type = normalize_block(
            block
        )


        if block_type == (
            "minecraft:snow"
        ):

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
# FIND SURFACE WITH RETRY
# ============================================================

def find_surface_retry(
    x,
    z,
    last_y,
    lane_color,
    distance
):

    # ========================================================
    # PHASE 1
    # 高速GETBLOCKLIST
    # ========================================================

    for attempt in range(
        GROUND_RETRY_COUNT
    ):

        surface_y = (
            get_surface_with_getblocklist(
                x,
                z,
                last_y
            )
        )

        if surface_y is not None:

            return surface_y


        if attempt < (
            GROUND_RETRY_COUNT - 1
        ):

            time.sleep(
                GROUND_RETRY_WAIT
            )


    # ========================================================
    # PHASE 2
    # GETBLOCK
    # ========================================================

    m.echo(
        f"GROUND FALLBACK "
        f"lane={lane_color} "
        f"distance={distance}"
    )

    time.sleep(
        FALLBACK_WAIT
    )


    surface_y = (
        find_surface_fallback(
            x,
            z,
            last_y
        )
    )


    if surface_y is not None:

        m.echo(
            f"GROUND FALLBACK OK "
            f"lane={lane_color} "
            f"distance={distance}"
        )

        return surface_y


    # ========================================================
    # PHASE 3
    # DEEP SEARCH
    # ========================================================

    m.echo(
        f"GROUND DEEP SEARCH "
        f"lane={lane_color} "
        f"distance={distance}"
    )

    time.sleep(
        DEEP_FALLBACK_WAIT
    )


    surface_y = (
        find_surface_deep(
            x,
            z,
            last_y
        )
    )


    if surface_y is not None:

        m.echo(
            f"GROUND DEEP OK "
            f"lane={lane_color} "
            f"distance={distance} "
            f"y={surface_y}"
        )

        return surface_y


    return None


# ============================================================
# GENERATE LANE HEIGHTS
# ============================================================

def generate_lane_heights(
    lane,
    start_distance,
    end_distance
):

    sx, sy, sz = lane[
        "start"
    ]

    heights = {}

    current_y = lane[
        "last_y"
    ]


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


        surface_y = (
            find_surface_retry(
                x,
                z,
                current_y,
                lane["color"],
                distance
            )
        )


        if surface_y is None:

            m.echo(
                "GROUND NOT FOUND "
                f"lane={lane['color']} "
                f"distance={distance} "
                f"x={x} "
                f"z={z} "
                f"last_y={current_y}"
            )

            return None


        heights[
            distance
        ] = surface_y


        current_y = surface_y


    return heights


# ============================================================
# SET WOOL
# ============================================================

def set_lane_block(
    lane,
    distance,
    ground_y
):

    sx, sy, sz = lane[
        "start"
    ]

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


# ============================================================
# FILL SAME HEIGHT
# ============================================================

def fill_lane_range(
    lane,
    start_distance,
    end_distance,
    ground_y
):

    if end_distance < start_distance:
        return


    sx, sy, sz = lane[
        "start"
    ]


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


    wool = (
        f"minecraft:"
        f"{lane['color']}"
        f"_wool"
    )


    if FX != 0:

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

    else:

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


    if (
        start_distance
        == end_distance
    ):

        set_lane_block(
            lane,
            start_distance,
            ground_y
        )

        return


    m.execute(
        f"fill "
        f"{min_x} {ground_y} {min_z} "
        f"{max_x} {ground_y} {max_z} "
        f"{wool}"
    )


# ============================================================
# APPLY HEIGHTS
# ============================================================

def apply_lane_heights(
    lane,
    heights,
    start_distance,
    end_distance
):

    if not heights:
        return False


    fill_start = None

    fill_y = None


    last_distance = (
        end_distance - 1
    )


    for distance in range(
        start_distance,
        end_distance
    ):

        ground_y = heights[
            distance
        ]


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
            last_distance,
            fill_y
        )


    lane[
        "last_y"
    ] = heights[
        last_distance
    ]


    if (
        last_distance
        > start_distance
    ):

        lane[
            "prev_y"
        ] = heights[
            last_distance - 1
        ]


    return True


# ============================================================
# START STRUCTURE
# ============================================================

def create_start_structure(state):

    """
    スタート地点の後ろに設備を作る。

    進行方向:
        Z+

    スタート地点:
        distance = 0

    設備:
        distance = -1

    高さ:
        地面 + 1

    構成:

        羊毛   ← レーン
        コンクリート
        ボタン

    各レーン:

        white concrete
        orange concrete
        light_blue concrete
        lime concrete
        yellow concrete

    ボタンはストーンボタン。
    コンクリートの進行方向側の面に設置。
    """

    lanes = state["lanes"]

    m.echo(
        "================================"
    )

    m.echo(
        "CREATING START STRUCTURE"
    )

    m.echo(
        "================================"
    )


    for lane in lanes:

        sx, sy, sz = lane[
            "start"
        ]

        color = lane[
            "color"
        ]


        # ====================================================
        # スタート地点の地面
        #
        # distance = -1
        # ====================================================

        x = (
            sx
            + FX * -1
        )

        z = (
            sz
            + FZ * -1
        )


        # ====================================================
        # 地面を取得
        # ====================================================

        ground_y = (
            lane["start"][1]
        )

        surface_y = (
            find_surface_retry(
                x,
                z,
                ground_y,
                color,
                -1
            )
        )


        if surface_y is None:

            m.echo(
                f"START GROUND NOT FOUND "
                f"lane={color}"
            )

            continue


        # ====================================================
        # コンクリート
        #
        # 地面の1個上
        # ====================================================

        concrete = (
            f"minecraft:"
            f"{color}_concrete"
        )


        concrete_y = (
            surface_y + 1
        )


        m.execute(
            f"setblock "
            f"{x} "
            f"{concrete_y} "
            f"{z} "
            f"{concrete}"
        )


        # ====================================================
        # ボタン
        #
        # コンクリートの進行方向側
        #
        # Z+進行なので
        # south face
        # ====================================================

        button_x = x

        button_y = concrete_y

        button_z = (
            z + FZ
        )


        # ----------------------------------------------------
        # ボタンをコンクリートの進行方向側に設置
        #
        # Stone Button
        # facing=south
        # ----------------------------------------------------

        m.execute(
            f"setblock "
            f"{button_x} "
            f"{button_y} "
            f"{button_z-2} "
            f"minecraft:stone_button"
            f"[face=wall,facing=north]"
        )


        m.echo(
            f"START {color} "
            f"concrete=({x},{concrete_y},{z}) "
            f"button=({button_x},{button_y},{button_z})"
        )


    m.echo(
        "================================"
    )

    m.echo(
        "START STRUCTURE COMPLETE"
    )

    m.echo(
        "================================"
    )


# ============================================================
# SPECTATOR TP TO AREA
# ============================================================

def spectator_tp_to_area(
    lane,
    area_start,
    area_end
):

    sx, sy, sz = lane[
        "start"
    ]


    center_distance = (
        area_start
        + TP_CENTER_OFFSET
    )


    if center_distance >= area_end:

        center_distance = (
            area_start
            + (
                area_end
                - area_start
            ) // 2
        )


    x = (
        sx
        + FX * center_distance
    )

    z = (
        sz
        + FZ * center_distance
    )


    y = (
        lane["last_y"]
        + SPECTATOR_HEIGHT
    )


    m.execute(
        "gamemode spectator"
    )

    time.sleep(
        0.15
    )


    m.echo(
        f"Spectator TP -> "
        f"{center_distance} "
        f"({x}, {y}, {z})"
    )


    m.execute(
        f"tp @s "
        f"{x} "
        f"{y} "
        f"{z}"
    )


    time.sleep(
        TP_WAIT
    )


# ============================================================
# PRELOAD AREA
# ============================================================

def preload_area(
    lane,
    area_start,
    area_end
):

    sx, sy, sz = lane[
        "start"
    ]


    test_distances = [

        area_start,

        min(
            area_start + 50,
            area_end - 1
        ),

        min(
            area_start + 100,
            area_end - 1
        ),

        min(
            area_start + 150,
            area_end - 1
        ),

        area_end - 1
    ]


    test_distances = list(
        dict.fromkeys(
            test_distances
        )
    )


    for attempt in range(
        GROUND_RETRY_COUNT
    ):

        success_count = 0


        for distance in test_distances:

            x = (
                sx
                + FX * distance
            )

            z = (
                sz
                + FZ * distance
            )


            try:

                block = m.getblock(
                    x,
                    lane["last_y"],
                    z
                )


                if isinstance(
                    block,
                    str
                ):

                    success_count += 1


            except Exception:

                pass


        if (
            success_count
            == len(test_distances)
        ):

            return True


        time.sleep(
            GROUND_RETRY_WAIT
        )


    return False


# ============================================================
# GENERATE AREA
# ============================================================

def generate_area(
    state,
    area_start,
    area_end
):

    lanes = state[
        "lanes"
    ]


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
        "FAST GETBLOCKLIST MODE"
    )

    m.echo(
        "================================"
    )


    area_start_time = time.time()


    # ========================================================
    # TP
    # ========================================================

    first_lane = lanes[0]


    spectator_tp_to_area(
        first_lane,
        area_start,
        area_end
    )


    # ========================================================
    # PRELOAD
    # ========================================================

    preload_ok = preload_area(
        first_lane,
        area_start,
        area_end
    )


    if not preload_ok:

        m.echo(
            "GROUND LOAD FAILED"
        )

        return False


    # ========================================================
    # 50 BLOCK SLICES
    # ========================================================

    current = area_start


    while current < area_end:

        slice_end = min(
            current + SLICE_LENGTH,
            area_end
        )


        slice_start_time = time.time()


        m.echo(
            f"GROUND "
            f"{slice_end}/"
            f"{area_end}"
        )


        # ====================================================
        # HEIGHT SCAN
        # ====================================================

        height_data = []


        for lane in lanes:

            heights = (
                generate_lane_heights(
                    lane,
                    current,
                    slice_end
                )
            )


            if heights is None:

                m.echo(
                    "================================"
                )

                m.echo(
                    "GROUND LOAD FAILED"
                )

                m.echo(
                    f"AREA "
                    f"{area_start}-"
                    f"{area_end}"
                )

                m.echo(
                    f"distance={current}"
                )

                m.echo(
                    f"lane={lane['color']}"
                )

                m.echo(
                    "================================"
                )

                return False


            height_data.append(
                heights
            )


        # ====================================================
        # BUILD
        # ====================================================

        for index, lane in enumerate(
            lanes
        ):

            success = (
                apply_lane_heights(
                    lane,
                    height_data[index],
                    current,
                    slice_end
                )
            )


            if not success:

                return False


        # ====================================================
        # SAVE
        # ====================================================

        current = slice_end


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
            - slice_start_time,
            3
        )


        m.echo(
            f"GROUND "
            f"{current}/"
            f"{area_end} "
            f"| {elapsed}s"
        )


    # ========================================================
    # AREA COMPLETE
    # ========================================================

    area_elapsed = round(
        time.time()
        - area_start_time,
        2
    )


    m.echo(
        "================================"
    )

    m.echo(
        f"AREA COMPLETE "
        f"{area_start}-"
        f"{area_end}"
    )

    m.echo(
        f"TIME : {area_elapsed}s"
    )

    m.echo(
        "================================"
    )


    return True


# ============================================================
# GENERATE COURSE
# ============================================================

def generate_course():

    save_player_state()


    state = load_state()


    current = state.get(
        "current_length",
        0
    )


    lanes = state[
        "lanes"
    ]


    # ========================================================
    # 最初にスタート設備
    # ========================================================

    if current == 0:

        create_start_structure(
            state
        )


    # ========================================================
    # TIME LOG
    # ========================================================

    if os.path.exists(
        TIME_FILE
    ):

        try:

            with open(
                TIME_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                time_log = json.load(f)

        except Exception:

            time_log = {}

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
        "VERSION : v0.8.00"
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
        "Ground  : GETBLOCKLIST"
    )

    m.echo(
        "Fallback: GETBLOCK"
    )

    m.echo(
        "Start   : CONCRETE + BUTTON"
    )

    m.echo(
        "================================"
    )


    total_start = time.time()


    try:

        m.execute(
            "gamemode spectator"
        )

        time.sleep(
            0.3
        )


        # ====================================================
        # AREA LOOP
        # ====================================================

        while current < TOTAL_LENGTH:

            area_start = current

            area_end = min(
                current + AREA_LENGTH,
                TOTAL_LENGTH
            )


            success = generate_area(
                state,
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
                    "Run 'set' again to retry."
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


            total_elapsed = round(
                time.time()
                - total_start,
                2
            )


            time_log[
                str(current)
            ] = total_elapsed


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
                f"PROGRESS "
                f"{current}/"
                f"{TOTAL_LENGTH} "
                f"| total "
                f"{total_elapsed}s"
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
            "Lanes  : 5"
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

        # ====================================================
        # SURVIVAL + 元位置
        # ====================================================

        restore_player()


# ============================================================
# SET0
# ============================================================

def setup_only():

    """
    set0

    現在位置をスタート地点として登録し、
    スタート設備だけを作る。

    レーン本体は生成しない。
    """

    save_player_state()


    state = create_state()


    m.echo(
        "================================"
    )

    m.echo(
        "LINERACE START SETUP"
    )

    m.echo(
        "COMMAND : set0"
    )

    m.echo(
        "================================"
    )


    # ========================================================
    # スタート設備作成
    # ========================================================

    create_start_structure(
        state
    )


    # ========================================================
    # プレイヤーを元位置へ
    # ========================================================

    restore_player()


    m.echo(
        "================================"
    )

    m.echo(
        "SET0 COMPLETE"
    )

    m.echo(
        "Start structure created."
    )

    m.echo(
        "Run 'set' to generate course."
    )

    m.echo(
        "================================"
    )


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
            "World blocks were NOT deleted."
        )

        m.echo(
            "Run 'set0' to create start."
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
            "  set0"
        )

        m.echo(
            "  reset"
        )

        sys.exit()


    command = sys.argv[1]


    if command == "set":

        generate_course()


    elif command == "set0":

        setup_only()


    elif command == "reset":

        reset_course()


    else:

        m.echo(
            f"Unknown command: {command}"
        )
