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
# 散歩
# ------------------------------------------------------------
elif arg1 == "stroll":
    x, y, z = map(int, minescript.player_position())

    if arg2 == "allay":
        # アレイ召喚（そのままのサイズ）
        execute(f'/summon minecraft:allay {x} {y+1} {z} {{Invulnerable:1b,Glowing:1b}}')
        # プレイヤーを0.5に縮小
        execute('/attribute @p minecraft:generic.scale base set 0.5')
        # ライド
        execute('/ride @p mount @e[type=allay,limit=1,sort=nearest,distance=..3]')
        echo("ちっちゃくなってアレイに乗って空中散歩へ…！")

    elif arg2 == "enderman":
        # エンダーマン召喚
        execute(f'/summon minecraft:enderman {x} {y+1} {z} {{Invulnerable:1b,Glowing:1b}}')
        # エンダーマンを巨大化（scale 10）
        execute('/execute as @e[type=enderman,limit=1,sort=nearest,distance=..5] run attribute @s minecraft:generic.scale base set 10')
        # プレイヤーのサイズを元に戻す
        execute('/attribute @p minecraft:generic.scale base set 1')
        # ライド
        execute('/ride @p mount @e[type=enderman,limit=1,sort=nearest,distance=..5]')
        echo("巨大なエンダーマンに乗って異世界の旅へ…！")

    else:
        echo("未対応のサブコマンドです。'allay' または 'enderman' を指定してください。")

# ------------------------------------------------------------
# 未対応
# ------------------------------------------------------------
else:
    echo(f"未対応のコマンドです: {arg1}")
