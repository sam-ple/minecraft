import minescript as m
import time
import random
from queue import Empty
from minescript import EventQueue, EventType

TOTAL_TIME = 30
bossbar_id = "minecraft:mission_timer"
prev_bossbar_value = None
prev_bossbar_name = None

def title_subtitle(title_text, subtitle_text=None, title_color="gold", subtitle_color="aqua", delay=1):
    m.execute("title @a clear")
    m.execute(f'title @a title {{"text":"{title_text}","color":"{title_color}","bold":true}}')
    if subtitle_text and subtitle_text.strip():
        m.execute(f'title @a subtitle {{"text":"{subtitle_text}","color":"{subtitle_color}","bold":true}}')
    time.sleep(delay)

def setup_bossbar():
    m.execute(f"bossbar remove {bossbar_id}")
    m.execute(f'bossbar add {bossbar_id} {{"text":"Mission Timer","color":"yellow"}}')
    m.execute(f"bossbar set {bossbar_id} max {TOTAL_TIME}")
    m.execute(f"bossbar set {bossbar_id} value {TOTAL_TIME}")
    m.execute(f"bossbar set {bossbar_id} players @a")
    m.execute(f"bossbar set {bossbar_id} visible true")

def update_bossbar(time_left):
    global prev_bossbar_value, prev_bossbar_name
    time_left_int = int(time_left)
    if prev_bossbar_value != time_left_int:
        m.execute(f"bossbar set {bossbar_id} value {time_left_int}")
        prev_bossbar_value = time_left_int
    name_text = f"Time Left: {time_left_int}s"
    if prev_bossbar_name != name_text:
        m.execute(f'bossbar set {bossbar_id} name {{"text":"{name_text}","color":"yellow"}}')
        prev_bossbar_name = name_text

# --- Mission Check Functions ---

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
    # Wait for left click (button 0, action 1)
    start = time.time()
    while time.time() - start < 0.3:
        try:
            event = eq.get(timeout=0.01)
            if event.type == EventType.MOUSE and event.button == 0 and event.action == 1:
                # On left-click, check if iron shovel is held
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

def run_mission(label, check_func, eq):
    title_subtitle("🎮 Mission", f"{label} ☆")
    setup_bossbar()
    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        time_left = max(0, TOTAL_TIME - elapsed)
        update_bossbar(time_left)

        if check_func(eq):
            title_subtitle("✅ Mission Cleared!", f"{label} ★")
            m.execute(f"bossbar remove {bossbar_id}")
            return

        if elapsed > TOTAL_TIME:
            title_subtitle("💀 Time Over!", f"{label} ×")
            m.execute(f"kill {m.player_name()}")
            m.execute(f"bossbar remove {bossbar_id}")
            return

        time.sleep(0.1)

def main():
    with EventQueue() as eq:
        eq.register_key_listener()
        eq.register_mouse_listener()
        while True:
            label, func = random.choice(missions)
            run_mission(label, func, eq)
            time.sleep(2)

if __name__ == "__main__":
    main()
