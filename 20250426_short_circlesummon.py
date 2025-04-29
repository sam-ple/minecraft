# -------------------------
# 標準ライブラリ
# -------------------------
from sys import (argv, exit)
from time import sleep
import random
import math
from datetime import datetime

# -------------------------
# 外部ライブラリ
# -------------------------
# import minescript as msc
import minescript
from minescript import (execute, echo)

# -------------------------
# 引数
# -------------------------
arg1 = argv[1] if len(argv) > 1 else (echo("コマンドを指定してください。") or exit(1))
arg2 = argv[2] if len(argv) > 2 else None  # 指定がなければ None

# ------------------------------------------------------------
# 帰還
# ------------------------------------------------------------
if arg1 == "return":
    execute(f"/tp @p -12 64 -136")

# ------------------------------------------------------------
# モブ召喚
# ------------------------------------------------------------
elif arg1 == "mobs":
    # プレイヤーの位置を取得
    x, y, z = minescript.player_position()
    
    # アレイを出現させる数と半径
    num_allays = 12       # アレイの数（例：24体）
    radius = 1            # プレイヤーからの距離（円の半径）
    
    # 放射状にアレイを配置
    for i in range(num_allays):
        angle = 2 * math.pi * i / num_allays
        dx = round(math.cos(angle) * radius, 2)
        dz = round(math.sin(angle) * radius, 2)
        sy = y
        sx = x + dx
        sz = z + dz
        execute(f'/summon minecraft:allay {sx} {sy} {sz} {{}}')
    
    # 視覚＆音の演出
    execute('/playsound minecraft:entity.allay.ambient_with_item master @a')

    sleep(5)

    # プレイヤーの位置を取得
    x, y, z = minescript.player_position()
    
    # アレイを出現させる数と半径
    num_allays = 12       # アレイの数（例：24体）
    radius = 1            # プレイヤーからの距離（円の半径）
    
    # 放射状にアレイを配置
    for i in range(num_allays):
        angle = 2 * math.pi * i / num_allays
        dx = round(math.cos(angle) * radius, 2)
        dz = round(math.sin(angle) * radius, 2)
        sy = y
        sx = x + dx
        sz = z + dz
        execute(f'/summon minecraft:bee {sx} {sy} {sz} {{}}')
    
    # 視覚＆音の演出
    execute('/playsound minecraft:entity.bee.ambient master @a')

    sleep(5)

    # プレイヤーの位置を取得
    x, y, z = minescript.player_position()
    
    # アレイを出現させる数と半径
    num_allays = 12       # アレイの数（例：24体）
    radius = 1            # プレイヤーからの距離（円の半径）
    
    # 放射状にアレイを配置
    for i in range(num_allays):
        angle = 2 * math.pi * i / num_allays
        dx = round(math.cos(angle) * radius, 2)
        dz = round(math.sin(angle) * radius, 2)
        sy = y 
        sx = x + dx
        sz = z + dz
        execute(f'/summon minecraft:parrot {sx} {sy} {sz} {{}}')
    
    # 視覚＆音の演出
    execute('/playsound minecraft:entity.parrot.ambient master @a')

    sleep(5)

    # プレイヤーの位置を取得
    x, y, z = minescript.player_position()
    
    # アレイを出現させる数と半径
    num_allays = 12       # アレイの数（例：24体）
    radius = 1            # プレイヤーからの距離（円の半径）
    
    # 放射状にアレイを配置
    for i in range(num_allays):
        angle = 2 * math.pi * i / num_allays
        dx = round(math.cos(angle) * radius, 2)
        dz = round(math.sin(angle) * radius, 2)
        sy = y 
        sx = x + dx
        sz = z + dz
        variant = random.randint(0, 4)  # 0〜4のランダム
        execute(f'/summon minecraft:parrot {sx} {sy} {sz} {{Variant:{variant}}}')
    
    # 視覚＆音の演出
    execute('/playsound minecraft:entity.parrot.ambient master @a')

    sleep(5)

# ------------------------------------------------------------
# 未対応
# ------------------------------------------------------------
else:
    echo(f"未対応のコマンドです: {arg1}")
