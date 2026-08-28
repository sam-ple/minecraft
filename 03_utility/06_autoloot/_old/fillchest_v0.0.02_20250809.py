# Fill a chest with random swords/armor/shield/snowballs (uniform random)
import minescript as m
import math
import random
from time import sleep

# Player position → place a chest 3 blocks ahead
x, y, z = m.player_position()
ix, iy, iz = math.floor(x) + 3, math.floor(y), math.floor(z)

m.execute(f'/setblock {ix} {iy} {iz} chest')
sleep(0.5)

# ===== Item pool =====
SWORDS = [
    "minecraft:wooden_sword",
    "minecraft:stone_sword",
    "minecraft:iron_sword",
    "minecraft:golden_sword",
    "minecraft:diamond_sword",
    "minecraft:netherite_sword",
]

ARMOR = [
    # Leather
    "minecraft:leather_helmet", "minecraft:leather_chestplate",
    "minecraft:leather_leggings", "minecraft:leather_boots",
    # Chain
    "minecraft:chainmail_helmet", "minecraft:chainmail_chestplate",
    "minecraft:chainmail_leggings", "minecraft:chainmail_boots",
    # Iron
    "minecraft:iron_helmet", "minecraft:iron_chestplate",
    "minecraft:iron_leggings", "minecraft:iron_boots",
    # Gold
    "minecraft:golden_helmet", "minecraft:golden_chestplate",
    "minecraft:golden_leggings", "minecraft:golden_boots",
    # Diamond
    "minecraft:diamond_helmet", "minecraft:diamond_chestplate",
    "minecraft:diamond_leggings", "minecraft:diamond_boots",
    # Netherite
    "minecraft:netherite_helmet", "minecraft:netherite_chestplate",
    "minecraft:netherite_leggings", "minecraft:netherite_boots",
    # Special
    "minecraft:turtle_helmet",
]

SHIELD = ["minecraft:shield"]
SNOWBALL = [("minecraft:snowball", 16)]  # (id, max_stack)

# Normalize to (item_id, max_stack); swords/armor/shield are stack 1
items: list[tuple[str, int]] = []
items += [(i, 1) for i in SWORDS]
items += [(i, 1) for i in ARMOR]
items += [(i, 1) for i in SHIELD]
items += SNOWBALL  # only snowballs stack to 16

# Fill 10–20 random chest slots (0..26)
available_slots = list(range(27))
num_items_to_place = random.randint(10, 20)

for _ in range(num_items_to_place):
    if not available_slots:
        break

    slot = random.choice(available_slots)
    available_slots.remove(slot)

    item_id, max_stack = random.choice(items)
    count = 1 if max_stack == 1 else random.randint(1, max_stack)

    # count is appended at the end (1.20.5+ /item replace syntax)
    cmd = f'/item replace block {ix} {iy} {iz} container.{slot} with {item_id} {count}'
    m.execute(cmd)
    sleep(0.05)

m.echo("✅ Placed random swords/armor/shield/snowballs into the chest.")