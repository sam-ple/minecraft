import minescript as m
import time
import math

# =========================
# 設定
# =========================
TARGET_ITEM = "minecraft:apple"

# =========================
# 座標
# =========================
px, py, pz = m.player().position
px, py, pz = map(math.floor, (px, py, pz))

# 横並び
input_pos  = (px + 1, py, pz + 2)
target_pos = (px - 1, py, pz + 2)

ix, iy, iz = input_pos
tx, ty, tz = target_pos

# 額縁位置
input_frame_pos  = (ix, iy, iz-1)
target_frame_pos = (tx, ty, tz-1)

# =========================
# 設置
# =========================
def place():

    # 初期化
    m.execute('kill @e[type=item_frame,tag=input_frame]')
    m.execute('kill @e[type=item_frame,tag=target_frame]')

    # 入力（ゴールド）
    m.execute(f"setblock {ix} {iy} {iz} minecraft:gold_block")
    m.execute(
        f'summon minecraft:item_frame {input_frame_pos[0]} {input_frame_pos[1]} {input_frame_pos[2]} '
        f'{{Facing:2b,Tags:["input_frame"]}}'
    )

    # 出力（エメラルド）
    m.execute(f"setblock {tx} {ty} {tz} minecraft:emerald_block")
    m.execute(
        f'summon minecraft:item_frame {target_frame_pos[0]} {target_frame_pos[1]} {target_frame_pos[2]} '
        f'{{Facing:2b,Tags:["target_frame"]}}'
    )

    m.echo("✔ 設置完了")

place()

# =========================
# メインループ（コマンド任せ）
# =========================
while True:

    # =========================
    # 🍎 入れたら出現
    # =========================
    m.execute(
        'execute if entity @e[type=item_frame,tag=input_frame,nbt={Item:{id:"minecraft:apple"}}] '
        'run data merge entity @e[type=item_frame,tag=target_frame,limit=1] {Item:{id:"minecraft:apple",count:1}}'
    )

    # =========================
    # ✨ 演出
    # =========================
    m.execute(
        f'execute if entity @e[type=item_frame,tag=input_frame,nbt={{Item:{{id:"{TARGET_ITEM}"}}}}] '
        f'run particle minecraft:totem_of_undying {tx} {ty+1} {tz} 0.3 0.5 0.3 0 30'
    )

    m.execute(
        'execute if entity @e[type=item_frame,tag=input_frame,nbt={Item:{id:"minecraft:apple"}}] '
        'run playsound minecraft:entity.player.levelup master @a'
    )

    # =========================
    # 🧹 入力側を消す（チェスト化）
    # =========================
    m.execute(
        'execute if entity @e[type=item_frame,tag=input_frame,nbt={Item:{id:"minecraft:apple"}}] '
        'run data merge entity @e[type=item_frame,tag=input_frame,limit=1] {Item:{}}'
    )

    time.sleep(0.2)
