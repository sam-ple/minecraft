import minescript as m
import time

DIST = 3

def test_detect(player_name):
    # 視線先にいるモブにタグ付け
    m.execute(f"execute as {player_name} at @s anchored eyes run execute positioned ^ ^ ^{DIST} run tag @e[type=!player,limit=1,sort=nearest,distance=..1] add test_hit")

while True:
    players = m.players()

    for p in players:
        test_detect(p.name)

    # 可視化（光らせる）
    m.execute("effect give @e[tag=test_hit] glowing 1 1 true")
    m.execute("tag @e[tag=test_hit] remove test_hit")

    time.sleep(0.2)
