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
# 引数チェック
# -------------------------
if len(argv) <= 1:
    echo("コマンドを指定してください。")
    exit(1)

arg1 = argv[1]
arg2 = argv[2] if len(argv) > 2 else None

# -------------------------
# モブ召喚関数
# -------------------------
def summon_circle(entity, sound=None, count=12, radius=1):
    x, y, z = minescript.player_position()

    for i in range(count):
        angle = 2 * math.pi * i / count
        dx = round(math.cos(angle) * radius, 2)
        dz = round(math.sin(angle) * radius, 2)
        sx = x + dx
        sy = y
        sz = z + dz

        execute(f'/summon {entity} {sx} {sy} {sz} {{}}')

    if sound:
        execute(f"playsound {sound} master @a ~ ~ ~ 1 1 1")

    sleep(5)

# ------------------------------------------------------------
# コマンド分岐
# ------------------------------------------------------------
if arg1 == "return":
    execute(f"/tp @p -12 64 -136")

elif arg1 == "mobs":
    summon_circle("minecraft:allay", "minecraft:entity.allay.ambient_with_item")
    summon_circle("minecraft:bee", "minecraft:entity.bee.ambient")
    summon_circle("minecraft:parrot", "minecraft:entity.parrot.ambient")

else:
    echo(f"未対応のコマンドです: {arg1}")
