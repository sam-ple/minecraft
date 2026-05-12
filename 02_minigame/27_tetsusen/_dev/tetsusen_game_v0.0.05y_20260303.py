import minescript as m
import math
import json
import sys
import time
import os

# ===============================
# 定数設定
# ===============================

# ANNOUNCE_MINUTES = [15, 30, 60]  # ←ここ変更で自由設定
ANNOUNCE_MINUTES = [1] 
CLEAR_COUNT = 100
SLOT_COUNT = 27

BASE_DIR = "minescript"
os.makedirs(BASE_DIR, exist_ok=True)

FILE_START_POS = f"{BASE_DIR}/tetsusen_start_pos.json"
FILE_GAME_STATE = f"{BASE_DIR}/tetsusen_game_state.json"
FILE_SHULKER = f"{BASE_DIR}/tetsusen_shulker_positions.json"
FILE_RESULTS = f"{BASE_DIR}/tetsusen_results.json"
FILE_CHUNK = f"{BASE_DIR}/tetsusen_chunk.json"

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
    m_ = seconds // 60
    s_ = seconds % 60
    return f"{m_}:{s_:02d}"

# ===============================
# start処理
# ===============================

def start_game(restart=False):

    # -------------------------
    # 座標読み込み
    # -------------------------
    start_pos = load_json(FILE_START_POS, None)
    if not start_pos:
        m.echo("Start position not found.")
        return

    sx, sy, sz = start_pos["x"], start_pos["y"], start_pos["z"]

    # -------------------------
    # チャンク再ロード保証
    # -------------------------
    chunk = load_json(FILE_CHUNK, None)
    if chunk:
        m.execute(
            f'forceload add {chunk["x1"]} {chunk["z1"]} {chunk["x2"]} {chunk["z2"]}'
        )

    # -------------------------
    # restartでなければカウントダウン
    # -------------------------
    if not restart:

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

    # -------------------------
    # 既クリア取得
    # -------------------------
    results = load_json(FILE_RESULTS, [])
    cleared_players = {r["player"] for r in results}

    # -------------------------
    # shulker読み込み
    # -------------------------
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

    # -------------------------
    # scoreboard準備
    # -------------------------
    m.execute("scoreboard objectives remove iron")
    m.execute("scoreboard objectives remove temp")
    m.execute("scoreboard objectives add iron dummy")
    m.execute("scoreboard objectives add temp dummy")
    m.execute(
        'scoreboard objectives modify iron displayname '
        '{"text":"Iron Ingots","color":"gold"}'
    )
    m.execute("scoreboard objectives setdisplay sidebar iron")

    # -------------------------
    # 監視ループ
    # -------------------------
    while True:

        elapsed = int(time.time() - start_time)

        # ---- 時間アナウンス ----
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

        # ---- 各プレイヤー処理 ----
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

            # ---- スコア取得 ----
            result = m.execute(f"scoreboard players get {PLAYER} iron")
            # m.echo(f"DEBUG: {PLAYER} iron score raw: {result}")
            value = int(result.split()[-1]) if result else 0

            # ---- アクションバー ----
            m.execute(
                f'execute as {PLAYER} run title {PLAYER} actionbar '
                f'{{"text":"Iron: ","color":"gold",'
                f'"extra":[{{"score":{{"name":"{PLAYER}","objective":"iron"}}}}]}}'
            )

            # ---- クリア判定 ----
            if value >= CLEAR_COUNT:

                clear_time = elapsed
                time_str = format_time(clear_time)

                m.execute(
                    f'title @a title '
                    f'{{"text":"{PLAYER} CLEARED!","color":"green"}}'
                )
                m.execute(
                    f'title @a subtitle '
                    f'{{"text":"{time_str}","color":"gold"}}'
                )

                m.execute(
                    f'summon firework_rocket {X} {Y+2} {Z} '
                    '{LifeTime:20,FireworksItem:{id:"firework_rocket",Count:1b,tag:{Fireworks:{Explosions:[{Type:1,Flicker:1b,Trail:1b,Colors:[I;11743532]}]}}}}'
                )

                m.execute(f"gamemode spectator {PLAYER}")

                results.append({
                    "player": PLAYER,
                    "time_seconds": clear_time,
                    "time_display": time_str
                })

                save_json(FILE_RESULTS, results)

                cleared_players.add(PLAYER)

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
