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
# 巨大エンダーマンに乗る
# -------------------------
execute('/attribute @p minecraft:scale base set 1')
execute(f'/summon minecraft:enderman {x} {y+1} {z} {{Invulnerable:1b}}')
execute('/execute as @e[type=enderman,limit=1,sort=nearest,distance=..5] run attribute @s minecraft:scale base set 3')
time.sleep(1)
execute('/ride @p mount @e[type=enderman,limit=1,sort=nearest,distance=..5]')
echo("巨大なエンダーマンに乗って異世界の旅へ…！")

time.sleep(10)
execute('/ride @p dismount')
time.sleep(1)

# -------------------------
# アレイに乗って空中散歩
# -------------------------
execute('/attribute @p minecraft:scale base set 0.5')
execute(f'/summon minecraft:allay {x} {y+1} {z} {{Invulnerable:1b}}')
execute('/ride @p mount @e[type=allay,limit=1,sort=nearest,distance=..3]')
time.sleep(1)
echo("ちっちゃくなってアレイに乗って空中散歩へ…！")

time.sleep(10)
execute('/ride @p dismount')
time.sleep(1)
