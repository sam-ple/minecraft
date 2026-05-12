# ============================================================
# BINGO BASE GENERATOR
# Version : v0.0.01
# ============================================================

import minescript as m
import math
import sys


# ============================================================
# BASE POSITION
# ============================================================

px, py, pz = m.player().position
x = math.floor(px)
y = math.floor(py)
z = math.floor(pz)


# ============================================================
# SETTINGS
# ============================================================

SET_OFFSETS = [-20, -10, 0, 10, 20]  # 横並び
FRAME_BLOCK = "minecraft:quartz_block"
BASE_BLOCK  = "minecraft:light_gray_concrete"
INPUT_BLOCK = "minecraft:gold_block"
SAMPLE_BLOCK = "minecraft:diamond_block"


# ============================================================
# FLATTEN
# ============================================================

def flatten_area():

    m.execute(f"fill {x-25} {y-1} {z-25} {x+25} {y-1} {z+25} minecraft:grass_block")

    m.execute(f"fill {x-25} {y} {z-25} {x+25} {y+9} {z+25} minecraft:air")
    m.execute(f"fill {x-25} {y+10} {z-25} {x+25} {y+20} {z+25} minecraft:air")

    # 額縁削除
    m.execute(f"kill @e[type=item_frame,x={x-25},y={y-5},z={z-25},dx=50,dy=30,dz=50]")

    m.execute(f"setworldspawn {x} {y} {z}")
    m.execute(f"spawnpoint @a {x} {y} {z}")

    m.echo("Flatten completed.")


# ============================================================
# BUILD ONE SET
# ============================================================

def build_set(offset_x, is_sample=False):

    base_x = x + offset_x
    base_y = y
    base_z = z - 7

    # =========================
    # 土台（5マス横）
    # =========================
    m.execute(
        f"fill {base_x} {base_y} {base_z} "
        f"{base_x+4} {base_y} {base_z} {BASE_BLOCK}"
    )

    # =========================
    # 壁（3x3）
    # =========================
    m.execute(
        f"fill {base_x+1} {base_y+1} {base_z} "
        f"{base_x+3} {base_y+3} {base_z} {FRAME_BLOCK}"
    )

    # =========================
    # 額縁（※必ず外側に出す）
    # =========================
    for dx in range(1,4):
        for dy in range(1,4):
            m.execute(
                f'summon minecraft:item_frame '
                f'{base_x+dx} {base_y+dy} {base_z+1} '
                f'{{Facing:3b}}'
            )

    # =========================
    # 見本セット（中央だけ）
    # =========================
    if is_sample:
        m.execute(
            f"fill {base_x+1} {base_y+1} {base_z} "
            f"{base_x+3} {base_y+3} {base_z} {SAMPLE_BLOCK}"
        )

    # =========================
    # 入力装置
    # =========================
    input_x = base_x + 2
    input_z = base_z + 5

    # 土台
    m.execute(f"setblock {input_x} {base_y} {input_z} {INPUT_BLOCK}")

    # 背面ブロック（重要）
    m.execute(f"setblock {input_x} {base_y+1} {input_z} minecraft:stone")

    # 額縁（外側）
    m.execute(
        f'summon minecraft:item_frame '
        f'{input_x} {base_y+1} {input_z+1} '
        f'{{Facing:3b,Tags:["input_frame"]}}'
    )


# ============================================================
# BUILD ALL
# ============================================================

def build_all():

    for i, offset in enumerate(SET_OFFSETS):
        build_set(offset, is_sample=(i == 2))

    m.echo("Bingo base created.")


# ============================================================
# MAIN
# ============================================================

def main():

    arg = sys.argv[1] if len(sys.argv) > 1 else "flat"

    if arg == "flat":
        flatten_area()
        return

    if arg == "set":
        build_all()
        return


main()
