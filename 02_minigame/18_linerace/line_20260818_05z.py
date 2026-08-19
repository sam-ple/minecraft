# ============================================================
# LINERACE COURSE GENERATOR
# Version : v0.2.10
#
# Minecraft Java Edition + Minescript
#
# Features
#   ・5レーン直線コース
#   ・1レーンずつ生成
#   ・地形追従
#   ・getblocklist() による高速地面探索
#   ・「一番上の床」を取得
#   ・雪などがある場合は雪をウールに置換
#   ・同一高度区間は fill
#   ・生成途中保存
#   ・途中から再開可能
#   ・reset による完全リセット
#
# Commands
#   set   : コース生成
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
# TOTAL_LENGTH = 2000

# 1回に探索する距離
SLICE_LENGTH = 50

# 何ブロックごとに状態保存するか
SAVE_INTERVAL = 100

# 進行方向
# Z+
FX, FZ = 0, 1

# 横方向
RX, RZ = 1, 0

# レーンカラー
COLORS = [
    "white",
    "orange",
    "light_blue",
    "lime",
    "yellow"
]


# ============================================================
# GROUND SETTINGS
# ============================================================

# 「床」として扱うブロック
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
    "minecraft:mossy_cobblestone",
    "minecraft:dirt_path",
    "minecraft:mycelium",
    "minecraft:snow_block",
}


# ============================================================
# TOP SURFACE SETTINGS
# ============================================================

# 一番上にある「表面ブロック」を探す範囲
SURFACE_SEARCH_UP = 8

# 前回Yから下へ探す範囲
SURFACE_SEARCH_DOWN = 20

# 表面として扱うブロック
#
# 例えば雪があった場合、
#
#   dirt
#   snow
#
# の snow を表面として取得する。
#
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
# BLOCK TYPE NORMALIZATION
# ============================================================

def normalize_block(block):
    """
    ブロック状態を除去。

    例:

    minecraft:grass_block[snowy=false]
        ↓
    minecraft:grass_block
    """

    if not isinstance(block, str):
        return ""

    return block.split("[", 1)[0]


# ============================================================
# SURFACE CHECK
# ============================================================

def is_surface(block):
    """
    表面として扱えるブロックか判定。
    """

    return (
        normalize_block(block)
        in SURFACE_BLOCKS
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

    # --------------------------------------------------------
    # Lane information
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Generation state
    # --------------------------------------------------------

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
# SEARCH Y VALUES
# ============================================================

def make_search_ys(last_y):

    """
    前回Yを中心に検索。

    上方向を先に見ることで、
    雪などの表面ブロックを優先して取得する。
    """

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
    """
    getblocklist() で取得した結果から
    一番上の表面を探す。

    上から下へ探索するため、
    雪がある場合も雪を優先する。
    """

    for index, block in enumerate(blocks):

        if is_surface(block):

            return search_ys[index]

    return None


# ============================================================
# GENERATE ONE LANE - TERRAIN SEARCH
# ============================================================

def generate_lane_heights(
    lane,
    start_distance,
    end_distance
):
    """
    1レーン分の地形高さを取得。

    ここではまだブロックを置かない。

    50ブロック分をまとめて
    getblocklist() で取得する。
    """

    sx, sy, sz = lane["start"]

    heights = {}

    current_y = lane["last_y"]

    # --------------------------------------------------------
    # distanceごとに探索
    # --------------------------------------------------------

    for distance in range(
        start_distance,
        end_distance
    ):

        x = sx + FX * distance
        z = sz + FZ * distance

        search_ys = make_search_ys(
            current_y
        )

        positions = []

        for y in search_ys:

            positions.append([
                x,
                y,
                z
            ])

        # ----------------------------------------------------
        # 一括取得
        # ----------------------------------------------------

        blocks = m.getblocklist(
            positions
        )

        # ----------------------------------------------------
        # 表面探索
        # ----------------------------------------------------

        found_y = find_surface(
            blocks,
            search_ys
        )

        # ----------------------------------------------------
        # 見つからなかった場合
        # ----------------------------------------------------

        if found_y is None:

            m.echo(
                f"GROUND NOT FOUND "
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
# GENERATE ONE LANE - TERRAIN SEARCH OPTIMIZED
# ============================================================

def generate_lane_heights_fast(
    lane,
    start_distance,
    end_distance
):
    """
    1レーンを高速生成するための地形探索。

    getblocklist() を距離単位でまとめて使用。

    ただし各地点のY探索は独立しているので、
    地形追従の精度は維持する。
    """

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

            # 最後まで見つからなかった場合
            # 前回の高さを維持
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
# FILL RANGE
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
    # fill
    # --------------------------------------------------------

    m.execute(
        f"fill "
        f"{min_x} {ground_y} {min_z} "
        f"{max_x} {ground_y} {max_z} "
        f"{block}"
    )


# ============================================================
# APPLY ONE LANE
# ============================================================

def apply_lane_heights(
    lane,
    heights,
    start_distance,
    end_distance
):
    """
    高さ情報をもとに、
    同一高度区間をfillする。
    """

    if not heights:
        return

    fill_start = None
    fill_y = None

    # --------------------------------------------------------
    # 高さを走査
    # --------------------------------------------------------

    for distance in range(
        start_distance,
        end_distance
    ):

        ground_y = heights[distance]

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

    last_distance = end_distance - 1

    lane["last_y"] = (
        heights[last_distance]
    )

    if last_distance > start_distance:

        lane["prev_y"] = (
            heights[last_distance - 1]
        )


# ============================================================
# GENERATE ONE LANE
# ============================================================

def generate_one_lane(
    lane_index,
    lane
):
    """
    1レーンを最後まで生成する。
    """

    m.echo(
        "--------------------------------"
    )

    m.echo(
        f"LANE {lane_index + 1}/{LINE_COUNT} "
        f"{lane['color']}"
    )

    m.echo(
        f"START "
        f"{lane['start']}"
    )

    current = 0

    total_start = time.time()

    while current < TOTAL_LENGTH:

        end_distance = min(
            current + SLICE_LENGTH,
            TOTAL_LENGTH
        )

        start_time = time.time()

        # ----------------------------------------------------
        # 地形取得
        # ----------------------------------------------------

        heights = (
            generate_lane_heights_fast(
                lane,
                current,
                end_distance
            )
        )

        # ----------------------------------------------------
        # ブロック配置
        # ----------------------------------------------------

        apply_lane_heights(
            lane,
            heights,
            current,
            end_distance
        )

        # ----------------------------------------------------
        # 進行
        # ----------------------------------------------------

        current = end_distance

        elapsed = round(
            time.time() - start_time,
            3
        )

        total_elapsed = round(
            time.time() - total_start,
            2
        )

        m.echo(
            f"{lane['color']} "
            f"{current}/{TOTAL_LENGTH} "
            f"| slice {elapsed}s "
            f"| total {total_elapsed}s"
        )

    m.echo(
        f"LANE {lane_index + 1} COMPLETE "
        f"{lane['color']}"
    )

    return lane


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

    # --------------------------------------------------------
    # Time log
    # --------------------------------------------------------

    if os.path.exists(TIME_FILE):

        with open(
            TIME_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            time_log = json.load(f)

    else:

        time_log = {}

    # --------------------------------------------------------
    # Start
    # --------------------------------------------------------

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
        f"Current Lane : "
        f"{current_lane + 1}/{LINE_COUNT}"
    )

    m.echo(
        "================================"
    )

    # ========================================================
    # LANE LOOP
    # ========================================================

    for lane_index in range(
        current_lane,
        LINE_COUNT
    ):

        lane = lanes[lane_index]

        # ----------------------------------------------------
        # 既に完了したレーン
        # ----------------------------------------------------

        if (
            lane_index < current_lane
        ):
            continue

        # ----------------------------------------------------
        # 1レーン生成
        # ----------------------------------------------------

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
        # レーン完了
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

        m.echo(
            f"LANE COMPLETE "
            f"{lane_index + 1}/{LINE_COUNT} "
            f"| {lane_elapsed}s"
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

    # --------------------------------------------------------
    # progress削除
    # --------------------------------------------------------

    if os.path.exists(STATE_FILE):

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
            f"Unknown command: {command}"
        )