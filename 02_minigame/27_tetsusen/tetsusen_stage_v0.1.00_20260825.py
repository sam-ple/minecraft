# ============================================================
# TETSUSEN BASE GENERATOR
# Version : v0.1.00
# Date: 2026-08-25
#
# Minecraft Java Edition + MineScript
#
# File
#   tetsusen_stage.py : 鉄千ゲーム用ステージ生成
#
# Features
#   ・フィールド整地
#   ・焼き場5個の生成
#   ・シェルカー生成
#   ・焼き場選択ボタン設置
#   ・ホッパー生成
#   ・溶鉱炉生成
#   ・ビーコン生成
#   ・チェスト・物資生成
#   ・松明設置
#   ・装飾猫設置
#   ・forceload設定
#
# Notes
#   ・ゲームロジックはSkript側で管理
#   ・プレイヤーヘッドはSkript側で管理
#   ・forceloadはMineScript側で管理
#   ・JSON保存なし
#
# Author : crocado
# ============================================================

import minescript as m
import math


# ============================================================
# GAME SETTINGS
# ============================================================

COLORS = [
    "red",
    "blue",
    "green",
    "yellow",
    "purple",
]


# ============================================================
# BASE POSITION
# ============================================================

px, py, pz = m.player().position

x = math.floor(px)
y = math.floor(py)
z = math.floor(pz)

FRONT_Z = z + 5
CHEST_Z = z - 2


# ============================================================
# FORCELOAD
# ============================================================

def setup_forceload():

    # --------------------------------------------------------
    # Remove existing force-loaded chunks
    #
    # 旧Minescript版と同じ方式
    # --------------------------------------------------------

    m.execute(
        "forceload remove all"
    )

    # --------------------------------------------------------
    # Force-load TETSUSEN area
    #
    # 現在動作確認済みの範囲をそのまま使用
    #
    # X : x-32 ～ x+32
    # Z : z-32 ～ z+32
    #
    # ※この段階では範囲を縮小しない
    # --------------------------------------------------------

    m.execute(
        f"forceload add "
        f"{x-32} {z-32} "
        f"{x+32} {z+32}"
    )


# ============================================================
# FIELD FLATTEN
# ============================================================

def flatten_area():

    # --------------------------------------------------------
    # gamerule compatibility
    # --------------------------------------------------------

    m.execute(
        "gamerule send_command_feedback false"
    )


    # --------------------------------------------------------
    # Player orientation
    # --------------------------------------------------------

    m.execute(
        "tp @p ~ ~ ~ 0 30"
    )


    # --------------------------------------------------------
    # Field
    # --------------------------------------------------------

    x_min = x - 25
    x_max = x + 25

    z_min = z - 25
    z_max = z + 25


    # --------------------------------------------------------
    # Ground
    # --------------------------------------------------------

    m.execute(
        f"fill "
        f"{x_min} {y-1} {z_min} "
        f"{x_max} {y-1} {z_max} "
        f"minecraft:grass_block"
    )


    # --------------------------------------------------------
    # Clear building area
    # --------------------------------------------------------

    m.execute(
        f"fill "
        f"{x-25} {y} {z-25} "
        f"{x+25} {y+9} {z+25} "
        f"minecraft:air"
    )

    m.execute(
        f"fill "
        f"{x-25} {y+10} {z-25} "
        f"{x+25} {y+20} {z+25} "
        f"minecraft:air"
    )


    # --------------------------------------------------------
    # Remove existing cats
    # --------------------------------------------------------

    m.execute(
        f"tp @e[tag=sitting_cat,"
        f"x={x-25},y={y-5},z={z-25},"
        f"dx=50,dy=10,dz=50] ~ ~20 ~"
    )

    m.execute(
        f"kill @e[tag=sitting_cat,"
        f"x={x-25},y={y+15},z={z-25},"
        f"dx=50,dy=20,dz=50]"
    )


    # --------------------------------------------------------
    # Remove dropped items / item frames
    # --------------------------------------------------------

    m.execute(
        f"kill @e[type=item,"
        f"x={x-25},y={y-5},z={z-25},"
        f"dx=50,dy=30,dz=50]"
    )

    m.execute(
        f"kill @e[type=item_frame,"
        f"x={x-25},y={y-5},z={z-25},"
        f"dx=50,dy=30,dz=50]"
    )


    # --------------------------------------------------------
    # Spawn
    # --------------------------------------------------------

    m.execute(
        f"setworldspawn {x} {y} {z}"
    )

    m.execute(
        f"spawnpoint @p {x} {y} {z}"
    )


    # --------------------------------------------------------
    # Starting point marker
    # --------------------------------------------------------

    m.execute(
        f"setblock "
        f"{x} {y-1} {z} "
        f"minecraft:gold_block"
    )


# ============================================================
# BLAST FURNACE / SHULKER SYSTEM
# ============================================================

def build_furnace_system(offset_x, color):

    base_x = x + offset_x
    base_y = y
    base_z = FRONT_Z


    # --------------------------------------------------------
    # Colored floor
    # --------------------------------------------------------

    m.execute(
        f"fill "
        f"{base_x-2} {base_y-1} {base_z-1} "
        f"{base_x+2} {base_y-1} {base_z+3} "
        f"minecraft:{color}_concrete"
    )


    # --------------------------------------------------------
    # Shulker
    # --------------------------------------------------------

    m.execute(
        f"setblock "
        f"{base_x} {base_y} {base_z} "
        f"minecraft:{color}_shulker_box[facing=north]"
    )


    # --------------------------------------------------------
    # Selection button
    #
    # Shulker is facing north.
    # Button is placed directly in front of it.
    # --------------------------------------------------------

    m.execute(
        f"setblock "
        f"{base_x} {base_y} {base_z-1} "
        f"minecraft:stone_button[facing=north]"
    )


    # --------------------------------------------------------
    # Lower hopper system
    # --------------------------------------------------------

    m.execute(
        f"setblock "
        f"{base_x} {base_y} {base_z+1} "
        f"minecraft:hopper[facing=north]"
    )

    m.execute(
        f"setblock "
        f"{base_x+1} {base_y} {base_z+1} "
        f"minecraft:hopper[facing=west]"
    )

    m.execute(
        f"setblock "
        f"{base_x-1} {base_y} {base_z+1} "
        f"minecraft:hopper[facing=east]"
    )

    m.execute(
        f"setblock "
        f"{base_x} {base_y} {base_z+2} "
        f"minecraft:hopper[facing=north]"
    )


    # --------------------------------------------------------
    # Blast furnaces
    # --------------------------------------------------------

    m.execute(
        f"setblock "
        f"{base_x+1} {base_y+1} {base_z+1} "
        f"minecraft:blast_furnace[facing=north]"
    )

    m.execute(
        f"setblock "
        f"{base_x} {base_y+1} {base_z+1} "
        f"minecraft:blast_furnace[facing=north]"
    )

    m.execute(
        f"setblock "
        f"{base_x-1} {base_y+1} {base_z+1} "
        f"minecraft:blast_furnace[facing=north]"
    )


    # --------------------------------------------------------
    # Upper hopper
    # --------------------------------------------------------

    m.execute(
        f"setblock "
        f"{base_x} {base_y+1} {base_z+2} "
        f"minecraft:hopper"
    )


    # --------------------------------------------------------
    # Top blast furnace
    # --------------------------------------------------------

    m.execute(
        f"setblock "
        f"{base_x} {base_y+2} {base_z+2} "
        f"minecraft:blast_furnace[facing=north]"
    )


    # --------------------------------------------------------
    # Beacon
    # --------------------------------------------------------

    beacon_x = base_x
    beacon_z = base_z + 7


    for xi in range(
        beacon_x - 1,
        beacon_x + 2
    ):

        for zi in range(
            beacon_z - 1,
            beacon_z + 2
        ):

            m.execute(
                f"setblock "
                f"{xi} {base_y-3} {zi} "
                f"minecraft:iron_block"
            )


    m.execute(
        f"setblock "
        f"{beacon_x} {base_y-2} {beacon_z} "
        f"minecraft:beacon"
    )

    m.execute(
        f"setblock "
        f"{beacon_x} {base_y-1} {beacon_z} "
        f"minecraft:{color}_stained_glass"
    )


# ============================================================
# CHEST SUPPLIES
# ============================================================

def place_all_chests_horizontal():

    offsets_x = [
        -8,
        -5,
        -2,
        1,
        4,
        7
    ]

    contents = [
        ("dried_kelp", 64),
        ("dried_kelp", 64),
        ("diamond_pickaxe", 1),
        ("diamond_pickaxe", 1),
        ("torch", 64),
        ("torch", 64),
    ]


    for offset_x, content in zip(
        offsets_x,
        contents
    ):

        cx = x + offset_x
        cy = y
        cz = CHEST_Z


        # ----------------------------------------------------
        # Double chest
        # ----------------------------------------------------

        m.execute(
            f"setblock "
            f"{cx} {cy} {cz} "
            f"minecraft:chest[facing=south,type=right]"
        )

        m.execute(
            f"setblock "
            f"{cx+1} {cy} {cz} "
            f"minecraft:chest[facing=south,type=left]"
        )


        item_id, count = content


        # ----------------------------------------------------
        # Fill chest
        # ----------------------------------------------------

        for slot in range(27):

            if item_id == "diamond_pickaxe":

                ench = (
                    '[enchantments='
                    '{"minecraft:efficiency":5,'
                    '"minecraft:fortune":3}]'
                )


                m.execute(
                    f'minecraft:item replace block '
                    f'{cx} {cy} {cz} '
                    f'container.{slot} '
                    f'with minecraft:diamond_pickaxe'
                    f'{ench} 1'
                )

                m.execute(
                    f'minecraft:item replace block '
                    f'{cx+1} {cy} {cz} '
                    f'container.{slot} '
                    f'with minecraft:diamond_pickaxe'
                    f'{ench} 1'
                )


            else:

                m.execute(
                    f'minecraft:item replace block '
                    f'{cx} {cy} {cz} '
                    f'container.{slot} '
                    f'with minecraft:{item_id} {count}'
                )

                m.execute(
                    f'minecraft:item replace block '
                    f'{cx+1} {cy} {cz} '
                    f'container.{slot} '
                    f'with minecraft:{item_id} {count}'
                )


        # ----------------------------------------------------
        # Invisible item frame
        # ----------------------------------------------------

        m.execute(
            f'summon minecraft:item_frame '
            f'{cx} {cy} {cz+1} '
            f'{{Facing:3,Invisible:1b,'
            f'Item:{{id:"minecraft:{item_id}",Count:1b}}}}'
        )


# ============================================================
# LIGHTING
# ============================================================

def place_torches():

    for dx in range(
        21,
        -22,
        -6
    ):

        for dz in range(
            21,
            -22,
            -6
        ):

            m.execute(
                f"setblock "
                f"{x+dx} {y} {z+dz} "
                f"minecraft:torch"
            )


# ============================================================
# DECORATION CATS
# ============================================================

def place_sitting_cats():

    for dx in range(
        19,
        -18,
        -6
    ):

        for dz in range(
            19,
            -18,
            -6
        ):

            m.execute(
                f"summon minecraft:cat "
                f"{x+dx} {y} {z+dz} "
                f'{{NoAI:1b,Sitting:1b,'
                f'Silent:1b,Rotation:[180f,0f],'
                f'Tags:["sitting_cat"]}}'
            )


# ============================================================
# MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # 0. FORCELOAD
    #
    # 旧バージョンで動作確認済みの範囲をそのまま使用
    #
    # IMPORTANT:
    # /forceload はチャンク単位。
    # この段階では範囲を縮小しない。
    # --------------------------------------------------------

    setup_forceload()


    # --------------------------------------------------------
    # 1. Flatten
    # --------------------------------------------------------

    flatten_area()


    # --------------------------------------------------------
    # 2. Build five furnace stations
    # --------------------------------------------------------

    furnace_offsets = [
        -12,
        -6,
        0,
        6,
        12
    ]


    for offset, color in zip(
        furnace_offsets,
        COLORS
    ):

        build_furnace_system(
            offset,
            color
        )


    # --------------------------------------------------------
    # 3. Supplies
    # --------------------------------------------------------

    place_all_chests_horizontal()


    # --------------------------------------------------------
    # 4. Lighting
    # --------------------------------------------------------

    place_torches()


    # --------------------------------------------------------
    # 5. Decoration
    # --------------------------------------------------------

    place_sitting_cats()


    # --------------------------------------------------------
    # Complete
    # --------------------------------------------------------

    m.echo(
        "TETSUSEN STAGE completed."
    )


# ============================================================
# RUN
# ============================================================

main()
