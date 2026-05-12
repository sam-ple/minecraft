# ============================================================
# ITEM RACE GAME SYSTEM
# Version : v0.0.07
# Date    : 2026-03-09
#
# Minecraft Java Edition + MineScript
#
# File
#   itemrace_game.py : Item Race Game
#
# Features
#   ・指定アイテム取得レース
#   ・Sneakトリガー取得判定
#   ・BossBarタイマー
#   ・スコア表示
#
# Commands
#   setup  : 初期セットアップ
#   start  : ゲーム開始
#   stop   : 強制終了
#   reset  : リセット
#
# Data Directory
#   minescript/data/itemrace/
#
# Author : crocado
# ============================================================


# ============================================================
# Imports
# ============================================================

import minescript as m
import time
import json
import os
import sys


# ============================================================
# PATH SETTINGS
# ============================================================

BASE_DIR = "minescript/data/itemrace"
os.makedirs(BASE_DIR, exist_ok=True)

CONFIG_FILE = f"{BASE_DIR}/config.json"


# ============================================================
# DEFAULT CONFIG
# ============================================================

DEFAULT_CONFIG = {

    # ゲーム時間（秒）
    "duration": 900,

    # メインループ遅延
    "tick_delay": 1.0,

    # 対象プレイヤー
    # 空なら全員
    "players": [],

    # 取得対象アイテム
    "target_items": [
        "minecraft:apple",
        "minecraft:diamond",
        "minecraft:gold_ingot"
    ]
}


# ============================================================
# COMMAND UTILITIES
# ============================================================

def cmd(c):
    """Minecraftコマンド実行"""
    m.execute(c)


def chat(msg, color="yellow"):
    """全体チャット"""
    cmd(
        f'tellraw @a {json.dumps({"text": msg, "color": color})}'
    )


# ============================================================
# TIME UTIL
# ============================================================

def sec_to_mmss(sec):
    """秒 → MM:SS"""
    m_, s_ = divmod(sec, 60)
    return f"{m_:02d}:{s_:02d}"


# ============================================================
# ITEM UTIL
# ============================================================

def fmt(item):
    """scoreboard用名前"""
    return item.replace("minecraft:", "").replace(":", "_")


def item_name(item):
    """表示用アイテム名"""
    return item.replace("minecraft:", "").replace("_", " ").title()


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


# ============================================================
# GAME STATE
# ============================================================

game_active = False
start_time = 0

current_cfg = None
current_targets = None


# ============================================================
# SETUP
# ============================================================

def setup():

    cfg = load_config()

    # --------------------------------
    # sneak detection objectives
    # --------------------------------

    for obj in [
        "sneak_time",
        "sneak_prev",
        "is_sneaking",
        "sneak_edge",
        "points"
    ]:
        cmd(f"scoreboard objectives remove {obj}")

    cmd("scoreboard objectives add sneak_time minecraft.custom:minecraft.sneak_time")
    cmd("scoreboard objectives add sneak_prev dummy")
    cmd("scoreboard objectives add is_sneaking dummy")
    cmd("scoreboard objectives add sneak_edge dummy")

    # ポイント
    cmd("scoreboard objectives add points dummy")
    cmd("scoreboard objectives setdisplay sidebar points")

    # --------------------------------
    # item objectives
    # --------------------------------

    for item in cfg["target_items"]:

        name = fmt(item)

        cmd(f"scoreboard objectives remove has_{name}")
        cmd(f"scoreboard objectives remove collected_{name}")

        cmd(f"scoreboard objectives add has_{name} dummy")
        cmd(f"scoreboard objectives add collected_{name} dummy")

    chat("🟦 ItemRace setup complete", "aqua")


# ============================================================
# RESET
# ============================================================

def reset_game():

    cfg = load_config()

    targets = cfg["players"] if cfg["players"] else ["@a"]

    # スコアリセット
    for t in targets:
        cmd(f"scoreboard players reset {t}")

    cmd("bossbar remove itemrace")
    cmd("gamemode survival @a")

    chat("🔄 ItemRace RESET", "gray")


# ============================================================
# START GAME
# ============================================================

def start_game():

    global game_active
    global start_time
    global current_cfg
    global current_targets

    current_cfg = load_config()

    current_targets = (
        current_cfg["players"]
        if current_cfg["players"]
        else ["@a"]
    )

    # gamerule
    cmd("gamerule sendCommandFeedback false")

    # bossbar
    cmd("bossbar remove itemrace")
    cmd('bossbar add itemrace "ItemRace"')

    cmd(f"bossbar set itemrace max {current_cfg['duration']}")
    cmd(f"bossbar set itemrace value {current_cfg['duration']}")

    cmd("bossbar set itemrace players @a")

    start_time = time.time()

    game_active = True

    chat("🏁 ItemRace START!", "gold")


# ============================================================
# STOP GAME
# ============================================================

def stop_game():

    global game_active

    if not game_active:
        return

    game_active = False

    cmd("bossbar remove itemrace")

    cmd("gamerule sendCommandFeedback true")


# ============================================================
# ENTRY
# ============================================================

if len(sys.argv) >= 2:

    c = sys.argv[1]

    if c == "setup":
        setup()
        sys.exit(0)

    elif c == "start":
        start_game()

    elif c == "stop":
        stop_game()
        sys.exit(0)

    elif c == "reset":
        reset_game()
        sys.exit(0)


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    if not game_active:

        time.sleep(0.2)
        continue

    # --------------------------------
    # timer
    # --------------------------------

    elapsed = int(time.time() - start_time)

    remain = max(
        current_cfg["duration"] - elapsed,
        0
    )

    cmd(f"bossbar set itemrace value {remain}")

    cmd(
        f'bossbar set itemrace name "{sec_to_mmss(remain)}"'
    )


    # --------------------------------
    # sneak edge detection
    # --------------------------------

    cmd(
        'execute as @a if score @s sneak_time > @s sneak_prev '
        'run scoreboard players set @s is_sneaking 1'
    )

    cmd(
        'execute as @a unless score @s sneak_time > @s sneak_prev '
        'run scoreboard players set @s is_sneaking 0'
    )

    cmd(
        'execute as @a if score @s is_sneaking matches 1 '
        'if score @s sneak_edge matches 0 '
        'run scoreboard players set @s sneak_edge 1'
    )

    cmd(
        'execute as @a unless score @s is_sneaking matches 1 '
        'run scoreboard players set @s sneak_edge 0'
    )


    # --------------------------------
    # item detection
    # --------------------------------

    for t in current_targets:

        base = f"execute as {t}"

        for item in current_cfg["target_items"]:

            name = fmt(item)
            pretty = item_name(item)

            cond_get = (
                f'if score @s sneak_edge matches 1 '
                f'if data entity @s SelectedItem{{id:"{item}"}} '
                f'unless score @s collected_{name} matches 1'
            )

            # points
            cmd(f'{base} {cond_get} run scoreboard players add @s points 1')

            cmd(f'{base} {cond_get} run scoreboard players set @s collected_{name} 1')

            # sound
            cmd(
                f'{base} {cond_get} run execute at @s run '
                f'playsound minecraft:entity.player.levelup master @a ~ ~ ~ 1 1'
            )

            # title
            cmd(
                f'{base} {cond_get} run title @a title '
                + json.dumps({
                    "text": f"GET {pretty}",
                    "color": "gold",
                    "bold": True
                })
            )

            cmd(
                f'{base} {cond_get} run title @a subtitle '
                + json.dumps({
                    "text": "",
                    "extra": [
                        {"text": "by ", "color": "gray"},
                        {"selector": "@s", "color": "aqua", "bold": True}
                    ]
                })
            )

            # chat
            cmd(
                f'{base} {cond_get} run tellraw @a '
                + json.dumps({
                    "text": "",
                    "extra": [
                        {"text": "✨ ", "color": "gold"},
                        {"selector": "@s", "color": "yellow"},
                        {"text": " obtained ", "color": "white"},
                        {"text": pretty, "color": "gold", "bold": True}
                    ]
                })
            )

    # --------------------------------
    # sneak_prev update
    # --------------------------------

    cmd(
        'execute as @a run scoreboard players operation '
        '@s sneak_prev = @s sneak_time'
    )


    # --------------------------------
    # end
    # --------------------------------

    if remain <= 0:

        stop_game()

        chat("🏆 ItemRace TIME UP!", "gold")


    time.sleep(current_cfg["tick_delay"])
