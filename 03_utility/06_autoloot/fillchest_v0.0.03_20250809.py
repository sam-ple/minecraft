# Fabric 1.21.8 / Minescript 5.0b1
# Fill a chest with weighted random loot (fewer items; rarer gear is rarer)
import minescript as m
import math, random
from time import sleep

# Place a chest 3 blocks ahead of the player
x, y, z = m.player_position()
ix, iy, iz = math.floor(x) + 3, math.floor(y), math.floor(z)
m.execute(f'/setblock {ix} {iy} {iz} chest')
sleep(0.3)

# ---- Rarity weights (smaller number = rarer) ----
W_COMMON     = 12
W_UNCOMMON   = 5
W_RARE       = 2
W_LEGENDARY  = 1

def add(pool, ids, weight, max_stack=1):
    for _id in ids:
        pool.append((_id, max_stack, weight))

items = []

# Swords
add(items, [
    "minecraft:wooden_sword",
    "minecraft:stone_sword",
], W_COMMON)
add(items, [
    "minecraft:iron_sword",
    "minecraft:golden_sword",
], W_UNCOMMON)
add(items, ["minecraft:diamond_sword"], W_RARE)
add(items, ["minecraft:netherite_sword"], W_LEGENDARY)

# Armor
add(items, [
    "minecraft:leather_helmet","minecraft:leather_chestplate",
    "minecraft:leather_leggings","minecraft:leather_boots",
], W_COMMON)
add(items, [
    "minecraft:chainmail_helmet","minecraft:chainmail_chestplate",
    "minecraft:chainmail_leggings","minecraft:chainmail_boots",
    "minecraft:iron_helmet","minecraft:iron_chestplate",
    "minecraft:iron_leggings","minecraft:iron_boots",
    "minecraft:golden_helmet","minecraft:golden_chestplate",
    "minecraft:golden_leggings","minecraft:golden_boots",
], W_UNCOMMON)
add(items, [
    "minecraft:diamond_helmet","minecraft:diamond_chestplate",
    "minecraft:diamond_leggings","minecraft:diamond_boots",
    "minecraft:turtle_helmet",  # make turtle helmet relatively rare
], W_RARE)
add(items, [
    "minecraft:netherite_helmet","minecraft:netherite_chestplate",
    "minecraft:netherite_leggings","minecraft:netherite_boots",
], W_LEGENDARY)

# Shield
add(items, ["minecraft:shield"], W_UNCOMMON)

# Snowballs (stackable)
add(items, ["minecraft:snowball"], W_COMMON, max_stack=16)

# Choose only 6–12 items for the chest
available_slots = list(range(27))
num_to_place = random.randint(6, 12)

weights = [w for (_, _, w) in items]

for _ in range(num_to_place):
    if not available_slots:
        break

    slot = random.choice(available_slots)
    available_slots.remove(slot)

    # pick one item using weights
    item_id, max_stack, _w = random.choices(items, weights=weights, k=1)[0]

    # count: 1 for gear/swords/shield; 1..max_stack for snowballs
    count = 1 if max_stack == 1 else random.randint(1, max_stack)

    m.execute(f'/item replace block {ix} {iy} {iz} container.{slot} with {item_id} {count}')
    sleep(0.03)

m.echo("✅ Spawned weighted random loot (fewer items; rarer gear is rarer).")