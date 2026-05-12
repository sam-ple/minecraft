import minescript as m
import time

# Add Timer for Start and Completion
# Track start time and show **elapsed time** once all ores are collected.
# → Time appears in chat when the game ends.

target_ores = [
    "minecraft:diamond",
    "minecraft:gold_ingot",
    "minecraft:iron_ingot",
]

got = {ore: False for ore in target_ores}

def format_ore_list():
    lines = []
    for ore in target_ores:
        mark = "[x]" if got[ore] else "[ ]"
        ore_name = ore.split(":")[1]
        lines.append(f"{mark} {ore_name}")
    return "\n".join(lines)

def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

m.echo("Starting ore collection!")

start_time = time.time()
m.echo(f"Start time: {time.strftime('%H:%M:%S', time.localtime(start_time))}")

# Show initial ore list in chat
m.echo("\n".join(ore.split(":")[1] for ore in target_ores))

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
            m.echo(f"Collected: {ore.split(':')[1]}")

            m.echo(format_ore_list())

            if all(got.values()):
                end_time = time.time()
                elapsed = end_time - start_time
                m.echo("Congratulations! You have collected all ores!")
                m.echo(format_ore_list())
                m.echo(f"End time: {time.strftime('%H:%M:%S', time.localtime(end_time))}")
                m.echo(f"Elapsed time: {format_time(elapsed)}")
                exit()  # end script

    prev_items = current_items

    time.sleep(0.25)
