# Example: Randomly Fill a Chest with Items
import minescript as m
import math
import random
from time import sleep

# Get player's current position (floating point)
x, y, z = m.player_position()

# Determine chest placement 3 blocks in front of the player
ix = math.floor(x) + 3
iy = math.floor(y)
iz = math.floor(z)

# Place a chest at the target location
m.execute(f'/setblock {ix} {iy} {iz} chest')
sleep(0.5)

# Item pool (item ID, max stack size)
items = [
    ("minecraft:iron_ingot", 64),
    ("minecraft:gold_ingot", 64),
    ("minecraft:diamond", 64),
    ("minecraft:emerald", 64),
    ("minecraft:coal", 64),
]

# Chest has 27 slots (0–26)
available_slots = list(range(27))

# Randomly fill between 10–20 slots with random items and amounts
num_items_to_place = random.randint(10, 20)

for _ in range(num_items_to_place):
    if not available_slots:
        break

    slot = random.choice(available_slots)
    available_slots.remove(slot)

    item_id, max_stack = random.choice(items)
    count = random.randint(1, max_stack)

    # Use `/item replace` to put the item into the chest
    cmd = (
        f'/item replace block {ix} {iy} {iz} container.{slot} with {item_id}'
    )
    m.execute(cmd)
    sleep(0.1)  # Brief delay to prevent overload

m.echo("✅ Random items placed into chest.")
