# Face SOUTH (+Z direction) before running this script

import minescript as m
import math

# Get player's position using floor
px, py, pz = m.player().position
x = math.floor(px)
y = math.floor(py)
z = math.floor(pz)

# Base position:
# Shulker box will be placed one block in front of player
base_x = x
base_y = y
base_z = z + 5


# -------------------------
# Layer 1 (Bottom Layer)
# -------------------------

# Place shulker box (front center)
color = "black"
# white / orange / magenta / light_blue / yellow / lime / pink / gray / light_gray / cyan / purple / blue / brown / green / red / black
m.execute(f"/setblock {base_x} {base_y} {base_z} minecraft:{color}_shulker_box")

# Hoppers feeding into shulker
m.execute(f"/setblock {base_x} {base_y} {base_z+1} minecraft:hopper[facing=north]")
m.execute(f"/setblock {base_x+1} {base_y} {base_z+1} minecraft:hopper[facing=west]")
m.execute(f"/setblock {base_x-1} {base_y} {base_z+1} minecraft:hopper[facing=east]")
m.execute(f"/setblock {base_x} {base_y} {base_z+2} minecraft:hopper[facing=north]")


# -------------------------
# Layer 2 (Middle Furnaces)
# -------------------------

# Place 3 blast furnaces facing the player (south)
m.execute(f"/setblock {base_x+1} {base_y+1} {base_z+1} minecraft:blast_furnace[facing=north]")
m.execute(f"/setblock {base_x} {base_y+1} {base_z+1} minecraft:blast_furnace[facing=north]")
m.execute(f"/setblock {base_x-1} {base_y+1} {base_z+1} minecraft:blast_furnace[facing=north]")

# Hopper receiving items from top furnace
m.execute(f"/setblock {base_x} {base_y+1} {base_z+2} minecraft:hopper")

# -------------------------
# Layer 3 (Top Furnace)
# -------------------------

# Place the fourth blast furnace
m.execute(f"/setblock {base_x} {base_y+2} {base_z+2} minecraft:blast_furnace[facing=north]")


m.echo(f"4-blast-furnace system built at base {base_x} {base_y} {base_z}")
