import minescript as m
import time

# Basic Ore Collection Check
# Detect when the player collects **diamond**, **gold**, or **iron** ingots.
# Announce each collection in the chat.

target_ores = [
    "minecraft:diamond",
    "minecraft:gold_ingot",
    "minecraft:iron_ingot",
]

got = {ore: False for ore in target_ores}

m.echo("Starting ore collection!")

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
            m.echo(f"Collected: {ore}")

            if all(got.values()):
                m.echo("Congratulations! You have collected all ores!")

    prev_items = current_items

    time.sleep(0.25)
