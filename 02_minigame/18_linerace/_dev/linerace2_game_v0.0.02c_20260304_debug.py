import minescript as m
from minescript import EventQueue
import time, json, os, sys
from queue import Empty
import math

# ==============================
# paths & config
# ==============================
# BASE_DIR = "minescript"
# os.makedirs(BASE_DIR, exist_ok=True)
# LANES_FILE = f"{BASE_DIR}/linerace_lanes.json"
BASE_DIR = "minescript/data/linerace"
os.makedirs(BASE_DIR, exist_ok=True)
LANES_FILE = f"{BASE_DIR}/lanes.json"

# ==============================
# game state
# ==============================
game_active = False
start_time = 0
last_boss_update = 0
lanes = []
tolerance = 0.5
time_limit = 900

FX, FZ = 0, 1  # 前進方向（南向き）
RX, RZ = 1, 0  # 横方向

COLORS = ["white","orange","light_blue","lime","yellow"]

# ==============================
# ヘルパー関数
# ==============================
def chat(msg, color="yellow"):
    m.execute(f'tellraw @a {json.dumps({"text": msg, "color": color})}')

def format_time(sec):
    m_, s_ = divmod(sec, 60)
    return f"{m_:02d}:{s_:02d}"

def load_data():
    global lanes, tolerance, time_limit
    if not os.path.exists(LANES_FILE):
        return False
    with open(LANES_FILE) as f:
        data = json.load(f)
    lanes = data["lanes"]
    tolerance = data["tolerance"]
    time_limit = data["time_limit"]
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
def countdown():
    for i in [3, 2, 1]:
        chat(str(i), "red")
        time.sleep(1)
    chat("GO!", "green")

# ==============================
# start game
# ==============================
def start_game():
    global game_active, start_time

    if not load_data():
        chat("Run setup first.", "red")
        return

    # scoreboard
    m.execute("scoreboard objectives remove LineDist")
    m.execute('scoreboard objectives add LineDist dummy "Distance"')
    m.execute("scoreboard objectives setdisplay sidebar LineDist")

    # teleport & spawnpoint
    for lane in lanes:
        p = lane["player"]
        if not p:
            continue
        sx, sy, sz = lane["start"]
        m.execute(f"spawnpoint {p} {sx} {sy+1} {sz}")
        m.execute(f"tp {p} {sx} {sy+1} {sz}")
        m.execute(f"scoreboard players set {p} LineDist 0")

    setup_bossbar()
    countdown()

    start_time = time.time()
    game_active = True
    chat("LineRace START!", "gold")

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
        pl = next((x for x in players if x.name == p), None)
        if not pl:
            continue
        sx, sy, sz = lane["start"]
        px, py, pz = pl.position
        dist = max(0, int((px - sx) * FX + (pz - sz) * FZ))
        results.append((p, dist))

    ranking = sorted(results, key=lambda x: x[1], reverse=True)
    chat("===== RESULT =====", "gold")
    for i, (p, d) in enumerate(ranking, 1):
        chat(f"{i}. {p} - {d} blocks")
        # スタート地点に戻す
        for lane in lanes:
            if lane["player"] == p:
                sx, sy, sz = lane["start"]
                m.execute(f"tp {p} {sx} {sy+1} {sz}")
    chat("==================")

# ==============================
# main loop
# ==============================
if len(sys.argv) >= 2 and sys.argv[1] == "start":
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
    remaining = max(0, time_limit - elapsed)

    # bossbarは1秒ごとに更新
    # if time.time() - last_boss_update >= 1:
    #     update_bossbar(remaining)
    #     last_boss_update = time.time()

    players = m.players(nbt=False)

    if time.time() - last_boss_update >= 1:
        update_bossbar(remaining)

        for lane in lanes:
            p = lane["player"]
            if not p:
                continue

            pl = next((x for x in players if x.name == p), None)
            if not pl:
                continue

            sx, sy, sz = lane["start"]
            px, py, pz = pl.position

            # スタート中心
            start_x = sx + 0.5
            start_z = sz + 0.5

            delta_x = px - start_x
            lateral = abs(delta_x)

            chat(
                f"{p}  "
                f"S({start_x:.2f},{sy+1:.2f},{start_z:.2f})  "
                f"P({px:.2f},{py:.2f},{pz:.2f})  "
                f"ΔX:{delta_x:.3f}  lat:{lateral:.3f}",
                "gray"
            )

        last_boss_update = time.time()
        
    for lane in lanes:
        p = lane["player"]
        if not p:
            continue
        sx, sy, sz = lane["start"]
        pl = next((x for x in players if x.name == p), None)
        if not pl:
            continue

        px, py, pz = pl.position

        # 前進距離
        forward = (px - sx) * FX + (pz - sz) * FZ
        dist = max(0, int(forward))
        m.execute(f"scoreboard players set {p} LineDist {dist}")

        # 横ずれ kill（修正版）
        # lateral = abs(px - sx)
        # lateral = abs((px + 0.5) - (sx + 0.5))

        # 横ずれ kill（完全修正版）
        center_x = sx + 0.5
        lateral = abs(px - center_x)

        if lateral > tolerance:
            m.execute(f"kill {p}")
            continue

    # Wool アイテム消去（全色、プレイヤー周囲10ブロック）
    for color in COLORS:
        m.execute(
            f'/execute as @a at @s run kill @e[type=item,nbt={{Item:{{id:"minecraft:{color}_wool"}}}},distance=..10]'
        )

    if remaining <= 0:
        end_game()
