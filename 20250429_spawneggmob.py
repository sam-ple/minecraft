# -------------------------
# 標準ライブラリ
# -------------------------
from sys import (argv, exit)
import time
import random

# -------------------------
# 外部ライブラリ
# -------------------------
# import minescript as msc
import minescript
from minescript import (execute, echo)

# spawn_eggs = [
#     "allay", "sniffer", "glow_squid", "tadpole", "axolotl", "strider",
#     "camel", "frog", "vex", "phantom", "creeper", "warden", "blaze",
#     "chicken", "panda"
# ]

# BGMを再生（プレイヤーに向けて）
# execute('/playsound minecraft:music.overworld.jaguar record @p ~ ~ ~ 1')
# execute('/playsound minecraft:music.creative record @p ~ ~ ~ 1')
# execute('/playsound minecraft:music.game record @p ~ ~ ~ 1')
# execute('/playsound minecraft:music.menu record @p ~ ~ ~ 1')
# execute('/playsound minecraft:music_disc.cat record @p ~ ~ ~ 1')

spawn_eggs = [
     "allay", "glow_squid", "axolotl", "strider",
     "frog", "vex", "creeper", "blaze", "chicken"
 ]

# 召喚したモブのエンティティIDを保存しておく
spawned_entities = []

for mob in spawn_eggs:
    # プレイヤーにスポーンエッグを渡す
    # execute(f'/give @p minecraft:{mob}_spawn_egg 1')
    execute(f'/item replace entity @p weapon.mainhand with minecraft:{mob}_spawn_egg')    

    time.sleep(0.5)  # 少し待つ（giveコマンドがちゃんと反映されるように）

    # プレイヤーの向いている方向にモブを召喚
    execute(f'/execute as @p at @s run summon minecraft:{mob} ^1 ^0 ^1')

    # 効果音を再生（召喚演出）
    execute('/playsound minecraft:entity.illusioner.cast_spell master @p ~ ~ ~ 1 1')

    # 召喚したモブにタグをつけて管理
    execute(f'/tag @e[type=minecraft:{mob},distance=..5,limit=1,sort=nearest] add current_mob')

    # モブを静止＆敵対を解除
    execute(f'/data merge entity @e[tag=current_mob,limit=1,sort=nearest] {{NoAI:1b,Silent:1b,PersistenceRequired:1b}}')

    # 2秒待つ
    time.sleep(2)

    # 召喚したモブを安全にどこかへ飛ばす
    execute(f'/tp @e[tag=current_mob] ~200 ~200 ~200')  # 上空に飛ばす

    # タグをリセット
    execute(f'/tag @e[tag=current_mob] remove current_mob')
