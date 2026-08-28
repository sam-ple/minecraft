# ============================================================
# ADVANCEMENT RACE GAME SYSTEM
# Version : v0.0.06
# Date    : 2026-03-09
#
# Minecraft Java Edition + Minescript
#
# File
#   advrace_game.py : Advancement Race Game
#
# Features
#   ・Advancement取得レース
#   ・BossBarタイマー
#   ・FIRST取得ボーナス
#   ・採取ログ保存
#   ・ランキング表示
#
# Commands
#   setup  : 初期セットアップ
#   start  : ゲーム開始
#   stop   : 強制終了
#   reset  : リセット
#
# Data Directory
#   minescript/data/advrace/
#
# Author : crocado
# ============================================================


# ============================================================
# Imports
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


# ============================================================
# PATH SETTINGS
# ============================================================

BASE_DIR = "minescript/data/advrace"
os.makedirs(BASE_DIR, exist_ok=True)

CONFIG_FILE = f"{BASE_DIR}/config.json"
START_POS_FILE = f"{BASE_DIR}/start_pos.json"


# ============================================================
# LANGUAGE / MODE SETTINGS (Future use)
# ============================================================

LANG = "EN"      # EN / JP
FIRST_MODE = True
PICKUP_MODE = False


# ============================================================
# DEFAULT CONFIG
# ============================================================

DEFAULT_CONFIG = {

    # ゲーム時間（秒）
    "duration": 1800,

    # スコア方式
    # 0 = normal
    # 1 = FIRST +1
    # 2 = PICKUP (future)
    "option": 1
}


# ============================================================
# ADVANCEMENT CHAT REGEX
# (English environment)
# ============================================================

adv_pattern = re.compile(
    r"^(\w+) has (made the advancement|completed the challenge|reached the goal) \[(.+)\]"
)


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def sec_to_mmss(sec):
    """秒 → MM:SS"""
    m_, s_ = divmod(sec, 60)
    return f"{m_:02d}:{s_:02d}"


def chat(msg, color="aqua"):
    """全体チャット"""
    m.execute(
        f'tellraw @a {json.dumps({"text": msg, "color": color})}'
    )


def echo(msg):
    """実行者のみに表示"""
    m.execute(
        f'tellraw {m.player_name()} {json.dumps({"text": msg, "color": "yellow"})}'
    )


# ============================================================
# CONFIG / POSITION
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

        m.execute(
            "playsound minecraft:block.note_block.pling master @a"
        )

        time.sleep(1)

    m.execute(
        f'title @a title {json.dumps({"text": final, "color": "gold", "bold": True})}'
    )

    m.execute(
        "playsound minecraft:entity.player.levelup master @a"
    )

    time.sleep(1)


# ============================================================
# GAME STATE
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
# LOGGING
# ============================================================

def log_adv(player, adv, is_first):

    elapsed = int(time.time() - game_start_time)

    tag = " (FIRST)" if is_first else ""

    line = f"[{sec_to_mmss(elapsed)}] {adv}{tag}"

    with open(GAME_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{player} : {line}\n")

    player_adv_log.setdefault(player, []).append(line)


# ============================================================
# SCORING
# ============================================================

def calc_points(adv):

    # FIRSTモード
    if cfg["option"] == 1 and adv not in first_advancements:

        first_advancements.add(adv)

        chat(f"✨ FIRST! {adv} (+1)", "gold")

        return 2, True

    return 1, False


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
# START GAME
# ============================================================

def start_game():

    global game_active
    global game_start_time
    global GAME_LOG_FILE, PLAYER_LOG_FILE

    save_start_pos()
    pos = load_start_pos()

    # ワールド準備
    m.execute(f"setworldspawn {pos['x']} {pos['y']} {pos['z']}")
    m.execute(f"spawnpoint @a {pos['x']} {pos['y']} {pos['z']}")

    m.execute("gamerule sendCommandFeedback false")
    m.execute("gamemode adventure @a")
    m.execute("clear @a")

    # 全アドバンスメントリセット
    m.execute("advancement revoke @a everything")

    # スタート地点へ
    m.execute(f"tp @a {pos['x']} {pos['y']} {pos['z']}")

    # カウントダウン
    countdown(3, "GAME START")

    m.execute("gamemode survival @a")

    # ログファイル作成
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    GAME_LOG_FILE = f"{BASE_DIR}/advrace_{ts}.txt"
    PLAYER_LOG_FILE = f"{BASE_DIR}/advrace_{ts}_players.txt"

    with open(GAME_LOG_FILE, "w", encoding="utf-8") as f:

        f.write(
            f"=== Advancement Race ===\n"
            f"Start: {ts}\n\n"
        )

    # プレイヤーデータ初期化
    player_points.clear()
    player_adv_count.clear()
    player_adv_log.clear()
    first_advancements.clear()

    # scoreboard
    m.execute("scoreboard objectives remove advPoints")
    m.execute("scoreboard objectives add advPoints dummy Points")
    m.execute("scoreboard objectives setdisplay sidebar advPoints")

    # bossbar
    m.execute("bossbar remove advrace")
    m.execute('bossbar add advrace "Time"')
    m.execute("bossbar set advrace players @a")
    m.execute(f"bossbar set advrace max {cfg['duration']}")
    m.execute(f"bossbar set advrace value {cfg['duration']}")

    game_active = True
    game_start_time = time.time()

    chat(f"🎮 Advancement Race START ({sec_to_mmss(cfg['duration'])})")


# ============================================================
# END GAME
# ============================================================

def end_game():

    global game_active

    if not game_active:
        return

    chat("⏰ Time Up!", "red")

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

    with open(PLAYER_LOG_FILE, "w", encoding="utf-8") as f:

        for p, logs in player_adv_log.items():

            f.write(f"{p}:\n")

            for l in logs:
                f.write(f"  {l}\n")

            f.write("\n")


# ============================================================
# RESET
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


# ============================================================
# ENTRY
# ============================================================

cfg = load_config()

echo(f"Config loaded: duration={cfg['duration']}, option={cfg['option']}")

if len(sys.argv) >= 2:

    cmd = sys.argv[1]

    if cmd == "setup":

        save_config()
        cfg = load_config()

        echo("Setup complete.")

        sys.exit(0)

    elif cmd == "start":

        cfg = load_config()

        start_game()

    elif cmd == "stop":

        end_game()
        sys.exit(0)

    elif cmd == "reset":

        reset_game()
        sys.exit(0)


# ============================================================
# EVENT LOOP
# ============================================================

eq = EventQueue()
eq.register_chat_listener()

while True:

    try:
        event = eq.get(timeout=0.1)

    except Empty:
        event = None


    # ------------------------------
    # timer update
    # ------------------------------

    if game_active:

        remain = max(
            cfg["duration"] - int(time.time() - game_start_time),
            0
        )

        update_bossbar(remain)

        if remain <= 0:
            end_game()


    # ------------------------------
    # advancement detect
    # ------------------------------

    if event and event.type == EventType.CHAT and game_active:

        m_ = adv_pattern.match(event.message.strip())

        if m_:

            player, _, adv = m_.groups()

            pt, is_first = calc_points(adv)

            player_points[player] = player_points.get(player, 0) + pt

            player_adv_count[player] = player_adv_count.get(player, 0) + 1

            m.execute(
                f"scoreboard players add {player} advPoints {pt}"
            )

            log_adv(player, adv, is_first)
