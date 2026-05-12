import minescript as m
import math

# =========================================
# 基本座標（SOUTH向き前提）
# =========================================
px, py, pz = m.player().position
x = math.floor(px)
y = math.floor(py)
z = math.floor(pz)

FRONT_Z = z + 5   # 前方固定ライン

# =========================================
# 4ブラスターシステム（横展開対応）
# =========================================
def build_furnace_system(offset_x, color):

    base_x = x + offset_x
    base_y = y
    base_z = FRONT_Z

    # --- Layer 1 ---
    m.execute(f"setblock {base_x} {base_y} {base_z} minecraft:{color}_shulker_box")

    m.execute(f"setblock {base_x} {base_y} {base_z+1} minecraft:hopper[facing=north]")
    m.execute(f"setblock {base_x+1} {base_y} {base_z+1} minecraft:hopper[facing=west]")
    m.execute(f"setblock {base_x-1} {base_y} {base_z+1} minecraft:hopper[facing=east]")
    m.execute(f"setblock {base_x} {base_y} {base_z+2} minecraft:hopper[facing=north]")

    # --- Layer 2 ---
    m.execute(f"setblock {base_x+1} {base_y+1} {base_z+1} minecraft:blast_furnace[facing=north]")
    m.execute(f"setblock {base_x} {base_y+1} {base_z+1} minecraft:blast_furnace[facing=north]")
    m.execute(f"setblock {base_x-1} {base_y+1} {base_z+1} minecraft:blast_furnace[facing=north]")

    m.execute(f"setblock {base_x} {base_y+1} {base_z+2} minecraft:hopper")

    # --- Layer 3 ---
    m.execute(f"setblock {base_x} {base_y+2} {base_z+2} minecraft:blast_furnace[facing=north]")

    m.echo(f"{color} furnace built at {base_x} {base_y} {base_z}")


# =========================================
# ダブルチェスト（プレイヤー後ろ）
# =========================================
def place_double_chest():

    cx = x
    cy = y
    cz = z - 2

    m.execute(f"setblock {cx-2} {cy} {cz} minecraft:chest[facing=south,type=right]")
    m.execute(f"setblock {cx-1} {cy} {cz} minecraft:chest[facing=south,type=left]")

    for slot in range(27):
        m.execute(
            f'item replace block {cx-2} {cy} {cz} container.{slot} '
            f'with minecraft:diamond_pickaxe'
            f'[enchantments={{"minecraft:efficiency":5,"minecraft:fortune":3}}] 1'
        )
    for slot in range(27):
        m.execute(
            f'item replace block {cx-1} {cy} {cz} container.{slot} '
            f'with minecraft:diamond_pickaxe'
            f'[enchantments={{"minecraft:efficiency":5,"minecraft:fortune":3}}] 1'
        )

    m.echo("Double chest built.")


# =========================================
# メイン
# =========================================
def main():

    m.execute("tp @p ~ ~ ~ 0 0")

    # 横一列（X方向）
    offsets = [-12, -6, 0, 6, 12]
    colors = ["red", "blue", "green", "yellow", "purple"]

    for offset, color in zip(offsets, colors):
        build_furnace_system(offset, color)

    place_double_chest()

    m.echo("Horizontal furnace line completed.")

main()
