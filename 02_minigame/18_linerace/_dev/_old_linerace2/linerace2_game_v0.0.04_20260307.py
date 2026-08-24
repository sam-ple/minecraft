import minescript as m
from minescript import EventQueue
import time, json, os, sys
from queue import Empty
import math

# /gamerule send_command_feedback false

# ==============================
# paths & config
# ==============================
BASE_DIR = "minescript/data/linerace"
os.makedirs(BASE_DIR, exist_ok=True)
LANES_FILE = f"{BASE_DIR}/lanes.json"

# ==============================
# game state
# ==============================
DEBUG = False

game_active = False
start_time = 0
last_boss_update = 0
lanes = []

tolerance_left = 0.6
tolerance_right = 0.6

time_limit = 900

FX, FZ = 0, 1
RX, RZ = 1, 0

COLORS = ["white","orange","light_blue","lime","yellow"]

# ==============================
# ヘルパー
# ==============================
def chat(msg, color="yellow"):
    m.execute(f'tellraw @a {json.dumps({"text": msg, "color": color})}')

def format_time(sec):
    m_, s_ = divmod(sec, 60)
    return f"{m_:02d}:{s_:02d}"

# def load_data():
#     global lanes, time_limit
#     if not os.path.exists(LANES_FILE):
#         return False
#     with open(LANES_FILE) as f:
#         data = json.load(f)

#     lanes = data["lanes"]
#     time_limit = data["time_limit"]
#     return True

def load_data():
    global lanes
    if not os.path.exists(LANES_FILE):
        return False

    with open(LANES_FILE) as f:
        data = json.load(f)

    lanes = data["lanes"]
    return True

# ==============================
# bossbar
# ==============================
def setup_bossbar():
    m.execute("bossbar remove linerace")
    m.execute('bossbar add linerace "LineRace"')
    m.execute(f"bossbar set linerace max {time_limit}")
    m.execute("bossbar set linerace players @a")

def update_bossbar(remaining):
    m.execute(f'bossbar set linerace value {remaining}')
    m.execute(f'bossbar set linerace name "Time {format_time(remaining)}"')

# ==============================
# countdown
# ==============================
# def countdown():
#     for i in [3,2,1]:
#         chat(str(i),"red")
#         time.sleep(1)
#     chat("GO!","green")

# ==============================
# countdown
# ==============================
def countdown():

    for i in [3,2,1]:

        # タイトル表示
        m.execute(
            f'title @a title {{"text":"{i}","color":"red","bold":true}}'
        )

        # カウント音
        m.execute(
            "playsound minecraft:block.note_block.hat master @a ~ ~ ~ 1 1"
        )

        time.sleep(1)

    # GO
    m.execute(
        'title @a title {"text":"GO!","color":"green","bold":true}'
    )

    m.execute(
        "playsound minecraft:entity.player.levelup master @a ~ ~ ~ 1 1"
    )

    m.execute("summon firework_rocket ~ ~1 ~ {LifeTime:20,FireworksItem:{id:firework_rocket,Count:1,tag:{Fireworks:{Explosions:[{Type:1,Colors:[I;16777215]}]}}}}")

    m.execute(
        "playsound minecraft:entity.firework_rocket.launch master @a"
    )

    time.sleep(1)

    m.execute("title @a clear")

# ==============================
# start game
# ==============================
def start_game():
    global game_active,start_time

    # コマンドログ非表示
#    m.execute("gamerule sendCommandFeedback false")
    m.execute("gamerule send_command_feedback false")

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

# ==============================
# end game
# ==============================
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

        results.append((p,dist))

    ranking = sorted(results,key=lambda x:x[1],reverse=True)

    chat("===== RESULT =====","gold")

    for i,(p,d) in enumerate(ranking,1):

        chat(f"{i}. {p} - {d} blocks")

        for lane in lanes:
            if lane["player"] == p:
                sx,sy,sz = lane["start"]
                m.execute(f"tp {p} {sx} {sy+1} {sz}")

    chat("==================")

# ==============================
# main
# ==============================
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

    elapsed = int(time.time() - start_time)

    remaining = max(0,time_limit-elapsed)

    players = m.players(nbt=False)

    if time.time() - last_boss_update >= 1:
        
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

            center_x = sx + 0.5
            center_z = sz + 0.5

            dx = px - center_x
            dz = pz - center_z

            lateral = dx*RX + dz*RZ

            if DEBUG:
                chat(
                    f"{p}  "
                    f"L:{lateral:.3f}  "
                    f"Rlimit:{tolerance_right:.2f} "
                    f"Llimit:{-tolerance_left:.2f}",
                    "gray"
                )

        last_boss_update = time.time()

    for lane in lanes:

        p = lane["player"]

        if not p:
            continue

        sx,sy,sz = lane["start"]

        pl = next((x for x in players if x.name == p),None)

        if not pl:
            continue

        px,py,pz = pl.position

        forward = (px-sx)*FX + (pz-sz)*FZ

        dist = max(0,int(forward))

        m.execute(f"scoreboard players set {p} LineDist {dist}")

        center_x = sx + 0.5
        center_z = sz + 0.5

        dx = px - center_x
        dz = pz - center_z

        lateral = dx*RX + dz*RZ

        if lateral < -tolerance_left:
            m.execute(f"kill {p}")
            continue

        if lateral > tolerance_right:
            m.execute(f"kill {p}")
            continue

    for color in COLORS:

        m.execute(
            f'/execute as @a at @s run kill @e[type=item,nbt={{Item:{{id:"minecraft:{color}_wool"}}}},distance=..10]'
        )

    if remaining <= 0:
        end_game()
