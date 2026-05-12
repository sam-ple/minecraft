# ============================================================
# WEREWOLF COMBAT SYSTEM
# Version : v0.0.01
# Date : 2026-05-08
# ============================================================

import minescript as m
from minescript import EventQueue
import sys
from queue import Empty

# ============================================================
# SETTINGS
# ============================================================

TICK = 0.05

# ============================================================
# UTIL
# ============================================================

def cmd(c):
    m.execute(c)

def chat(msg,color="yellow"):

    cmd(
        f'tellraw @a {{"text":"{msg}","color":"{color}"}}'
    )

# ============================================================
# SAFE REMOVE OBJECTIVE
# ============================================================

def remove_objective(name):

    cmd(
        f'execute if entity @a run scoreboard objectives remove {name}'
    )

# ============================================================
# RESET
# ============================================================

def reset_game():

    remove_objective("dead")
    remove_objective("triHit")
    remove_objective("roleCheck")

    cmd("tag @a remove dead")
    cmd("tag @a remove tri1")
    cmd("tag @a remove wolf")
    cmd("tag @a remove villager")
    cmd("tag @a remove vampire")

    cmd("gamemode survival @a")

    cmd("effect clear @a")

    chat("RESET COMPLETE","red")

# ============================================================
# SET ROLE
# ============================================================

def set_roles():

    cmd("tag @a remove wolf")
    cmd("tag @a remove villager")

    cmd("tag crocadooo add wolf")
    cmd("tag saaample add villager")

    chat("ROLE SET COMPLETE","green")

# ============================================================
# START
# ============================================================

def start_game():

    cmd("scoreboard objectives add dead dummy")
    cmd("scoreboard objectives add triHit dummy")

    cmd(
        "scoreboard objectives add roleCheck minecraft.used:minecraft.carrot_on_a_stick"
    )

    chat("WEREWOLF SYSTEM START","gold")

# ============================================================
# ARG
# ============================================================

if len(sys.argv) >= 2:

    if sys.argv[1] == "reset":

        reset_game()
        sys.exit()

    if sys.argv[1] == "set":

        set_roles()
        sys.exit()

    if sys.argv[1] == "start":

        start_game()

# ============================================================
# MAIN LOOP
# ============================================================

eq = EventQueue()

while True:

    try:
        eq.get(timeout=TICK)

    except Empty:
        pass

    # ========================================================
    # SNOWBALL
    # ========================================================

    cmd(
        'execute if entity @e[type=snowball,tag=!hit] '
        'as @e[type=snowball,tag=!hit] '
        'at @s '
        'if entity @a[distance=..1.5,gamemode=!spectator,tag=!dead] '
        'run effect give @a[distance=..1.5,gamemode=!spectator,tag=!dead,limit=1,sort=nearest] minecraft:darkness 3 0 true'
    )

    cmd(
        'execute if entity @e[type=snowball,tag=!hit] '
        'as @e[type=snowball,tag=!hit] '
        'at @s '
        'if entity @a[distance=..1.5,gamemode=!spectator,tag=!dead] '
        'run effect give @a[distance=..1.5,gamemode=!spectator,tag=!dead,limit=1,sort=nearest] minecraft:slowness 3 255 true'
    )

    cmd(
        'execute if entity @e[type=snowball,tag=!hit] '
        'as @e[type=snowball,tag=!hit] '
        'at @s '
        'if entity @a[distance=..1.5,gamemode=!spectator,tag=!dead] '
        'run effect give @a[distance=..1.5,gamemode=!spectator,tag=!dead,limit=1,sort=nearest] minecraft:jump_boost 3 250 true'
    )

    cmd(
        'execute if entity @e[type=snowball,tag=!hit] '
        'as @e[type=snowball,tag=!hit] '
        'at @s '
        'if entity @a[distance=..1.5,gamemode=!spectator,tag=!dead] '
        'run tag @s add hit'
    )

    # ========================================================
    # ARROW
    # ========================================================

    cmd(
        'execute if entity @e[type=arrow,tag=!hit] '
        'as @e[type=arrow,tag=!hit] '
        'at @s '
        'if entity @a[distance=..1.2,gamemode=!spectator,tag=!dead] '
        'run tag @a[distance=..1.2,gamemode=!spectator,tag=!dead,limit=1,sort=nearest] add dead'
    )

    cmd(
        'execute if entity @e[type=arrow,tag=!hit] '
        'as @e[type=arrow,tag=!hit] '
        'at @s '
        'if entity @a[distance=..1.2,gamemode=!spectator,tag=!dead] '
        'run tag @s add hit'
    )

    # ========================================================
    # TRIDENT
    # ========================================================

    cmd(
        'execute if entity @e[type=trident,tag=!hit] '
        'as @e[type=trident,tag=!hit] '
        'at @s '
        'if entity @a[distance=..1.5,gamemode=!spectator,tag=!dead] '
        'run scoreboard players add @a[distance=..1.5,gamemode=!spectator,tag=!dead,limit=1,sort=nearest] triHit 1'
    )

    cmd(
        'execute if entity @e[type=trident,tag=!hit] '
        'as @e[type=trident,tag=!hit] '
        'at @s '
        'if entity @a[distance=..1.5,gamemode=!spectator,tag=!dead] '
        'run tag @s add hit'
    )

    cmd(
        'execute if entity @a[scores={triHit=1},tag=!tri1] '
        'as @a[scores={triHit=1},tag=!tri1] '
        'run tag @s add tri1'
    )

    cmd(
        'execute if entity @a[scores={triHit=2..},tag=!dead] '
        'as @a[scores={triHit=2..},tag=!dead] '
        'run tag @s add dead'
    )

    # ========================================================
    # DEAD
    # ========================================================

    cmd(
        'execute if entity @a[tag=dead,scores={dead=0}] '
        'as @a[tag=dead,scores={dead=0}] '
        'run scoreboard players set @s dead 1'
    )

    cmd(
        'execute if entity @a[tag=dead,gamemode=!spectator] '
        'as @a[tag=dead,gamemode=!spectator] '
        'run gamemode spectator @s'
    )

    # ========================================================
    # roleCheck
    # ========================================================

    cmd(
        'execute if entity @a[scores={roleCheck=1..}] '
        'as @a[scores={roleCheck=1..}] '
        'run tellraw @s [{"text":"Dead : ","color":"red"},{"selector":"@a[tag=dead]","color":"gray"}]'
    )

    cmd(
        'execute if entity @a[scores={roleCheck=1..}] '
        'as @a[scores={roleCheck=1..}] '
        'run clear @s carrot_on_a_stick 1'
    )

    cmd(
        'execute if entity @a[scores={roleCheck=1..}] '
        'run scoreboard players set @a[scores={roleCheck=1..}] roleCheck 0'
    )
