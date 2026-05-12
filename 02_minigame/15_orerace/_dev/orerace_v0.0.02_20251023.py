import minescript as m
import time

ORES = {
    "stone": 1,
    "coal_ore": 2,
    "iron_ore": 3,
    "gold_ore": 5,
    "diamond_ore": 10,
    "emerald_ore": 15,
    "deepslate_diamond_ore": 10,
    "deepslate_emerald_ore": 15
}

# ---------- 初期化（1回だけ実行） ----------
def setup():
    m.execute("scoreboard objectives add minePoints dummy")

    for ore in ORES:
        m.execute(f"scoreboard objectives add mined_{ore} mined:{ore}")
        m.execute(f"scoreboard objectives add Last_{ore} dummy")
        m.execute(f"scoreboard objectives add Temp_{ore} dummy")

    m.execute("scoreboard objectives setdisplay sidebar minePoints")

setup()

# ---------- メインループ ----------
TICK_DELAY = 0.5

while True:
    for ore, points in ORES.items():

        # Temp_<ore> = mined_<ore>
        m.execute(
            f"scoreboard players operation @a Temp_{ore} = @a mined_{ore}"
        )

        # Temp_<ore> -= Last_<ore>
        m.execute(
            f"scoreboard players operation @a Temp_{ore} -= @a Last_{ore}"
        )

        # 差分がある人だけポイント加算
        m.execute(
            f"execute as @a if score @s Temp_{ore} matches 1.. "
            f"run scoreboard players add @s minePoints {points}"
        )

        # Last_<ore> = mined_<ore>
        m.execute(
            f"scoreboard players operation @a Last_{ore} = @a mined_{ore}"
        )

    time.sleep(TICK_DELAY)
