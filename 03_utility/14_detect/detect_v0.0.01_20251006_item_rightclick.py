import minescript as m
import time

# --- Objectives ---
m.execute('scoreboard objectives add has_carrot dummy')
m.execute('scoreboard objectives add right_click dummy')
m.execute('scoreboard objectives add used_carrot minecraft.used:carrot_on_a_stick')

# --- Initialize ---
m.execute('scoreboard players set @a has_carrot 0')
m.execute('scoreboard players set @a right_click 0')
m.execute('scoreboard players set @a right_click_prev 0')
m.execute('scoreboard players set @a used_carrot 0')

SLEEP = 0.1  # check interval

while True:
    # Check if player is holding a carrot-on-a-stick
    m.execute('execute as @a if entity @s[nbt={SelectedItem:{id:"minecraft:carrot_on_a_stick"}}] run scoreboard players set @s has_carrot 1')
    m.execute('execute as @a unless entity @s[nbt={SelectedItem:{id:"minecraft:carrot_on_a_stick"}}] run scoreboard players set @s has_carrot 0')

    # Check if player has right-clicked the carrot-on-a-stick
    m.execute('execute as @a if score @s used_carrot matches 1.. run scoreboard players set @s right_click 1')
    m.execute('execute as @a unless score @s used_carrot matches 1.. run scoreboard players set @s right_click 0')

    # Detect rising edge (right-click just happened)
    m.execute('execute as @a if score @s right_click matches 1.. unless score @s right_click_prev matches 1.. if score @s has_carrot matches 1.. run tellraw @a ["",{"selector":"@s"},{"text":" right-clicked the carrot-on-a-stick!","color":"gold"}]')

    # Update previous right-click state
    m.execute('execute as @a if score @s right_click matches 1.. run scoreboard players set @s right_click_prev 1')
    m.execute('execute as @a unless score @s right_click matches 1.. run scoreboard players set @s right_click_prev 0')

    # Reset used_carrot for next detection
    m.execute('scoreboard players set @a used_carrot 0')

    time.sleep(SLEEP)
