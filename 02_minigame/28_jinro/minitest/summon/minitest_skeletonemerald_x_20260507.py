import minescript as m
import time

TICK = 0.1

m.execute("scoreboard objectives add SkeletonKill minecraft.killed:minecraft.skeleton")
m.execute("scoreboard objectives add PrevSkeletonKill dummy")
m.execute("scoreboard objectives add Diff dummy")
m.execute("scoreboard objectives add Rand dummy")

print("System Start")

while True:

    # 差分
    m.execute(
        "execute as @a run scoreboard players operation @s Diff = @s SkeletonKill"
    )

    m.execute(
        "execute as @a run scoreboard players operation @s Diff -= @s PrevSkeletonKill"
    )

    # 1回だけカウント
    m.execute(
        "execute as @a[scores={Diff=1..}] run scoreboard players set @s Rand 0"
    )

    m.execute(
        "execute as @a[scores={Diff=1..}] run scoreboard players add @s Rand 1"
    )

    # 50%判定（0-49）
    m.execute(
        "execute as @a[scores={Diff=1..,Rand=0..49}] run give @s minecraft:emerald 1"
    )

    m.execute(
        'execute as @a[scores={Diff=1..,Rand=0..49}] run tellraw @s {"text":"Lucky! Emerald GET!","color":"green"}'
    )

    # Prev更新
    m.execute(
        "execute as @a run scoreboard players operation @s PrevSkeletonKill = @s SkeletonKill"
    )

    time.sleep(TICK)
