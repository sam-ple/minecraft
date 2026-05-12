import minescript as m
import time

m.echo("💣 足元TNT")

while True:
    m.execute(
        "execute as @a at @s "
        "unless block ~ ~-1 ~ minecraft:water "
        "unless block ~ ~-1 ~ minecraft:bedrock "
        "unless block ~ ~-1 ~ minecraft:cave_air "
        "unless block ~ ~-1 ~ minecraft:void_air "
        "unless block ~ ~-1 ~ minecraft:air "
        "unless block ~ ~-1 ~ minecraft:obsidian "
        "run setblock ~ ~-1 ~ minecraft:tnt"
    )

    time.sleep(0.1) 
