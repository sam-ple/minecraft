import minescript as m
import time, json, os, sys, math

# ==============================
# ファイル
# ==============================
CONFIG_FILE = "orerace_config.json"
START_POS_FILE = "orerace_start_pos.json"

# ==============================
# デフォルト設定
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
        "deepslate_emerald_ore": 4,
        "diamond_ore": 5,
        "deepslate_diamond_ore": 5
    }
}

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
def chat(msg, color="aqua"):
    m.execute(f'tellraw @a {json.dumps({"text": msg, "color": color})}')

def title(main, sub=""):
    m.execute(f'title @a title {json.dumps({"text": main, "bold": True, "color": "gold"})}')
    if sub:
        m.execute(f'title @a subtitle {json.dumps({"text": sub, "color": "yellow"})}')

def sec_to_mmss(sec):
    m_, s_ = divmod(max(sec, 0), 60)
    return f"{m_:02d}:{s_:02d}"

# ==============================
# カウントダウン
# ==============================
def countdown(sec, final_text):
    for i in range(sec, 0, -1):
        title(str(i))
        m.execute("playsound minecraft:block.note_block.pling master @a")
        time.sleep(1)
    title(final_text)
    m.execute("playsound minecraft:entity.player.levelup master @a")
    time.sleep(0.5)

# ==============================
# start pos
# ==============================
def save_start_pos():
    x, y, z = m.player_position()
    with open(START_POS_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "x": math.floor(x),
            "y": math.floor(y),
            "z": math.floor(z)
        }, f)

def load_start_pos():
    if not os.path.exists(START_POS_FILE):
        return None
    with open(START_POS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ==============================
# 状態
# ==============================
game_active = False
start_time = 0
last_boss_update = 0
double_announced = False
end_countdown_started = False

# ==============================
# setup
# ==============================
def setup():
    cfg = load_config()
    save_config(cfg)

    m.execute("gamerule sendCommandFeedback false")

    # scoreboard
    m.execute("scoreboard objectives remove minePoints")
    m.execute('scoreboard objectives add minePoints dummy "OreRace Points"')

    for ore in cfg["ores"]:
        m.execute(f"scoreboard objectives add mined_{ore} mined:{ore}")
        m.execute(f"scoreboard objectives add Last_{ore} dummy")
        m.execute(f"scoreboard objectives add Temp_{ore} dummy")

    m.execute("scoreboard objectives setdisplay sidebar minePoints")
    chat("🪨 OreRace setup complete!")

# ==============================
# bossbar
# ==============================
def setup_bossbar(cfg):
    m.execute("bossbar remove orerace")
    m.execute('bossbar add orerace "OreRace"')
    m.execute(f"bossbar set orerace max {cfg['duration']}")
    m.execute(f"bossbar set orerace value {cfg['duration']}")
    m.execute("bossbar set orerace players @a")

def update_bossbar(cfg):
    global last_boss_update
    now = time.time()
    if now - last_boss_update < 1:
        return None

    remain = max(cfg["duration"] - int(now - start_time), 0)
    m.execute(f"bossbar set orerace value {remain}")
    m.execute(f'bossbar set orerace name "{sec_to_mmss(remain)}"')

    last_boss_update = now
    return remain

# ==============================
# start
# ==============================
def start_game():
    global game_active, start_time, double_announced, end_countdown_started

    cfg = load_config()

    save_start_pos()
    pos = load_start_pos()

    m.execute("clear @a")
    m.execute("gamemode adventure @a")
    if pos:
        m.execute(f"tp @a {pos['x']} {pos['y']} {pos['z']}")

    setup_bossbar(cfg)

    countdown(3, "GAME START!")
    m.execute("gamemode survival @a")

    game_active = True
    start_time = time.time()
    double_announced = False
    end_countdown_started = False

    for pl in m.players(nbt=False):
        name = pl.name
        m.execute(f"scoreboard players set {name} minePoints 0")
        for ore in cfg["ores"]:
            m.execute(f"scoreboard players set {name} Last_{ore} 0")

    title("OreRace Start!", sec_to_mmss(cfg["duration"]))

# ==============================
# end
# ==============================
def end_game(reason="Time Up"):
    global game_active
    if not game_active:
        return

    game_active = False
    m.execute("bossbar remove orerace")
    m.execute("gamemode adventure @a")

    chat(f"🏁 OreRace Results ({reason})", "gold")

    pos = load_start_pos()
    if pos:
        m.execute(f"tp @a {pos['x']} {pos['y']} {pos['z']}")

# ==============================
# reset
# ==============================
def reset_game():
    global game_active
    game_active = False
    m.execute("bossbar remove orerace")

    pos = load_start_pos()
    if pos:
        m.execute(f"tp @a {pos['x']} {pos['y']} {pos['z']}")

    chat("🔄 OreRace reset", "gray")

# ==============================
# command
# ==============================
if len(sys.argv) >= 2:
    cmd = sys.argv[1]
    if cmd == "setup":
        setup()
    elif cmd == "start":
        start_game()
    elif cmd == "end":
        end_game()
    elif cmd == "reset":
        reset_game()

# ==============================
# main loop
# ==============================
while True:
    cfg = load_config()

    if game_active:
        remain = update_bossbar(cfg)

        if cfg["option"]["enable_double_time"] and not double_announced and remain <= cfg["double_time"]:
            chat("🔥 DOUBLE POINT TIME!", "gold")
            double_announced = True

        if remain == 10 and not end_countdown_started:
            end_countdown_started = True
            countdown(10, "GAME END!")

        for ore, base_pt in cfg["ores"].items():
            m.execute(f"scoreboard players operation @a Temp_{ore} = @a mined_{ore}")
            m.execute(f"scoreboard players operation @a Temp_{ore} -= @a Last_{ore}")

            add = base_pt * (2 if cfg["option"]["enable_double_time"] and remain <= cfg["double_time"] else 1)

            m.execute(
                f"execute as @a if score @s Temp_{ore} matches 1.. "
                f"run scoreboard players add @s minePoints {add}"
            )

            m.execute(f"scoreboard players operation @a Last_{ore} = @a mined_{ore}")

        if remain is not None and remain <= 0:
            end_game()

    time.sleep(cfg["tick_delay"])
