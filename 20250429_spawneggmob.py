# -------------------------
# 標準ライブラリ
# -------------------------
from sys import argv, exit
import time
import random

# -------------------------
# 外部ライブラリ
# -------------------------
import minescript
from minescript import execute, echo

# -------------------------
# モブリスト
# -------------------------
spawn_eggs = [
    "allay", "glow_squid", "axolotl", "strider",
    "frog", "vex", "creeper", "blaze", "chicken"
]

# -------------------------
# モブ処理関数
# -------------------------
def summon_and_manage_mob(mob):
    # スポーンエッグを持たせる
    execute(f'/item replace entity @p weapon.mainhand with minecraft:{mob}_spawn_egg')
    time.sleep(0.5)

    # モブ召喚（プレイヤーの前方）
    execute(f'/execute as @p at @s run summon minecraft:{mob} ^1 ^0 ^1')

    # 演出（効果音）
    execute('/playsound minecraft:entity.illusioner.cast_spell master @p ~ ~ ~ 1 1')

    # 一時タグ付け
    execute(f'/tag @e[type=minecraft:{mob},distance=..5,limit=1,sort=nearest] add current_mob')

    # モブを無力化
    execute('/data merge entity @e[tag=current_mob,limit=1,sort=nearest] {NoAI:1b,Silent:1b,PersistenceRequired:1b}')

    time.sleep(2)

    # 上空へ移動
    execute('/tp @e[tag=current_mob] ~200 ~200 ~200')

    # タグ削除
    execute('/tag @e[tag=current_mob] remove current_mob')

# -------------------------
# メイン処理
# -------------------------
for mob in spawn_eggs:
    summon_and_manage_mob(mob)
