import minescript as m
import time
import random

m.echo("⛏ 足元ランダム鉱石生成 起動中...")

# 出現させたい鉱石ブロックのリスト
ores = [
    "minecraft:diamond_ore",
    "minecraft:gold_ore",
    "minecraft:iron_ore",
    "minecraft:coal_ore",
    "minecraft:lapis_ore",
    "minecraft:redstone_ore",
    "minecraft:emerald_ore",
    "minecraft:copper_ore"
]

while True:
    # ランダムで鉱石を1つ選ぶ
    ore = random.choice(ores)

    # 全プレイヤーの足元にランダム鉱石を設置
    m.execute(
        f"execute as @a at @s "
        "unless block ~ ~-1 ~ minecraft:water "
        "unless block ~ ~-1 ~ minecraft:bedrock "
        "unless block ~ ~-1 ~ minecraft:cave_air "
        "unless block ~ ~-1 ~ minecraft:void_air "
        "unless block ~ ~-1 ~ minecraft:air "
        "unless block ~ ~-1 ~ minecraft:obsidian "
        f"run setblock ~ ~-1 ~ {ore}"
    )

    time.sleep(0.1)  # 0.5秒ごとにチェック
