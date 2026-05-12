# ============================================================
# LINERACE COURSE GENERATOR
# Version : v0.0.07
# Date: 2026-04-11
#
# Minecraft Java Edition + Minescript
#
# File
#   linerace_base.py : LineRaceコース生成
#
# Features
#   ・最大2000ブロックの直線コース生成
#   ・地形追従ウールライン
#   ・生成途中保存（再開可能）
#   ・プレイヤーヘッド設置
#
# Commands
#   set   : コース生成
#   set2  : プレイヤーヘッド設置
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

TOTAL_LENGTH = 1000  #2000
SEGMENT_LENGTH = 100 #200
TIME_SLICE = 50 #100

FX, FZ = 0, 1
RX, RZ = 1, 0

COLORS = ["white","orange","light_blue","lime","yellow"]


# ============================================================
# PLAYER SETTINGS
# ============================================================

PLAYERS = ["crocadooo","saaample","","",""]


# ============================================================
# TELEPORT SETTINGS
# ============================================================

USE_ALT_PLAYER = False
ALT_PLAYER_NAME = "saaample"

TP_GAMEMODE = "spectator"
END_GAMEMODE = "survival"


# ============================================================
# DATA DIRECTORY
# ============================================================

BASE_DIR = "minescript/data/linerace"
os.makedirs(BASE_DIR, exist_ok=True)

LANES_FILE = f"{BASE_DIR}/lanes.json"
STATE_FILE = f"{BASE_DIR}/progress.json"
TIME_FILE  = f"{BASE_DIR}/timelog.json"


# ============================================================
# GROUND SEARCH
# ============================================================

GROUND_BLOCKS = {
    "minecraft:dirt",
    "minecraft:grass_block[snowy=false]",
    "minecraft:grass_block[snowy=true]",
    "minecraft:sand",
    "minecraft:gravel",
    "minecraft:stone",
    "minecraft:andesite",
    "minecraft:diorite",
    "minecraft:granite",
    "minecraft:pozdol[snowy=false]",
    "minecraft:coarse_dirt",
    "minecraft:mossy_cobblestone",
    "minecraft:dirt_path",
}

SEARCH_UP = 6
SEARCH_DOWN = 20


# ============================================================
# GAMERULE SETTINGS
# ============================================================
m.execute("gamerule sendCommandFeedback false")
# m.execute("gamerule send_command_feedback false") #1.21.11

# ============================================================
# PLAYER SELECTOR
# ============================================================

def get_player():

    if USE_ALT_PLAYER:
        return ALT_PLAYER_NAME

    return "@p"


# ============================================================
# GROUND DETECTION
# ============================================================

def find_ground(x, last_y, z):

    for dy in range(3,-4,-1):

        y = last_y + dy

        if m.getblock(x,y+1,z) in GROUND_BLOCKS:
            return y

    for dy in range(SEARCH_UP,-SEARCH_DOWN-1,-1):

        y = last_y + dy

        if m.getblock(x,y+1,z) in GROUND_BLOCKS:
            return y

    return last_y


# ============================================================
# SAFE TELEPORT
# ============================================================

def safe_tp(x,z,approx_y):

    player = get_player()

    m.execute(f"gamemode {TP_GAMEMODE} {player}")

    for dy in range(10,-20,-1):

        y = approx_y + dy

        if m.getblock(x,y,z) in GROUND_BLOCKS:

            m.execute(f"tp {player} {x} {y+2} {z}")
            return y+2

    m.execute(f"tp {player} {x} {approx_y+5} {z}")
    return approx_y+5


# ============================================================
# LOAD OR INITIALIZE COURSE
# ============================================================

def load_or_init():

    if os.path.exists(STATE_FILE):

        with open(STATE_FILE) as f:
            return json.load(f)

    px,py,pz = map(math.floor,m.player_position())

    lanes = []

    for i in range(LINE_COUNT):

        offset = i * BLOCK_SPACING

        sx = px + RX*offset
        sz = pz + RZ*offset

        player_name = PLAYERS[i] if i < len(PLAYERS) else ""

        lanes.append({
            "player":player_name,
            "start":[sx,py,sz],
            "last_y":py,
            "color":COLORS[i]
        })

    data = {
        "lanes":lanes,
        "course_length":TOTAL_LENGTH
    }

    with open(LANES_FILE,"w") as f:
        json.dump(data,f,indent=2)

    return {
        "current_length":0,
        "lanes":lanes,
        "start_pos":[px,py,pz]
    }


# ============================================================
# COURSE GENERATION
# ============================================================

def cmd_set():

    state = load_or_init()

    current = state["current_length"]
    lanes = state["lanes"]

    time_log = {}

    if os.path.exists(TIME_FILE):

        with open(TIME_FILE) as f:
            time_log = json.load(f)

    while current < TOTAL_LENGTH:

        segment_end = min(current+SEGMENT_LENGTH,TOTAL_LENGTH)

        while current < segment_end:

            slice_end = min(current+TIME_SLICE,segment_end)

            start_time = time.time()

            for d in range(current,slice_end):

                for lane in lanes:

                    sx,sy,sz = lane["start"]

                    x = sx + FX*d
                    z = sz + FZ*d

                    ground_y = find_ground(x,lane["last_y"],z)

                    block = f"minecraft:{lane['color']}_wool"

                    m.execute(f"setblock {x} {ground_y+1} {z} {block}")

                    lane["last_y"] = ground_y

            elapsed = round(time.time()-start_time,3)

            time_log[f"{current}-{slice_end}"] = elapsed

            current = slice_end
            state["current_length"] = current

            with open(STATE_FILE,"w") as f:
                json.dump(state,f,indent=2)

            with open(TIME_FILE,"w") as f:
                json.dump(time_log,f,indent=2)

            m.echo(f"{current}/{TOTAL_LENGTH} ({elapsed}s)")

        base_x,base_y,base_z = lanes[0]["start"]

        tp_x = base_x + FX*current
        tp_z = base_z + FZ*current

        # safe_tp(tp_x,tp_z,lanes[0]["last_y"])

        time.sleep(0.3)

    m.echo("COURSE COMPLETE")

    player = get_player()

    sx,sy,sz = state["start_pos"]

    m.execute(f"tp {player} {sx} {sy+2} {sz}")
    m.execute(f"gamemode {END_GAMEMODE} {player}")

    os.remove(STATE_FILE)


# ============================================================
# PLAYER HEAD SETUP
# ============================================================

def cmd_set2():

    if not os.path.exists(LANES_FILE):

        m.echo("Run set first.")
        return

    with open(LANES_FILE) as f:
        data = json.load(f)

    lanes = data["lanes"]

    for lane in lanes:

        player = lane["player"]

        if not player:
            continue

        sx,sy,sz = lane["start"]

        back_x = sx - FX
        back_z = sz - FZ

        m.execute(
            f'setblock {back_x} {sy+1} {back_z} '
            f'minecraft:player_head[rotation=8]{{profile:"{player}"}} replace'
        )

    m.echo("Player heads placed.")

    for lane in lanes:
        sx, sy, sz = lane["start"]

        # 足元を金ブロックに
        m.execute(f"setblock {sx} {sy-1} {sz} minecraft:gold_block")



# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    if len(sys.argv) < 2:

        m.echo("Usage: set / set2")
        sys.exit()

    arg = sys.argv[1]

    if arg == "set":
        cmd_set()

    elif arg == "set2":
        cmd_set2()

    else:
        m.echo("Unknown command.")
