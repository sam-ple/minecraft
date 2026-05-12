import minescript as m
import time

# ==============================
# Settings
# ==============================
TICK_DELAY = 0.1  # Loop interval
SNEAK_SCOREBOARD = "sneak_time"
CARROT_ITEM = "minecraft:carrot_on_a_stick"

# ==============================
# Carrot-on-a-Stick Scoreboards
# ==============================
m.execute('scoreboard objectives add has_carrot dummy')
m.execute('scoreboard objectives add right_click dummy')
m.execute('scoreboard objectives add right_click_prev dummy')
m.execute('scoreboard objectives add used_carrot minecraft.used:carrot_on_a_stick')
m.execute('scoreboard players set @a has_carrot 0')
m.execute('scoreboard players set @a right_click 0')
m.execute('scoreboard players set @a right_click_prev 0')
m.execute('scoreboard players set @a used_carrot 0')

# ==============================
# Sneak Scoreboards
# ==============================
m.execute('scoreboard objectives add sneak_prev dummy')
m.execute('scoreboard objectives add is_sneaking dummy')
m.execute('scoreboard objectives add sneak_state dummy')  # 0=not sneaking, 1=sneaking

m.execute('scoreboard players reset @a sneak_prev')
m.execute('scoreboard players reset @a is_sneaking')
m.execute('scoreboard players reset @a sneak_state')

m.echo("Right-Click or Sneak + Carrot-on-a-Stick detection running...")

# ==============================
# Main loop
# ==============================
while True:
    # --- Check if player is holding carrot-on-a-stick ---
    m.execute(f'execute as @a if entity @s[nbt={{SelectedItem:{{id:"{CARROT_ITEM}"}}}}] run scoreboard players set @s has_carrot 1')
    m.execute(f'execute as @a unless entity @s[nbt={{SelectedItem:{{id:"{CARROT_ITEM}"}}}}] run scoreboard players set @s has_carrot 0')

    # --- Check right-click ---
    m.execute('execute as @a if score @s used_carrot matches 1.. run scoreboard players set @s right_click 1')
    m.execute('execute as @a unless score @s used_carrot matches 1.. run scoreboard players set @s right_click 0')

    # --- Detect rising edge for right-click ---
    m.execute('execute as @a if score @s right_click matches 1.. unless score @s right_click_prev matches 1.. if score @s has_carrot matches 1.. run tellraw @a ["",{"selector":"@s"},{"text":" right-clicked the carrot-on-a-stick!","color":"gold"}]')
    m.execute('execute as @a if score @s right_click matches 1.. run scoreboard players set @s right_click_prev 1')
    m.execute('execute as @a unless score @s right_click matches 1.. run scoreboard players set @s right_click_prev 0')
    m.execute('scoreboard players set @a used_carrot 0')

    # --- Sneak detection ---
    m.execute(f'execute as @a if score @s {SNEAK_SCOREBOARD} > @s sneak_prev run scoreboard players set @s is_sneaking 1')
    m.execute(f'execute as @a unless score @s {SNEAK_SCOREBOARD} > @s sneak_prev run scoreboard players set @s is_sneaking 0')

    # Sneak start
    # Only announce if holding carrot-on-a-stick
    m.execute(f'execute as @a if score @s is_sneaking matches 1 if score @s sneak_state matches 0 if score @s has_carrot matches 1 run tellraw @a ["",{{"selector":"@s"}},{{"text":" started sneaking with the carrot-on-a-stick!","color":"yellow"}}]')
    m.execute('execute as @a if score @s is_sneaking matches 1 run scoreboard players set @s sneak_state 1')

    # Sneak end
    m.execute(f'execute as @a if score @s is_sneaking matches 0 if score @s sneak_state matches 1 if score @s has_carrot matches 1 run tellraw @a ["",{{"selector":"@s"}},{{"text":" stopped sneaking with the carrot-on-a-stick!","color":"red"}}]')
    m.execute('execute as @a if score @s is_sneaking matches 0 run scoreboard players set @s sneak_state 0')

    # Update previous sneak time
    m.execute(f'execute as @a run scoreboard players operation @s sneak_prev = @s {SNEAK_SCOREBOARD}')

    time.sleep(TICK_DELAY)
