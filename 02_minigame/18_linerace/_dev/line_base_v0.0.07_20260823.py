# ============================================================
# LINERACE COURSE GENERATOR
# Version : v0.4.00
#
# Minecraft Java Edition + Minescript
#
# Generation method
#   ・200ブロック単位で進行
#   ・1区間につき5レーンを生成
#   ・白 → オレンジ → 水色 → 黄緑 → 黄色
#   ・5レーン完了後、次の200ブロックへ移動
#   ・Spectatorで生成予定地点を先読み
#   ・forceload 不使用
#   ・長距離TPは区間開始時のみ
#   ・地面に近い高さでSpectator移動
#   ・getblocklist() による地面探索
#   ・地面上の雪は使用
#   ・木や葉の上の雪は無視
#   ・同一高度区間はfill
#   ・200ブロック単位で状態保存
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

# レーン間隔
BLOCK_SPACING = 2

# コース長
TOTAL_LENGTH = 1000

# ------------------------------------------------------------
# 200ブロック単位
# ------------------------------------------------------------

AREA_LENGTH = 200

# 地形探索単位
SLICE_LENGTH = 50


# ============================================================
# SPECTATOR SETTINGS
# ============================================================

# 区間へ移動した後の待機
TP_WAIT = 0.8

# 200区間を先読みするときの移動間隔
LOAD_STEP = 16

# 各移動後の待機
LOAD_WAIT = 0.10

# 地面から上へ何ブロック離すか
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

# この順番で1区間ずつ生成する
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
# PLAYER STATE
# ============================================================

def save_player_state():

    try:

        px, py, pz = (
            m.player_position()
        )

        state = {
            "position": [
                px,
                py,
                pz
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

        x, y, z = (
            state["position"]
        )

        # Creativeへ戻す
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
# INITIAL STATE
# ============================================================

def create_initial_state():

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

    # --------------------------------------------------------
    # Lane information
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Generation state
    # --------------------------------------------------------

    state = {

        # ★ 現在の200ブロック区間
        #
        # 0 = 0～200
        # 1 = 200～400
        # 2 = 400～600
        # ...

        "current_area": 0,

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
            last_y
            + SURFACE_SEARCH_UP,

            last_y
            - SURFACE_SEARCH_DOWN
            - 1,

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

        if not is_surface(
            block
        ):

            continue

        y = search_ys[index]

        block_type = (
            normalize_block(
                block
            )
        )

        # ----------------------------------------------------
        # 通常の地面
        # ----------------------------------------------------

        if (
            block_type
            != "minecraft:snow"
        ):

            return y

        # ----------------------------------------------------
        # 雪の場合
        #
        # 雪の下が木・葉なら無視
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
# GENERATE HEIGHTS
# ============================================================

def generate_lane_heights_fast(
    lane,
    start_distance,
    end_distance
):

    sx, sy, sz = (
        lane["start"]
    )

    heights = {}

    current_y = (
        lane["last_y"]
    )

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

        search_ys = (
            make_search_ys(
                current_y
            )
        )

        positions = [
            [
                x,
                y,
                z
            ]

            for y in search_ys
        ]

        blocks = (
            m.getblocklist(
                positions
            )
        )

        found_y = (
            find_surface_safe(
                x,
                z,
                search_ys,
                blocks
            )
        )

        if found_y is None:

            found_y = current_y

        heights[
            distance
        ] = found_y

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

    sx, sy, sz = (
        lane["start"]
    )

    x = (
        sx
        + FX * distance
    )

    z = (
        sz
        + FZ * distance
    )

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

    if (
        end_distance
        < start_distance
    ):

        return

    sx, sy, sz = (
        lane["start"]
    )

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

    block = (
        f"minecraft:{lane['color']}_wool"
    )

    # --------------------------------------------------------
    # 1ブロック
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # X方向
    # --------------------------------------------------------

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
    # FILL
    # --------------------------------------------------------

    m.execute(
        f"fill "
        f"{min_x} {ground_y} {min_z} "
        f"{max_x} {ground_y} {max_z} "
        f"{block}"
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

        return

    fill_start = None
    fill_y = None

    for distance in range(
        start_distance,
        end_distance
    ):

        ground_y = (
            heights[distance]
        )

        # ----------------------------------------------------
        # 初回
        # ----------------------------------------------------

        if fill_start is None:

            fill_start = distance
            fill_y = ground_y

            continue

        # ----------------------------------------------------
        # 同じ高さ
        # ----------------------------------------------------

        if ground_y == fill_y:

            continue

        # ----------------------------------------------------
        # 高さ変更
        # ----------------------------------------------------

        fill_lane_range(
            lane,
            fill_start,
            distance - 1,
            fill_y
        )

        fill_start = distance
        fill_y = ground_y

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

    # --------------------------------------------------------
    # Y履歴
    # --------------------------------------------------------

    last_distance = (
        end_distance - 1
    )

    lane["last_y"] = (
        heights[last_distance]
    )

    if (
        last_distance
        > start_distance
    ):

        lane["prev_y"] = (
            heights[
                last_distance - 1
            ]
        )


# ============================================================
# SPECTATOR TP
# ============================================================

def spectator_tp(
    lane,
    distance
):

    sx, sy, sz = (
        lane["start"]
    )

    x = (
        sx
        + FX * distance
    )

    z = (
        sz
        + FZ * distance
    )

    # --------------------------------------------------------
    # 現在の地面高さ付近
    # --------------------------------------------------------

    y = (
        lane["last_y"]
        + SPECTATOR_HEIGHT
    )

    m.execute(
        "gamemode spectator"
    )

    time.sleep(
        0.05
    )

    m.execute(
        f"tp @s {x} {y} {z}"
    )

    time.sleep(
        TP_WAIT
    )


# ============================================================
# PREPARE AREA
# ============================================================

def prepare_area(
    lane,
    start_distance,
    end_distance
):

    """
    200ブロック区間を
    Spectatorで先読みする。

    forceloadは使用しない。
    """

    m.echo(
        f"PREPARE "
        f"{start_distance}"
        f"-"
        f"{end_distance}"
    )

    distance = (
        start_distance
    )

    # --------------------------------------------------------
    # 区間内を16ブロックずつ移動
    # --------------------------------------------------------

    while (
        distance
        < end_distance
    ):

        spectator_tp(
            lane,
            distance
        )

        distance += LOAD_STEP

        time.sleep(
            LOAD_WAIT
        )

    # --------------------------------------------------------
    # 区間終端
    # --------------------------------------------------------

    spectator_tp(
        lane,
        end_distance - 1
    )

    m.echo(
        "PREPARE COMPLETE"
    )


# ============================================================
# GENERATE ONE LANE / ONE AREA
# ============================================================

def generate_lane_area(
    lane_index,
    lane,
    start_distance,
    end_distance
):

    m.echo(
        "--------------------------------"
    )

    m.echo(
        f"LANE "
        f"{lane_index + 1}/"
        f"{LINE_COUNT} "
        f"{lane['color']}"
    )

    m.echo(
        f"AREA "
        f"{start_distance}-"
        f"{end_distance}"
    )

    current = (
        start_distance
    )

    lane_start = time.time()

    while (
        current
        < end_distance
    ):

        slice_end = min(
            current + SLICE_LENGTH,
            end_distance
        )

        start_time = (
            time.time()
        )

        # ----------------------------------------------------
        # その地点へ移動
        # ----------------------------------------------------

        spectator_tp(
            lane,
            current
        )

        # ----------------------------------------------------
        # 地形取得
        # ----------------------------------------------------

        heights = (
            generate_lane_heights_fast(
                lane,
                current,
                slice_end
            )
        )

        # ----------------------------------------------------
        # レール生成
        # ----------------------------------------------------

        apply_lane_heights(
            lane,
            heights,
            current,
            slice_end
        )

        current = (
            slice_end
        )

        elapsed = round(
            time.time()
            - start_time,
            3
        )

        m.echo(
            f"{lane['color']} "
            f"{current}/"
            f"{TOTAL_LENGTH} "
            f"| {elapsed}s"
        )

    return round(
        time.time()
        - lane_start,
        2
    )


# ============================================================
# GENERATE ONE 200-BLOCK AREA
# ============================================================

def generate_area(
    area_index,
    lanes
):

    start_distance = (
        area_index
        * AREA_LENGTH
    )

    end_distance = min(
        start_distance
        + AREA_LENGTH,
        TOTAL_LENGTH
    )

    m.echo(
        ""
    )

    m.echo(
        "================================"
    )

    m.echo(
        f"AREA "
        f"{area_index + 1}"
    )

    m.echo(
        f"{start_distance}"
        f"-"
        f"{end_distance}"
    )

    m.echo(
        "================================"
    )

    # ========================================================
    # STEP 1
    # 200ブロック先を先読み
    # ========================================================

    # 最初は白レーンを基準に移動
    prepare_area(
        lanes[0],
        start_distance,
        end_distance
    )

    # ========================================================
    # STEP 2
    # 5レーン生成
    # ========================================================

    area_start = time.time()

    for lane_index in range(
        LINE_COUNT
    ):

        lane = lanes[
            lane_index
        ]

        lane_elapsed = (
            generate_lane_area(
                lane_index,
                lane,
                start_distance,
                end_distance
            )
        )

        m.echo(
            f"LANE "
            f"{lane_index + 1} "
            f"AREA COMPLETE "
            f"| {lane_elapsed}s"
        )

    area_elapsed = round(
        time.time()
        - area_start,
        2
    )

    m.echo(
        "================================"
    )

    m.echo(
        f"AREA COMPLETE "
        f"{start_distance}-"
        f"{end_distance}"
    )

    m.echo(
        f"AREA TIME : "
        f"{area_elapsed}s"
    )

    m.echo(
        "================================"
    )

    return area_elapsed


# ============================================================
# COURSE GENERATION
# ============================================================

def generate_course():

    # --------------------------------------------------------
    # プレイヤー位置保存
    # --------------------------------------------------------

    save_player_state()

    # --------------------------------------------------------
    # State
    # --------------------------------------------------------

    state = load_state()

    current_area = state.get(
        "current_area",
        0
    )

    lanes = state[
        "lanes"
    ]

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

            time_log = json.load(
                f
            )

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

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    total_areas = math.ceil(
        TOTAL_LENGTH
        / AREA_LENGTH
    )

    m.echo(
        "================================"
    )

    m.echo(
        "LineRace Course Generator"
    )

    m.echo(
        "Version : v0.4.00"
    )

    m.echo(
        f"Length : "
        f"{TOTAL_LENGTH}"
    )

    m.echo(
        f"Area : "
        f"{AREA_LENGTH}"
    )

    m.echo(
        f"Areas : "
        f"{total_areas}"
    )

    m.echo(
        f"Current Area : "
        f"{current_area + 1}/"
        f"{total_areas}"
    )

    m.echo(
        "Order : "
        "white → orange → "
        "light_blue → lime → yellow"
    )

    m.echo(
        "Mode : SPECTATOR"
    )

    m.echo(
        "forceload : OFF"
    )

    m.echo(
        "================================"
    )

    try:

        # ====================================================
        # AREA LOOP
        # ====================================================

        for area_index in range(
            current_area,
            total_areas
        ):

            # ------------------------------------------------
            # 200ブロック区間
            # ------------------------------------------------

            area_elapsed = (
                generate_area(
                    area_index,
                    lanes
                )
            )

            # ------------------------------------------------
            # 区間完了保存
            # ------------------------------------------------

            state[
                "current_area"
            ] = area_index + 1

            state[
                "lanes"
            ] = lanes

            save_state(
                state
            )

            # ------------------------------------------------
            # 時間保存
            # ------------------------------------------------

            time_log[
                f"area_{area_index + 1}"
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

            # ------------------------------------------------
            # 完了表示
            # ------------------------------------------------

            m.echo(
                f"AREA SAVED "
                f"{area_index + 1}/"
                f"{total_areas}"
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
            ""
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
            f"AREA SIZE : "
            f"{AREA_LENGTH}"
        )

        m.echo(
            f"TOTAL TIME : "
            f"{total_elapsed}s"
        )

        m.echo(
            "================================"
        )

        # ----------------------------------------------------
        # 完全終了したのでprogress削除
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

    removed = 0

    for path in [

        STATE_FILE,
        LANES_FILE,
        TIME_FILE,
        PLAYER_STATE_FILE

    ]:

        if os.path.exists(
            path
        ):

            os.remove(
                path
            )

            removed += 1

    m.echo(
        "LineRace reset complete "
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

    command = (
        sys.argv[1]
    )

    # --------------------------------------------------------
    # SET
    # --------------------------------------------------------

    if command == "set":

        generate_course()

    # --------------------------------------------------------
    # RESET
    # --------------------------------------------------------

    elif command == "reset":

        reset_course()

    # --------------------------------------------------------
    # UNKNOWN
    # --------------------------------------------------------

    else:

        m.echo(
            f"Unknown command: "
            f"{command}"
        )
