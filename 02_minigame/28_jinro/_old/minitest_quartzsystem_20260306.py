import minescript as m
import time
import random

INTERVAL = 5
timer = INTERVAL

items = [
    "minecraft:cooked_beef",
    "minecraft:iron_ingot",
    "minecraft:iron_axe"
]

def random_item():
    return random.choice(items)


def chat(msg):
    m.execute(f'tellraw @a {{"text":"{msg}","color":"yellow"}}')


# -------------------------
# scoreboard setup
# -------------------------

try:
    m.execute("scoreboard objectives add crafted_quartz minecraft.crafted:minecraft.quartz_block")
except:
    pass

try:
    m.execute("scoreboard objectives add Last_quartz dummy")
except:
    pass

try:
    m.execute("scoreboard objectives add Temp_quartz dummy")
except:
    pass


chat("Quartz System Ready")


# -------------------------
# quartz block craft check
# -------------------------

def check_craft():

    # Temp = crafted - Last
    m.execute("scoreboard players operation @a Temp_quartz = @a crafted_quartz")
    m.execute("scoreboard players operation @a Temp_quartz -= @a Last_quartz")

    players = m.players()

    for p in players:

        name = p.name

        # クラフトされた
        item = random_item()

        # ランダムアイテム付与
        m.execute(
            f"execute as {name} if score @s Temp_quartz matches 1.. run give {name} {item}"
        )

        # クォーツブロック1個削除
        m.execute(
            f"execute as {name} if score @s Temp_quartz matches 1.. run clear {name} minecraft:quartz_block 1"
        )

    # Last更新
    m.execute("scoreboard players operation @a Last_quartz = @a crafted_quartz")


# -------------------------
# quartz配布
# -------------------------

def give_quartz():

    m.execute("give @a minecraft:quartz 1")

    m.execute(
        'tellraw @a {"text":"Quartz 配布！","color":"aqua"}'
    )


# -------------------------
# actionbar
# -------------------------

def show_timer(sec):

    m.execute(
        f'title @a actionbar {{"text":"次のQuartzまで {sec} 秒","color":"yellow"}}'
    )


# -------------------------
# main loop
# -------------------------

while True:

    show_timer(timer)

    check_craft()

    time.sleep(1)

    timer -= 1

    if timer <= 0:

        give_quartz()

        timer = INTERVAL
