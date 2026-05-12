import minescript as m 
import time
import random
from queue import Empty
from minescript import EventQueue, EventType

# ========== 設定 ==========
BASE_TIME_PER_MISSION = 10  # 各ミッションあたりの時間
BOSSBAR_ID = "minecraft:mission_timer"
player = m.player_name()

prev_bossbar_value = None
prev_bossbar_name = None

# ========== 表示ヘルパー関数 ==========

def title_subtitle(title_text, subtitle_text=None, title_color="gold", subtitle_color="aqua", delay=1):
    m.execute("title @a clear")
    m.execute(f'title @a title {{"text":"{title_text}","color":"{title_color}","bold":true}}')
    if subtitle_text and subtitle_text.strip():
        m.execute(f'title @a subtitle {{"text":"{subtitle_text}","color":"{subtitle_color}","bold":true}}')
    time.sleep(delay)

def update_bossbar(time_left, total_time):
    global prev_bossbar_value, prev_bossbar_name
    time_left_int = int(time_left)
    if prev_bossbar_value != time_left_int:
        m.execute(f"bossbar set {BOSSBAR_ID} value {time_left_int}")
        prev_bossbar_value = time_left_int
    name_text = f"Time Left: {time_left_int}s"
    if prev_bossbar_name != name_text:
        m.execute(f'bossbar set {BOSSBAR_ID} name {{"text":"{name_text}","color":"yellow"}}')
        prev_bossbar_name = name_text

def setup_bossbar(total_time):
    m.execute(f"bossbar remove {BOSSBAR_ID}")
    m.execute(f'bossbar add {BOSSBAR_ID} {{"text":"Mission Timer","color":"yellow"}}')
    m.execute(f"bossbar set {BOSSBAR_ID} max {total_time}")
    m.execute(f"bossbar set {BOSSBAR_ID} value {total_time}")
    m.execute(f"bossbar set {BOSSBAR_ID} players @a")
    m.execute(f"bossbar set {BOSSBAR_ID} visible true")

# ========== ミッションチェック関数 ==========

def check_sneak(eq):
    start = time.time()
    while time.time() - start < 0.1:
        try:
            event = eq.get(timeout=0.01)
            if event.type == EventType.KEY and event.key == 340 and event.action == 1:
                return True
        except Empty:
            pass
    return False

def check_look_up(eq=None):
    pitch = m.player_orientation()[1]
    return pitch < -45

def check_look_down(eq=None):
    pitch = m.player_orientation()[1]
    return pitch > 45

def check_use_shovel(eq):
    start = time.time()
    while time.time() - start < 0.3:
        try:
            event = eq.get(timeout=0.01)
            if event.type == EventType.MOUSE and event.button == 0 and event.action == 1:
                hands = m.player_hand_items()
                mainhand_item = getattr(hands, "main_hand", None)
                if mainhand_item and mainhand_item.item == "minecraft:iron_shovel":
                    return True
        except Empty:
            pass
    return False

def check_offhand_stick(eq=None):
    hands = m.player_hand_items()
    offhand_item = getattr(hands, "off_hand", None)
    return offhand_item and offhand_item.item == "minecraft:stick"

def check_on_dirt(eq=None):
    pos = m.player_position()
    x, y, z = int(pos[0]), int(pos[1]) - 1, int(pos[2])
    block = m.getblock(x, y, z)
    return str(block).lower().find("dirt") >= 0

def check_throw_item(eq):
    start = time.time()
    while time.time() - start < 0.1:
        try:
            event = eq.get(timeout=0.01)
            if event.type == EventType.KEY and event.key == 81 and event.action == 1:
                return True
        except Empty:
            pass
    return False

def check_clear_hotbar(eq=None):
    inv = m.player_inventory()
    for item in inv:
        if 0 <= item.slot <= 8 and item.count > 0:
            return False
    return True

# ========== ミッション一覧 ==========
missions = [
    ("Sneak", check_sneak),
    ("Look Up", check_look_up),
    ("Look Down", check_look_down),
    ("Use Iron Shovel", check_use_shovel),
    ("Hold Stick in Offhand", check_offhand_stick),
    ("Stand on Dirt", check_on_dirt),
    ("Throw an Item", check_throw_item),
    ("Clear Hotbar", check_clear_hotbar),
]

# ========== 複数ミッション処理 ==========
def run_mission_sequence(mission_count, eq):
    total_time = mission_count * BASE_TIME_PER_MISSION
    setup_bossbar(total_time)
    start_time = time.time()
    completed = 0
    selected = random.sample(missions, k=mission_count)

    for label, func in selected:
        title_subtitle("🎮 Mission", f"{label} ☆", delay=0.7)
        while True:
            elapsed = time.time() - start_time
            time_left = max(0, total_time - elapsed)
            update_bossbar(time_left, total_time)

            if func(eq):
                title_subtitle("✅ Cleared!", f"{label} ★", delay=0.5)
                completed += 1
                break

            if elapsed > total_time:
                title_subtitle("💀 Time Over!", f"{label} ×")
                m.execute(f"kill {player}")
                m.execute(f"bossbar remove {BOSSBAR_ID}")
                return False

            time.sleep(0.1)

    m.execute(f"bossbar remove {BOSSBAR_ID}")
    return True

# ========== メインループ ==========
def main():
    with EventQueue() as eq:
        eq.register_key_listener()
        eq.register_mouse_listener()
        mission_count = 1

        while True:
            try:
                m.chat(f"[Stage {mission_count}] ミッション数: {mission_count} / 時間: {mission_count * BASE_TIME_PER_MISSION}s")
                success = run_mission_sequence(mission_count, eq)
                if not success:
                    break

                mission_count += 1
                title_subtitle(f"Stage {mission_count - 1} Complete!", f"次は {mission_count}ミッション！", delay=1.5)
                time.sleep(1)

            except Exception as e:
                m.chat(f"[ERROR] {e}")
                break

if __name__ == "__main__":
    main()
