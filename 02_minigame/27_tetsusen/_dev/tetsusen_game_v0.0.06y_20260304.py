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
# 定数設定
# ===============================

# ANNOUNCE_MINUTES = [15, 30, 60]  # ←ここ変更で自由設定
ANNOUNCE_MINUTES = [5,10] 
CLEAR_COUNT = 100
# SLOT_COUNT = 27
SLOT_COUNT = math.ceil(CLEAR_COUNT / 64)
# math.ceil(100/64) = 2

# BASE_DIR = "minescript"
# os.makedirs(BASE_DIR, exist_ok=True)

# FILE_START_POS = f"{BASE_DIR}/tetsusen_start_pos.json"
# FILE_GAME_STATE = f"{BASE_DIR}/tetsusen_game_state.json"
# FILE_SHULKER = f"{BASE_DIR}/tetsusen_shulker_positions.json"
# FILE_RESULTS = f"{BASE_DIR}/tetsusen_results.json"
# FILE_CHUNK = f"{BASE_DIR}/tetsusen_chunk.json"

BASE_DIR = "minescript/data/tetsusen"
os.makedirs(BASE_DIR, exist_ok=True)

FILE_START_POS = f"{BASE_DIR}/start_pos.json"
FILE_GAME_STATE = f"{BASE_DIR}/game_state.json"
FILE_SHULKER = f"{BASE_DIR}/shulker_positions.json"
FILE_RESULTS = f"{BASE_DIR}/results.json"
FILE_CHUNK = f"{BASE_DIR}/chunk.json"


# ===============================
# ユーティリティ
# ===============================

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def load_json(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return default

def format_time(seconds):
    m_, s_ = divmod(seconds, 60)
    return f"{m_}:{s_:02d}"

# ===============================
# start処理
# ===============================

def start_game(restart=False):

    start_pos = load_json(FILE_START_POS, None)
    if not start_pos:
        m.echo("Start position not found.")
        return

    sx, sy, sz = start_pos["x"], start_pos["y"], start_pos["z"]

    chunk = load_json(FILE_CHUNK, None)
    if chunk:
        m.execute(
            f'forceload add {chunk["x1"]} {chunk["z1"]} {chunk["x2"]} {chunk["z2"]}'
        )

    if not restart:

        save_json(FILE_RESULTS, [])  # ←追加

        m.execute(f"spawnpoint @a {sx} {sy} {sz}")
        m.execute(f"tp @a {sx} {sy+1} {sz}")
        m.execute("gamemode survival @a")

        for i in [3,2,1]:
            m.execute(f'title @a title {{"text":"{i}","color":"red"}}')
            time.sleep(1)

        m.execute('title @a title {"text":"START!","color":"gold"}')

        start_time = time.time()

        save_json(FILE_GAME_STATE, {
            "start_time": start_time,
            "announced": []
        })

    else:
        state = load_json(FILE_GAME_STATE, None)
        if not state:
            m.echo("No previous game state.")
            return
        start_time = state["start_time"]

    results = load_json(FILE_RESULTS, [])
    cleared_players = {r["player"] for r in results}

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

    # scoreboard準備
    m.execute("scoreboard objectives remove iron")
    m.execute("scoreboard objectives remove temp")
    m.execute("scoreboard objectives add iron dummy")
    m.execute("scoreboard objectives add temp dummy")
    m.execute("scoreboard objectives setdisplay sidebar iron")

    # ===============================
    # EventQueue準備
    # ===============================

    eq = EventQueue()
    eq.register_chat_listener()

    # clear_pattern = re.compile(r"\[CLEAR\](\w+):(\d+)")
    clear_pattern = re.compile(r"\[CLEAR\]([^:]+):(\d+)")
    executor = m.player_name()

    # ===============================
    # 監視ループ
    # ===============================

    while True:

        # -------------------------
        # チャットイベント取得
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
                        f'{{"text":"{player} CLEARED!","color":"green"}}'
                    )

                    m.execute(
                        f'title @a subtitle '
                        f'{{"text":"{time_str}","color":"gold"}}'
                    )

                    m.execute(
                        f'tellraw @a '
                        f'{{"text":"{player} reached {amount}!","color":"gold"}}'
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
        # 時間処理
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
        # 各プレイヤー処理
        # -------------------------

        for PLAYER, (X,Y,Z) in SHULKER_MAP.items():

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

            # ---- アクションバー表示 ----
            m.execute(
                f'execute as {PLAYER} run title {PLAYER} actionbar '
                f'{{"text":"Iron: ","color":"gold",'
                f'"extra":[{{"score":{{"name":"{PLAYER}","objective":"iron"}}}}]}}'
            )

            # ---- クリア検知（チャット方式）----
            m.execute(
                f'execute if score {PLAYER} iron matches {CLEAR_COUNT}.. '
                f'run tellraw {executor} '
                f'{{"text":"[CLEAR]{PLAYER}:",'
                f'"extra":[{{"score":{{"name":"{PLAYER}","objective":"iron"}}}}]}}'
            )

        time.sleep(1)

# ===============================
# エントリ
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
