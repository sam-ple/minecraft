import minescript as m
import math


# ==================================================
# MINECRAFT 26.2
# STAGE GENERATOR
#
# Version : v1.0.00
#
# Purpose
#   26.2対応のシンプルなステージ生成テスト
#
# Policy
#   ・Scoreboardなし
#   ・Sneak検知なし
#   ・NBT selectorなし
#   ・Sign textなし
#   ・Villager custom tradeなし
#   ・Chest NBTなし
#   ・Item Stackはコマンド形式を使用
#   ・必要最低限のCommand Blockのみ使用
#
# ==================================================


# ==================================================
# COMMAND
# ==================================================

def cmd(command):
    m.execute(command)


# ==================================================
# BASE POSITION
# ==================================================

p = m.player()
px, py, pz = p.position

x = math.floor(px)
y = math.floor(py)
z = math.floor(pz)


def pos(dx=0, dy=0, dz=0):
    return f"{x + dx} {y + dy} {z + dz}"


# ==================================================
# INITIAL SETUP
# ==================================================

cmd("gamerule spawnMonsters false")
cmd("difficulty easy")
cmd("time set night")
cmd("clear @a")

# North
cmd("tp @p ~ ~ ~ 180 0")


# ==================================================
# FLOOR
# ==================================================

cmd(
    f"fill {pos(-25,-1,-25)} "
    f"{pos(25,-1,25)} "
    f"minecraft:grass_block"
)


# ==================================================
# CLEAR AREA
# ==================================================

cmd(
    f"fill {pos(-25,0,-25)} "
    f"{pos(25,9,25)} "
    f"minecraft:air"
)

cmd(
    f"fill {pos(-25,10,-25)} "
    f"{pos(25,20,25)} "
    f"minecraft:air"
)


# ==================================================
# ARMOR STANDS
# ==================================================

# --------------------------------------------------
# Iron
# --------------------------------------------------

cmd(
    f'summon minecraft:armor_stand {pos(-14,0,-5)} '
    f'{{ShowArms:1b,NoGravity:1b,PersistenceRequired:1b,'
    f'equipment:{{'
    f'head:{{id:"minecraft:player_head",count:1}},'
    f'chest:{{id:"minecraft:iron_chestplate",count:1}},'
    f'legs:{{id:"minecraft:iron_leggings",count:1}},'
    f'feet:{{id:"minecraft:iron_boots",count:1}}'
    f'}}}}'
)


# --------------------------------------------------
# Diamond
# --------------------------------------------------

cmd(
    f'summon minecraft:armor_stand {pos(-13,0,-5)} '
    f'{{ShowArms:1b,NoGravity:1b,PersistenceRequired:1b,'
    f'equipment:{{'
    f'head:{{id:"minecraft:wither_skeleton_skull",count:1}},'
    f'chest:{{id:"minecraft:diamond_chestplate",count:1}},'
    f'legs:{{id:"minecraft:diamond_leggings",count:1}},'
    f'feet:{{id:"minecraft:diamond_boots",count:1}}'
    f'}}}}'
)


# --------------------------------------------------
# Netherite
# --------------------------------------------------

cmd(
    f'summon minecraft:armor_stand {pos(-12,0,-5)} '
    f'{{ShowArms:1b,NoGravity:1b,PersistenceRequired:1b,'
    f'equipment:{{'
    f'head:{{id:"minecraft:netherite_helmet",count:1}},'
    f'chest:{{id:"minecraft:netherite_chestplate",count:1}},'
    f'legs:{{id:"minecraft:netherite_leggings",count:1}},'
    f'feet:{{id:"minecraft:netherite_boots",count:1}}'
    f'}}}}'
)


# ==================================================
# BASIC BLOCKS
# ==================================================

cmd(f"setblock {pos(-10,0,-5)} minecraft:chiseled_bookshelf")

cmd(f"setblock {pos(-9,0,-5)} minecraft:enchanting_table")

cmd(f"setblock {pos(-8,0,-5)} minecraft:brewing_stand")

cmd(
    f"setblock {pos(-7,0,-5)} "
    f"minecraft:blast_furnace[facing=south]"
)


# ==================================================
# DOUBLE CHEST
# ==================================================

cmd(
    f"setblock {pos(-6,0,-5)} "
    f"minecraft:chest[facing=south,type=right]"
)

cmd(
    f"setblock {pos(-5,0,-5)} "
    f"minecraft:chest[facing=south,type=left]"
)


# ==================================================
# CHEST ITEMS
#
# /data merge block を使用せず
# /item replace を使用
# ==================================================

chest_x = x - 6
chest_y = y
chest_z = z - 5

items = [
    ("cobblestone", 64),
    ("iron_ingot", 64),
    ("stone_pickaxe", 1),
    ("shield", 1),
    ("bow", 1),
    ("arrow", 64),
    ("trident", 1),
    ("obsidian", 64),
    ("crying_obsidian", 64),
    ("diamond", 64),
    ("dried_ghast", 1),
    ("sniffer_egg", 1),
    ("wheat_seeds", 64),
    ("blaze_rod", 64),
    ("dragon_egg", 1),
    ("dragon_breath", 64),
    ("elytra", 1),
    ("pumpkin", 64),
]


for slot, (item, count) in enumerate(items):

    cmd(
        f"item replace block "
        f"{chest_x} {chest_y} {chest_z} "
        f"container.{slot} "
        f"with minecraft:{item} {count}"
    )


# ==================================================
# BED
# ==================================================

cmd(
    f"setblock {pos(-4,0,-5)} "
    f"minecraft:red_bed[facing=south,part=foot]"
)

cmd(
    f"setblock {pos(-4,0,-4)} "
    f"minecraft:red_bed[facing=south,part=head]"
)


# ==================================================
# VILLAGER
#
# Custom tradeは一旦使用しない
# ==================================================

cmd(
    f"summon minecraft:villager "
    f"{pos(-3,0,-5)} "
    f'{{Silent:1b,Invulnerable:1b,NoAI:1b}}'
)


# ==================================================
# SKELETON
# ==================================================

cmd(
    f'summon minecraft:skeleton {pos(-2,0,-5)} '
    f'{{NoAI:1b,PersistenceRequired:1b,Health:2.0f,Rotation:[0f,0f]}}'
)


# ==================================================
# SIGN
#
# 26.2ではSign textの設定を行わない
# ==================================================

cmd(
    f"setblock {pos(-1,0,-5)} minecraft:oak_sign"
)


# ==================================================
# CRAFTING TABLE
# ==================================================

cmd(
    f"setblock {pos(0,0,-5)} minecraft:crafting_table"
)


# ==================================================
# ANIMALS
# ==================================================

cmd(
    f'summon minecraft:parrot {pos(1,0,-5)} '
    f'{{NoAI:1b,Silent:1b,Rotation:[0f,0f]}}'
)

cmd(
    f'summon minecraft:armadillo {pos(2,0,-5)} '
    f'{{NoAI:1b,Silent:1b}}'
)

cmd(
    f'summon minecraft:allay {pos(3,0,-5)} '
    f'{{Silent:1b,NoGravity:1b,PersistenceRequired:1b}}'
)


# ==================================================
# GOLD BLOCK GIMMICK
#
# 金ブロックを踏んだプレイヤーの足元に
# suspicious_sandを出す
#
# Command Blockは使用
# ==================================================

cmd(
    f"setblock {pos(10,-1,-5)} minecraft:gold_block"
)


gold_command = (
    f"execute as @a at @s "
    f"if block ~ ~-1 ~ minecraft:gold_block "
    f"run setblock {pos(10,0,-7)} minecraft:suspicious_sand"
)


cmd(
    f'setblock {pos(10,-2,-5)} '
    f'minecraft:repeating_command_block'
)


cmd(
    f'data merge block {pos(10,-2,-5)} '
    f'{{auto:1b,Command:"{gold_command}"}}'
)


# ==================================================
# TP DEVICE
#
# ボタン
# ↓
# Command Block
# ==================================================

cmd(
    f"setblock {pos(11,0,-5)} minecraft:stone"
)

cmd(
    f"setblock {pos(11,0,-4)} "
    f"minecraft:stone_button[facing=south]"
)


tp_command = (
    f"tp @p {pos(0,1,0)}"
)


cmd(
    f"setblock {pos(11,-1,-5)} minecraft:command_block"
)


cmd(
    f'data merge block {pos(11,-1,-5)} '
    f'{{Command:"{tp_command}"}}'
)


# ==================================================
# WATER
# ==================================================

cmd(
    f"fill {pos(-5,-1,0)} "
    f"{pos(-2,-1,1)} "
    f"minecraft:water"
)


# ==================================================
# LAVA
# ==================================================

cmd(
    f"fill {pos(2,-1,0)} "
    f"{pos(2,-1,1)} "
    f"minecraft:lava"
)


# ==================================================
# WATER ANIMALS
# ==================================================

cmd(
    f'summon minecraft:axolotl {pos(-3,-1,0)} '
    f'{{NoAI:1b}}'
)

cmd(
    f'summon minecraft:tadpole {pos(-5,-1,1)} '
    f'{{NoAI:1b}}'
)


# ==================================================
# NETHER PORTAL FRAME
# ==================================================

BASE_X = 5
BASE_Y = -1
BASE_Z = -5


for dy in range(5):

    for dx in range(4):

        if dx in [0, 3] or dy in [0, 4]:

            block = "minecraft:obsidian"

        else:

            block = "minecraft:air"

        cmd(
            f"setblock "
            f"{pos(BASE_X + dx, BASE_Y + dy, BASE_Z)} "
            f"{block}"
        )


# --------------------------------------------------
# Fire
# --------------------------------------------------

cmd(
    f"setblock "
    f"{pos(BASE_X + 1, BASE_Y + 1, BASE_Z)} "
    f"minecraft:fire"
)


# ==================================================
# PLAYER ITEMS
#
# Scoreboard / NBT selectorは使わない
# ==================================================

items = [

    'minecraft:fishing_rod[enchantments={"minecraft:luck_of_the_sea":3,"minecraft:lure":3,"minecraft:unbreaking":3,"minecraft:mending":1}] 1',

    "minecraft:emerald 64",
    "minecraft:bone 64",
    "minecraft:glow_ink_sac 64",
    "minecraft:copper_ingot 64",
    "minecraft:feather 64",
    "minecraft:stick 64",
    "minecraft:suspicious_sand 64",
    "minecraft:compass 1",
]


for item in items:

    cmd(
        f"give @a {item}"
    )


# ==================================================
# WOLF VARIANTS
# ==================================================

WOLF_VARIANTS = [

    "pale",
    "woods",
    "ashen",
    "black",
    "chestnut",
    "rusty",
    "spotted",
    "striped",
    "snowy",
    "classic",
    "big",
    "grumpy",

]


base_x = -11
z_line = -10


for i, variant in enumerate(WOLF_VARIANTS):

    cmd(
        f'summon minecraft:wolf '
        f'{pos(base_x + i,0,z_line)} '
        f'{{NoAI:1b,Sitting:1b,Silent:1b,'
        f'variant:"minecraft:{variant}"}}'
    )


# ==================================================
# WOLF CHEST
# ==================================================

cmd(
    f"setblock {pos(-12,0,-10)} "
    f"minecraft:chest[facing=south]"
)


for slot in range(8):

    cmd(
        f"item replace block "
        f"{pos(-12,0,-10)} "
        f"container.{slot} "
        f"with minecraft:bone 64"
    )


# ==================================================
# CAT VARIANTS
# ==================================================

CAT_VARIANTS = [

    "tabby",
    "black",
    "red",
    "siamese",
    "british_shorthair",
    "calico",
    "persian",
    "ragdoll",
    "white",
    "jellie",
    "all_black",

]


base_x = -11
z_line = -14


for i, variant in enumerate(CAT_VARIANTS):

    cmd(
        f'summon minecraft:cat '
        f'{pos(base_x + i,0,z_line)} '
        f'{{NoAI:1b,Sitting:1b,Silent:1b,'
        f'variant:"minecraft:{variant}"}}'
    )


# ==================================================
# CAT CHEST
# ==================================================

cmd(
    f"setblock {pos(-12,0,-14)} "
    f"minecraft:chest[facing=south]"
)


cat_items = [

    ("cod", 64),
    ("cod", 64),
    ("salmon", 64),
    ("salmon", 64),

]


for slot, (item, count) in enumerate(cat_items):

    cmd(
        f"item replace block "
        f"{pos(-12,0,-14)} "
        f"container.{slot} "
        f"with minecraft:{item} {count}"
    )


# ==================================================
# FROG VARIANTS
# ==================================================

FROG_VARIANTS = [

    "temperate",
    "warm",
    "cold",

]


base_x = -11
z_line = -18


for i, variant in enumerate(FROG_VARIANTS):

    cmd(
        f'summon minecraft:frog '
        f'{pos(base_x + i,0,z_line)} '
        f'{{NoAI:1b,Silent:1b,'
        f'variant:"minecraft:{variant}"}}'
    )


# ==================================================
# FROG CHEST
# ==================================================

cmd(
    f"setblock {pos(-12,0,-18)} "
    f"minecraft:chest[facing=south]"
)


for slot in range(3):

    cmd(
        f"item replace block "
        f"{pos(-12,0,-18)} "
        f"container.{slot} "
        f"with minecraft:lead 64"
    )


# ==================================================
# COMPLETE
# ==================================================

print("==============================================")
print(" Minecraft 26.2 Stage Generator")
print(" COMPLETE")
print("==============================================")