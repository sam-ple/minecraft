import minescript as m
import time
import json
from threading import Thread

# === Settings ===
target_ores = [
    "minecraft:diamond",
    "minecraft:gold_ingot",
    "minecraft:iron_ingot",
    "minecraft:copper_ingot",
    "minecraft:amethyst_shard",
    "minecraft:emerald",
    "minecraft:lapis_lazuli",
]
scoreboard_name = "ores_left"
bossbar_id = "orehunt:remaining"
STATUS_COOLDOWN = 5  # seconds

# === State Variables ===
got = {ore: False for ore in target_ores}
lap_times = {}
prev_items = {}
start_time = 0
last_status_time = 0
is_running = False

# === Utility ===
def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def snapshot_inventory():
    inv = m.player_inventory()
    return {item.item: item.count for item in inv if item.count > 0}

def tellraw(lines):
    components = []
    for text, color in lines:
        components.append({"text": text, "color": color})
        components.append({"text": "\n"})
    if components:
        components.pop()
    msg = {"text": "", "extra": components}
    m.execute(f"tellraw @a {json.dumps(msg, ensure_ascii=False)}")

def print_separator():
    m.execute('tellraw @a {"text":"----------","color":"gray"}')

def title(text, color="white"):
    m.execute(f'title @a title {{"text":"{text}","color":"{color}","bold":true}}')

def title_subtitle(title_text, subtitle_text, title_color="gold", subtitle_color="aqua"):
    m.execute(f'title @a title {{"text":"{title_text}","color":"{title_color}","bold":true}}')
    m.execute(f'title @a subtitle {{"text":"{subtitle_text}","color":"{subtitle_color}"}}')

def format_ore_list_colored():
    lines = []
    for ore in target_ores:
        ore_name = ore.split(":")[1].replace("_", " ").title()
        color = "green" if got[ore] else "red"
        prefix = "[x]" if got[ore] else "[ ]"
        lines.append((f"{prefix} {ore_name}", color))
    return lines

# === Scoreboard & Bossbar ===
def setup_scoreboard():
    m.execute(f"scoreboard objectives remove {scoreboard_name}")
    m.execute(f'scoreboard objectives add {scoreboard_name} dummy "Ore Checklist"')
    m.execute(f"scoreboard objectives setdisplay sidebar {scoreboard_name}")
    for ore in target_ores:
        ore_id = ore.split(":")[1]
        m.execute(f"scoreboard players set {ore_id} {scoreboard_name} 1")

def update_scoreboard(ore_id, value):
    m.execute(f"scoreboard players set {ore_id} {scoreboard_name} {value}")

def setup_bossbar():
    m.execute(f"bossbar remove {bossbar_id}")
    m.execute(f'bossbar add {bossbar_id} {{"text":"Ores Remaining: {len(target_ores)}","color":"red"}}')
    m.execute(f"bossbar set {bossbar_id} max {len(target_ores)}")
    m.execute(f"bossbar set {bossbar_id} value {len(target_ores)}")
    m.execute(f"bossbar set {bossbar_id} players @a")
    m.execute(f"bossbar set {bossbar_id} visible true")

def update_bossbar():
    remaining = sum(1 for collected in got.values() if not collected)
    color = "red" if remaining >= 5 else "yellow" if remaining >= 2 else "blue"
    m.execute(f'bossbar set {bossbar_id} name {{"text":"Ores Remaining: {remaining}","color":"{color}"}}')
    m.execute(f"bossbar set {bossbar_id} value {remaining}")
    m.execute(f"bossbar set {bossbar_id} color {color}")

def update_actionbar():
    remaining = sum(1 for collected in got.values() if not collected)
    m.execute(f'title @a actionbar {{"text":"Ores Left: {remaining}","color":"aqua"}}')

def update_all_displays():
    update_bossbar()
    update_actionbar()

# === Game Control ===
def start_game():
    global start_time, prev_items, is_running
    is_running = True
    print_separator()
    for countdown in ["3", "2", "1"]:
        title(countdown, "gold")
        time.sleep(1)
    title("Start!", "green")
    time.sleep(1)

    setup_scoreboard()
    setup_bossbar()
    update_all_displays()

    start_time = time.time()
    print_separator()
    tellraw([
        ("Ore Collection Started!", "yellow"),
        (f"Start Time: {time.strftime('%H:%M:%S', time.localtime(start_time))}", "green"),
    ])
    print_separator()
    tellraw(format_ore_list_colored())

    prev_items = snapshot_inventory()

def reset_game():
    global is_running, got, lap_times, prev_items
    is_running = False
    got = {ore: False for ore in target_ores}
    lap_times.clear()
    prev_items.clear()
    m.execute(f"scoreboard objectives remove {scoreboard_name}")
    m.execute(f"bossbar remove {bossbar_id}")
    print_separator()
    tellraw([("Game has been reset.", "red")])
    print_separator()

def show_status():
    now = time.time()
    print_separator()
    tellraw([
        ("Ore Collection Status:", "yellow"),
        (f"Elapsed Time: {format_time(now - start_time)}", "green"),
    ] + format_ore_list_colored())
    print_separator()

# === Chat Command Listener ===
def listen_chat_commands():
    global is_running, last_status_time
    with m.EventQueue() as eq:
        eq.register_chat_listener()
        while True:
            event = eq.get()
            if event.type == m.EventType.CHAT:
                msg = event.message.strip().lower()

                # プレイヤー名が含まれていれば除去（例: "<playername> --start" → "--start"）
                if msg.startswith("<") and ">" in msg:
                    msg = msg.split(">", 1)[1].strip()

                now = time.time()

                if msg == "--start" and not is_running:
                    start_game()
                elif msg == "--reset":
                    reset_game()
                elif msg == "--status" and is_running:
                    if now - last_status_time > STATUS_COOLDOWN:
                        show_status()
                        last_status_time = now
                elif msg == "--help":
                    print_separator()
                    tellraw([
                        ("Ore Hunt Game Commands:", "yellow"),
                        ("--start", "aqua"),
                        ("    Starts the ore collection game.", "gray"),
                        ("--reset", "aqua"),
                        ("    Resets the game state and clears progress.", "gray"),
                        ("--status", "aqua"),
                        ("    Shows current progress and elapsed time.", "gray"),
                        ("--help", "aqua"),
                        ("    Displays this help message.", "gray"),
                    ])
                    print_separator()

# === Main Loop ===
def main_loop():
    global prev_items, is_running
    while True:
        if not is_running:
            time.sleep(0.2)
            continue

        current_items = snapshot_inventory()
        for ore in target_ores:
            if not got[ore]:
                prev_count = prev_items.get(ore, 0)
                curr_count = current_items.get(ore, 0)
                if curr_count > prev_count:
                    got[ore] = True
                    lap = time.time() - start_time
                    ore_id = ore.split(":")[1]
                    update_scoreboard(ore_id, 0)
                    update_all_displays()

                    print_separator()
                    title_subtitle("Collected!", ore_id.replace("_", " ").title())
                    tellraw([
                        (f"Collected: {ore_id.replace('_', ' ').title()}", "aqua"),
                        (f"Lap Time: {format_time(lap)}", "yellow"),
                    ] + format_ore_list_colored())

                    if all(got.values()):
                        total = time.time() - start_time
                        print_separator()
                        title("All Ores Collected!", "gold")
                        tellraw([
                            ("All ores collected!", "gold"),
                            (f"Total Time: {format_time(total)}", "green"),
                        ])
                        m.execute(f"bossbar set {bossbar_id} visible false")
                        is_running = False
                        print_separator()
        prev_items = current_items
        time.sleep(0.2)

# === Startup Message ===
print_separator()
tellraw([
    ("Type --start to begin the Ore Collection Game.", "aqua"),
    ("Type --help for command instructions.", "gray")
])
print_separator()

# === Threads Start ===
Thread(target=listen_chat_commands, daemon=True).start()
Thread(target=main_loop, daemon=True).start()

# Main thread hold
while True:
    time.sleep(1)
