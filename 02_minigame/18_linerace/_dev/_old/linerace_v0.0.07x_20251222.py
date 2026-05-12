import minescript as m
import time, json, os, sys, math
from datetime import datetime

# ==============================
# paths
# ==============================
# CONFIG_FILE = "linerace_config.json"
# START_POS_FILE = "linerace_start_pos.json"

# ==============================
# paths
# ==============================
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

CONFIG_FILE = os.path.join(LOG_DIR, "linerace_config.json")
START_POS_FILE = os.path.join(LOG_DIR, "linerace_start_pos.json")


# ==============================
# デフォルト設定
# ==============================
DEFAULT_CONFIG = {
    "duration": 120,
    "length": 200,
    "direction": "x",        # "x" or "z"
    "lane_gap": 2,           # レーン間隔（1なら隣接）
    "block_gap": 0,          # 0=連続
    "tolerance": 1.2,        # 横ズレ許容
    "players": [
        "crocadooo",
        "saaample",
        "test3",
        "test4",
        "test5"
    ],
    "blocks": [
        "minecraft:white_concrete",
        "minecraft:orange_concrete",
        "minecraft:magenta_concrete",
        "minecraft:light_blue_concrete",
        "minecraft:yellow_concrete",
        "minecraft:lime_concrete",
        "minecraft:pink_concrete",
        "minecraft:gray_concrete",
        "minecraft:light_gray_concrete",
        "minecraft:cyan_concrete",
        "minecraft:purple_concrete",
        "minecraft:blue_concrete",
        "minecraft:brown_concrete",
        "minecraft:green_concrete",
        "minecraft:red_concrete",
        "minecraft:black_concrete"
    ]
}

# ==============================
# 地面ブロック完全限定
# ==============================
GROUND_BLOCKS = {
    "minecraft:dirt",
    "minecraft:grass_block[snowy=false]",
    "minecraft:grass_block[snowy=true]",
    "minecraft:coarse_dirt",
    "minecraft:podzol",
    "minecraft:mycelium",
    "minecraft:rooted_dirt",
    "minecraft:sand",
    "minecraft:red_sand",
    "minecraft:gravel",
    "minecraft:stone",
    "minecraft:andesite",
    "minecraft:diorite",
    "minecraft:granite",
    "minecraft:deepslate",
    "minecraft:tuff",
    "minecraft:calcite",
}

SEARCH_UP = 12
SEARCH_DOWN = 60

# ==============================
# config
# ==============================
def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)

# ==============================
# util
# ==============================
def chat(msg, color="white"):
    m.execute(f'tellraw @a {json.dumps({"text": msg, "color": color})}')

def title_main(text):
    m.execute(f'title @a title {json.dumps({"text": text, "bold": True, "color": "gold"})}')

def title_sub(text):
    m.execute(f'title @a subtitle {json.dumps({"text": text, "color": "yellow"})}')

def sec_to_mmss(sec):
    m_, s_ = divmod(sec, 60)
    return f"{m_:02d}:{s_:02d}"

def countdown(sec, final_text):
    for i in range(sec, 0, -1):
        title_main(str(i))
        time.sleep(1)
    title_main(final_text)
    time.sleep(1)

# ==============================
# 開始地点
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
# 状態
# ==============================
game_active = False
start_time = 0
end_countdown_started = False

lanes = {}        # player -> (sx, sy, sz)
max_dist = {}     # player -> distance

# ==============================
# scoreboard
# ==============================
def setup_scoreboard():
    m.execute("scoreboard objectives remove LineDist")
    m.execute('scoreboard objectives add LineDist dummy "Distance"')
    m.execute("scoreboard objectives setdisplay sidebar LineDist")

# ==============================
# レーン生成（setup専用）
# ==============================
def build_lanes(cfg):
    px, py, pz = map(int, m.player_position())
    lanes.clear()
    max_dist.clear()

    for i, p in enumerate(cfg["players"]):
        offset = i * cfg["lane_gap"]

        if cfg["direction"] == "x":
            sx, sz = px, pz + offset
        else:
            sx, sz = px + offset, pz

        current_y = py
        lanes[p] = (sx, py, sz)
        max_dist[p] = 0

        for d in range(cfg["length"]):
            if cfg["block_gap"] > 0 and d % (cfg["block_gap"] + 1) != 0:
                continue

            x = sx + d if cfg["direction"] == "x" else sx
            z = sz if cfg["direction"] == "x" else sz + d

            for y in range(current_y + SEARCH_UP, current_y - SEARCH_DOWN - 1, -1):
                block = m.getblock(x, y, z)
                if block not in GROUND_BLOCKS:
                    continue

                block_type = cfg["blocks"][i % len(cfg["blocks"])]
                m.execute(f"setblock {x} {y} {z} {block_type}")
                current_y = y
                break

    chat("🟦 LineRace lanes generated (setup complete)", "aqua")

# ==============================
# setup
# ==============================
def setup():
    save_start_pos()
    setup_scoreboard()
    build_lanes(cfg)

# ==============================
# start
# ==============================
def start_game():
    global game_active, start_time, end_countdown_started

    if not lanes:
        chat("⚠ Run setup first.", "red")
        return

    for p, (sx, sy, sz) in lanes.items():
        m.execute(f"tp {p} {sx} {sy+1} {sz}")
        m.execute(f"scoreboard players set {p} LineDist 0")
        max_dist[p] = 0

    countdown(3, "RUN!")

    m.execute("bossbar remove linerace")
    m.execute('bossbar add linerace "LineRace"')
    m.execute(f"bossbar set linerace max {cfg['duration']}")
    m.execute(f"bossbar set linerace value {cfg['duration']}")
    m.execute("bossbar set linerace players @a")

    start_time = time.time()
    game_active = True
    end_countdown_started = False

# ==============================
# end
# ==============================
def end_game(reason="Time Up"):
    global game_active
    if not game_active:
        return
    game_active = False

    m.execute("bossbar remove linerace")
    m.execute("scoreboard objectives remove LineDist")

    ranking = sorted(max_dist.items(), key=lambda x: x[1], reverse=True)
    chat(f"🏁 LINE RACE RESULT ({reason})", "gold")
    for i, (p, d) in enumerate(ranking):
        chat(f"{i+1}. {p} : {d} blocks", "yellow")

    # 各プレイヤーを自分のレーンスタートに戻す
    for p, (sx, sy, sz) in lanes.items():
        m.execute(f"tp {p} {sx} {sy+1} {sz}")

# ==============================
# stop
# ==============================
def stop_game():
    global game_active
    if not game_active:
        return
    game_active = False
    m.execute("bossbar remove linerace")
    m.execute("scoreboard objectives remove LineDist")
    for p, (sx, sy, sz) in lanes.items():
        m.execute(f"tp {p} {sx} {sy+1} {sz}")
    chat("⛔ LineRace stopped (forced stop)", "red")


# ==============================
# reset
# ==============================
def reset_game():
    global game_active
    game_active = False
    m.execute("bossbar remove linerace")
    m.execute("scoreboard objectives remove LineDist")
    m.execute("gamemode adventure @a")
    for p, (sx, sy, sz) in lanes.items():
        m.execute(f"tp {p} {sx} {sy+1} {sz}")
    chat("Reset complete.", "yellow")

# ==============================
# entry
# ==============================
cfg = load_config()  # 起動時1回読み込み

if len(sys.argv) >= 2:
    cmd = sys.argv[1].lower()
    if cmd == "setup":
        setup()
        sys.exit(0)
    elif cmd == "start":
        start_game()
    elif cmd == "stop":
        stop_game()
        sys.exit(0)
    elif cmd == "reset":
        reset_game()
        sys.exit(0)

# ==============================
# main loop
# ==============================
while True:
    if game_active:
        elapsed = int(time.time() - start_time)
        remain = max(cfg["duration"] - elapsed, 0)

        m.execute(f"bossbar set linerace value {remain}")
        m.execute(f'bossbar set linerace name "{sec_to_mmss(remain)}"')

        for p, (sx, sy, sz) in lanes.items():
            pls = [pl for pl in m.players(nbt=False) if pl.name == p]
            if not pls:
                continue
            pl = pls[0]
            px, py, pz = pl.position

            forward = abs(px - sx) if cfg["direction"] == "x" else abs(pz - sz)
            lateral = abs(pz - sz) if cfg["direction"] == "x" else abs(px - sx)

            if lateral > cfg["tolerance"]:
                m.execute(f"tp {p} {sx} {sy+1} {sz}")
                max_dist[p] = 0
                m.execute(f"scoreboard players set {p} LineDist 0")
                continue

            dist = int(forward)
            if dist > max_dist[p]:
                max_dist[p] = dist
                m.execute(f"scoreboard players set {p} LineDist {dist}")

        if remain <= 0:
            end_game()

    time.sleep(0.1)
