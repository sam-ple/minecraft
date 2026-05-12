import minescript as m
import time, json, os, sys

# ==================================================
# paths
# ==================================================
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

CONFIG_FILE = f"{LOG_DIR}/itemrace_config.json"

# ==================================================
# default config
# ==================================================
DEFAULT_CONFIG = {
    "duration": 120,        # ゲーム時間（秒）
    "tick_delay": 0.2,      # ループ間隔
    "players": [],          # [] = 全員(@a)
    "target_items": [
        "minecraft:diamond",
        "minecraft:gold_ingot"
    ]
}

# ==================================================
# util
# ==================================================
def cmd(c):
    m.execute(c)

def chat(msg, color="yellow"):
    m.execute(f'tellraw @a {json.dumps({"text": msg, "color": color})}')

def fmt(item):
    return item.replace("minecraft:", "").replace(":", "_")

def sec_to_mmss(sec):
    m_, s_ = divmod(sec, 60)
    return f"{m_:02d}:{s_:02d}"

# ==================================================
# config
# ==================================================
def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def has_player_limit(cfg):
    return bool(cfg["players"])

# ==================================================
# game state
# ==================================================
game_active = False
start_time = 0

# ==================================================
# setup
# ==================================================
def setup():
    cfg = load_config()

    # sneak 判定
    cmd("scoreboard objectives remove sneak_time")
    cmd("scoreboard objectives remove sneak_prev")
    cmd("scoreboard objectives remove is_sneaking")
    cmd("scoreboard objectives remove sneak_edge")

    cmd("scoreboard objectives add sneak_time minecraft.custom:minecraft.sneak_time")
    cmd("scoreboard objectives add sneak_prev dummy")
    cmd("scoreboard objectives add is_sneaking dummy")
    cmd("scoreboard objectives add sneak_edge dummy")

    # points
    cmd("scoreboard objectives remove points")
    cmd("scoreboard objectives add points dummy")
    cmd("scoreboard objectives setdisplay sidebar points")

    # items
    for item in cfg["target_items"]:
        name = fmt(item)
        cmd(f"scoreboard objectives remove has_{name}")
        cmd(f"scoreboard objectives remove collected_{name}")
        cmd(f"scoreboard objectives add has_{name} dummy")
        cmd(f"scoreboard objectives add collected_{name} dummy")

    # 初期化
    targets = cfg["players"] if cfg["players"] else ["@a"]
    for t in targets:
        cmd(f"scoreboard players reset {t} sneak_prev")
        cmd(f"scoreboard players reset {t} is_sneaking")
        cmd(f"scoreboard players reset {t} sneak_edge")
        cmd(f"scoreboard players reset {t} points")
        for item in cfg["target_items"]:
            name = fmt(item)
            cmd(f"scoreboard players reset {t} has_{name}")
            cmd(f"scoreboard players reset {t} collected_{name}")

    chat("🟦 ItemRace setup complete", "aqua")

# ==================================================
# start
# ==================================================
def start_game():
    global game_active, start_time
    cfg = load_config()

    start_time = time.time()
    game_active = True

    # collected を必ずリセット
    targets = cfg["players"] if cfg["players"] else ["@a"]
    for t in targets:
        for item in cfg["target_items"]:
            name = fmt(item)
            cmd(f"scoreboard players reset {t} collected_{name}")
        cmd(f"scoreboard players set {t} points 0")

    cmd("bossbar remove itemrace")
    cmd('bossbar add itemrace "ItemRace"')
    cmd(f"bossbar set itemrace max {cfg['duration']}")
    cmd(f"bossbar set itemrace value {cfg['duration']}")
    cmd("bossbar set itemrace players @a")

    chat("🏁 ItemRace START!", "gold")

# ==================================================
# stop
# ==================================================
def stop_game():
    global game_active
    if not game_active:
        return
    game_active = False
    cmd("bossbar remove itemrace")
    chat("⛔ ItemRace stopped", "red")

# ==================================================
# reset
# ==================================================
def reset_game():
    stop_game()
    cmd("scoreboard objectives remove points")
    chat("🔄 ItemRace reset complete", "yellow")

# ==================================================
# entry
# ==================================================
cfg = load_config()

if len(sys.argv) >= 2:
    c = sys.argv[1]
    if c == "setup":
        setup(); sys.exit(0)
    elif c == "start":
        start_game()
    elif c == "stop":
        stop_game(); sys.exit(0)
    elif c == "reset":
        reset_game(); sys.exit(0)

# ==================================================
# main loop
# ==================================================
m.echo("🕹️ ItemRace running")

while True:
    if not game_active:
        time.sleep(0.2)
        continue

    cfg = load_config()
    elapsed = int(time.time() - start_time)
    remain = max(cfg["duration"] - elapsed, 0)

    cmd(f"bossbar set itemrace value {remain}")
    cmd(f'bossbar set itemrace name "{sec_to_mmss(remain)}"')

    # ------------------------------
    # sneak 判定
    # ------------------------------
    cmd('execute as @a if score @s sneak_time > @s sneak_prev run scoreboard players set @s is_sneaking 1')
    cmd('execute as @a unless score @s sneak_time > @s sneak_prev run scoreboard players set @s is_sneaking 0')
    cmd('execute as @a if score @s is_sneaking matches 1 if score @s sneak_edge matches 0 run scoreboard players set @s sneak_edge 1')
    cmd('execute as @a unless score @s is_sneaking matches 1 run scoreboard players set @s sneak_edge 0')

    # ------------------------------
    # アイテム判定
    # ------------------------------
    if cfg["players"]:
        selectors = cfg["players"]
    else:
        selectors = [None]

    for sel in selectors:
        base = f"execute as {sel}" if sel else "execute as @a"
        for item in cfg["target_items"]:
            name = fmt(item)
            cmd(f'{base} if entity @s[nbt={{SelectedItem:{{id:"{item}"}}}}] run scoreboard players set @s has_{name} 1')
            cmd(f'{base} unless entity @s[nbt={{SelectedItem:{{id:"{item}"}}}}] run scoreboard players set @s has_{name} 0')
            cmd(f'{base} if score @s sneak_edge matches 1 if score @s has_{name} matches 1 unless score @s collected_{name} matches 1 run scoreboard players add @s points 1')
            cmd(f'{base} if score @s sneak_edge matches 1 if score @s has_{name} matches 1 unless score @s collected_{name} matches 1 run scoreboard players set @s collected_{name} 1')

    cmd('execute as @a run scoreboard players operation @s sneak_prev = @s sneak_time')

    # ------------------------------
    # time up
    # ------------------------------
    if remain <= 0:
        stop_game()
        chat("🏆 ItemRace TIME UP!", "gold")

    time.sleep(cfg["tick_delay"])
