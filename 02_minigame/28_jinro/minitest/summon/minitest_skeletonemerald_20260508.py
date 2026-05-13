import minescript as m
import random
import time

TICK = 0.1

PLAYERS = ["crocadooo", "saaample"]

m.execute("scoreboard objectives add Kill minecraft.killed:minecraft.skeleton")
m.execute("scoreboard objectives add Prev dummy")
m.execute("scoreboard objectives add Diff dummy")
m.execute("scoreboard objectives add Rand dummy")

print("Start")

while True:

    # Diff更新
    m.execute(
        "execute as @a run scoreboard players operation @s Diff = @s Kill"
    )
    time.sleep(0.02)

    m.execute(
        "execute as @a run scoreboard players operation @s Diff -= @s Prev"
    )
    time.sleep(0.02)

    # 抽選
    for name in PLAYERS:

        roll = random.randint(0, 1)

        # print(name, roll)

        m.execute(
            f"scoreboard players set {name} Rand {roll}"
        )

    time.sleep(0.02)

    # 成功判定
    m.execute(
        "execute as @a[scores={Diff=1..,Rand=1}] run give @s minecraft:emerald 1"
    )

    m.execute(
        'execute as @a[scores={Diff=1..,Rand=1}] run tellraw @s {"text":"Lucky 50%!","color":"green"}'
    )

    # Prev更新
    m.execute(
        "execute as @a run scoreboard players operation @s Prev = @s Kill"
    )

    time.sleep(TICK)

# 100%
# import minescript as m
# import time

# TICK = 0.1

# m.execute("scoreboard objectives add Kill minecraft.killed:minecraft.skeleton")
# m.execute("scoreboard objectives add Prev dummy")
# m.execute("scoreboard objectives add Diff dummy")

# print("Start")

# while True:

#     # Diff = Kill
#     m.execute(
#         "execute as @a run scoreboard players operation @s Diff = @s Kill"
#     )

#     # Diff -= Prev
#     m.execute(
#         "execute as @a run scoreboard players operation @s Diff -= @s Prev"
#     )

#     # キルしたら100%で配布
#     m.execute(
#         "execute as @a[scores={Diff=1..}] run give @s minecraft:emerald 1"
#     )

#     m.execute(
#         'execute as @a[scores={Diff=1..}] run tellraw @s {"text":"SUCCESS","color":"green"}'
#     )

#     # Prev更新
#     m.execute(
#         "execute as @a run scoreboard players operation @s Prev = @s Kill"
#     )

#     time.sleep(TICK)
