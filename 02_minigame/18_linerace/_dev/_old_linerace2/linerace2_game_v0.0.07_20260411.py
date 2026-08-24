# ============================================================
# LINERACE GAME SYSTEM
# Version : v0.0.07
# Date: 2026-04-11
#
# Minecraft Java Edition + Minescript
#
# File
#   linerace_game.py : LineRaceゲーム進行管理
#
# Features
#   ・カウントダウン演出
#   ・BossBarタイマー
#   ・レーン逸脱判定
#   ・距離スコア管理
#   ・結果ランキング表示
#
# Commands
#   start : ゲーム開始
#
# Data Directory
#   minescript/data/linerace/
#
# Author : crocado
# ============================================================

import minescript as m
from minescript import EventQueue
import time
import json
import os
import sys
from queue import Empty

# ============================================================
# DATA DIRECTORY
# ============================================================

BASE_DIR = "minescript/data/linerace"
os.makedirs(BASE_DIR, exist_ok=True)

LANES_FILE = f"{BASE_DIR}/lanes.json"

# ============================================================
# GAME SETTINGS
# ============================================================

time_limit = 300 #1800

tolerance_left  = 0.6
tolerance_right = 0.6

FX,FZ = 0,1
RX,RZ = 1,0

COLORS = ["white","orange","light_blue","lime","yellow"]

# ============================================================
# STATE
# ============================================================

game_active = False
start_time = 0
last_boss_update = -1   # ★追加（NoChange対策）

lanes = []

# ============================================================
# UTIL
# ============================================================

def chat(msg,color="yellow"):
    m.execute(f'tellraw @a {json.dumps({"text":msg,"color":color})}')

def format_time(sec):
    m_,s_ = divmod(sec,60)
    return f"{m_:02d}:{s_:02d}"

# ============================================================
# LOAD
# ============================================================

def load_data():
    global lanes

    if not os.path.exists(LANES_FILE):
        return False

    with open(LANES_FILE) as f:
        data = json.load(f)

    lanes = data["lanes"]
    return True

# ============================================================
# BOSSBAR
# ============================================================

def setup_bossbar():

    # removeしない（エラー回避）
    m.execute('bossbar add linerace "LineRace"')
    m.execute(f"bossbar set linerace max {time_limit}")
    m.execute("bossbar set linerace players @a")


def update_bossbar(remaining):

    global last_boss_update

    # ★同じ値なら更新しない
    if remaining == last_boss_update:
        return

    last_boss_update = remaining

    m.execute(f"bossbar set linerace value {remaining}")
    m.execute(f'bossbar set linerace name "Time {format_time(remaining)}"')

# ============================================================
# COUNTDOWN
# ============================================================

def countdown():

    for i in [3,2,1]:

        m.execute(f'title @a title {{"text":"{i}","color":"red","bold":true}}')
        m.execute("playsound minecraft:block.note_block.hat master @a ~ ~ ~ 1 1")
        time.sleep(1)

    m.execute('title @a title {"text":"GO!","color":"green","bold":true}')
    m.execute("playsound minecraft:entity.player.levelup master @a ~ ~ ~ 1 1")
    m.execute("playsound minecraft:entity.firework_rocket.launch master @a")
    time.sleep(1)

    m.execute("title @a clear")

# ============================================================
# START
# ============================================================

def start_game():

    global game_active,start_time,last_boss_update

    m.execute("gamerule sendCommandFeedback false")
    m.execute("tag @a remove started")

    last_boss_update = -1  # ★リセット

    if not load_data():
        chat("Run setup first.","red")
        return

    m.execute("scoreboard objectives remove LineDist")
    m.execute('scoreboard objectives add LineDist dummy "Distance"')
    m.execute("scoreboard objectives setdisplay sidebar LineDist")

    for lane in lanes:

        p = lane["player"]
        if not p:
            continue

        sx,sy,sz = lane["start"]

        m.execute(f"spawnpoint {p} {sx} {sy+1} {sz}")
        m.execute(f"tp {p} {sx} {sy+1} {sz}")
        m.execute(f"scoreboard players set {p} LineDist 0")

    setup_bossbar()
    countdown()

    start_time = time.time()
    game_active = True

    chat("LineRace START!","gold")

# ============================================================
# END
# ============================================================

def end_game():

    global game_active

    if not game_active:
        return

    game_active = False

    m.execute("bossbar remove linerace")

    players = m.players(nbt=False)
    results = []

    for lane in lanes:

        p = lane["player"]
        if not p:
            continue

        pl = next((x for x in players if x.name == p),None)
        if not pl:
            continue

        sx,sy,sz = lane["start"]
        px,py,pz = pl.position

        dist = max(0,int((px-sx)*FX + (pz-sz)*FZ))
        results.append((p,dist,px,py,pz))

    ranking = sorted(results,key=lambda x:x[1],reverse=True)

    chat("===== RESULT =====","gold")

    for i,(p,d,x,y,z) in enumerate(ranking,1):

        chat(f"{i}. {p} - {d} blocks")

        # ★ アーマースタンド生成（フル装備＋頭）
        m.execute(
            f'summon minecraft:armor_stand {int(x)} {int(y)} {int(z)} '
            f'{{NoGravity:1b,ShowArms:1b,PersistenceRequired:1b,'
            f'equipment:{{'
            f'head:{{id:"minecraft:player_head",Count:1,components:{{profile:{{name:"{p}"}}}}}},'
            f'chest:{{id:"minecraft:netherite_chestplate",Count:1}},'
            f'legs:{{id:"minecraft:netherite_leggings",Count:1}},'
            f'feet:{{id:"minecraft:netherite_boots",Count:1}}'
            f'}}}}'
        )

        # 元位置に戻す
        for lane in lanes:
            if lane["player"] == p:
                sx,sy,sz = lane["start"]
                m.execute(f"tp {p} {sx} {sy+1} {sz}")

    chat("==================")

# ============================================================
# START ITEMS
# ============================================================

def cmd_start():

    # 弓
    m.execute('execute as @a[tag=!started] at @s if block ~ ~-1 ~ minecraft:gold_block run clear @s minecraft:bow')
    m.execute('execute as @a[tag=!started] at @s if block ~ ~-1 ~ minecraft:gold_block run give @s minecraft:bow[enchantments={"minecraft:infinity":1},unbreakable={}] 1')

    # 矢
    m.execute('execute as @a[tag=!started] at @s if block ~ ~-1 ~ minecraft:gold_block run clear @s minecraft:arrow')
    m.execute('execute as @a[tag=!started] at @s if block ~ ~-1 ~ minecraft:gold_block run give @s minecraft:arrow 1')

    # 釣り竿
    m.execute('execute as @a[tag=!started] at @s if block ~ ~-1 ~ minecraft:gold_block run clear @s minecraft:fishing_rod')
    m.execute('execute as @a[tag=!started] at @s if block ~ ~-1 ~ minecraft:gold_block run give @s minecraft:fishing_rod[enchantments={"minecraft:luck_of_the_sea":3,"minecraft:lure":3,"minecraft:unbreaking":3,"minecraft:mending":1}] 1')

    # タグ
    m.execute('execute as @a[tag=!started] at @s if block ~ ~-1 ~ minecraft:gold_block run tag @s add started')

# ============================================================
# MAIN LOOP
# ============================================================

if len(sys.argv)>=2 and sys.argv[1]=="start":
    start_game()

eq = EventQueue()

while True:

    try:
        eq.get(timeout=0.1)
    except Empty:
        pass

    if not game_active:
        continue

    cmd_start()

    elapsed = int(time.time() - start_time)
    remaining = max(0,time_limit-elapsed)

    players = m.players(nbt=False)

    update_bossbar(remaining)

    for lane in lanes:

        p = lane["player"]
        if not p:
            continue

        pl = next((x for x in players if x.name == p),None)
        if not pl:
            continue

        sx,sy,sz = lane["start"]
        px,py,pz = pl.position

        forward = (px-sx)*FX + (pz-sz)*FZ
        dist = max(0,int(forward))

        m.execute(f"scoreboard players set {p} LineDist {dist}")

        center_x = sx + 0.5
        center_z = sz + 0.5

        dx = px - center_x
        dz = pz - center_z

        lateral = dx*RX + dz*RZ

        if lateral < -tolerance_left or lateral > tolerance_right:
            # m.execute(f"tag {p} remove started")
            m.execute(f"execute as @a[name={p},tag=started] run tag @s remove started")
            m.execute(f"kill {p}")

    for color in COLORS:
        m.execute(
            f'/execute as @a at @s run kill @e[type=item,nbt={{Item:{{id:"minecraft:{color}_wool"}}}},distance=..10]'
        )

    # 弓
    m.execute(
        'execute as @a at @s run kill @e[type=item,nbt={Item:{id:"minecraft:bow"}},distance=..10]'
    )

    # 矢
    m.execute(
        'execute as @a at @s run kill @e[type=item,nbt={Item:{id:"minecraft:arrow"}},distance=..10]'
    )

    # 釣り竿
    m.execute(
        'execute as @a at @s run kill @e[type=item,nbt={Item:{id:"minecraft:fishing_rod"}},distance=..10]'
    )

    if remaining <= 0:
        end_game()
