# -------------------------
# 標準ライブラリ
# -------------------------
import time

# -------------------------
# 外部ライブラリ
# -------------------------
import minescript
from minescript import execute, echo, player_position

# -------------------------
# 初期位置
# -------------------------
x, y, z = map(int, player_position())

# -------------------------
# アレイに乗って空中散歩
# -------------------------
execute(f'/summon minecraft:allay {x} {y+1} {z} {{Invulnerable:1b,Glowing:1b}}')
execute('/attribute @p minecraft:generic.scale base set 0.5')
execute('/ride @p mount @e[type=allay,limit=1,sort=nearest,distance=..3]')
echo("ちっちゃくなってアレイに乗って空中散歩へ…！")

time.sleep(10)

# -------------------------
# 巨大エンダーマンに乗る
# -------------------------
execute(f'/summon minecraft:enderman {x} {y+1} {z} {{Invulnerable:1b,Glowing:1b}}')
execute('/execute as @e[type=enderman,limit=1,sort=nearest,distance=..5] run attribute @s minecraft:generic.scale base set 10')
execute('/attribute @p minecraft:generic.scale base set 1')
execute('/ride @p mount @e[type=enderman,limit=1,sort=nearest,distance=..5]')
echo("巨大なエンダーマンに乗って異世界の旅へ…！")

time.sleep(10)
