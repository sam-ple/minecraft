# ============================================================
# LINERACE COURSE GENERATOR
# Version : v0.9.02
#
# Minecraft Java Edition + Minescript
#
# Features
#   ・5レーン直線コース
#   ・レーン本体は各色の羊毛
#   ・スタート地点に各色コンクリート
#   ・コンクリートにストーンボタン
#   ・set0でスタート設備だけ設置
#   ・setでスタート設備設置後にレーン生成
#   ・200ブロック単位で処理
#   ・50ブロック単位で地形取得
#   ・getblocklist()による高速探索
#   ・失敗時はgetblock()による強化探索
#   ・地面候補を広く判定
#   ・崖 / 坂 / 大きな段差対応
#   ・地形の高さに追従
#   ・地面の雪をウールに置換
#   ・木 / 葉の上の雪は無視
#   ・AREAごとのFORCELOAD
#   ・前後1チャンクのバッファ
#   ・FORCELOAD後にロード確認
#   ・AREA完了後にFORCELOAD REMOVE
#   ・Spectator TP不使用
#   ・200ブロックごとに自動保存
#   ・途中から再開可能
#   ・resetで生成状態をリセット
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

BLOCK_SPACING = 2

TOTAL_LENGTH = 1000

AREA_LENGTH = 200

SLICE_LENGTH = 50


# ============================================================
# FORCELOAD SETTINGS
# ============================================================

FORCELOAD_BUFFER_CHUNKS = 1

FORCELOAD_WAIT = 1.5

FORCELOAD_RETRY_COUNT = 5

FORCELOAD_RETRY_WAIT = 0.5


# ============================================================
# GROUND SEARCH SETTINGS
# ============================================================

GROUND_RETRY_COUNT = 3

GROUND_RETRY_WAIT = 0.15

FALLBACK_WAIT = 0.3

DEEP_FALLBACK_WAIT = 0.5

# 通常探索
FAST_SEARCH_UP = 16
FAST_SEARCH_DOWN = 24

# fallback
FALLBACK_SEARCH_UP = 48
FALLBACK_SEARCH_DOWN = 128

# deep
DEEP_SEARCH_UP = 96
DEEP_SEARCH_DOWN = 192


# ============================================================
# DIRECTION
# ============================================================

DIRECTION = "south"

DIRECTIONS = {
    "north": (0, -1),
    "south": (0, 1),
    "east":  (1, 0),
    "west":  (-1, 0)
}

FX, FZ = DIRECTIONS[DIRECTION]

RX = -FZ
RZ = FX


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

    "minecraft:deepslate",

    "minecraft:tuff",

    "minecraft:calcite",

    "minecraft:dripstone_block",

    "minecraft:mud",

    "minecraft:packed_mud",

    "minecraft:podzol",
    "minecraft:coarse_dirt",

    "minecraft:moss_block",

    "minecraft:mossy_cobblestone",

    "minecraft:cobblestone",

    "minecraft:dirt_path",

    "minecraft:mycelium",

    "minecraft:snow_block",

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
# NON-GROUND BLOCKS
# ============================================================

NON_GROUND_BLOCKS = {

    "minecraft:air",
    "minecraft:cave_air",
    "minecraft:void_air",

    "minecraft:water",
    "minecraft:lava",

    "minecraft:kelp",
    "minecraft:kelp_plant",

    "minecraft:seagrass",
    "minecraft:tall_seagrass",

    "minecraft:grass",
    "minecraft:fern",
    "minecraft:large_fern",

    "minecraft:vine",

    "minecraft:torch",
    "minecraft:wall_torch",

    "minecraft:redstone_torch",
    "minecraft:redstone_wall_torch",

    "minecraft:fire",
    "minecraft:soul_fire",

    "minecraft:snow",
}


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
# IS SURFACE
# ============================================================

def is_surface(block):

    block = normalize_block(block)

    return block in SURFACE_BLOCKS


# ============================================================
# IS TREE / LEAF
# ============================================================

def is_tree_or_leaf(block):

    block = normalize_block(block)

    return (
        block in WOOD_BLOCKS
        or block in LEAF_BLOCKS
    )


# ============================================================
# IS AIR
# ============================================================

def is_air(block):

    block = normalize_block(block)

    return block in {
        "minecraft:air",
        "minecraft:cave_air",
        "minecraft:void_air"
    }


# ============================================================
# IS WATER
# ============================================================

def is_water(block):

    block = normalize_block(block)

    return block == "minecraft:water"


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
# MAKE SEARCH Y
# ============================================================

def make_search_ys(last_y):

    ys = []

    # まず現在地付近
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


    # 重複削除
    return list(
        dict.fromkeys(
            ys
        )
    )


# ============================================================
# CHECK SURFACE CANDIDATE
# ============================================================

def check_surface_candidate(
    x,
    y,
    z
):

    try:

        block = m.getblock(
            x,
            y,
            z
        )

    except Exception:

        return False


    block_type = normalize_block(
        block
    )


    # --------------------------------------------------------
    # 明確な地面
    # --------------------------------------------------------

    if is_surface(
        block_type
    ):

        # 雪の場合
        if block_type == "minecraft:snow":

            try:

                below = m.getblock(
                    x,
                    y - 1,
                    z
                )

                if is_tree_or_leaf(
                    below
                ):

                    return False

            except Exception:

                pass


        return True


    # --------------------------------------------------------
    # 木・葉は地面ではない
    # --------------------------------------------------------

    if is_tree_or_leaf(
        block_type
    ):

        return False


    # --------------------------------------------------------
    # 水・溶岩は地面ではない
    # --------------------------------------------------------

    if is_water(
        block_type
    ):

        return False

    if block_type == "minecraft:lava":

        return False


    # --------------------------------------------------------
    # 空気は地面ではない
    # --------------------------------------------------------

    if is_air(
        block_type
    ):

        return False


    # --------------------------------------------------------
    # 明らかな非地面ブロック
    # --------------------------------------------------------

    if block_type in NON_GROUND_BLOCKS:

        return False


    # --------------------------------------------------------
    # 一般ブロック
    #
    # 「その下が空気」なら地表候補
    #
    # これによりSURFACE_BLOCKSにない
    # 自然地形ブロックにも対応
    # --------------------------------------------------------

    try:

        below = m.getblock(
            x,
            y - 1,
            z
        )

    except Exception:

        return False


    below_type = normalize_block(
        below
    )


    if is_air(
        below_type
    ):

        return False


    return False


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

        if not is_surface(
            block
        ):

            continue


        y = search_ys[index]

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

    except Exception as e:

        m.echo(
            f"GETBLOCKLIST ERROR "
            f"x={x} z={z} "
            f"error={e}"
        )

        return None


    if blocks is None:

        return None


    if len(blocks) != len(
        search_ys
    ):

        m.echo(
            f"GETBLOCKLIST LENGTH ERROR "
            f"x={x} z={z} "
            f"blocks={len(blocks)} "
            f"expected={len(search_ys)}"
        )

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

    # --------------------------------------------------------
    # まず現在の高さから下を優先
    # --------------------------------------------------------

    for dy in range(
        8,
        -FALLBACK_SEARCH_DOWN - 1,
        -1
    ):

        y = last_y + dy

        if check_surface_candidate(
            x,
            y,
            z
        ):

            return y


    # --------------------------------------------------------
    # それでもダメなら上方向
    # --------------------------------------------------------

    for dy in range(
        9,
        FALLBACK_SEARCH_UP + 1
    ):

        y = last_y + dy

        if check_surface_candidate(
            x,
            y,
            z
        ):

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

    # --------------------------------------------------------
    # 下方向
    # --------------------------------------------------------

    for dy in range(
        12,
        -DEEP_SEARCH_DOWN - 1,
        -1
    ):

        y = last_y + dy

        if check_surface_candidate(
            x,
            y,
            z
        ):

            return y


    # --------------------------------------------------------
    # 上方向
    # --------------------------------------------------------

    for dy in range(
        13,
        DEEP_SEARCH_UP + 1
    ):

        y = last_y + dy

        if check_surface_candidate(
            x,
            y,
            z
        ):

            return y


    return None


# ============================================================
# DEBUG BLOCK
# ============================================================

def debug_ground(
    x,
    z,
    last_y
):

    try:

        m.echo(
            "GROUND DEBUG "
            f"x={x} "
            f"z={z} "
            f"last_y={last_y}"
        )

        for dy in range(
            5,
            -16,
            -1
        ):

            y = last_y + dy

            block = m.getblock(
                x,
                y,
                z
            )

            m.echo(
                f"  y={y} "
                f"{normalize_block(block)}"
            )

    except Exception as e:

        m.echo(
            f"GROUND DEBUG ERROR {e}"
        )


# ============================================================
# FIND SURFACE RETRY
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
    # GETBLOCKLIST
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
            f"distance={distance} "
            f"y={surface_y}"
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


    # ========================================================
    # DEBUG
    # ========================================================

    m.echo(
        "GROUND SEARCH FAILED"
    )

    debug_ground(
        x,
        z,
        last_y
    )


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

    m.echo(
        "================================"
    )

    m.echo(
        "CREATING START STRUCTURE"
    )

    m.echo(
        "================================"
    )


    for lane in state["lanes"]:

        sx, sy, sz = lane[
            "start"
        ]

        color = lane[
            "color"
        ]


        x = (
            sx
            + FX * -1
        )

        z = (
            sz
            + FZ * -1
        )


        ground_y = lane[
            "start"
        ][1]


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


        button_x = x

        button_y = concrete_y

        button_z = (
            z + FZ
        )


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
# AREA BLOCK RANGE
# ============================================================

def get_area_block_range(
    lanes,
    area_start,
    area_end
):

    positions = []


    for lane in lanes:

        sx, sy, sz = lane[
            "start"
        ]


        start_x = (
            sx
            + FX * area_start
        )

        start_z = (
            sz
            + FZ * area_start
        )


        end_x = (
            sx
            + FX * (area_end - 1)
        )

        end_z = (
            sz
            + FZ * (area_end - 1)
        )


        positions.append(
            (
                start_x,
                start_z
            )
        )

        positions.append(
            (
                end_x,
                end_z
            )
        )


    min_x = min(
        p[0]
        for p in positions
    )

    max_x = max(
        p[0]
        for p in positions
    )

    min_z = min(
        p[1]
        for p in positions
    )

    max_z = max(
        p[1]
        for p in positions
    )


    return (
        min_x,
        max_x,
        min_z,
        max_z
    )


# ============================================================
# BLOCK TO CHUNK
# ============================================================

def block_to_chunk(
    block
):

    return math.floor(
        block / 16
    )


# ============================================================
# FORCELOAD CHUNK RANGE
# ============================================================

def get_forceload_chunk_range(
    lanes,
    area_start,
    area_end
):

    (
        min_x,
        max_x,
        min_z,
        max_z
    ) = get_area_block_range(
        lanes,
        area_start,
        area_end
    )


    min_chunk_x = (
        block_to_chunk(
            min_x
        )
        - FORCELOAD_BUFFER_CHUNKS
    )

    max_chunk_x = (
        block_to_chunk(
            max_x
        )
        + FORCELOAD_BUFFER_CHUNKS
    )

    min_chunk_z = (
        block_to_chunk(
            min_z
        )
        - FORCELOAD_BUFFER_CHUNKS
    )

    max_chunk_z = (
        block_to_chunk(
            max_z
        )
        + FORCELOAD_BUFFER_CHUNKS
    )


    return (
        min_chunk_x,
        max_chunk_x,
        min_chunk_z,
        max_chunk_z
    )


# ============================================================
# FORCELOAD TEST
# ============================================================

def test_forceload_area(
    lanes,
    area_start,
    area_end
):

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


    positions = []


    for lane in lanes:

        sx, sy, sz = lane[
            "start"
        ]

        for distance in test_distances:

            x = (
                sx
                + FX * distance
            )

            z = (
                sz
                + FZ * distance
            )

            positions.append([
                x,
                lane["last_y"],
                z
            ])


    expected = len(
        positions
    )


    for attempt in range(
        FORCELOAD_RETRY_COUNT
    ):

        try:

            blocks = m.getblocklist(
                positions
            )

        except Exception as e:

            m.echo(
                f"FORCELOAD CHECK ERROR "
                f"attempt={attempt + 1}/"
                f"{FORCELOAD_RETRY_COUNT} "
                f"error={e}"
            )

            blocks = None


        if blocks is not None:

            actual = len(
                blocks
            )

            if actual == expected:

                m.echo(
                    f"FORCELOAD READY "
                    f"({actual}/{expected}) "
                    f"attempt={attempt + 1}"
                )

                return True


        if attempt < (
            FORCELOAD_RETRY_COUNT - 1
        ):

            time.sleep(
                FORCELOAD_RETRY_WAIT
            )


    m.echo(
        "FORCELOAD LOAD CHECK FAILED"
    )

    return False


# ============================================================
# FORCELOAD ADD
# ============================================================

def forceload_area(
    lanes,
    area_start,
    area_end
):

    (
        min_chunk_x,
        max_chunk_x,
        min_chunk_z,
        max_chunk_z
    ) = get_forceload_chunk_range(
        lanes,
        area_start,
        area_end
    )


    x1 = (
        min_chunk_x * 16
    )

    z1 = (
        min_chunk_z * 16
    )

    x2 = (
        max_chunk_x * 16
    )

    z2 = (
        max_chunk_z * 16
    )


    m.echo(
        "================================"
    )

    m.echo(
        "FORCELOAD ADD"
    )

    m.echo(
        f"AREA : "
        f"{area_start}-"
        f"{area_end}"
    )

    m.echo(
        f"CHUNK X : "
        f"{min_chunk_x} ~ "
        f"{max_chunk_x}"
    )

    m.echo(
        f"CHUNK Z : "
        f"{min_chunk_z} ~ "
        f"{max_chunk_z}"
    )

    m.echo(
        f"BUFFER : "
        f"{FORCELOAD_BUFFER_CHUNKS}"
    )

    m.echo(
        f"WAIT : "
        f"{FORCELOAD_WAIT}s"
    )

    m.echo(
        "================================"
    )


    m.execute(
        f"forceload add "
        f"{x1} {z1} "
        f"{x2} {z2}"
    )


    time.sleep(
        FORCELOAD_WAIT
    )


    test_forceload_area(
        lanes,
        area_start,
        area_end
    )


    return (
        min_chunk_x,
        max_chunk_x,
        min_chunk_z,
        max_chunk_z
    )


# ============================================================
# FORCELOAD REMOVE
# ============================================================

def remove_forceload(
    chunk_range
):

    if chunk_range is None:
        return


    (
        min_chunk_x,
        max_chunk_x,
        min_chunk_z,
        max_chunk_z
    ) = chunk_range


    x1 = (
        min_chunk_x * 16
    )

    z1 = (
        min_chunk_z * 16
    )

    x2 = (
        max_chunk_x * 16
    )

    z2 = (
        max_chunk_z * 16
    )


    m.echo(
        "================================"
    )

    m.echo(
        "FORCELOAD REMOVE"
    )

    m.echo(
        f"CHUNK X : "
        f"{min_chunk_x} ~ "
        f"{max_chunk_x}"
    )

    m.echo(
        f"CHUNK Z : "
        f"{min_chunk_z} ~ "
        f"{max_chunk_z}"
    )

    m.echo(
        "================================"
    )


    m.execute(
        f"forceload remove "
        f"{x1} {z1} "
        f"{x2} {z2}"
    )


    time.sleep(
        0.2
    )


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
        "FORCELOAD MODE"
    )

    m.echo(
        "================================"
    )


    area_start_time = time.time()

    force_range = None


    try:

        force_range = forceload_area(
            lanes,
            area_start,
            area_end
        )


        current = area_start


        while current < area_end:

            slice_end = min(
                current + SLICE_LENGTH,
                area_end
            )


            slice_start_time = (
                time.time()
            )


            m.echo(
                f"GROUND "
                f"{slice_end}/"
                f"{area_end}"
            )


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


    finally:

        if force_range is not None:

            remove_forceload(
                force_range
            )


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


    if current == 0:

        create_start_structure(
            state
        )


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


    m.echo(
        "================================"
    )

    m.echo(
        "LINERACE COURSE GENERATOR"
    )

    m.echo(
        "VERSION : v0.9.02"
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
        "Mode    : FORCELOAD"
    )

    m.echo(
        "Ground  : GETBLOCKLIST + FALLBACK"
    )

    m.echo(
        "================================"
    )


    total_start = time.time()


    try:

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

        restore_player()


# ============================================================
# SET0
# ============================================================

def setup_only():

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


    create_start_structure(
        state
    )


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
