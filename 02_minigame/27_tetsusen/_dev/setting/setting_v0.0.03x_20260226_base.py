# Base Minecraft automation skeleton
import minescript as m
import math

px, py, pz = m.player().position
x = math.floor(px)
y = math.floor(py)
z = math.floor(pz)

# -------------------------
# 各種構築関数
# -------------------------
def flatten_area():
    """整地用"""
    # 地面を草ブロックに
    m.execute(f"fill {x-16} {y-1} {z-22} {x+22} {y-1} {z+22} minecraft:grass_block")
    # 上空を空気に（Y ～ Y+20）
    m.execute(f"fill {x-16} {y} {z-22} {x+22} {y+20} {z+22} minecraft:air")


def place_torches():
    """外周ラインに等間隔でトーチ設置"""
    # X方向：+21 から -12 まで 3刻み
    for dx in range(21, -13, -3):
        # Z方向：+21 から -21 まで 3刻み
        for dz in range(21, -22, -3):
            m.execute(f"setblock {x+dx} {y} {z+dz} minecraft:torch")

def place_sitting_cats():
    """動かない座った猫を設置"""
    for dx in range(18, -13, -6):     # 18 → -12
        for dz in range(18, -19, -6): # 18 → -18
            m.execute(f"summon minecraft:cat {x+dx} {y} {z+dz} {{NoAI:1b,Sitting:1b,Rotation:[180f,0f]}}")

def build_furnace_system(base_x, base_y, base_z, color):
    """溶鉱炉一式とビーコンを設置"""
    # Shulker
    m.execute(f"setblock {base_x} {base_y} {base_z - 1} minecraft:{color}_shulker_box")
    # Hoppers
    m.execute(f"setblock {base_x} {base_y} {base_z} minecraft:hopper[facing=north]")
    m.execute(f"setblock {base_x+1} {base_y} {base_z} minecraft:hopper[facing=west]")
    m.execute(f"setblock {base_x-1} {base_y} {base_z} minecraft:hopper[facing=east]")
    m.execute(f"setblock {base_x} {base_y} {base_z+1} minecraft:hopper[facing=north]")
    # Blast furnaces
    m.execute(f"setblock {base_x+1} {base_y+1} {base_z} minecraft:blast_furnace[facing=north]")
    m.execute(f"setblock {base_x} {base_y+1} {base_z} minecraft:blast_furnace[facing=north]")
    m.execute(f"setblock {base_x-1} {base_y+1} {base_z} minecraft:blast_furnace[facing=north]")
    m.execute(f"setblock {base_x} {base_y+1} {base_z+1} minecraft:hopper")
    m.execute(f"setblock {base_x} {base_y+2} {base_z+1} minecraft:blast_furnace[facing=north]")
    # 地面を色つきのコンクリートブロックに
    m.execute(f"fill {base_x-2} {base_y-1} {base_z-2} {base_x+2} {base_y-1} {base_z+2} minecraft:{color}_concrete")
    # ビーコン設置
    m.execute(f"fill {base_x+6} {base_y-3} {base_z-1} {base_x+8} {base_y-3} {base_z+1} minecraft:iron_block")
    m.execute(f"setblock {base_x+7} {base_y-2} {base_z} minecraft:beacon")
    m.execute(f"setblock {base_x+7} {base_y-1} {base_z} minecraft:{color}_stained_glass")

def fill_double_chest(base_z, item_id, count):
    """
    ダブルチェスト1基を満タンにする
    base_z は右側チェストのZ
    """

    # 右チェスト
    for slot in range(27):
        m.execute(
            f'item replace block {x-2} {y} {z+base_z} container.{slot} '
            f'with minecraft:{item_id} {count}'
        )

    # 左チェスト
    for slot in range(27):
        m.execute(
            f'item replace block {x-2} {y} {z+base_z-1} container.{slot} '
            f'with minecraft:{item_id} {count}'
        )

def place_chest():
    """チェスト設置＋中身充填"""

    bases = [8, 5, 2, -1, -4, -7]  # ダブルチェスト6基
    for base in bases:
        m.execute(f"setblock {x-2} {y} {z+base} minecraft:chest[facing=south,type=right]")
        m.execute(f"setblock {x-2} {y} {z+base-1} minecraft:chest[facing=south,type=left]")
    # for base in range(8, -9, -3):
    #     m.execute(f"setblock {x-2} {y} {z+base} minecraft:chest[facing=south,type=right]")
    #     m.execute(f"setblock {x-2} {y} {z+base-1} minecraft:chest[facing=south,type=left]")

    # -------------------------
    # 左2基 → 乾燥した昆布（64）
    # -------------------------
    fill_double_chest(8, "dried_kelp", 64)
    fill_double_chest(5, "dried_kelp", 64)

    # -------------------------
    # 真ん中2基 → ダイヤピッケル（1）
    # -------------------------
    fill_double_chest(2, "diamond_pickaxe", 1)
    fill_double_chest(-1, "diamond_pickaxe", 1)

    # -------------------------
    # 右2基 → たいまつ（64）
    # -------------------------
    fill_double_chest(-4, "torch", 64)
    fill_double_chest(-7, "torch", 64)

# -------------------------
# メイン処理
# -------------------------
def main():

    m.execute("tp @p ~ ~ ~ 0 0")
    m.execute(f"setworldspawn {x} {y} {z}")

    # 1. 整地
    flatten_area()

    # 2. トーチ
    place_torches()

    # 3. 猫
    place_sitting_cats()

    # 4. 溶鉱炉5個（色違い）
    positions = [
        (x+6, y, z, "red"),
        (x+6, y, z+6, "blue"),
        (x+6, y, z-6, "green"),
        (x+6, y, z+12, "yellow"),
        (x+6, y, z-12, "purple"),
    ]

    for bx, by, bz, color in positions:
        build_furnace_system(bx, by, bz, color)

    # 5. チェスト
    place_chest()

    m.echo("Base setup completed.")
# 実行
main()