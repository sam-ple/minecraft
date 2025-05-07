# -------------------------
# 標準ライブラリ
# -------------------------
import time
import math

# -------------------------
# 外部ライブラリ
# -------------------------
import minescript
from minescript import execute, echo, player_position

# -------------------------
# モブ召喚関数
# -------------------------
def summon_circle(entity, sound=None, count=12, radius=1):
    x, y, z = map(int, player_position())

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

    time.sleep(5)

# -------------------------
# 呼び出し
# -------------------------
summon_circle("minecraft:allay", "minecraft:entity.allay.ambient_with_item")
summon_circle("minecraft:bee", "minecraft:entity.bee.ambient")
summon_circle("minecraft:parrot", "minecraft:entity.parrot.ambient")
