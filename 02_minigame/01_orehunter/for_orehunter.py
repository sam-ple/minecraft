import minescript as m

x, y, z = map(int, m.player_position())
# Teleport player facing south (yaw=0 pitch=0)
m.execute(f"/tp @p {x} {y} {z} 0 0")

# --- Give items ---
# Give iron pickaxe and coal fuel to player
m.execute("/give @p minecraft:iron_pickaxe 1")
m.execute("/give @p minecraft:coal 16")  # 16 coal

# --- Place ore blocks in front of the player ---
base_x, base_y, base_z = x, y, z + 3  # 3 blocks south

ores = [
    "minecraft:diamond_ore",
    "minecraft:gold_ore",
    "minecraft:iron_ore",
    "minecraft:copper_ore",
    "minecraft:amethyst_cluster",  # Amethyst cluster is placed one block higher
    "minecraft:emerald_ore",
    "minecraft:lapis_ore",
]

for i, ore in enumerate(ores):
    ore_x = base_x + i  # place horizontally
    place_y = base_y + 1 if ore == "minecraft:amethyst_cluster" else base_y
    m.execute(f"/setblock {ore_x} {place_y} {base_z} {ore}")

# --- Place a furnace ---
furnace_x = base_x + len(ores) + 1
furnace_y = base_y
furnace_z = base_z
m.execute(f"/setblock {furnace_x} {furnace_y} {furnace_z} minecraft:furnace[facing=south]")

# --- Place a chest and put items inside ---
chest_x = furnace_x + 1
chest_y = base_y
chest_z = base_z
m.execute(f"/setblock {chest_x} {chest_y} {chest_z} minecraft:chest[facing=south]")

chest_items = [
    "minecraft:diamond",
    "minecraft:gold_ingot",
    "minecraft:iron_ingot",
    "minecraft:copper_ingot",
    "minecraft:amethyst_shard",
    "minecraft:emerald",
    "minecraft:lapis_lazuli",
]

nbt_list = []
for slot, item_id in enumerate(chest_items):
    nbt_list.append(f'{{Slot:{slot}b,id:"{item_id}",Count:1b}}')

nbt_items = ",".join(nbt_list)
m.execute(f"/data merge block {chest_x} {chest_y} {chest_z} {{Items:[{nbt_items}]}}")

m.echo("Given iron pickaxe and fuel, placed ores, furnace, and chest with items!")
