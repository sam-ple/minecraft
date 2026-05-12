import minescript as m
import time
import json

# Colored Chat Output & Separator Lines
# Enhance chat messages using `tellraw` with **colors** and **line separators**.
# → More visual clarity and feedback for each update.


target_ores = [
    "minecraft:diamond",
    "minecraft:gold_ingot",
    "minecraft:iron_ingot",
]

got = {ore: False for ore in target_ores}

def format_ore_list_colored():
    lines = []
    for ore in target_ores:
        ore_name = ore.split(":")[1]
        if got[ore]:
            lines.append((f"[x] {ore_name}", "green"))
        else:
            lines.append((f"[ ] {ore_name}", "red"))
    return lines

def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

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

def print_separator():
    sep = "----------"
    m.execute(f'tellraw @a {{"text":"{sep}","color":"gray"}}')

start_time = time.time()

print_separator()
tellraw_message([
    ("Starting ore collection!", "yellow"),
    (f"Start time: {time.strftime('%H:%M:%S', time.localtime(start_time))}", "green"),
])
print_separator()

tellraw_message(format_ore_list_colored())

def snapshot_inventory():
    inv = m.player_inventory()
    return {item.item: item.count for item in inv if item.count > 0}

prev_items = snapshot_inventory()

while True:
    current_items = snapshot_inventory()

    for ore in target_ores:
        prev_count = prev_items.get(ore, 0)
        current_count = current_items.get(ore, 0)

        if current_count > prev_count and not got[ore]:
            got[ore] = True
            print_separator()
            tellraw_message([
                (f"Collected: {ore.split(':')[1]}", "aqua"),
            ] + format_ore_list_colored())

            if all(got.values()):
                end_time = time.time()
                elapsed = end_time - start_time
                print_separator()
                tellraw_message([
                    ("Congratulations! You have collected all ores!", "gold"),
                ] + format_ore_list_colored() + [
                    (f"End time: {time.strftime('%H:%M:%S', time.localtime(end_time))}", "green"),
                    (f"Elapsed time: {format_time(elapsed)}", "green"),
                ])
                print_separator()
                exit()

    prev_items = current_items
    time.sleep(0.25)
