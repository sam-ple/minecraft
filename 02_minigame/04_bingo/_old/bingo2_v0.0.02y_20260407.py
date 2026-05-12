# ============================================================
# BINGO SYSTEM (BASE + GAME)
# Version : v0.0.02
# ============================================================

import minescript as m
import math
import sys
import json
import time
import os

# ============================================================
# DATA
# ============================================================

BASE_DIR = "minescript/data/bingo"
os.makedirs(BASE_DIR, exist_ok=True)

FILE_POS = f"{BASE_DIR}/positions.json"

# ============================================================
# SETTINGS
# ============================================================

SET_OFFSETS = [-20, -10, 0, 10, 20]

BINGO_ITEMS = [
    "minecraft:apple", "minecraft:bread", "minecraft:carrot",
    "minecraft:potato", "minecraft:cooked_beef",
    "minecraft:cooked_porkchop", "minecraft:melon_slice",
    "minecraft:cookie", "minecraft:beetroot_soup",
]

FRAME_BLOCK = "minecraft:quartz_block"
BASE_BLOCK  = "minecraft:light_gray_concrete"
INPUT_BLOCK = "minecraft:gold_block"
TARGET_BLOCK = "minecraft:emerald_block"

# ============================================================
# BASE POSITION
# ============================================================

px, py, pz = m.player().position
x, y, z = map(math.floor, (px, py, pz))

# ============================================================
# FLATTEN
# ============================================================

def flatten():

    m.execute(f"fill {x-25} {y-1} {z-25} {x+25} {y-1} {z+25} minecraft:grass_block")
    m.execute(f"fill {x-25} {y} {z-25} {x+25} {y+9} {z+25} minecraft:air")
    m.execute(f"fill {x-25} {y+10} {z-25} {x+25} {y+20} {z+25} minecraft:air")

    m.execute(f"kill @e[type=item_frame,x={x-25},y={y-5},z={z-25},dx=50,dy=30,dz=50]")

    m.execute(f"setworldspawn {x} {y} {z}")
    m.execute(f"spawnpoint @a {x} {y} {z}")

    m.echo("FLATTEN DONE")

# ============================================================
# BUILD
# ============================================================

def build():

    data = []

    for si, offset in enumerate(SET_OFFSETS):

        base_x = x + offset
        base_z = z - 7

        # 土台
        m.execute(f"fill {base_x} {y} {base_z} {base_x+4} {y} {base_z} {BASE_BLOCK}")

        # 壁
        m.execute(f"fill {base_x+1} {y+1} {base_z} {base_x+3} {y+3} {base_z} {FRAME_BLOCK}")

        set_data = []

        # 3x3
        idx = 0
        for dx in range(1,4):
            for dy in range(1,4):

                fx = base_x + dx
                fy = y + dy
                fz = base_z + 1

                # 額縁
                m.execute(
                    f'summon minecraft:item_frame {fx} {fy} {fz} '
                    f'{{Facing:3b,Tags:["target_{si}_{idx}"]}}'
                )

                set_data.append({
                    "index": idx,
                    "x": fx,
                    "y": fy,
                    "z": fz
                })

                idx += 1

        # 入力
        ix = base_x + 2
        iz = base_z + 5

        m.execute(f"setblock {ix} {y} {iz} {INPUT_BLOCK}")
        m.execute(f"setblock {ix} {y+1} {iz} minecraft:stone")

        m.execute(
            f'summon minecraft:item_frame {ix} {y+1} {iz+1} '
            f'{{Facing:3b,Tags:["input_{si}"]}}'
        )

        data.append({
            "set": si,
            "targets": set_data,
            "input": {"x": ix, "y": y+1, "z": iz+1}
        })

    with open(FILE_POS, "w") as f:
        json.dump(data, f, indent=4)

    m.echo("BUILD DONE + JSON saved")

# ============================================================
# GAME LOOP
# ============================================================

def start():

    with open(FILE_POS) as f:
        data = json.load(f)

    while True:

        for s in data:

            si = s["set"]

            for i, item in enumerate(BINGO_ITEMS):

                target = s["targets"][i]

                tx, ty, tz = target["x"], target["y"], target["z"]

                input_tag = f"input_{si}"
                target_tag = f"target_{si}_{i}"

                # =========================
                # 入力 → 反映
                # =========================
                m.execute(
                    f'execute as @e[type=item_frame,tag={input_tag},'
                    f'nbt={{Item:{{id:"{item}"}}}},tag=!done] '
                    f'run data merge entity @e[type=item_frame,tag={target_tag},limit=1] '
                    f'{{Item:{{id:"{item}",Count:1b}}}}'
                )

                # ブロック変化
                m.execute(
                    f'execute as @e[type=item_frame,tag={input_tag},'
                    f'nbt={{Item:{{id:"{item}"}}}},tag=!done] '
                    f'run setblock {tx} {ty-1} {tz} {TARGET_BLOCK}'
                )

                # 演出
                m.execute(
                    f'execute as @e[type=item_frame,tag={input_tag},'
                    f'nbt={{Item:{{id:"{item}"}}}},tag=!done] '
                    f'run playsound minecraft:entity.player.levelup master @a'
                )

                # 入力削除
                m.execute(
                    f'execute as @e[type=item_frame,tag={input_tag},'
                    f'nbt={{Item:{{id:"{item}"}}}},tag=!done] '
                    f'run data remove entity @s Item'
                )

                # done
                m.execute(
                    f'execute as @e[type=item_frame,tag={input_tag},'
                    f'nbt={{Item:{{id:"{item}"}}}},tag=!done] '
                    f'run tag @s add done'
                )

                # リセット
                m.execute(
                    f'execute as @e[type=item_frame,tag={input_tag},nbt=!{{Item:{{}}}},tag=done] '
                    f'run tag @s remove done'
                )

        time.sleep(0.2)

# ============================================================
# MAIN
# ============================================================

def main():

    arg = sys.argv[1] if len(sys.argv) > 1 else "flat"

    if arg == "flat":
        flatten()

    elif arg == "set":
        build()

    elif arg == "start":
        start()

main()
