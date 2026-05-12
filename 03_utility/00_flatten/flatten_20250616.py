
from sys import argv
from minescript import execute, echo, player_position

# -------------------------
# Argument handling (with type checking)
# -------------------------
arg1 = argv[1] if len(argv) > 1 and argv[1].strip() else "quartz_block"
arg2 = argv[2] if len(argv) > 2 and argv[2].strip() else "10"
arg3 = argv[3] if len(argv) > 3 and argv[3].strip() else "1"

# Translate shorthand block names
if arg1 == "gol":
    block_type = "gold_block"
elif arg1 == "qua":
    block_type = "quartz_block"
elif arg1 == "eme":
    block_type = "emerald_block"
else:
    block_type = arg1

# Convert dimensions with error handling
try:
    width = max(1, int(arg2))    # Width must be at least 1
    height = max(0, int(arg3))   # Height must be 0 or more
except ValueError:
    echo("Invalid number input. Using default values.")
    width = 10
    height = 1

# -------------------------
# Get player position (rounded to nearest block)
# -------------------------
x, y, z = [round(coord) for coord in player_position()]

# -------------------------
# Terrain leveling
# -------------------------
half = width // 2
for dx in range(-half, width - half):
    for dz in range(-half, width - half):
        for dy in range(-1, height + 1):  # From ground level to above
            bx, by, bz = x + dx, y + dy, z + dz
            if dy == -1:
                execute(f"setblock {bx} {by} {bz} minecraft:{block_type}")
            else:
                execute(f"setblock {bx} {by} {bz} minecraft:air")

# -------------------------
# Completion message
# -------------------------
echo(f"Leveled the area with {block_type}.")
execute('/tellraw @a {"text":"Done leveling!","color":"aqua"}')
