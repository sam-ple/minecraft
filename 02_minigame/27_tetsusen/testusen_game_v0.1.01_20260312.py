# ============================================================
# TETSUSEN GAME SYSTEM
# Version : v0.1.01
# Date: 2026-03-12
#
# Minecraft Java Edition + MineScript
#
# File
#   tetsusen_game.py : ゲーム進行管理
#
# Features
#   ・5プレイヤー対応鉄千ゲーム
#   ・クリアタイム記録
#   ・経過時間アナウンス
#   ・restart対応
#   ・EventQueueによるクリア検知
#
# Data Directory
#   minescript/data/tetsusen/
#
# Author : crocado
# ============================================================

import minescript as m
from minescript import EventQueue, EventType
import math
import json
import sys
import time
import os
import re
from queue import Empty


# ===============================
# GAME SETTINGS
# ===============================

# ANNOUNCE_MINUTES = [5, 10]          # 経過時間アナウンス
ANNOUNCE_MINUTES = [15, 30, 45, 60, 75, 90, 105, 120]          # 経過時間アナウンス
# CLEAR_COUNT = 1000                   # クリア条件（鉄インゴット）
CLEAR_COUNT = 100                   # クリア条件（鉄インゴット）
SLOT_COUNT = math.ceil(CLEAR_COUNT / 64)


# ===============================
# DATA FILES
# ===============================

BASE_DIR = "minescript/data/tetsusen"
os.makedirs(BASE_DIR, exist_ok=True)

FILE_START_POS = f"{BASE_DIR}/start_pos.json"
FILE_GAME_STATE = f"{BASE_DIR}/game_state.json"
FILE_SHULKER = f"{BASE_DIR}/shulker_positions.json"
FILE_RESULTS = f"{BASE_DIR}/results.json"
FILE_CHUNK = f"{BASE_DIR}/chunk.json"


# ===============================
# UTILITY FUNCTIONS
# ===============================

def save_json(path, data):
    """JSON保存"""
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def load_json(path, default):
    """JSON読み込み（存在しない場合はdefault）"""
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return default


# def format_time(seconds):
#     """秒 → m:ss 表示"""
#     m_, s_ = divmod(seconds, 60)
#     return f"{m_}:{s_:02d}"

# def format_time(seconds):
#     h = seconds // 3600
#     m_ = (seconds % 3600) // 60
#     s_ = seconds % 60
#     return f"{h}:{m_:02d}:{s_:02d}"

def format_time(seconds):
    """秒 → h:mm:ss 表示"""
    h = seconds // 3600
    m_ = (seconds % 3600) // 60
    s_ = seconds % 60

    if h > 0:
        return f"{h}:{m_:02d}:{s_:02d}"
    else:
        return f"{m_}:{s_:02d}"

# ===============================
# GAME START / RESTART
# ===============================

def start_game(restart=False):

    # 開始位置取得
    start_pos = load_json(FILE_START_POS, None)
    if not start_pos:
        m.echo("Start position not found.")
        return

    sx, sy, sz = start_pos["x"], start_pos["y"], start_pos["z"]

    # チャンクロード
    chunk = load_json(FILE_CHUNK, None)
    if chunk:
        m.execute(
            f'forceload add {chunk["x1"]} {chunk["z1"]} {chunk["x2"]} {chunk["z2"]}'
        )

    # ---------------------------
    # 新規ゲーム開始
    # ---------------------------
    if not restart:

        save_json(FILE_RESULTS, [])

        m.execute(f"spawnpoint @a {sx} {sy} {sz}")
        m.execute(f"tp @a {sx} {sy+1} {sz}")
        m.execute("gamemode survival @a")
        m.chat(f"{sx} {sy} {sz}")

        for i in [3, 2, 1]:
            m.execute(f'title @a title {{"text":"{i}","color":"red"}}')
            m.execute('playsound minecraft:block.note_block.hat master @a ~ ~ ~ 1 1')
            time.sleep(1)

        m.execute('title @a title {"text":"START!","color":"gold"}')
        m.execute('playsound minecraft:entity.player.levelup master @a ~ ~ ~ 1 1')
        m.execute('particle minecraft:totem_of_undying ~ ~1 ~ 1 1 1 0.5 100 force @a')

        start_time = time.time()

        save_json(FILE_GAME_STATE, {
            "start_time": start_time,
            "announced": []
        })

    # ---------------------------
    # restart復帰
    # ---------------------------
    else:

        state = load_json(FILE_GAME_STATE, None)
        if not state:
            m.echo("No previous game state.")
            return

        start_time = state["start_time"]

    # ---------------------------
    # クリア済みプレイヤー
    # ---------------------------

    results = load_json(FILE_RESULTS, [])
    cleared_players = {r["player"] for r in results}

    # ---------------------------
    # シュルカー位置取得
    # ---------------------------

    data = load_json(FILE_SHULKER, [])
    SHULKER_MAP = {}

    for entry in data:
        if entry.get("player"):
            SHULKER_MAP[entry["player"]] = (
                entry["x"], entry["y"], entry["z"]
            )

    if not SHULKER_MAP:
        m.echo("No players defined.")
        return

    # ---------------------------
    # scoreboard準備
    # ---------------------------

    m.execute("scoreboard objectives remove iron")
    m.execute("scoreboard objectives remove temp")
    m.execute("scoreboard objectives add iron dummy")
    m.execute("scoreboard objectives add temp dummy")
    m.execute("scoreboard objectives setdisplay sidebar iron")

    # ---------------------------
    # EventQueue準備
    # ---------------------------

    eq = EventQueue()
    eq.register_chat_listener()

    clear_pattern = re.compile(r"\[CLEAR\]([^:]+):(\d+)")
    executor = m.player_name()

    # ===============================
    # MAIN GAME LOOP
    # ===============================

    while True:

        # -------------------------
        # Chat Event Handling
        # -------------------------

        try:
            event = eq.get(timeout=0.05)
        except Empty:
            event = None

        if event and event.type == EventType.CHAT:

            msg = event.message.strip()
            m_ = clear_pattern.search(msg)

            if m_:

                player = m_.group(1)
                amount = int(m_.group(2))

                if player not in cleared_players:

                    clear_time = int(time.time() - start_time)
                    time_str = format_time(clear_time)

                    m.execute(
                        f'title @a title '
                        f'{{"text":"{player}","color":"green"}}'
                    )

                    m.execute(
                        f'title @a subtitle '
                        f'{{"text":"CLEARED! {time_str}","color":"gold"}}'
                    )

                    m.execute(
                        'playsound minecraft:ui.toast.challenge_complete master @a ~ ~ ~ 1 1'
                    )

                    m.execute(
                        f'particle minecraft:firework ~ ~1 ~ 1 1 1 0.2 100 force'
                    )

                    m.execute(
                        f'tellraw @a '
                        f'{{"text":"{player} reached {amount}!({time_str})","color":"gold"}}'
                    )

                    m.execute(f"gamemode spectator {player}")

                    results.append({
                        "player": player,
                        "time_seconds": clear_time,
                        "time_display": time_str
                    })

                    save_json(FILE_RESULTS, results)
                    cleared_players.add(player)

        # -------------------------
        # Timer Announcements
        # -------------------------

        elapsed = int(time.time() - start_time)
        state = load_json(FILE_GAME_STATE, {"announced": []})
        announced = state.get("announced", [])

        for minute in ANNOUNCE_MINUTES:

            if elapsed >= minute*60 and minute not in announced:

                m.execute(
                    f'title @a title '
                    f'{{"text":"{minute} Minutes Passed!","color":"red"}}'
                )

                announced.append(minute)

                save_json(FILE_GAME_STATE, {
                    "start_time": start_time,
                    "announced": announced
                })

        # -------------------------
        # Player Progress Check
        # -------------------------

        for PLAYER, (X, Y, Z) in SHULKER_MAP.items():

            if PLAYER in cleared_players:
                continue

            m.execute(f"scoreboard players set {PLAYER} iron 0")

            for i in range(SLOT_COUNT):

                m.execute(f"scoreboard players set {PLAYER} temp 0")

                m.execute(
                    f'execute if data block {X} {Y} {Z} '
                    f'Items[{{Slot:{i}b,id:"minecraft:iron_ingot"}}] '
                    f'run execute store result score {PLAYER} temp run '
                    f'data get block {X} {Y} {Z} '
                    f'Items[{{Slot:{i}b,id:"minecraft:iron_ingot"}}].count'
                )

                m.execute(
                    f"scoreboard players operation {PLAYER} iron += {PLAYER} temp"
                )

            m.execute(
                f'execute as {PLAYER} run title {PLAYER} actionbar '
                f'{{"text":"Iron: ","color":"gold",'
                f'"extra":[{{"score":{{"name":"{PLAYER}","objective":"iron"}}}}]}}'
            )

            m.execute(
                f'execute if score {PLAYER} iron matches {CLEAR_COUNT}.. '
                f'run tellraw {executor} '
                f'{{"text":"[CLEAR]{PLAYER}:",'
                f'"extra":[{{"score":{{"name":"{PLAYER}","objective":"iron"}}}}]}}'
            )

        m.execute("execute as @a at @s if block ~ ~-1 ~ minecraft:gold_block run effect give @a saturation infinite 0 true")
        m.execute("execute as @a at @s if block ~ ~-1 ~ minecraft:gold_block run effect give @a minecraft:night_vision infinite 0 true")
                    
        time.sleep(1)


# ===============================
# ENTRY POINT
# ===============================

def main():

    arg = "start"

    if len(sys.argv) > 1:
        arg = sys.argv[1]

    if arg == "start":
        start_game(restart=False)

    elif arg == "restart":
        start_game(restart=True)


main()
