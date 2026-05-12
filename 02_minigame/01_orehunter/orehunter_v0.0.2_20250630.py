import minescript as m
import time

# Show Checklist with Marks
# Display a real-time checklist with `[x]` and `[ ]` indicators.
# → Players can see which ores are still uncollected.

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

m.echo("Starting ore collection!")

# Show initial ore names in chat
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

            # Show checklist with marks
            m.echo(format_ore_list())

            if all(got.values()):
                m.echo("Congratulations! You have collected all ores!")
                m.echo(format_ore_list())

    prev_items = current_items

    time.sleep(0.25)
