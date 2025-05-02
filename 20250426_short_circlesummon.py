# -------------------------
# 標準ライブラリ
# -------------------------
from sys import argv, exit
from time import sleep
import random
import math
from datetime import datetime

# -------------------------
# 外部ライブラリ
# -------------------------
import minescript
from minescript import execute, echo

# -------------------------
# 引数
# -------------------------
arg1 = argv[1] if len(argv) > 1 else (echo("コマンドを指定してください。") or exit(1))
arg2 = argv[2] if len(argv) > 2 else None

# -------------------------
# 共通関数
# -------------------------

def summon_circle(entity, sound, count=12, radius=1, variant=False):
    x, y, z = minescript.player_position()

    for i in range(count):
        angle = 2 * math.pi * i / count
        dx = round(math.cos(angle) * radius, 2)
        dz = round(math.sin(angle) * radius, 2)
        sx = x + dx
        sy = y
        sz = z + dz

        if variant:
            v = random.randint(0, 4)
            execute(f'/summon {entity} {sx} {sy} {sz} {{Variant:{v}}}')
        else:
            execute(f'/summon {entity} {sx} {sy} {sz} {{}}')

    # 音と花火
    execute(f'/playsound {sound} master @a')
    summon_fireworks(x, y, z)
    sleep(5)

def summon_fireworks(x, y, z, count=5):
    for _ in range(count):
        fx = x + random.uniform(-2, 2)
        fz = z + random.uniform(-2, 2)
        fy = y + 1
        execute(f'/summon minecraft:firework_rocket {fx} {fy} {fz} {{}}')

# ------------------------------------------------------------
# 帰還
# ------------------------------------------------------------
if arg1 == "return":
    execute(f"/tp @p -12 64 -136")

# ------------------------------------------------------------
# モブ召喚
# ------------------------------------------------------------
elif arg1 == "mobs":
    summon_circle("minecraft:allay", "minecraft:entity.allay.ambient_with_item")
    summon_circle("minecraft:bee", "minecraft:entity.bee.ambient")
    summon_circle("minecraft:parrot", "minecraft:entity.parrot.ambient")
    summon_circle("minecraft:parrot", "minecraft:entity.parrot.ambient", variant=True)

# ------------------------------------------------------------
# 未対応
# ------------------------------------------------------------
else:
    echo(f"未対応のコマンドです: {arg1}")
