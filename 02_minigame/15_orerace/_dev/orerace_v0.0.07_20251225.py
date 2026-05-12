import minescript as m
import time, json, os, sys, math, copy
from datetime import datetime

# ==============================
# paths
# ==============================
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

CONFIG_FILE = os.path.join(LOG_DIR, "orerace_config.json")
START_POS_FILE = os.path.join(LOG_DIR, "orerace_start_pos.json")

# ==============================
# default config
# ==============================
DEFAULT_CONFIG = {
    "duration": 300,
    "tick_delay": 0.5,
    "option": {
        "enable_double_time": True
    },
    "double_time": 30,
    "ores": {
        "copper_ore": 1,
        "iron_ore": 2,
        "gold_ore": 2,
        "lapis_ore": 3,
        "emerald_ore": 4,
        "diamond_ore": 5,
        "deepslate_copper_ore": 1,
        "deepslate_iron_ore": 2,
        "deepslate_gold_ore": 2,
        "deepslate_lapis_ore": 3,
        "deepslate_emerald_ore": 4,
        "deepslate_diamond_ore": 5,
    }
}

# ==============================
# config
# ==============================
def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return copy.deepcopy(DEFAULT_CONFIG)
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ★ 初期CFG（setup後に確定し直す）
CFG = copy.deepcopy(load_config())

# ==============================
# util
# ==============================
def chat(msg, color="aqua"):
    m.execute(f'tellraw @a {json.dumps({"text": msg, "color": color})}')

def title(main, sub=None):
    m.execute(f'title @a title {json.dumps({"text": main, "bold": True, "color": "gold"})}')
    if sub:
        m.execute(f'title @a subtitle {json.dumps({"text": sub, "color": "yellow"})}')

def sec_to_mmss(sec):
    m_, s_ = divmod(max(sec, 0), 60)
    return f"{m_:02d}:{s_:02d}"

# ==============================
# start position
# ==============================
def save_start_pos():
    x, y, z = m.player_position()
    with open(START_POS_FILE, "w", encoding="utf-8") as f:
        json.dump({"x": math.floor(x), "y": math.floor(y), "z": math.floor(z)}, f)

def load_start_pos():
    if not os.path.exists(START_POS_FILE):
        return None
    with open(START_POS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ==============================
# state
# ==============================
game_active = False
start_time = 0
last_boss_update = 0
double_announced = False
LOG_FILE = ""

# ==============================
# setup
# ==============================
def setup():
    global CFG

    # ★ 毎回必ず DEFAULT_CONFIG を上書き保存
    save_config(DEFAULT_CONFIG)

    # ★ 書いた内容を即再読込（完全同期）
    CFG = copy.deepcopy(load_config())

    m.execute("gamerule sendCommandFeedback false")

    try: m.execute("scoreboard objectives remove minePoints")
    except: pass
    m.execute('scoreboard objectives add minePoints dummy "OreRace Points"')

    m.execute("scoreboard objectives add Work dummy")

    for ore in CFG["ores"]:
        for obj in [f"mined_{ore}", f"Last_{ore}", f"Temp_{ore}", f"Log_{ore}"]:
            try: m.execute(f"scoreboard objectives remove {obj}")
            except: pass
        m.execute(f"scoreboard objectives add mined_{ore} mined:{ore}")
        m.execute(f"scoreboard objectives add Last_{ore} dummy")
        m.execute(f"scoreboard objectives add Temp_{ore} dummy")
        m.execute(f"scoreboard objectives add Log_{ore} dummy")

    m.execute("scoreboard objectives setdisplay sidebar minePoints")
    chat("🪨 OreRace setup complete!", "aqua")

# ==============================
# bossbar
# ==============================
def setup_bossbar():
    try: m.execute("bossbar remove orerace")
    except: pass
    m.execute('bossbar add orerace "OreRace"')
    m.execute(f"bossbar set orerace max {CFG['duration']}")
    m.execute(f"bossbar set orerace value {CFG['duration']}")
    m.execute("bossbar set orerace players @a")

def update_bossbar():
    global last_boss_update
    now = time.time()
    if now - last_boss_update < 1:
        return None

    remain = max(CFG["duration"] - int(now - start_time), 0)
    m.execute(f"bossbar set orerace value {remain}")
    m.execute(f'bossbar set orerace name {json.dumps({"text": sec_to_mmss(remain)})}')
    last_boss_update = now
    return remain

# ==============================
# countdown
# ==============================
def countdown(sec, final):
    for i in range(sec, 0, -1):
        title(str(i))
        m.execute("playsound minecraft:block.note_block.pling master @a")
        time.sleep(1)
    title(final)
    m.execute("playsound minecraft:entity.player.levelup master @a")
    time.sleep(0.5)

# ==============================
# get_score（★ 修正済み）
# ==============================
def get_score(player, objective):
    out = m.execute(f"scoreboard players get {player} {objective}")
    if not out:
        return 0
    for tok in out.split():
        if tok.isdigit():
            return int(tok)
    return 0

# ==============================
# show_ranking
# ==============================
def show_ranking():
    scores = []
    for pl in m.players(nbt=False):
        pt = get_score(pl.name, "minePoints")
        scores.append((pl.name, pt))

    scores.sort(key=lambda x: x[1], reverse=True)

    chat("🏆 === OreRace Ranking ===", "gold")
    for i, (name, pt) in enumerate(scores, start=1):
        medal = "🥇 " if i == 1 else "🥈 " if i == 2 else "🥉 " if i == 3 else ""
        chat(f"{medal}{i}位 {name} : {pt} pt", "white")

# ==============================
# start
# ==============================
def start_game():
    global game_active, start_time, double_announced, LOG_FILE

    save_start_pos()
    pos = load_start_pos()

    m.execute("clear @a")
    m.execute("gamemode adventure @a")

    if pos:
        m.execute(f"setworldspawn {pos['x']} {pos['y']} {pos['z']}")
        m.execute(f"tp @a {pos['x']} {pos['y']} {pos['z']}")

    setup_bossbar()
    countdown(3, "GAME START!")

    start_time = time.time()
    game_active = True
    double_announced = False

    m.execute("gamemode survival @a")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    LOG_FILE = os.path.join(LOG_DIR, f"orerace_{ts}.txt")

    for pl in m.players(nbt=False):
        m.execute(f"scoreboard players set {pl.name} minePoints 0")
        for ore in CFG["ores"]:
            m.execute(f"scoreboard players set {pl.name} Last_{ore} 0")
            m.execute(f"scoreboard players set {pl.name} Log_{ore} 0")

    title("OreRace Start!", sec_to_mmss(CFG["duration"]))

# ==============================
# end
# ==============================
def end_game(reason="Time Up"):
    global game_active
    if not game_active:
        return

    game_active = False
    try: m.execute("bossbar remove orerace")
    except: pass

    m.execute("gamemode adventure @a")
    chat(f"🏁 OreRace Results ({reason})", "gold")

    if LOG_FILE:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("OreRace Log\n")
            f.write(f"Start : {datetime.fromtimestamp(start_time)}\n")
            f.write(f"End   : {datetime.now()}\n")
            f.write(f"Reason: {reason}\n\n")

    m.execute("scoreboard objectives setdisplay sidebar minePoints")
    chat("📄 Log saved", "gray")
    show_ranking()

# ==============================
# reset
# ==============================
def reset_game():
    global game_active
    game_active = False
    try: m.execute("bossbar remove orerace")
    except: pass
    chat("🔄 OreRace reset", "gray")

# ==============================
# command
# ==============================
if len(sys.argv) >= 2:
    cmd = sys.argv[1]
    if cmd == "setup":
        setup()
        sys.exit(0)
    elif cmd == "start":
        start_game()
    elif cmd == "stop":
        end_game("FORCED STOP")
        sys.exit(0)
    elif cmd == "reset":
        reset_game()
        sys.exit(0)

# ==============================
# main loop
# ==============================
while True:
    if game_active:
        remain = update_bossbar()
        if remain is not None:
            if CFG["option"]["enable_double_time"] and not double_announced and remain <= CFG["double_time"]:
                chat("🔥 DOUBLE POINT TIME!", "gold")
                double_announced = True

            for ore, base_pt in CFG["ores"].items():
                m.execute(f"scoreboard players operation @a Temp_{ore} = @a mined_{ore}")
                m.execute(f"scoreboard players operation @a Temp_{ore} -= @a Last_{ore}")

                mult = 2 if CFG["option"]["enable_double_time"] and remain <= CFG["double_time"] else 1
                total_pt = base_pt * mult

                m.execute(
                    f"execute as @a if score @s Temp_{ore} matches 1.. "
                    f"run scoreboard players operation @s Log_{ore} += @s Temp_{ore}"
                )

                m.execute(
                    f"execute as @a if score @s Temp_{ore} matches 1.. "
                    f"run scoreboard players operation @s Work = @s Temp_{ore}"
                )

                for _ in range(total_pt - 1):
                    m.execute(
                        f"execute as @a if score @s Temp_{ore} matches 1.. "
                        f"run scoreboard players operation @s Work += @s Temp_{ore}"
                    )

                m.execute(
                    f"execute as @a if score @s Temp_{ore} matches 1.. "
                    f"run scoreboard players operation @s minePoints += @s Work"
                )

                m.execute(f"scoreboard players operation @a Last_{ore} = @a mined_{ore}")

            if remain <= 0:
                end_game("Time Up")

    time.sleep(CFG["tick_delay"])
