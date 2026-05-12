import minescript as m
from minescript import EventQueue, EventType
import sys, json, time, re, os
from queue import Empty
from datetime import datetime
import math

# ==============================
# ファイル定義
# ==============================
CONFIG_FILE = "advrace_config.json"
START_POS_FILE = "advrace_start_pos.json"
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# ==============================
# デフォルト設定
# ==============================
DEFAULT_CONFIG = {
    "duration": 300,
    "option": 0   # 0=通常, 1=FIRST+1
    # "lang": "en"   // "en" or "jp"
}

# ==============================
# 正規表現（英語環境前提）
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

def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config()
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config():
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_CONFIG, f, indent=2)

def save_start_pos():
    x, y, z = m.player_position()
    x, y, z = math.floor(x), math.floor(y), math.floor(z)
    with open(START_POS_FILE, "w", encoding="utf-8") as f:
        json.dump({"x": x, "y": y, "z": z}, f)
    echo(f"Saved start position: X={x}, Y={y}, Z={z}")

def load_start_pos():
    if not os.path.exists(START_POS_FILE):
        # デフォルト位置
        return {"x": 0, "y": 70, "z": 0}
    with open(START_POS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ==============================
# countdown
# ==============================
def countdown(
    seconds,
    final_text,
    *,
    number_color="aqua",
    final_color="gold",
    number_sound="minecraft:block.note_block.pling",
    final_sound="minecraft:entity.player.levelup"
):
    for i in range(seconds, 0, -1):
        m.execute(
            f'title @a title '
            f'{json.dumps({"text": str(i), "color": number_color, "bold": True})}'
        )
        m.execute(f'playsound {number_sound} master @a')
        time.sleep(1)

    m.execute(
        f'title @a title '
        f'{json.dumps({"text": final_text, "color": final_color, "bold": True})}'
    )
    m.execute(f'playsound {final_sound} master @a')
    time.sleep(1)

# ==============================
# ゲーム状態
# ==============================
game_active = False
game_start_time = 0
last_boss_update = 0
end_countdown_started = False

player_points = {}
player_adv_count = {}
player_adv_log = {}
first_advancements = set()

game_ts = ""
GAME_LOG_FILE = ""
PLAYER_LOG_FILE = ""

# ==============================
# ログ
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
def calc_points(adv, option):
    base = 1
    is_first = False

    if option == 1 and adv not in first_advancements:
        first_advancements.add(adv)
        is_first = True
        chat(f"✨ FIRST! {adv} (+1)", "gold")
        return base + 1, is_first

    return base, False

# ==============================
# game control
# ==============================
def start_game():
    global game_active, game_start_time, end_countdown_started
    global GAME_LOG_FILE, PLAYER_LOG_FILE, game_ts

    cfg = load_config()
    save_start_pos()

    m.execute("gamerule sendCommandFeedback false")
    m.execute("gamemode adventure @a")
    m.execute("clear @a")
    m.execute("advancement revoke @a everything")

    pos = load_start_pos()
    m.execute(f"tp @a {pos['x']} {pos['y']} {pos['z']}")

    countdown(3, "GAME START")

    m.execute("gamemode survival @a")

    game_ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    GAME_LOG_FILE = f"{LOG_DIR}/advrace_{game_ts}.txt"
    PLAYER_LOG_FILE = f"{LOG_DIR}/advrace_{game_ts}_players.txt"

    with open(GAME_LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"=== Advancement Race Log ===\nStart: {game_ts}\n\n")

    player_points.clear()
    player_adv_count.clear()
    player_adv_log.clear()
    first_advancements.clear()

    game_active = True
    end_countdown_started = False
    game_start_time = time.time()

    m.execute("bossbar remove advrace")
    m.execute('bossbar add advrace "Time"')
    m.execute('bossbar set advrace players @a')
    m.execute(f'bossbar set advrace max {cfg["duration"]}')
    m.execute(f'bossbar set advrace value {cfg["duration"]}')
    m.execute('bossbar set advrace color blue')

    chat(f"🎮 Advancement Race START ({sec_to_mmss(cfg['duration'])})")

# ==============================
# 🏁 end（時間満了）
# ==============================
def end_game():
    global game_active
    chat("⏰ Time Up!", "red")
    show_result()
    cleanup_after_game()

# ==============================
# ⛔ stop（強制終了）
# ==============================
def stop_game():
    chat("⛔ Game Stopped", "red")
    show_result()
    cleanup_after_game()

# ==============================
# 共通後処理
# ==============================
def show_result():
    ranking = sorted(player_points.items(), key=lambda x: x[1], reverse=True)

    chat("🏁 === Result ===", "white")
    for i, (p, pt) in enumerate(ranking, 1):
        advs = player_adv_count.get(p, 0)
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else ""
        chat(f"{medal} {i}. {p} : {pt} pt ({advs} adv)")

    if ranking:
        winner, pt = ranking[0]
        advs = player_adv_count.get(winner, 0)
        m.execute(f'title @a title {json.dumps({"text": f"🏆 Winner: {winner}", "color": "gold", "bold": True})}')
        m.execute(f'title @a subtitle {json.dumps({"text": f"{pt} pt / {advs} adv", "color": "yellow"})}')

    with open(PLAYER_LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"=== Player Logs ===\n")
        for p, logs in player_adv_log.items():
            f.write(f"{p}:\n")
            for l in logs:
                f.write(f"  {l}\n")
            f.write("\n")

    chat("📄 Logs saved")

def cleanup_after_game():
    global game_active
    game_active = False

    m.execute("bossbar remove advrace")
    m.execute("gamerule sendCommandFeedback true")
    m.execute("gamemode adventure @a")

    pos = load_start_pos()
    m.execute(f"tp @a {pos['x']} {pos['y']} {pos['z']}")

# ==============================
# reset
# ==============================
def reset_game():
    m.execute("bossbar remove advrace")
    m.execute("gamemode adventure @a")
    pos = load_start_pos()
    m.execute(f"tp @a {pos['x']} {pos['y']} {pos['z']}")
    echo("Reset complete.")

# ==============================
# command entry
# ==============================
# if len(sys.argv) >= 2:
#     cmd = sys.argv[1]
#     if cmd == "setup":
#         save_config()
#         echo("Setup complete.")
#     elif cmd == "start":
#         start_game()
#     elif cmd == "stop":
#         stop_game()
#     elif cmd == "reset":
#         reset_game()
#     # sys.exit(0)

if len(sys.argv) >= 2:
    cmd = sys.argv[1]

    if cmd == "setup":
        save_config()
        sys.exit(0)

    elif cmd == "start":
        start_game()
        # exit しない（ループに入る）

    elif cmd == "end":
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

    cfg = load_config()
    if game_active:
        remaining = max(cfg["duration"] - int(time.time() - game_start_time), 0)

        # bossbar更新
        if time.time() - last_boss_update >= 1:
            m.execute(f'bossbar set advrace value {remaining}')
            m.execute(f'bossbar set advrace name {json.dumps({"text": sec_to_mmss(remaining), "color":"gold"})}')
            last_boss_update = time.time()

        # 終了10秒前カウントダウン
        if remaining <= 10 and not end_countdown_started:
            end_countdown_started = True
            countdown(
                10,
                "GAME END",
                number_color="red",
                final_color="dark_red",
                number_sound="minecraft:block.note_block.bass",
                final_sound="minecraft:entity.ender_dragon.growl"
            )

        # 時間切れ
        if remaining <= 0:
            end_game()

    # advancement検知
    if event and event.type == EventType.CHAT and game_active:
        m_ = adv_pattern.match(event.message.strip())
        if m_:
            player, _, adv = m_.groups()
            pt, is_first = calc_points(adv, cfg["option"])
            player_points[player] = player_points.get(player, 0) + pt
            player_adv_count[player] = player_adv_count.get(player, 0) + 1
            log_adv(player, adv, is_first)
