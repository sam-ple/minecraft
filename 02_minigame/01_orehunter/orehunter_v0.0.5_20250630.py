import minescript as m
import time
import json
from threading import Thread

# Intermediate Version with Lap Times and Titles
# Track multiple ores with individual **lap times** and display progress using **titles** and **colored checklists**.
# This step focuses on improving feedback and clarity, but UI elements like bossbars and scoreboards are not yet included.


# Target ores
target_ores = [
    "minecraft:diamond",
    "minecraft:gold_ingot",
    "minecraft:iron_ingot",
    "minecraft:copper_ingot",
    "minecraft:amethyst_shard",
    "minecraft:emerald",
    "minecraft:lapis_lazuli",
]

got = {ore: False for ore in target_ores}
lap_times = {}

# Format checklist with colors
def format_ore_list_colored():
    lines = []
    for ore in target_ores:
        ore_name = ore.split(":")[1].replace("_", " ").title()
        if got[ore]:
            lines.append((f"[x] {ore_name}", "green"))
        else:
            lines.append((f"[ ] {ore_name}", "red"))
    return lines

# Format time as mm:ss
def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

# Display multiline tellraw message
def tellraw_message(lines):
    components = []
    for text, color in lines:
        components.append({"text": text, "color": color})
        components.append({"text": "\n"})
    if components:
        components.pop()
    json_text = {"text": "", "extra": components}
    json_str = json.dumps(json_text, ensure_ascii=False)
    m.execute(f'tellraw @a {json_str}')

# Print visual separator
def print_separator():
    m.execute('tellraw @a {"text":"----------","color":"gray"}')

# Show title
def title(text, color="white"):
    m.execute(f'title @a title {{"text":"{text}","color":"{color}","bold":true}}')

# Listen for "reset" in chat (runs in separate thread)
def listen_reset():
    global got, lap_times, start_time, prev_items
    with m.EventQueue() as eq:
        eq.register_chat_listener()
        while True:
            event = eq.get()  # Fixed: use get() instead of poll()
            if event.type == m.EventType.CHAT:
                if "reset" in event.message.lower():
                    got = {ore: False for ore in target_ores}
                    lap_times = {}
                    start_game()
                    break

# Start game with countdown and checklist
def start_game():
    global start_time, prev_items
    print_separator()
    for i in ["3", "2", "1"]:
        title(i, "gold")
        time.sleep(1)
    title("Start!", "green")
    time.sleep(1)
    start_time = time.time()
    print_separator()
    tellraw_message([
        ("Start Ore Collection!", "yellow"),
        (f"Start Time: {time.strftime('%H:%M:%S', time.localtime(start_time))}", "green"),
    ])
    print_separator()
    tellraw_message(format_ore_list_colored())
    prev_items = snapshot_inventory()

# Snapshot current inventory
def snapshot_inventory():
    inv = m.player_inventory()
    return {item.item: item.count for item in inv if item.count > 0}

# Main game loop: track ore collection and show lap times
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

                    ore_name = ore.split(":")[1].replace("_", " ").title()
                    print_separator()
                    title(f"Collected: {ore_name}", "aqua")
                    tellraw_message([
                        (f"Collected: {ore_name}", "aqua"),
                        (f"Lap Time: {format_time(lap)}", "yellow"),
                    ] + format_ore_list_colored())

                    if all(got.values()):
                        end = time.time()
                        total = end - start_time
                        print_separator()
                        title("All Ores Collected!", "gold")
                        tellraw_message([
                            ("All ores collected!", "gold"),
                            (f"Total Time: {format_time(total)}", "green"),
                        ])
                        print_separator()
        prev_items = current_items
        time.sleep(0.2)

# Startup
Thread(target=listen_reset).start()
start_game()
main_loop()
