# /gamerule sendCommandFeedback false
import minescript as m
import time

# ---- 初期化（1回だけ） ----
def setup():
    m.execute("scoreboard objectives add mineCount mined:stone")
    m.execute("scoreboard objectives add minePoints dummy")
    m.execute("scoreboard objectives add LastMineCount dummy")
    m.execute("scoreboard objectives add Temp dummy")
    m.execute("scoreboard objectives setdisplay sidebar minePoints")

setup()

TICK_DELAY = 0.2

while True:
    # Temp = mineCount
    m.execute("scoreboard players operation @a Temp = @a mineCount")

    # Temp = Temp - LastMineCount
    m.execute("scoreboard players operation @a Temp -= @a LastMineCount")

    # Temp > 0 のプレイヤーだけポイント加算
    m.execute(
        "execute as @a if score @s Temp matches 1.. "
        "run scoreboard players operation @s minePoints += @s Temp"
    )

    # LastMineCount 更新（全員）
    m.execute("scoreboard players operation @a LastMineCount = @a mineCount")

    time.sleep(TICK_DELAY)
