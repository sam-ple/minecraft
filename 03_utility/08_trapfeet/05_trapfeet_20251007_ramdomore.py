import minescript as m
import time
import random

m.echo("⛏ 足元ランダム鉱石（重み付き） 起動中...")

# 鉱石リスト
ores = [
    "minecraft:diamond_ore",   # レア
    "minecraft:emerald_ore",   # レア
    "minecraft:gold_ore",      # ややレア
    "minecraft:lapis_ore",     # 普通
    "minecraft:redstone_ore",  # 普通
    "minecraft:iron_ore",      # よく出る
    "minecraft:coal_ore",      # よく出る
    "minecraft:copper_ore"     # よく出る
]

# 重み（数値が大きいほど出やすい）
weights = [
    1,   # diamond
    1,   # emerald
    3,   # gold
    5,   # lapis
    5,   # redstone
    10,  # iron
    10,  # coal
    10   # copper
]

while True:
    # 重み付きでランダムに鉱石を選ぶ
    ore = random.choices(ores, weights=weights, k=1)[0]

    # 全プレイヤーの足元に設置
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

    time.sleep(0.1)
