import minescript as m
import time
import math

TARGET_ITEM = "minecraft:apple"

px, py, pz = m.player().position
px, py, pz = map(math.floor, (px, py, pz))

input_pos  = (px + 1, py, pz + 2)
target_pos = (px - 1, py, pz + 2)

ix, iy, iz = input_pos
tx, ty, tz = target_pos

input_frame_pos  = (ix, iy, iz-1)
target_frame_pos = (tx, ty, tz-1)

# =========================
# 設置
# =========================
def place():
    m.execute('kill @e[type=item_frame,tag=input_frame]')
    m.execute('kill @e[type=item_frame,tag=target_frame]')

    m.execute(f"setblock {ix} {iy} {iz} minecraft:gold_block")
    m.execute(
        f'summon minecraft:item_frame {input_frame_pos[0]} {input_frame_pos[1]} {input_frame_pos[2]} '
        f'{{Facing:2b,Tags:["input_frame"]}}'
    )

    m.execute(f"setblock {tx} {ty} {tz} minecraft:emerald_block")
    m.execute(
        f'summon minecraft:item_frame {target_frame_pos[0]} {target_frame_pos[1]} {target_frame_pos[2]} '
        f'{{Facing:2b,Tags:["target_frame"]}}'
    )

place()

# =========================
# メイン
# =========================
while True:

    # =========================
    # 🍎 一回だけ発火
    # =========================
    m.execute(
        'execute as @e[type=item_frame,tag=input_frame,nbt={Item:{id:"minecraft:apple"}},tag=!done] '
        'run data merge entity @e[type=item_frame,tag=target_frame,limit=1] {Item:{id:"minecraft:apple",count:1}}'
    )

    # 演出（1回）
    m.execute(
        f'execute as @e[type=item_frame,tag=input_frame,nbt={{Item:{{id:"{TARGET_ITEM}"}}}},tag=!done] '
        f'run particle minecraft:totem_of_undying {tx} {ty+1} {tz} 0.3 0.5 0.3 0 30'
    )

    m.execute(
        'execute as @e[type=item_frame,tag=input_frame,nbt={Item:{id:"minecraft:apple"}},tag=!done] '
        'run playsound minecraft:entity.player.levelup master @a'
    )

    # 入力側を消す（確実版）
    m.execute(
        'execute as @e[type=item_frame,tag=input_frame,nbt={Item:{id:"minecraft:apple"}},tag=!done] '
        'run data remove entity @s Item'
    )

    # doneタグ付け（連打防止）
    m.execute(
        'execute as @e[type=item_frame,tag=input_frame,nbt={Item:{id:"minecraft:apple"}},tag=!done] '
        'run tag @s add done'
    )

    # =========================
    # 🔄 リセット（空になったら再使用）
    # =========================
    m.execute(
        'execute as @e[type=item_frame,tag=input_frame,nbt=!{Item:{}},tag=done] run tag @s remove done'
    )

    time.sleep(0.2)
