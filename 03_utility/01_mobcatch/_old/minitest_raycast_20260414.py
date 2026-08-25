import minescript as m
import time

ITEM = "minecraft:stick"
DIST = 3

def test_detect(player_name):
    m.execute(f'execute as {player_name} at @s anchored eyes positioned ^ ^ ^{DIST} if entity @s[nbt={{SelectedItem:{{id:"{ITEM}"}}}}] run tag @e[type=!player,limit=1,sort=nearest,distance=..1] add test_hit')

while True:
    for p in m.players():
        test_detect(p.name)

    m.execute("effect give @e[tag=test_hit] glowing 1 1 true")
    m.execute("tag @e[tag=test_hit] remove test_hit")

    time.sleep(0.5)
