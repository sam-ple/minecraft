import minescript as m
import time

TOOLS = [
    "wooden_pickaxe",
    "wooden_axe",
    "wooden_shovel",
    "wooden_sword",
    "wooden_hoe",
]

def chat(msg):
    m.execute(f'tellraw @a {{"text":"{msg}","color":"yellow"}}')

# setup
for tool in TOOLS:
    try:
        m.execute(f"scoreboard objectives add crafted_{tool} minecraft.crafted:minecraft.{tool}")
    except:
        pass

chat("🔍 Craft Debug START")

# main loop
while True:
    for tool in TOOLS:
        m.execute(
            f'execute as @a run tellraw @s '
            f'{{"text":"{tool}: ","color":"aqua","extra":[{{"score":{{"name":"@s","objective":"crafted_{tool}"}}}}]}}'
        )
    time.sleep(2)
