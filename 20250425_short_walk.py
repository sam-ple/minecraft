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
# 空中散歩
# ------------------------------------------------------------
elif arg1 == "skywalk":
    x, y, z = map(int, minescript.player_position())

    # アレイを浮かせて召喚（NoAI: 動かず、Silent: 音なし、Invulnerable: 壊れない）
    # execute(f'/summon minecraft:allay {x} {y+1} {z} {{NoAI:1b,Silent:1b,Invulnerable:1b}}')
    # アレイを浮かせて召喚（Invulnerable: 壊れない、Glowing: 光彩）
    execute(f'/summon minecraft:allay {x} {y+1} {z} {{Invulnerable:1b,Glowing:1b}}')

    # プレイヤーをそのアレイにライド
    execute('/ride @p mount @e[type=allay,limit=1,sort=nearest,distance=..3]')

    echo("アレイに乗って優雅に空中散歩へ…！")

# ------------------------------------------------------------
# 未対応
# ------------------------------------------------------------
else:
    echo(f"未対応のコマンドです: {arg1}")
