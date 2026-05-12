import minescript as m
from minescript import EventQueue, EventType
import sys, json, time, re, os, math
from queue import Empty
from datetime import datetime

# ==============================
# paths
# ==============================
BASE_DIR = "logs"
CONFIG_FILE = f"{BASE_DIR}/advrace_config.json"
START_POS_FILE = f"{BASE_DIR}/advrace_start_pos.json"
os.makedirs(BASE_DIR, exist_ok=True)

# ==============================
# default config
# ==============================
DEFAULT_CONFIG = {
    "duration": 300,
    "option": 0   # 0=normal, 1=FIRST+1
    # "lang": "en"   // "en" or "jp"
}

# ==============================
# regex（英語環境）
# ==============================
adv_pattern = re.compile(
    r"^(\w+) has (made the advancement|completed the challenge|reached the goal) \[(.+)\]"
)

# ==============================
# util
# ==============================
def sec_to_mmss(sec):
    m_, s_ = divmod(sec, 60)
    return f"{m_:02d}:{s_:02d}"

def chat(msg, color="aqua"):
    m.execute(f'tellraw @a {json.dumps({"text": msg, "color": color})}')

def echo(msg):
    m.execute(f'tellraw {m.player_name()} {json.dumps({"text": msg, "color": "yellow"})}')

# ==============================
# config / position
# ==============================
def save_config():
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_CONFIG, f, indent=2)

def load_config_once():
    if not os.path.exists(CONFIG_FILE):
        save_config()
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

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
# countdown（開始時のみ使用）
# ==============================
def countdown(sec, final):
    for i in range(sec, 0, -1):
        m.execute(f'title @a title {json.dumps({"text": str(i), "color": "aqua", "bold": True})}')
        m.execute("playsound minecraft:block.note_block.pling master @a")
        time.sleep(1)
    m.execute(f'title @a title {json.dumps({"text": final, "color": "gold", "bold": True})}')
    m.execute("playsound minecraft:entity.player.levelup master @a")
    time.sleep(1)

# ==============================
# game state
# ==============================
game_active = False
game_start_time = 0
last_boss_update = 0
end_countdown_started = False

player_points = {}
player_adv_count = {}
player_adv_log = {}
first_advancements = set()

GAME_LOG_FILE = ""
PLAYER_LOG_FILE = ""

# ==============================
# logging
# ==============================
def log_adv(player, adv, is_first):
    elapsed = int(time.time() - game_start_time)
    tag = " (FIRST)" if is_first else ""
    line = f"[{sec_to_mmss(elapsed)}] {adv}{tag}"

    with open(GAME_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{player} : {line}\n")

    player_adv_log.setdefault(player, []).append(line)

# ==============================
# scoring
# ==============================
def calc_points(adv):
    if cfg["option"] == 1 and adv not in first_advancements:
        first_advancements.add(adv)
        chat(f"✨ FIRST! {adv} (+1)", "gold")
        return 2, True
    return 1, False

# ==============================
# bossbar
# ==============================
def update_bossbar(remain):
    global last_boss_update
    if time.time() - last_boss_update >= 1:
        m.execute(f"bossbar set advrace value {remain}")
        m.execute(
            f'bossbar set advrace name {json.dumps({"text": sec_to_mmss(remain), "color": "gold"})}'
        )
        last_boss_update = time.time()

# ==============================
# start
# ==============================
def start_game():
    global game_active, game_start_time, end_countdown_started
    global GAME_LOG_FILE, PLAYER_LOG_FILE

    save_start_pos()
    pos = load_start_pos()

    m.execute(f"setworldspawn {pos['x']} {pos['y']} {pos['z']}")
    m.execute("gamerule sendCommandFeedback false")
    m.execute("gamemode adventure @a")
    m.execute("clear @a")
    m.execute("advancement revoke @a everything")
    m.execute(f"tp @a {pos['x']} {pos['y']} {pos['z']}")

    countdown(3, "GAME START")
    m.execute("gamemode survival @a")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    GAME_LOG_FILE = f"{BASE_DIR}/advrace_{ts}.txt"
    PLAYER_LOG_FILE = f"{BASE_DIR}/advrace_{ts}_players.txt"

    with open(GAME_LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"=== Advancement Race ===\nStart: {ts}\n\n")

    player_points.clear()
    player_adv_count.clear()
    player_adv_log.clear()
    first_advancements.clear()

    m.execute("scoreboard objectives remove advPoints")
    m.execute("scoreboard objectives add advPoints dummy Points")
    m.execute("scoreboard objectives setdisplay sidebar advPoints")

    m.execute("bossbar remove advrace")
    m.execute('bossbar add advrace "Time"')
    m.execute("bossbar set advrace players @a")
    m.execute(f"bossbar set advrace max {cfg['duration']}")
    m.execute(f"bossbar set advrace value {cfg['duration']}")

    game_active = True
    end_countdown_started = False
    game_start_time = time.time()

    chat(f"🎮 Advancement Race START ({sec_to_mmss(cfg['duration'])})")

# ==============================
# end
# ==============================
def end_game():
    global game_active
    if not game_active:
        return

    chat("⏰ Time Up!", "red")
    show_result()

    game_active = False
    m.execute("bossbar remove advrace")
    m.execute("gamemode adventure @a")
    m.execute("gamerule sendCommandFeedback true")

# ==============================
# stop (forced stop)
# ==============================
def stop_game():
    global game_active
    if not game_active:
        return
    chat("⛔ Advancement Race stopped (forced stop)", "red")
    show_result()  # 結果も出す
    game_active = False
    m.execute("bossbar remove advrace")
    m.execute("gamemode adventure @a")
    m.execute("gamerule sendCommandFeedback true")

# ==============================
# result
# ==============================
def show_result():
    ranking = sorted(player_points.items(), key=lambda x: x[1], reverse=True)
    chat("🏁 === Result ===", "white")

    for i, (p, pt) in enumerate(ranking, 1):
        advs = player_adv_count.get(p, 0)
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else ""
        chat(f"{medal} {i}. {p} : {pt} pt ({advs} adv)")

    with open(PLAYER_LOG_FILE, "w", encoding="utf-8") as f:
        for p, logs in player_adv_log.items():
            f.write(f"{p}:\n")
            for l in logs:
                f.write(f"  {l}\n")
            f.write("\n")

# ==============================
# reset
# ==============================
def reset_game():
    global game_active
    game_active = False

    m.execute("bossbar remove advrace")
    m.execute("scoreboard objectives remove advPoints")
    m.execute("gamemode adventure @a")

    pos = load_start_pos()
    m.execute(f"tp @a {pos['x']} {pos['y']} {pos['z']}")
    echo("Reset complete.")

# ==============================
# entry
# ==============================
cfg = load_config_once()

if len(sys.argv) >= 2:
    cmd = sys.argv[1]
    if cmd == "setup":
        save_config()
        echo("Setup complete.")
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
# event loop
# ==============================
eq = EventQueue()
eq.register_chat_listener()

while True:
    try:
        event = eq.get(timeout=0.1)
    except Empty:
        event = None

    if game_active:
        remain = max(cfg["duration"] - int(time.time() - game_start_time), 0)
        update_bossbar(remain)

        if remain <= 0:
            end_game()

    if event and event.type == EventType.CHAT and game_active:
        m_ = adv_pattern.match(event.message.strip())
        if m_:
            player, _, adv = m_.groups()
            pt, is_first = calc_points(adv)

            player_points[player] = player_points.get(player, 0) + pt
            player_adv_count[player] = player_adv_count.get(player, 0) + 1
            m.execute(f"scoreboard players add {player} advPoints {pt}")
            log_adv(player, adv, is_first)
