# ============================================================
# BINGO SYSTEM (CLEAN BUILD)
# ============================================================

import minescript as m
import math, sys, json, time, os

# ============================================================
# SETTINGS
# ============================================================

SET_OFFSETS = [-20, -10, 0, 10, 20]

BINGO_ITEMS = [
    "minecraft:apple","minecraft:bread","minecraft:carrot",
    "minecraft:potato","minecraft:cooked_beef",
    "minecraft:cooked_porkchop","minecraft:melon_slice",
    "minecraft:cookie","minecraft:beetroot_soup",
]

COLORS = ["red","blue","green","yellow","purple"]

PLAYERS = ["saaample","crocadooo","","",""]

FRAME_BLOCK = "minecraft:quartz_block"
BASE_BLOCK  = "minecraft:light_gray_concrete"
INPUT_BLOCK = "minecraft:gold_block"

# ============================================================
# BASE POSITION
# ============================================================

px, py, pz = m.player().position
x, y, z = map(math.floor,(px,py,pz))

# ============================================================
# FLATTEN
# ============================================================

def flatten():
    m.execute(f"fill {x-25} {y-1} {z-25} {x+25} {y-1} {z+25} minecraft:grass_block")

    m.execute(f"fill {x-25} {y} {z-25} {x+25} {y+9} {z+25} minecraft:air")
    m.execute(f"fill {x-25} {y+10} {z-25} {x+25} {y+20} {z+25} minecraft:air")

    m.execute(f"kill @e[type=item_frame,x={x-25},y={y-5},z={z-25},dx=50,dy=30,dz=50]")
    m.execute("kill @e[type=item_display]")


    m.execute(f"setworldspawn {x} {y} {z}")
    m.execute(f"spawnpoint @a {x} {y} {z}")

# ============================================================
# BUILD（完全新規配置ロジック）
# ============================================================

def build():

    data = []

    for si, offset in enumerate(SET_OFFSETS):

        base_x = x + offset
        base_z = z - 7

        # =========================
        # 土台
        # =========================
        m.execute(f"fill {base_x} {y} {base_z} {base_x+4} {y} {base_z} {BASE_BLOCK}")

        # 壁
        m.execute(f"fill {base_x+1} {y+1} {base_z} {base_x+3} {y+3} {base_z} {FRAME_BLOCK}")

        set_data = []

        # =========================
        # 3x3額縁
        # =========================
        for idx in range(9):

            dx = idx % 3
            dy = idx // 3

            fx = base_x + 1 + dx
            fy = y + 3 - dy
            fz = base_z + 1

            m.execute(
                f'summon minecraft:item_frame {fx} {fy} {fz} '
                f'{{Facing:3b,Fixed:1b,Tags:["target_{si}_{idx}"]}}'
            )

            set_data.append({"x":fx,"y":fy,"z":fz})

        # =========================
        # 入力装置
        # =========================
        ix = base_x + 2
        iz = base_z + 5

        m.execute(f"setblock {ix} {y} {iz} {INPUT_BLOCK}")
        m.execute(f"setblock {ix} {y+1} {iz} minecraft:stone")

        m.execute(
            f'summon minecraft:item_frame {ix} {y+1} {iz+1} '
            f'{{Facing:3b,Tags:["input_{si}"]}}'
        )

        # =========================
        # ▼ 上部UI（修正版）
        # =========================

        player = PLAYERS[si] if si < len(PLAYERS) else ""
        color  = COLORS[si % len(COLORS)]

        if player:

            center = set_data[4]
            cx, cy, cz = center["x"], center["y"], center["z"]

            # =========================
            # 色ブロック（+1上げる）
            # =========================
            for dx in [-1, 0, 1]:
                m.execute(
                    f"setblock {cx+dx} {cy+2} {cz-1} minecraft:{color}_concrete"
                )

            # =========================
            # 巨大プレイヤーヘッド
            # =========================
            head_y = cy + 5

            # 召喚
            m.execute(
                f'summon minecraft:item_display {cx} {head_y} {cz-1} '
                f'{{item:{{id:"minecraft:player_head",Count:1b,'
                f'components:{{"minecraft:profile":{{name:"{player}"}}}}}},'
                f'billboard:"fixed",Tags:["big_head_{si}"]}}'
            )

            # サイズ
            m.execute(
                f'data modify entity @e[tag=big_head_{si},limit=1] '
                f'transformation.scale set value [4f,4f,0.1f]'
            )

            # =========================
            # 入力上ヘッド（向き反転）
            # =========================
            m.execute(
                f'setblock {ix} {y+2} {iz} '
                f'minecraft:player_head[rotation=8]{{profile:"{player}"}}'
            )


        # =========================

        data.append({
            "set": si,
            "targets": set_data,
            "input_tag": f"input_{si}"
        })

    # 保存（後で使う）
    with open("minescript/data/bingo/positions.json","w") as f:
        json.dump(data,f,indent=4)

# ============================================================
# MAIN
# ============================================================

def main():
    arg = sys.argv[1] if len(sys.argv)>1 else "flat"

    if arg=="flat":
        flatten()
    elif arg=="set":
        build()

main()
