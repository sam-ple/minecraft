import minescript as m
import time, json, os, sys, math
import re
from queue import Empty
from minescript import EventQueue, EventType

# ==============================
# ファイル
# ==============================
CONFIG_FILE = "advrace_config.json"
START_POS_FILE = "advrace_start_pos.json"

# ==============================
# デフォルト設定
# ==============================
DEFAULT_CONFIG = {
    "duration": 300,
    "players": [
        "crocadooo",
        "sampleee"
    ],
    "points": {
        "normal": 1,
        "first_bonus": 2
    },
    "option": {
        "enable_first_bonus": True
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
def chat(msg, color="white"):
    m.execute(f'tellraw @a {json.dumps({"text": msg, "color": color})}')

def title(text):
    m.execute(f'title @a title {json.dumps({"text": text, "bold": True, "color": "gold"})}')

def sound():
    m.execute("playsound minecraft:block.note_block.pling master @a")

def sec_to_mmss(sec):
    m_, s_ = divmod(sec, 60)
    return f"{m_:02d}:{s_:02d}"

# ==============================
# カウントダウン
# ==============================
def countdown_start():
    for n in [3, 2, 1]:
        title(str(n))
        sound()
        time.sleep(1)
    title("START")
    sound()

# ==============================
# start pos
# ==============================
def save_start_pos():
    x, y, z = m.player_position()
    x, y, z = math.floor(x), math.floor(y), math.floor(z)
    with open(START_POS_FILE, "w", encoding="utf-8") as f:
        json.dump({"x": x, "y": y, "z": z}, f)

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

scores = {}                   # player -> score
first_advancements = set()    # first達成済みadvancement

# ==============================
# scoreboard
# ==============================
def setup_scoreboard():
    m.execute("scoreboard objectives remove AdvPoint")
    m.execute('scoreboard objectives add AdvPoint dummy "AdvRace"')
    m.execute("scoreboard objectives setdisplay sidebar AdvPoint")

# ==============================
# bossbar
# ==============================
def setup_bossbar(duration):
    m.execute("bossbar remove advrace")
    m.execute('bossbar add advrace {"text":"AdvRace","color":"yellow"}')
    m.execute(f"bossbar set advrace max {duration}")
    m.execute(f"bossbar set advrace value {duration}")
    m.execute("bossbar set advrace players @a")

def update_bossbar(cfg):
    global last_boss_update

    now = time.time()
    if now - last_boss_update < 1:
        return None

    elapsed = int(now - start_time)
    remain = max(cfg["duration"] - elapsed, 0)

    m.execute(f"bossbar set advrace value {remain}")
    m.execute(
        f'bossbar set advrace name {json.dumps({"text": sec_to_mmss(remain), "color": "gold"})}'
    )

    last_boss_update = now
    return remain

# ==============================
# setup
# ==============================
def setup():
    save_config(DEFAULT_CONFIG)
    chat("🟨 AdvRace setup completed.", "yellow")

# ==============================
# start
# ==============================
def start_game():
    global game_active, start_time, scores, first_advancements

    cfg = load_config()

    save_start_pos()
    setup_scoreboard()
    setup_bossbar(cfg["duration"])

    scores.clear()
    first_advancements.clear()

    for p in cfg["players"]:
        scores[p] = 0
        m.execute(f"scoreboard players set {p} AdvPoint 0")

    countdown_start()

    start_time = time.time()
    game_active = True

# ==============================
# end
# ==============================
def end_game(reason="Time Up"):
    global game_active
    if not game_active:
        return

    game_active = False
    m.execute("bossbar remove advrace")

    ranking = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    chat(f"🏁 ADV RACE RESULT ({reason})", "gold")
    medals = ["🥇", "🥈", "🥉"]
    for i, (p, s) in enumerate(ranking):
        mark = medals[i] if i < 3 else "▫"
        chat(f"{mark} {p} : {s} pt", "yellow")

    pos = load_start_pos()
    if pos:
        m.execute(f"tp @a {pos['x']} {pos['y']} {pos['z']}")

# ==============================
# reset / stop
# ==============================
def reset_game():
    global game_active
    game_active = False
    m.execute("bossbar remove advrace")
    pos = load_start_pos()
    if pos:
        m.execute(f"tp @a {pos['x']} {pos['y']} {pos['z']}")
    chat("🔄 AdvRace reset.", "gray")

# ==============================
# Advancement chat pattern
# ==============================
adv_pattern = re.compile(r"^(\w+) has (made the advancement|completed the challenge|reached the goal) \[(.+)\]")

# Event queue
eq = EventQueue()
eq.register_chat_listener()

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
    try:
        event = eq.get(timeout=0.05)
    except:
        event = None

    if game_active and event and event.type == EventType.CHAT:
        msg = event.message.strip()
        match = adv_pattern.match(msg)
        if match:
            player_name, action, advancement_name = match.groups()

            add = DEFAULT_CONFIG["points"]["normal"]
            if DEFAULT_CONFIG["option"]["enable_first_bonus"]:
                if advancement_name not in first_advancements:
                    first_advancements.add(advancement_name)
                    add += DEFAULT_CONFIG["points"]["first_bonus"]
                    chat(f"✨ {player_name} is FIRST to achieve '{advancement_name}'! (+1 bonus)")

            # スコア加算
            scores[player_name] = scores.get(player_name, 0) + add
            m.execute(f"scoreboard players set {player_name} AdvPoint {scores[player_name]}")

    # bossbar update
    if game_active:
        cfg = load_config()
        remain = update_bossbar(cfg)
        if remain is not None and remain <= 0:
            end_game("Time Up")

    time.sleep(0.05)
