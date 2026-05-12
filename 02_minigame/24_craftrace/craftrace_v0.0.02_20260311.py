import minescript as m
import time
import json

# =========================
# 設定
# =========================

TARGET_ITEMS = [
    "minecraft:cake",
    "minecraft:bread",
    "minecraft:diamond_sword"
]

TICK = 0.2


# =========================
# util
# =========================

def cmd(c):
    m.execute(c)

def fmt(item):
    return item.replace("minecraft:", "")

def name(item):
    return item.replace("minecraft:", "").replace("_"," ").title()

def chat(msg):
    cmd(f'tellraw @a {json.dumps({"text":msg,"color":"yellow"})}')


# =========================
# setup
# =========================

cmd("scoreboard objectives add points dummy")
cmd("scoreboard objectives setdisplay sidebar points")

for item in TARGET_ITEMS:

    n = fmt(item)

    try:
        cmd(f"scoreboard objectives add crafted_{n} minecraft.crafted:{fmt(item)}")
    except:
        pass

    try:
        cmd(f"scoreboard objectives add got_{n} dummy")
    except:
        pass

chat("🍰 CraftRace START")


# =========================
# main loop
# =========================

while True:

    for item in TARGET_ITEMS:

        n = fmt(item)
        pretty = name(item)

        condition = (
            f'if score @s crafted_{n} matches 1.. '
            f'unless score @s got_{n} matches 1'
        )

        # ポイント
        cmd(
            f'execute as @a {condition} '
            f'run scoreboard players add @s points 1'
        )

        # フラグON（1回だけ）
        cmd(
            f'execute as @a {condition} '
            f'run scoreboard players set @s got_{n} 1'
        )

        # 通知
        cmd(
            f'execute as @a {condition} '
            f'run tellraw @a '
            f'[{{"selector":"@s","color":"yellow"}},'
            f'{{"text":" crafted "}},'
            f'{{"text":"{pretty}","color":"gold","bold":true}}]'
        )
        # サウンド
        cmd(
            f'execute as @a {condition} '
            f'run playsound minecraft:entity.player.levelup master @a'
        )

    time.sleep(TICK)
