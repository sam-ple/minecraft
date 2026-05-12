# ============================================================
# ADVANCEMENT RACE GAME SYSTEM
# Version : v0.0.07 (Effects Added)
# ============================================================

import minescript as m
from minescript import EventQueue, EventType

import sys
import json
import time
import re
import os
import math

from queue import Empty
from datetime import datetime


BASE_DIR = "minescript/data/advrace"
os.makedirs(BASE_DIR, exist_ok=True)

CONFIG_FILE = f"{BASE_DIR}/config.json"
START_POS_FILE = f"{BASE_DIR}/start_pos.json"

LANG = "EN"
FIRST_MODE = True
PICKUP_MODE = False

DEFAULT_CONFIG = {
    "duration": 60,
    "option": 1
}

adv_pattern = re.compile(
    r"^(\w+) has (made the advancement|completed the challenge|reached the goal) \[(.+)\]"
)


# ============================================================
# UTILS
# ============================================================

def sec_to_mmss(sec):
    m_, s_ = divmod(sec, 60)
    return f"{m_:02d}:{s_:02d}"


def chat(msg, color="aqua"):
    m.execute(f'tellraw @a {json.dumps({"text": msg, "color": color})}')


def echo(msg):
    m.execute(f'tellraw {m.player_name()} {json.dumps({"text": msg, "color": "yellow"})}')


# ============================================================
# ★ 追加：個人SE
# ============================================================

def play_personal_sound(player, is_first):

    if is_first:
        # m.execute(f"playsound minecraft:entity.player.levelup master {player}")
        # m.execute(f"playsound minecraft:ui.toast.challenge_complete master {player}")
        m.execute(f"playsound minecraft:block.note_block.pling master {player}")
    else:
        m.execute(f"playsound minecraft:block.note_block.pling master {player}")


# ============================================================
# CONFIG
# ============================================================

def save_config(config=None):
    if config is None:
        config = DEFAULT_CONFIG
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config()
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_start_pos():
    x, y, z = map(math.floor, m.player_position())
    with open(START_POS_FILE, "w", encoding="utf-8") as f:
        json.dump({"x": x, "y": y, "z": z}, f)


def load_start_pos():
    if not os.path.exists(START_POS_FILE):
        return {"x": 0, "y": 70, "z": 0}
    with open(START_POS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ============================================================
# COUNTDOWN
# ============================================================

def countdown(sec, final):
    for i in range(sec, 0, -1):

        m.execute(
            f'title @a title {json.dumps({"text": str(i), "color": "aqua", "bold": True})}'
        )
        m.execute("playsound minecraft:block.note_block.pling master @a")
        time.sleep(1)

    m.execute(
        f'title @a title {json.dumps({"text": final, "color": "gold", "bold": True})}'
    )
    m.execute("playsound minecraft:entity.player.levelup master @a")
    time.sleep(1)


# ============================================================
# STATE
# ============================================================

game_active = False
game_start_time = 0
last_boss_update = 0

player_points = {}
player_adv_count = {}
player_adv_log = {}

first_advancements = set()

GAME_LOG_FILE = ""
PLAYER_LOG_FILE = ""


# ============================================================
# LOG
# ============================================================

def log_adv(player, adv, is_first):

    elapsed = int(time.time() - game_start_time)
    tag = " (FIRST)" if is_first else ""
    line = f"[{sec_to_mmss(elapsed)}] {adv}{tag}"

    with open(GAME_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{player} : {line}\n")

    player_adv_log.setdefault(player, []).append(line)


# ============================================================
# SCORE
# ============================================================

def calc_points(adv):

    if cfg["option"] == 1 and adv not in first_advancements:
        first_advancements.add(adv)
        chat(f"✨ FIRST! {adv} (+1)", "gold")
        return 2, True

    return 1, False


# ============================================================
# ★ タイムアップ演出
# ============================================================

def timeup_effect():

    m.execute(
        f'title @a title {json.dumps({"text": "TIME UP!", "color": "red", "bold": True})}'
    )
    m.execute(
        f'title @a subtitle {json.dumps({"text": "Result Incoming...", "color": "gold"})}'
    )

    m.execute("playsound minecraft:entity.ender_dragon.growl master @a")
    m.execute("playsound minecraft:entity.lightning_bolt.thunder master @a")

    for _ in range(8):
        m.execute("summon firework_rocket ~ ~1 ~ {LifeTime:20}")


# ============================================================
# ★ 勝者演出
# ============================================================

def winner_effect(player):

    m.execute(
        f'title @a title {json.dumps({"text": f"{player} WINS!", "color": "gold", "bold": True})}'
    )

    m.execute(f"playsound minecraft:ui.toast.challenge_complete master {player}")
    m.execute(f"playsound minecraft:entity.player.levelup master {player}")

    for _ in range(12):
        m.execute(f"execute at {player} run summon firework_rocket ~ ~1 ~ {{LifeTime:25}}")


# ============================================================
# BOSSBAR
# ============================================================

def update_bossbar(remain):

    global last_boss_update

    if time.time() - last_boss_update >= 1:

        m.execute(f"bossbar set advrace value {remain}")
        m.execute(
            f'bossbar set advrace name {json.dumps({"text": sec_to_mmss(remain), "color": "gold"})}'
        )

        last_boss_update = time.time()


# ============================================================
# START
# ============================================================

def start_game():

    global game_active
    global game_start_time
    global GAME_LOG_FILE, PLAYER_LOG_FILE

    save_start_pos()
    pos = load_start_pos()

    m.execute(f"setworldspawn {pos['x']} {pos['y']} {pos['z']}")
    m.execute(f"spawnpoint @a {pos['x']} {pos['y']} {pos['z']}")

    m.execute("gamerule sendCommandFeedback false")
    m.execute("gamemode adventure @a")
    m.execute("clear @a")

    m.execute("advancement revoke @a everything")
    m.execute(f"tp @a {pos['x']} {pos['y']} {pos['z']}")

    countdown(3, "GAME START")

    m.execute("gamemode survival @a")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    GAME_LOG_FILE = f"{BASE_DIR}/advrace_{ts}.txt"
    PLAYER_LOG_FILE = f"{BASE_DIR}/advrace_{ts}_players.txt"

    with open(GAME_LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"=== Advancement Race ===\nStart: {ts}\n\n")

    player_points.clear()
    player_adv_count.clear()
    player_adv_log.clear()
    first_advancements.clear()

    m.execute("scoreboard objectives remove advPoints")
    m.execute("scoreboard objectives add advPoints dummy Points")
    m.execute("scoreboard objectives setdisplay sidebar advPoints")

    m.execute("bossbar remove advrace")
    m.execute('bossbar add advrace "Time"')
    m.execute("bossbar set advrace players @a")
    m.execute(f"bossbar set advrace max {cfg['duration']}")
    m.execute(f"bossbar set advrace value {cfg['duration']}")

    game_active = True
    game_start_time = time.time()

    chat(f"🎮 Advancement Race START ({sec_to_mmss(cfg['duration'])})")


# ============================================================
# END
# ============================================================

def end_game():

    global game_active

    if not game_active:
        return

    timeup_effect()

    ranking = sorted(
        player_points.items(),
        key=lambda x: x[1],
        reverse=True
    )

    if ranking:
        time.sleep(2)
        winner_effect(ranking[0][0])

    time.sleep(2)

    show_result()

    game_active = False

    m.execute("bossbar remove advrace")
    m.execute("gamemode adventure @a")
    m.execute("gamerule sendCommandFeedback true")


# ============================================================
# RESULT
# ============================================================

def show_result():

    ranking = sorted(
        player_points.items(),
        key=lambda x: x[1],
        reverse=True
    )

    chat("🏁 === Result ===", "white")

    for i, (p, pt) in enumerate(ranking, 1):

        advs = player_adv_count.get(p, 0)

        medal = (
            "🥇" if i == 1 else
            "🥈" if i == 2 else
            "🥉" if i == 3 else ""
        )

        chat(f"{medal} {i}. {p} : {pt} pt ({advs} adv)")


# ============================================================
# RESET / ENTRY / LOOP
# （ここは元のまま）
# ============================================================

def reset_game():

    global game_active

    game_active = False

    m.execute("bossbar remove advrace")
    m.execute("scoreboard objectives remove advPoints")
    m.execute("gamemode adventure @a")

    pos = load_start_pos()

    m.execute(f"tp @a {pos['x']} {pos['y']} {pos['z']}")

    echo("Reset complete.")


cfg = load_config()

echo(f"Config loaded: duration={cfg['duration']}, option={cfg['option']}")

if len(sys.argv) >= 2:

    cmd = sys.argv[1]

    if cmd == "setup":
        save_config()
        echo("Setup complete.")
        sys.exit(0)

    elif cmd == "start":
        start_game()

    elif cmd == "stop":
        end_game()
        sys.exit(0)

    elif cmd == "reset":
        reset_game()
        sys.exit(0)


eq = EventQueue()
eq.register_chat_listener()

while True:

    try:
        event = eq.get(timeout=0.1)
    except Empty:
        event = None

    if game_active:

        remain = max(
            cfg["duration"] - int(time.time() - game_start_time),
            0
        )

        update_bossbar(remain)

        if remain <= 0:
            end_game()

    if event and event.type == EventType.CHAT and game_active:

        m_ = adv_pattern.match(event.message.strip())

        if m_:

            player, _, adv = m_.groups()

            pt, is_first = calc_points(adv)

            player_points[player] = player_points.get(player, 0) + pt
            player_adv_count[player] = player_adv_count.get(player, 0) + 1

            # ★ 個人SE
            play_personal_sound(player, is_first)

            m.execute(
                f"scoreboard players add {player} advPoints {pt}"
            )

            log_adv(player, adv, is_first)
