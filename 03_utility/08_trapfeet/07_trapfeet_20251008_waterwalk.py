import minescript as m
import time

TICK_DELAY = 0.05

m.echo("❄️ Safe Ice Walking enabled")

while True:
    # 足元が水なら氷ブロックを置く
    m.execute(
        # "execute as @a at @s if block ~ ~-1 ~ minecraft:water run setblock ~ ~-1 ~ minecraft:barrier"
        "execute as @a at @s if block ~ ~-1 ~ minecraft:water run setblock ~ ~-1 ~ minecraft:ice"
        # "execute as @a at @s if block ~ ~-1 ~ minecraft:water run setblock ~ ~-1 ~ minecraft:packed_ice"
        # "execute as @a at @s if block ~ ~-1 ~ minecraft:water run setblock ~ ~-1 ~ minecraft:blue_ice"
    )

    time.sleep(TICK_DELAY)
