# ============================================================
# LINERACE COURSE GENERATOR
# Version : v0.3.00
#
# Minecraft Java Edition + Minescript
#
# Features
#   ・5レーン直線コース
#   ・1レーンずつ生成
#   ・200ブロック単位で進行
#   ・Spectator方式でチャンク読み込み
#   ・forceload 不使用
#   ・tp で生成地点付近へ移動
#   ・地面に近い高さへ移動
#   ・getblocklist() による高速地面探索
#   ・「一番上の床」を取得
#   ・地面上の雪はウールに置換
#   ・木や葉の上の雪は無視
#   ・木の根元の地面を優先
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

# レーン間隔
BLOCK_SPACING = 2

# コース長
TOTAL_LENGTH = 1000

# ------------------------------------------------------------
# 安定性重視
# ------------------------------------------------------------
# 200ブロックごとに区切る
CHUNK_LENGTH = 200

# 地形探索をまとめる単位
SLICE_LENGTH = 50

# ------------------------------------------------------------
# Spectator loading
# ------------------------------------------------------------

# TP後の待機時間
TP_WAIT = 0.6

# 200ブロック区間内で
# 追加のチャンク読み込み移動を行う間隔
LOAD_STEP = 16

# 追加移動後の待機
LOAD_WAIT = 0.12

# Spectatorで地面からどのくらい上にいるか
SPECTATOR_HEIGHT = 5


# ============================================================
# DIRECTION
# ============================================================

# 進行方向
# south
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

PLAYER_STATE_FILE = (
    f"{BASE_DIR}/player_state.json"
)


def save_player_state():

    try:

        px, py, pz = m.player_position()

        state = {
            "position": [
                px,
                py,
                pz
            ]
        }

        # gamemodeは取得できない環境もあるので
        # positionだけ保存
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

        # クリエイティブへ戻す
        m.execute(
            "gamemode creative"
        )

        time.sleep(0.2)

        m.execute(
            f"tp @s {x} {y} {z}"
        )

        time.sleep(0.3)

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

    for index, block in enumerate(blocks):

        if is_surface(block):

            return search_ys[index]

    return None


# ============================================================
# FIND SURFACE WITH TREE PROTECTION
# ============================================================

def find_surface_safe(
    x,
    z,
    search_ys,
    blocks
):

    for index, block in enumerate(blocks):

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
        #
        # 雪の下が木・葉なら
        # この雪は「地面の雪」ではない
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

        # ----------------------------------------------------
        # 雪の下が通常の地面
        # ----------------------------------------------------

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
    # 1ブロック
    # --------------------------------------------------------

    if start_distance == end_distance:

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
# SPECTATOR TP
# ============================================================

def spectator_tp(
    lane,
    distance
):

    sx, sy, sz = lane["start"]

    x = sx + FX * distance
    z = sz + FZ * distance

    # --------------------------------------------------------
    # 現在のYをざっくり利用
    # --------------------------------------------------------

    y = lane["last_y"] + SPECTATOR_HEIGHT

    # --------------------------------------------------------
    # Spectator
    # --------------------------------------------------------

    m.execute(
        "gamemode spectator"
    )

    time.sleep(0.1)

    m.execute(
        f"tp @s {x} {y} {z}"
    )

    time.sleep(
        TP_WAIT
    )


# ============================================================
# LOAD CHUNKS AROUND AREA
# ============================================================

def prepare_area(
    lane,
    start_distance,
    end_distance
):

    """
    200ブロック区間を、
    Spectatorで少しずつ移動して
    チャンクを読み込ませる。

    forceloadは使用しない。
    """

    m.echo(
        f"Preparing chunks "
        f"{start_distance}-{end_distance}"
    )

    distance = start_distance

    while distance < end_distance:

        spectator_tp(
            lane,
            distance
        )

        distance += LOAD_STEP

    # 最後の地点
    spectator_tp(
        lane,
        end_distance - 1
    )

    m.echo(
        "Chunk preparation complete."
    )


# ============================================================
# GENERATE ONE 200 BLOCK AREA
# ============================================================

def generate_area(
    lane,
    start_distance,
    end_distance
):

    m.echo(
        f"Generate "
        f"{start_distance}-{end_distance}"
    )

    current = start_distance

    while current < end_distance:

        slice_end = min(
            current + SLICE_LENGTH,
            end_distance
        )

        start_time = time.time()

        # ----------------------------------------------------
        # その区間へ移動
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
        # ブロック生成
        # ----------------------------------------------------

        apply_lane_heights(
            lane,
            heights,
            current,
            slice_end
        )

        elapsed = round(
            time.time() - start_time,
            3
        )

        current = slice_end

        m.echo(
            f"{lane['color']} "
            f"{current}/{TOTAL_LENGTH} "
            f"| {elapsed}s"
        )

    return lane


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

    lane_start = time.time()

    current = 0

    while current < TOTAL_LENGTH:

        end_distance = min(
            current + CHUNK_LENGTH,
            TOTAL_LENGTH
        )

        m.echo(
            "================================"
        )

        m.echo(
            f"AREA "
            f"{current}-{end_distance}"
        )

        # ----------------------------------------------------
        # まずSpectatorで周辺チャンクを読み込む
        # ----------------------------------------------------

        prepare_area(
            lane,
            current,
            end_distance
        )

        # ----------------------------------------------------
        # 実際に生成
        # ----------------------------------------------------

        generate_area(
            lane,
            current,
            end_distance
        )

        # ----------------------------------------------------
        # 200ごとに保存
        # ----------------------------------------------------

        current = end_distance

        m.echo(
            f"AREA COMPLETE "
            f"{current}/{TOTAL_LENGTH}"
        )

    lane_elapsed = round(
        time.time() - lane_start,
        2
    )

    m.echo(
        f"LANE COMPLETE "
        f"{lane_index + 1}/{LINE_COUNT} "
        f"| {lane_elapsed}s"
    )

    return lane_elapsed


# ============================================================
# COURSE GENERATION
# ============================================================

def generate_course():

    save_player_state()

    state = load_state()

    current_lane = state.get(
        "current_lane",
        0
    )

    lanes = state["lanes"]

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
    # Spectator開始
    # --------------------------------------------------------

    m.execute(
        "gamemode spectator"
    )

    time.sleep(0.3)

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
        f"Lane : "
        f"{current_lane + 1}/{LINE_COUNT}"
    )

    m.echo(
        "Mode : SPECTATOR"
    )

    m.echo(
        "Chunk loading : PLAYER"
    )

    m.echo(
        "forceload : OFF"
    )

    m.echo(
        "================================"
    )

    try:

        # ====================================================
        # LANE LOOP
        # ====================================================

        for lane_index in range(
            current_lane,
            LINE_COUNT
        ):

            lane = lanes[lane_index]

            lane_elapsed = generate_one_lane(
                lane_index,
                lane
            )

            # ------------------------------------------------
            # レーン完了保存
            # ------------------------------------------------

            state["current_lane"] = (
                lane_index + 1
            )

            state["current_length"] = 0

            state["lanes"] = lanes

            save_state(
                state
            )

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

        # ====================================================
        # COMPLETE
        # ====================================================

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

    finally:

        # ----------------------------------------------------
        # 終了時にプレイヤーを戻す
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
