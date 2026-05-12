import minescript as m
import time

m.echo("💣 足元TNT")

m.execute("scoreboard objectives add hp dummy")
m.execute("scoreboard objectives add hp_prev dummy")

# 初期化
m.execute(
    "execute as @a run scoreboard players operation @s hp_prev = @s hp"
)

while True:

    # HP取得
    m.execute(
        "execute as @a store result score @s hp run data get entity @s Health 1"
    )

    # ダメージ検知
    m.execute(
        "execute as @a if score @s hp < @s hp_prev at @s "
        "run summon tnt ~ ~ ~ {Fuse:0}"
    )

    # 更新
    m.execute(
        "execute as @a run scoreboard players operation @s hp_prev = @s hp"
    )

    # 足元TNT
    m.execute(
        "execute as @a at @s "
        "unless block ~ ~-1 ~ minecraft:water "
        "unless block ~ ~-1 ~ minecraft:lava "
        "unless block ~ ~-1 ~ minecraft:bedrock "
        "unless block ~ ~-1 ~ minecraft:cave_air "
        "unless block ~ ~-1 ~ minecraft:void_air "
        "unless block ~ ~-1 ~ minecraft:air "
        "unless block ~ ~-1 ~ minecraft:obsidian "
        "unless block ~ ~-1 ~ minecraft:chest "
        "unless block ~ ~-1 ~ minecraft:ender_chest "
        "unless block ~ ~-1 ~ minecraft:nether_portal "
        "unless block ~ ~-1 ~ minecraft:end_portal_frame "
        "unless block ~ ~-1 ~ minecraft:end_portal "
        "run setblock ~ ~-1 ~ minecraft:tnt"
    )

    time.sleep(0.1)
