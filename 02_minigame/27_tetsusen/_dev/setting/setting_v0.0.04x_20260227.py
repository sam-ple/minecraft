import minescript as m
import math

px, py, pz = m.player().position
x, y, z = math.floor(px), math.floor(py), math.floor(pz)

# -------------------------
# 整地（小分け設置で安全）
# -------------------------
# fillだと重する為、setblockで小分けにして設置する。
# 地面は草ブロック、上空は空気にする。
# なお、時間がかかる為、特定のキーを押したら次に進むかチャットを取得して次に進むが安全。
def flatten_area():
    x_min, x_max = x-16, x+22
    z_min, z_max = z-22, z+22
    y_ground = y-1
    y_air_top = y+20

    # 地面
    for xi in range(x_min, x_max+1):
        for zi in range(z_min, z_max+1):
            m.execute(f"setblock {xi} {y_ground} {zi} minecraft:grass_block")
    # 上空の空気
    for yi in range(y, y_air_top+1):
        for xi in range(x_min, x_max+1):
            for zi in range(z_min, z_max+1):
                m.execute(f"setblock {xi} {yi} {zi} minecraft:air")

# -------------------------
# トーチ
# -------------------------
def place_torches():
    for dx in range(21, -13, -3):
        for dz in range(21, -22, -3):
            m.execute(f"setblock {x+dx} {y} {z+dz} minecraft:torch")

# -------------------------
# 座った猫
# -------------------------
def place_sitting_cats():
    for dx in range(18, -13, -6):
        for dz in range(18, -19, -6):
            m.execute(f"summon minecraft:cat {x+dx} {y} {z+dz} {{NoAI:1b,Sitting:1b,Rotation:[180f,0f]}}")

# -------------------------
# 4ブラスターシステム（South固定）
# -------------------------
def build_furnace_system(base_x, base_y, base_z, color):
    # Shulker
    m.execute(f"setblock {base_x} {base_y} {base_z} minecraft:{color}_shulker_box")
    # Hoppers
    m.execute(f"setblock {base_x} {base_y} {base_z+1} minecraft:hopper[facing=north]")
    m.execute(f"setblock {base_x+1} {base_y} {base_z+1} minecraft:hopper[facing=west]")
    m.execute(f"setblock {base_x-1} {base_y} {base_z+1} minecraft:hopper[facing=east]")
    m.execute(f"setblock {base_x} {base_y} {base_z+2} minecraft:hopper[facing=north]")
    # Blast furnaces
    m.execute(f"setblock {base_x+1} {base_y+1} {base_z+1} minecraft:blast_furnace[facing=north]")
    m.execute(f"setblock {base_x} {base_y+1} {base_z+1} minecraft:blast_furnace[facing=north]")
    m.execute(f"setblock {base_x-1} {base_y+1} {base_z+1} minecraft:blast_furnace[facing=north]")
    m.execute(f"setblock {base_x} {base_y+2} {base_z+2} minecraft:blast_furnace[facing=north]")
    # 地面色
    for xi in range(base_x-2, base_x+3):
        for zi in range(base_z-1, base_z+4):
            m.execute(f"setblock {xi} {base_y-1} {zi} minecraft:{color}_concrete")
    # ビーコン
    for xi in range(base_x+6, base_x+9):
        for zi in range(base_z, base_z+3):
            m.execute(f"setblock {xi} {base_y-3} {zi} minecraft:iron_block")
    m.execute(f"setblock {base_x+7} {base_y-2} {base_z+1} minecraft:beacon")
    m.execute(f"setblock {base_x+7} {base_y-1} {base_z+1} minecraft:{color}_stained_glass")

# -------------------------
# チェスト（South固定）
# -------------------------
def place_chests():
    bases = [8, 5, 2, -1, -4, -7]  # ダブルチェスト6基
    for base in bases:
        m.execute(f"setblock {x-2} {y} {z+base} minecraft:chest[facing=south,type=right]")
        m.execute(f"setblock {x-2} {y} {z+base-1} minecraft:chest[facing=south,type=left]")
    # 中身（エンチャント済みダイヤピッケルに変更）
    def fill_double_chest(base_z, item_id, count, enchantments=None):
        for slot in range(27):
            ench = ""
            if enchantments:
                ench_list = [f'"{k}":{v}' for k, v in enchantments.items()]
                ench = f'[enchantments={{' + ",".join(ench_list) + '}}]'
            m.execute(
                f'item replace block {x-2} {y} {z+base_z} container.{slot} '
                f'with minecraft:{item_id}{ench} {count}'
            )
            m.execute(
                f'item replace block {x-2} {y} {z+base_z-1} container.{slot} '
                f'with minecraft:{item_id}{ench} {count}'
            )

    fill_double_chest(8, "dried_kelp", 64)
    fill_double_chest(5, "dried_kelp", 64)
    fill_double_chest(2, "diamond_pickaxe", 1, {"minecraft:efficiency":5,"minecraft:fortune":3})
    fill_double_chest(-1, "diamond_pickaxe", 1, {"minecraft:efficiency":5,"minecraft:fortune":3})
    fill_double_chest(-4, "torch", 64)
    fill_double_chest(-7, "torch", 64)

# -------------------------
# メイン
# -------------------------
def main():
    m.execute("tp @p ~ ~ ~ 0 0")
    m.execute(f"setworldspawn {x} {y} {z}")
    flatten_area()
    place_torches()
    place_sitting_cats()

    # 5つの色違い溶鉱炉システム
    positions = [
        (x+6, y, z, "red"),
        (x+6, y, z+6, "blue"),
        (x+6, y, z-6, "green"),
        (x+6, y, z+12, "yellow"),
        (x+6, y, z-12, "purple"),
    ]
    for bx, by, bz, color in positions:
        build_furnace_system(bx, by, bz, color)

    place_chests()
    m.echo("Base setup completed.")

main()
