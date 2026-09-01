# ============================================================
# ORERACE TEST GENERATOR
# Version : v0.1.00
#
# Minecraft Java Edition + MineScript
#
# Features
#   ・Diamond Pickaxe give
#   ・Random ore generation around player
#   ・8 ore types
#   ・Normal + Deepslate
#   ・Random amount
#
# Command
#   /orerace_test
#
# ============================================================

import minescript as m
import random
import math


# ============================================================
# CONFIG
# ============================================================

RADIUS = 30

MIN_ORE = 20
MAX_ORE = 40

MIN_Y_OFFSET = -5
MAX_Y_OFFSET = 5


ORES = [

    # normal
    "minecraft:coal_ore",
    "minecraft:copper_ore",
    "minecraft:iron_ore",
    "minecraft:gold_ore",
    "minecraft:redstone_ore",
    "minecraft:lapis_ore",
    "minecraft:emerald_ore",
    "minecraft:diamond_ore",

    # deepslate
    "minecraft:deepslate_coal_ore",
    "minecraft:deepslate_copper_ore",
    "minecraft:deepslate_iron_ore",
    "minecraft:deepslate_gold_ore",
    "minecraft:deepslate_redstone_ore",
    "minecraft:deepslate_lapis_ore",
    "minecraft:deepslate_emerald_ore",
    "minecraft:deepslate_diamond_ore"
]


# ============================================================
# COMMAND
# ============================================================

def cmd(command):

    m.execute(command)


# ============================================================
# PLAYER POSITION
# ============================================================

player = m.player()

px, py, pz = player.position

x0 = math.floor(px)
y0 = math.floor(py)
z0 = math.floor(pz)


# ============================================================
# GIVE DIAMOND PICKAXE
# ============================================================

cmd(
    "give @s minecraft:diamond_pickaxe"
)


# ============================================================
# GENERATE ORES
# ============================================================

total = 0


for ore in ORES:

    amount = random.randint(
        MIN_ORE,
        MAX_ORE
    )

    for i in range(amount):

        # ----------------------------------------------------
        # Random position
        # ----------------------------------------------------

        x = x0 + random.randint(
            -RADIUS,
            RADIUS
        )

        z = z0 + random.randint(
            -RADIUS,
            RADIUS
        )

        y = y0 + random.randint(
            MIN_Y_OFFSET,
            MAX_Y_OFFSET
        )

        # ----------------------------------------------------
        # Distance check
        # ----------------------------------------------------

        dx = x - x0
        dz = z - z0

        if dx * dx + dz * dz > RADIUS * RADIUS:

            continue

        # ----------------------------------------------------
        # Place ore
        # ----------------------------------------------------

        cmd(
            f"setblock {x} {y} {z} {ore}"
        )

        total += 1


# ============================================================
# MESSAGE
# ============================================================

cmd(
    'tellraw @s {"text":"OreRace test ores generated!","color":"green"}'
)

cmd(
    f'tellraw @s {{"text":"Total ores: {total}","color":"yellow"}}'
)

cmd(
    f'tellraw @s {{"text":"Area: radius {RADIUS}","color":"gray"}}'
)