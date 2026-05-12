import minescript as m
import json
import time
import os
import sys

# ============================================================
# SETTINGS
# ============================================================

BASE_DIR = "minescript/data/linerace"
LANES_FILE = f"{BASE_DIR}/lanes.json"

TICK = 0.1

tolerance_left = 0.6
tolerance_right = 0.6

COLORS = ["white","orange","light_blue","lime","yellow"]

game_active = False
lanes = []

# ============================================================
# SCOREBOARD INIT
# ============================================================

def init_scoreboards():

    m.execute("scoreboard objectives add PosX dummy")
    m.execute("scoreboard objectives add PosZ dummy")
    m.execute("scoreboard objectives add LineDist dummy")

# ============================================================
# LOAD
# ============================================================

def load():

    global lanes

    with open(LANES_FILE) as f:
        lanes = json.load(f)["lanes"]

# ============================================================
# START GAME
# ============================================================

def start():

    global game_active

    load()
    init_scoreboards()

    for lane in lanes:

        p = lane["player"]
        if not p:
            continue

        sx, sy, sz = lane["start"]

        lane["sx"] = sx
        lane["sy"] = sy
        lane["sz"] = sz

        # スタート配置
        m.execute(f"tp {p} {sx} {sy+1} {sz}")

        # 初期スコア
        m.execute(f"scoreboard players set {p} LineDist 0")

    game_active = True
    m.echo("LineRace START")

# ============================================================
# UPDATE PLAYER DATA (MC側で取得)
# ============================================================

def update_player_data(p):

    m.execute(
        f"execute as {p} store result score {p} PosX "
        "run data get entity @s Pos[0] 100"
    )

    m.execute(
        f"execute as {p} store result score {p} PosZ "
        "run data get entity @s Pos[2] 100"
    )

# ============================================================
# MAIN LOOP
# ============================================================

def run():

    while True:

        if not game_active:
            time.sleep(TICK)
            continue

        for lane in lanes:

            p = lane["player"]
            if not p:
                continue

            sx = lane["sx"]
            sy = lane["sy"]
            sz = lane["sz"]

            # =====================================================
            # Minecraftから座標取得（m.playersなし）
            # =====================================================
            update_player_data(p)

            px = m.scoreboard(p, "PosX") / 100
            pz = m.scoreboard(p, "PosZ") / 100

            dx = px - sx
            dz = pz - sz

            dir_x, dir_z = lane.get("dir", (0, 1))

            # =====================================================
            # 距離（進行方向）
            # =====================================================
            dist = dx * dir_x + dz * dir_z

            # =====================================================
            # 横ズレ（直交ベクトル）
            # =====================================================
            right_x = -dir_z
            right_z = dir_x

            lateral = dx * right_x + dz * right_z

            # スコア反映
            m.execute(f"scoreboard players set {p} LineDist {int(dist)}")

            # =====================================================
            # 判定（逸脱）
            # =====================================================
            if lateral < -tolerance_left or lateral > tolerance_right:

                # kill → 即リスポーン
                m.execute(f"kill {p}")
                m.execute(f"tp {p} {sx} {sy+1} {sz}")

                m.execute(f"scoreboard players set {p} LineDist 0")

        # アイテム掃除（軽量版）
        for color in COLORS:
            m.execute(
                f'/execute as @a at @s run kill @e[type=item,nbt={{Item:{{id:"minecraft:{color}_wool"}}}},distance=..10]'
            )

        time.sleep(TICK)

# ============================================================
# BOOT
# ============================================================

if __name__ == "__main__":
    start()
    run()