import minescript as m
import math
import json
import sys

# =========================================
# 基本座標（SOUTH向き前提）
# =========================================
px, py, pz = m.player().position
x = math.floor(px)
y = math.floor(py)
z = math.floor(pz)

FRONT_Z = z + 5
CHEST_Z = z - 2

# =========================================
# 整地
# =========================================
def flatten_area():

    x_min, x_max = x-20, x+20
    z_min, z_max = z-20, z+20

    for xi in range(x_min, x_max+1):
        for zi in range(z_min, z_max+1):
            m.execute(f"setblock {xi} {y-1} {zi} minecraft:grass_block")

    for yi in range(y, y+20):
        for xi in range(x_min, x_max+1):
            for zi in range(z_min, z_max+1):
                m.execute(f"setblock {xi} {yi} {zi} minecraft:air")

    # ドロップアイテム削除（範囲限定）
    m.execute(
        f"kill @e[type=item,"
        f"x={x-20},y={y-5},z={z-20},"
        f"dx=40,dy=30,dz=40]"
    )

    m.execute(f"setblock {x} {y-1} {z} minecraft:gold_block")

    m.echo("Flatten completed + dropped items cleared.")

# =========================================
# 4ブラスターシステム + 色床 + ビーコン
# =========================================
def build_furnace_system(offset_x, color, shulker_list):

    base_x = x + offset_x
    base_y = y
    base_z = FRONT_Z

    # JSON保存用
    shulker_list.append({
        "color": color,
        "x": base_x,
        "y": base_y,
        "z": base_z
    })

    # -------------------------
    # 床（色コンクリ 5x5）
    # -------------------------
    for xi in range(base_x-2, base_x+3):
        for zi in range(base_z-1, base_z+4):
            m.execute(f"setblock {xi} {base_y-1} {zi} minecraft:{color}_concrete")

    # -------------------------
    # Layer 1
    # -------------------------
    m.execute(f"setblock {base_x} {base_y} {base_z} minecraft:{color}_shulker_box")
    m.execute(f"setblock {base_x} {base_y} {base_z+1} minecraft:hopper[facing=north]")
    m.execute(f"setblock {base_x+1} {base_y} {base_z+1} minecraft:hopper[facing=west]")
    m.execute(f"setblock {base_x-1} {base_y} {base_z+1} minecraft:hopper[facing=east]")
    m.execute(f"setblock {base_x} {base_y} {base_z+2} minecraft:hopper[facing=north]")

    # -------------------------
    # Layer 2
    # -------------------------
    m.execute(f"setblock {base_x+1} {base_y+1} {base_z+1} minecraft:blast_furnace[facing=north]")
    m.execute(f"setblock {base_x} {base_y+1} {base_z+1} minecraft:blast_furnace[facing=north]")
    m.execute(f"setblock {base_x-1} {base_y+1} {base_z+1} minecraft:blast_furnace[facing=north]")
    m.execute(f"setblock {base_x} {base_y+1} {base_z+2} minecraft:hopper")

    # -------------------------
    # Layer 3
    # -------------------------
    m.execute(f"setblock {base_x} {base_y+2} {base_z+2} minecraft:blast_furnace[facing=north]")

    # -------------------------
    # ビーコン
    # -------------------------
    beacon_x = base_x
    beacon_z = base_z + 7

    for xi in range(beacon_x-1, beacon_x+2):
        for zi in range(beacon_z-1, beacon_z+2):
            m.execute(f"setblock {xi} {base_y-3} {zi} minecraft:iron_block")

    m.execute(f"setblock {beacon_x} {base_y-2} {beacon_z} minecraft:beacon")
    m.execute(f"setblock {beacon_x} {base_y-1} {beacon_z} minecraft:{color}_stained_glass")


# =========================================
# ダブルチェスト6基（横一列・間1マス）
# =========================================
def place_all_chests_horizontal():

    offsets_x = [-8, -5, -2, 1, 4, 7]

    contents = [
        ("dried_kelp", 64),
        ("dried_kelp", 64),
        ("diamond_pickaxe", 1),
        ("diamond_pickaxe", 1),
        ("torch", 64),
        ("torch", 64),
    ]

    for offset_x, content in zip(offsets_x, contents):

        cx = x + offset_x
        cy = y
        cz = CHEST_Z

        m.execute(f"setblock {cx} {cy} {cz} minecraft:chest[facing=south,type=right]")
        m.execute(f"setblock {cx+1} {cy} {cz} minecraft:chest[facing=south,type=left]")

        item_id, count = content

        for slot in range(27):

            if item_id == "diamond_pickaxe":

                ench = '[enchantments={"minecraft:efficiency":5,"minecraft:fortune":3}]'

                m.execute(
                    f'item replace block {cx} {cy} {cz} container.{slot} '
                    f'with minecraft:diamond_pickaxe{ench} 1'
                )
                m.execute(
                    f'item replace block {cx+1} {cy} {cz} container.{slot} '
                    f'with minecraft:diamond_pickaxe{ench} 1'
                )
            else:
                m.execute(
                    f'item replace block {cx} {cy} {cz} container.{slot} '
                    f'with minecraft:{item_id} {count}'
                )
                m.execute(
                    f'item replace block {cx+1} {cy} {cz} container.{slot} '
                    f'with minecraft:{item_id} {count}'
                )


# =========================================
# メイン
# =========================================
def main():

    arg = "set"
    if len(sys.argv) > 1:
        arg = sys.argv[1]

    if arg == "flat":
        m.execute("gamerule sendCommandFeedback false")
        m.execute("tp @p ~ ~ ~ 0 30")
        m.execute(f"setworldspawn {x} {y} {z}")
        flatten_area()
        return

    if arg == "set":

        m.execute("gamerule sendCommandFeedback false")
        m.execute("tp @p ~ ~ ~ 0 30")
        m.execute(f"setworldspawn {x} {y} {z}")

        furnace_offsets = [-12, -6, 0, 6, 12]
        colors = ["red", "blue", "green", "yellow", "purple"]

        shulker_positions = []

        for offset, color in zip(furnace_offsets, colors):
            build_furnace_system(offset, color, shulker_positions)

        place_all_chests_horizontal()

        # JSON出力
        BASE_DIR = "minescript"
        with open(f"{BASE_DIR}/shulker_positions.json", "w") as f:
            json.dump(shulker_positions, f, indent=4)

        m.echo("FULL BASE completed + JSON exported.")

    if arg == "start":
        m.echo("Game Start (future expansion).")


main()
