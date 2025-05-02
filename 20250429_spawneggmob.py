import time
import minescript
from minescript import execute, echo

# -------------------------
# モブリスト
# -------------------------
spawn_eggs = [
    "allay", "glow_squid", "axolotl", "strider", "frog", "vex", "creeper", "blaze", "chicken"
]

# -------------------------
# モブ処理関数
# -------------------------
def summon_mob(mob):
    # プレイヤーに指定モブのスポーンエッグを持たせる
    execute(f'/item replace entity @p weapon.mainhand with minecraft:{mob}_spawn_egg')
    time.sleep(0.5)

    # プレイヤーの前にモブを召喚
    execute(f'/execute as @p at @s run summon minecraft:{mob} ^1 ^0 ^1')

    # 効果音で演出（幻術師の呪文音）
    execute('/playsound minecraft:entity.illusioner.cast_spell master @p ~ ~ ~ 1 1')

    # 近くの召喚モブに一時タグを付与（current_mob）
    execute(f'/tag @e[type=minecraft:{mob},distance=..5,limit=1,sort=nearest] add current_mob')

    # モブを無力化（AI無効・音無・消えないように）
    execute('/data merge entity @e[tag=current_mob,limit=1,sort=nearest] {NoAI:1b,Silent:1b,PersistenceRequired:1b}')
    time.sleep(2)

    # 上空へモブを移動させて非表示にする
    execute('/tp @e[tag=current_mob] ~200 ~200 ~200')

    # タグを削除して後処理
    execute('/tag @e[tag=current_mob] remove current_mob')

# -------------------------
# メイン処理
# -------------------------
for mob in spawn_eggs:
    summon_mob(mob)
