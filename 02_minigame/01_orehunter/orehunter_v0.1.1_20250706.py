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

# === State variables ===
got = {ore: False for ore in target_ores}
lap_times = {}
prev_items = {}
start_time = 0
last_status_time = 0

# === Utility functions ===
def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def snapshot_inventory():
    inv = m.player_inventory()
    return {item.item: item.count for item in inv if item.count > 0}

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

def tellraw_message(lines):
    components = []
    for text, color in lines:
        components.append({"text": text, "color": color})
        components.append({"text": "\n"})
    if components:
        components.pop()
    json_text = {"text": "", "extra": components}
    m.execute(f'tellraw @a {json.dumps(json_text, ensure_ascii=False)}')

# === Display update functions ===
def update_actionbar():
    remaining = sum(1 for collected in got.values() if not collected)
    m.execute(f'title @a actionbar {{"text":"{remaining} ores left","color":"aqua"}}')

def update_bossbar():
    remaining = sum(1 for collected in got.values() if not collected)
    m.execute(f"bossbar set {bossbar_id} value {remaining}")

def update_scoreboard(ore_id, value):
    m.execute(f"scoreboard players set {ore_id} {scoreboard_name} {value}")

# === Initialization functions ===
def setup_scoreboard():
    m.execute(f"scoreboard objectives remove {scoreboard_name}")
    m.execute(f'scoreboard objectives add {scoreboard_name} dummy "Ore Checklist"')
    m.execute(f"scoreboard objectives setdisplay sidebar {scoreboard_name}")
    for ore in target_ores:
        ore_id = ore.split(":")[1]
        update_scoreboard(ore_id, 1)

def setup_bossbar():
    m.execute(f"bossbar remove {bossbar_id}")
    m.execute(f'bossbar add {bossbar_id} {{"text":"Ores Remaining","color":"blue"}}')
    m.execute(f"bossbar set {bossbar_id} max {len(target_ores)}")
    m.execute(f"bossbar set {bossbar_id} value {len(target_ores)}")
    m.execute(f"bossbar set {bossbar_id} players @a")
    m.execute(f"bossbar set {bossbar_id} visible true")

def update_all_displays():
    update_bossbar()
    update_actionbar()

# === Chat command listener ===
def listen_chat_commands():
    global got, lap_times, prev_items, last_status_time
    with m.EventQueue() as eq:
        eq.register_chat_listener()
        while True:
            event = eq.get()
            if event.type == m.EventType.CHAT:
                msg = event.message.lower()
                now = time.time()

                if "!reset" in msg:
                    got = {ore: False for ore in target_ores}
                    lap_times = {}
                    m.execute(f"scoreboard objectives remove {scoreboard_name}")
                    m.execute(f"bossbar remove {bossbar_id}")
                    start_game()

                elif "!status" in msg and now - last_status_time > STATUS_COOLDOWN:
                    last_status_time = now
                    print_separator()
                    tellraw_message([
                        ("Current Ore Collection Status:", "yellow"),
                        (f"Elapsed Time: {format_time(now - start_time)}", "green"),
                    ] + format_ore_list_colored())
                    print_separator()

                elif "!ping" in msg:
                    m.execute(f'tellraw @a {json.dumps({"text": "Pong!", "color": "aqua"})}')

# === Start game ===
def start_game():
    global start_time, prev_items
    print_separator()
    for count in ["3", "2", "1"]:
        title(count, "gold")
        time.sleep(1)
    title("Start!", "green")
    time.sleep(1)

    setup_scoreboard()
    setup_bossbar()
    update_all_displays()

    start_time = time.time()
    print_separator()
    tellraw_message([
        ("Start Ore Collection!", "yellow"),
        (f"Start Time: {time.strftime('%H:%M:%S', time.localtime(start_time))}", "green"),
    ])
    print_separator()
    tellraw_message(format_ore_list_colored())

    prev_items = snapshot_inventory()

# === Main loop ===
def main_loop():
    global prev_items
    while True:
        current_items = snapshot_inventory()
        for ore in target_ores:
            if not got[ore]:
                prev_count = prev_items.get(ore, 0)
                current_count = current_items.get(ore, 0)
                if current_count > prev_count:
                    got[ore] = True
                    now = time.time()
                    lap = now - start_time
                    lap_times[ore] = lap

                    ore_id = ore.split(":")[1]
                    update_scoreboard(ore_id, 0)
                    update_all_displays()

                    print_separator()
                    title_subtitle("Collected!", ore_id.replace("_", " ").title())
                    tellraw_message([
                        (f"Collected: {ore_id.replace('_', ' ').title()}", "aqua"),
                        (f"Lap Time: {format_time(lap)}", "yellow"),
                    ] + format_ore_list_colored())

                    if all(got.values()):
                        total = now - start_time
                        print_separator()
                        title("All Ores Collected!", "gold")
                        tellraw_message([
                            ("All ores collected!", "gold"),
                            (f"Total Time: {format_time(total)}", "green"),
                        ])
                        m.execute(f"bossbar set {bossbar_id} visible false")
                        print_separator()
        prev_items = current_items
        time.sleep(0.2)

# === Start threads ===
Thread(target=listen_chat_commands, daemon=True).start()
Thread(target=main_loop, daemon=True).start()
start_game()

# Keep script alive
while True:
    time.sleep(1)