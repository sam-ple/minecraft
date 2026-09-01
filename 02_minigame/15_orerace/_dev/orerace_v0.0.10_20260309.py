# ============================================================
# ORERACE GAME SYSTEM
# Version : v0.1.00
# Date: 2026-03-09
#
# Minecraft Java Edition + MineScript
#
# File
#   orerace_game.py : OreRaceゲーム管理
#
# Features
#   ・鉱石採掘ポイントゲーム
#   ・BossBarタイマー
#   ・ダブルポイント時間
#   ・採掘ログ保存
#   ・ランキング表示
#
# Commands
#   setup  : 初期セットアップ
#   start  : ゲーム開始
#   stop   : 強制終了
#   reset  : リセット
#
# Data Directory
#   minescript/data/linerace/
#
# Author : crocado
# ============================================================

import minescript as m
import time
import json
import os
import sys
import math
import copy
from datetime import datetime


# ============================================================
# DIRECTORY
# ============================================================

BASE_DIR = "minescript/data/orerace"
os.makedirs(BASE_DIR, exist_ok=True)

CFG_FILE = f"{BASE_DIR}/config.json"
POS_FILE = f"{BASE_DIR}/start_pos.json"


# ============================================================
# DEFAULT CONFIG
# ============================================================

DEFAULT_CFG = {

    "duration": 1800,
    "tick_delay": 0.5,

    "option": {
        "enable_double_time": False #True
    },

    "double_time": 30,

    "ores": {

        "copper_ore":1,
        "iron_ore":2,
        "gold_ore":2,
        "lapis_ore":3,
        "emerald_ore":4,
        "diamond_ore":5,

        "deepslate_copper_ore":1,
        "deepslate_iron_ore":2,
        "deepslate_gold_ore":2,
        "deepslate_lapis_ore":3,
        "deepslate_emerald_ore":4,
        "deepslate_diamond_ore":5
    }
}


# ============================================================
# CONFIG IO
# ============================================================

def save_cfg(c):

    json.dump(
        c,
        open(CFG_FILE,"w",encoding="utf-8"),
        indent=2,
        ensure_ascii=False
    )


def load_cfg():

    if os.path.exists(CFG_FILE):

        return json.load(
            open(CFG_FILE,"r",encoding="utf-8")
        )

    return copy.deepcopy(DEFAULT_CFG)


CFG = copy.deepcopy(load_cfg())


# ============================================================
# GAME STATE
# ============================================================

game_active = False
start_time = 0
last_boss = 0
double_announced = False

LOG_FILE = ""


# ============================================================
# CHAT UTILITIES
# ============================================================

def chat(text,color="aqua"):

    m.execute(
        f'tellraw @a {json.dumps({"text":text,"color":color})}'
    )


def title(t,sub=None):

    m.execute(
        f'title @a title {json.dumps({"text":t,"bold":True,"color":"gold"})}'
    )

    if sub:

        m.execute(
            f'title @a subtitle {json.dumps({"text":sub,"color":"yellow"})}'
        )


def mmss(sec):

    m_,s_ = divmod(max(sec,0),60)

    return f"{m_:02}:{s_:02}"


# ============================================================
# POSITION SAVE / LOAD
# ============================================================

def save_pos():

    x,y,z = m.player_position()

    json.dump(

        {
            "x":math.floor(x),
            "y":math.floor(y),
            "z":math.floor(z)
        },

        open(POS_FILE,"w",encoding="utf-8")
    )


def load_pos():

    if os.path.exists(POS_FILE):

        return json.load(open(POS_FILE))

    return None


# ============================================================
# SETUP
# ============================================================

def setup():

    global CFG

    save_cfg(DEFAULT_CFG)

    CFG = copy.deepcopy(load_cfg())


    # --------------------------------
    # gamerule compatibility
    # 1.21.10 / 1.21.11
    # --------------------------------

    v = m.version_info()
    print("Minecraft version:", v.minecraft)

    if v.minecraft == "1.21.11":
        m.execute("gamerule send_command_feedback false")   # 1.21.11
    else:
        m.execute("gamerule sendCommandFeedback false")

    # --------------------------------
    # scoreboard cleanup
    # --------------------------------

    for o in ["minePoints","Work"]:

        try:
            m.execute(f"scoreboard objectives remove {o}")
        except:
            pass


    m.execute('scoreboard objectives add minePoints dummy "OreRace Points"')
    m.execute("scoreboard objectives add Work dummy")


    # --------------------------------
    # ore objectives
    # --------------------------------

    for ore in CFG["ores"]:

        for s in ["mined","Last","Temp","Log"]:

            try:
                m.execute(f"scoreboard objectives remove {s}_{ore}")
            except:
                pass

        m.execute(f"scoreboard objectives add mined_{ore} mined:{ore}")

        for s in ["Last","Temp","Log"]:

            m.execute(
                f"scoreboard objectives add {s}_{ore} dummy"
            )


    m.execute("scoreboard objectives setdisplay sidebar minePoints")

    chat("🪨 OreRace setup complete!")


# ============================================================
# BOSSBAR
# ============================================================

def setup_bossbar():

    try:
        m.execute("bossbar remove orerace")
    except:
        pass

    m.execute('bossbar add orerace "OreRace"')

    m.execute(
        f"bossbar set orerace max {CFG['duration']}"
    )

    m.execute(
        f"bossbar set orerace value {CFG['duration']}"
    )

    m.execute("bossbar set orerace players @a")


def update_bossbar():

    global last_boss

    now = time.time()

    if now-last_boss < 1:

        return None

    rem = max(

        CFG["duration"] - int(now-start_time),

        0
    )

    m.execute(f"bossbar set orerace value {rem}")

    m.execute(
        f'bossbar set orerace name {json.dumps({"text":mmss(rem)})}'
    )

    last_boss = now

    return rem


# ============================================================
# COUNTDOWN
# ============================================================

def countdown(sec,msg):

    for i in range(sec,0,-1):

        title(str(i))

        m.execute(
            "playsound minecraft:block.note_block.pling master @a"
        )

        time.sleep(1)

    title(msg)

    m.execute(
        "playsound minecraft:entity.player.levelup master @a"
    )

    time.sleep(0.5)


# ============================================================
# RANKING DISPLAY
# ============================================================

def show_ranking():

    chat("🏆 === OreRace Ranking ===","gold")

    m.execute("gamerule sendCommandFeedback true")

    m.execute(
        "execute as @a run scoreboard players get @s minePoints"
    )

    m.execute("gamerule sendCommandFeedback false")


# ============================================================
# START GAME
# ============================================================

def start_game():

    global game_active,start_time,double_announced,LOG_FILE

    save_pos()

    pos = load_pos()

    m.execute("clear @a")
    m.execute("gamemode adventure @a")


    if pos:

        m.execute(
            f"setworldspawn {pos['x']} {pos['y']} {pos['z']}"
        )

        m.execute(
            f"spawnpoint @a {pos['x']} {pos['y']} {pos['z']}"
        )

        m.execute(
            f"tp @a {pos['x']} {pos['y']} {pos['z']}"
        )


    setup_bossbar()

    countdown(3,"GAME START!")


    start_time = time.time()

    game_active = True

    double_announced = False


    m.execute("gamemode survival @a")


    # --------------------------------
    # log file
    # --------------------------------

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    LOG_FILE = f"{BASE_DIR}/orerace_{ts}.txt"


    for pl in m.players(nbt=False):

        m.execute(
            f"scoreboard players set {pl.name} minePoints 0"
        )

        for ore in CFG["ores"]:

            for s in ["Last","Log"]:

                m.execute(
                    f"scoreboard players set {pl.name} {s}_{ore} 0"
                )


    title("OreRace Start!",mmss(CFG["duration"]))


# ============================================================
# END GAME
# ============================================================

def end_game(reason="Time Up"):

    global game_active

    if not game_active:

        return


    game_active = False


    try:
        m.execute("bossbar remove orerace")
    except:
        pass


    m.execute("gamemode adventure @a")

    chat(f"🏁 OreRace Results ({reason})","gold")


    if LOG_FILE:

        with open(LOG_FILE,"w",encoding="utf-8") as f:

            f.write(
                f"OreRace Log\n"
                f"Start:{datetime.fromtimestamp(start_time)}\n"
                f"End:{datetime.now()}\n"
                f"Reason:{reason}\n"
            )


    m.execute(
        "scoreboard objectives setdisplay sidebar minePoints"
    )

    chat("📄 Log saved","gray")

    show_ranking()


# ============================================================
# RESET
# ============================================================

def reset_game():

    global game_active

    game_active = False

    try:
        m.execute("bossbar remove orerace")
    except:
        pass

    chat("🔄 OreRace reset","gray")


# ============================================================
# COMMAND HANDLER
# ============================================================

if len(sys.argv)>=2:

    c = sys.argv[1]

    if c=="setup":

        setup()
        sys.exit(0)

    if c=="start":

        start_game()

    if c=="stop":

        end_game("FORCED STOP")
        sys.exit(0)

    if c=="reset":

        reset_game()
        sys.exit(0)


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    if game_active:

        rem = update_bossbar()

        if rem is not None:

            if CFG["option"]["enable_double_time"] and not double_announced and rem<=CFG["double_time"]:

                chat("🔥 DOUBLE POINT TIME!","gold")

                double_announced = True


            mult = 2 if (
                CFG["option"]["enable_double_time"]
                and rem<=CFG["double_time"]
            ) else 1


            for ore,pt in CFG["ores"].items():

                m.execute(
                    f"scoreboard players operation @a Temp_{ore} = @a mined_{ore}"
                )

                m.execute(
                    f"scoreboard players operation @a Temp_{ore} -= @a Last_{ore}"
                )

                for _ in range(pt*mult):

                    m.execute(
                        f"execute as @a if score @s Temp_{ore} matches 1.. run scoreboard players operation @s minePoints += @s Temp_{ore}"
                    )

                m.execute(
                    f"execute as @a if score @s Temp_{ore} matches 1.. run scoreboard players operation @s Log_{ore} += @s Temp_{ore}"
                )

                m.execute(
                    f"scoreboard players operation @a Last_{ore} = @a mined_{ore}"
                )

            if rem<=0:

                end_game("Time Up")

    time.sleep(CFG["tick_delay"])
