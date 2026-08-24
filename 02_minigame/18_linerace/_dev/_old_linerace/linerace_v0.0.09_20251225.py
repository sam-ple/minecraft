import minescript as m
from minescript import EventQueue
import time, json, os, sys, math
from queue import Empty

# ==============================
# paths
# ==============================
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

CONFIG_FILE = f"{LOG_DIR}/linerace_config.json"
START_POS_FILE = f"{LOG_DIR}/linerace_start_pos.json"
LANES_FILE = f"{LOG_DIR}/linerace_lanes.json"

# ==============================
# default config
# ==============================
DEFAULT_CONFIG = {
    "duration": 120,
    "length": 200,
    "direction": "x",
    "lane_gap": 2,
    "block_gap": 0,
    "tolerance": 1.2,
    "players": [
        "crocadooo",
        "sampleee"
    ],
    "blocks": [
        "minecraft:white_concrete",
        "minecraft:orange_concrete",
        "minecraft:light_blue_concrete",
        "minecraft:lime_concrete",
        "minecraft:yellow_concrete"
    ]
}

# ==============================
# ground blocks
# ==============================
GROUND_BLOCKS = {
    "minecraft:dirt",
    "minecraft:grass_block[snowy=false]",
    "minecraft:grass_block[snowy=true]",
    "minecraft:coarse_dirt",
    "minecraft:sand",
    "minecraft:gravel",
    "minecraft:stone",
    "minecraft:andesite",
    "minecraft:diorite",
    "minecraft:granite",
}

SEARCH_UP = 12
SEARCH_DOWN = 60

# ==============================
# util
# ==============================
def chat(msg, color="yellow"):
    m.execute(f'tellraw @a {json.dumps({"text": msg, "color": color})}')

def sec_to_mmss(sec):
    m_, s_ = divmod(sec, 60)
    return f"{m_:02d}:{s_:02d}"

# ==============================
# config（強制上書き対応）
# ==============================
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

# ==============================
# start pos
# ==============================
def save_start_pos():
    x, y, z = map(math.floor, m.player_position())
    with open(START_POS_FILE, "w", encoding="utf-8") as f:
        json.dump({"x": x, "y": y, "z": z}, f)

def load_start_pos():
    if not os.path.exists(START_POS_FILE):
        return {"x": 0, "y": 70, "z": 0}
    with open(START_POS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ==============================
# lane persistence
# ==============================
def save_lanes(lanes):
    with open(LANES_FILE, "w", encoding="utf-8") as f:
        json.dump(lanes, f, indent=2)

def load_lanes():
    if not os.path.exists(LANES_FILE):
        return {}
    with open(LANES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ==============================
# game state
# ==============================
game_active = False
game_start_time = 0
last_boss_update = 0

lanes = {}
max_dist = {}

# ==============================
# scoreboard
# ==============================
def setup_scoreboard():
    m.execute("scoreboard objectives remove LineDist")
    m.execute('scoreboard objectives add LineDist dummy "Distance"')
    m.execute("scoreboard objectives setdisplay sidebar LineDist")

# ==============================
# build lanes (setup only)
# ==============================
def build_lanes(cfg):
    pos = load_start_pos()
    lanes.clear()
    max_dist.clear()

    for i, p in enumerate(cfg["players"]):
        offset = i * cfg["lane_gap"]

        if cfg["direction"] == "x":
            sx, sz = pos["x"], pos["z"] + offset
        else:
            sx, sz = pos["x"] + offset, pos["z"]

        sy = pos["y"]
        lanes[p] = [sx, sy, sz]
        max_dist[p] = 0

        block = cfg["blocks"][i % len(cfg["blocks"])]

        for d in range(cfg["length"]):
            if cfg["block_gap"] > 0 and d % (cfg["block_gap"] + 1) != 0:
                continue

            x = sx + d if cfg["direction"] == "x" else sx
            z = sz if cfg["direction"] == "x" else sz + d

            for y in range(sy + SEARCH_UP, sy - SEARCH_DOWN, -1):
                if m.getblock(x, y, z) in GROUND_BLOCKS:
                    m.execute(f"setblock {x} {y} {z} {block}")
                    break

    save_lanes(lanes)
    chat("🟦 LineRace setup complete", "aqua")

# ==============================
# setup
# ==============================
def setup():
    save_start_pos()
    save_config()              # ★ 必ず上書き
    cfg = load_config()        # ★ 必ず再読込
    setup_scoreboard()
    build_lanes(cfg)

# ==============================
# start
# ==============================
def start_game():
    global game_active, game_start_time, lanes, max_dist, cfg

    cfg = load_config()        # ★ 最新設定を必ず読む
    lanes = load_lanes()

    if not lanes:
        chat("⚠ Run setup first.", "red")
        return

    max_dist = {p: 0 for p in lanes}

    m.execute("gamerule sendCommandFeedback false")
    m.execute("gamemode adventure @a")

    for p, (sx, sy, sz) in lanes.items():
        m.execute(f"tp {p} {sx} {sy+1} {sz}")
        m.execute(f"scoreboard players set {p} LineDist 0")

    m.execute("bossbar remove linerace")
    m.execute('bossbar add linerace "LineRace"')
    m.execute(f"bossbar set linerace max {cfg['duration']}")
    m.execute(f"bossbar set linerace value {cfg['duration']}")
    m.execute("bossbar set linerace players @a")

    m.execute("gamemode survival @a")

    game_start_time = time.time()
    game_active = True

    chat("🏁 LineRace START!", "gold")

# ==============================
# end
# ==============================
def end_game():
    global game_active
    if not game_active:
        return

    game_active = False
    m.execute("bossbar remove linerace")
    m.execute("gamemode adventure @a")
    m.execute("gamerule sendCommandFeedback true")

    ranking = sorted(max_dist.items(), key=lambda x: x[1], reverse=True)
    chat("🏆 RESULT", "gold")
    for i, (p, d) in enumerate(ranking, 1):
        chat(f"{i}. {p} : {d} blocks")

# ==============================
# entry
# ==============================
cfg = load_config()

if len(sys.argv) >= 2:
    if sys.argv[1] == "setup":
        setup()
        sys.exit(0)
    elif sys.argv[1] == "start":
        start_game()

# ==============================
# event loop
# ==============================
eq = EventQueue()

while True:
    try:
        eq.get(timeout=0.1)
    except Empty:
        pass

    if not game_active:
        continue

    elapsed = int(time.time() - game_start_time)
    remain = max(cfg["duration"] - elapsed, 0)

    if time.time() - last_boss_update >= 1:
        m.execute(f"bossbar set linerace value {remain}")
        m.execute(
            f'bossbar set linerace name {json.dumps({"text": sec_to_mmss(remain), "color": "yellow"})}'
        )
        last_boss_update = time.time()

    players = m.players(nbt=False)

    for p, (sx, sy, sz) in lanes.items():
        pl = next((x for x in players if x.name == p), None)
        if not pl:
            continue

        px, py, pz = pl.position

        forward = abs(px - sx) if cfg["direction"] == "x" else abs(pz - sz)
        lateral = abs(pz - sz) if cfg["direction"] == "x" else abs(px - sx)

        if lateral > cfg["tolerance"]:
            m.execute(f"tp {p} {sx} {sy+1} {sz}")
            max_dist[p] = 0
            m.execute(f"scoreboard players set {p} LineDist 0")
            continue

        dist = int(forward)
        m.execute(f"scoreboard players set {p} LineDist {dist}")

        if dist > max_dist[p]:
            max_dist[p] = dist

    if remain <= 0:
        end_game()
