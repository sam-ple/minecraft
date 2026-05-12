# ============================================================
# BINGO SYSTEM (EXECUTE BLOCK VERSION - FINAL STABLE)
# ============================================================

import minescript as m
import math, sys, json, time, os

# ============================================================
# SETTINGS
# ============================================================

SET_OFFSETS = [-20, -10, 0, 10, 20]

BINGO_ITEMS = [
    "minecraft:apple","minecraft:bread","minecraft:carrot",
    "minecraft:potato","minecraft:golden_apple","minecraft:cooked_beef",
    "minecraft:cooked_porkchop","minecraft:melon_slice","minecraft:cookie",
]

COLORS = ["red","blue","green","yellow","purple"]
PLAYERS = ["","crocadooo","saaample","",""]

FRAME_BLOCK = "minecraft:white_stained_glass"
BASE_BLOCK  = "minecraft:quartz_block"
INPUT_BLOCK = "minecraft:emerald_block"

px, py, pz = m.player().position
x, y, z = map(math.floor,(px,py,pz))

DATA_FILE = "minescript/data/bingo/positions.json"

# ============================================================
# BUILD
# ============================================================

def build():

    data = []

    for si, offset in enumerate(SET_OFFSETS):

        base_x = x + offset
        base_z = z - 7

        m.execute(f"fill {base_x+1} {y} {base_z} {base_x+3} {y} {base_z} {BASE_BLOCK}")
        m.execute(f"fill {base_x+1} {y+1} {base_z} {base_x+3} {y+3} {base_z} {FRAME_BLOCK}")

        set_data = []

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

        ix = base_x
        iz = base_z

        m.execute(f"setblock {ix} {y} {iz} {INPUT_BLOCK}")
        m.execute(f"setblock {ix} {y+1} {iz} minecraft:stone")

        m.execute(
            f'summon minecraft:item_frame {ix} {y+1} {iz+1} '
            f'{{Facing:3b,Tags:["input_{si}"]}}'
        )

        data.append({
            "set": si,
            "targets": set_data,
            "input_tag": f"input_{si}"
        })

    with open(DATA_FILE,"w") as f:
        json.dump(data,f,indent=4)

# ============================================================
# START
# ============================================================

def start():

    with open(DATA_FILE) as f:
        data = json.load(f)

    lines = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]

    while True:

        # =========================
        # 通常処理
        # =========================
        for entry in data:
            input_tag = entry["input_tag"]

            for i,item in enumerate(BINGO_ITEMS):

                target = entry["targets"][i]
                target_tag = f"target_{entry['set']}_{i}"

                cond = f'@e[type=item_frame,tag={input_tag},nbt={{Item:{{id:"{item}"}}}},tag=!done]'

                m.execute(
                    f'execute as {cond} run setblock {target["x"]} {target["y"]} {target["z"]-1} minecraft:gold_block'
                )

                m.execute(
                    f'execute as {cond} run kill @e[type=item_frame,tag={target_tag},distance=..0.1,limit=1]'
                )

                m.execute(
                    f'execute as {cond} run summon minecraft:glow_item_frame '
                    f'{target["x"]} {target["y"]} {target["z"]} '
                    f'{{Facing:3b,Fixed:1b,Tags:["{target_tag}"],Item:{{id:"{item}",Count:1b}}}}'
                )

                m.execute(
                    f'execute as {cond} run playsound minecraft:entity.player.levelup master @a'
                )

                m.execute(
                    f'execute as {cond} run data remove entity @s Item'
                )

                m.execute(
                    f'execute as {cond} run tag @s add done'
                )

        # =========================
        # BINGO判定（タグ方式）
        # =========================
        for entry in data:

            si = entry["set"]
            player = PLAYERS[si]

            if not player:
                continue

            for line in lines:

                a = entry["targets"][line[0]]
                b = entry["targets"][line[1]]
                c = entry["targets"][line[2]]

                # 条件成立 → bingocheck付与
                m.execute(
                    f'execute '
                    f'if block {a["x"]} {a["y"]} {a["z"]-1} minecraft:gold_block '
                    f'if block {b["x"]} {b["y"]} {b["z"]-1} minecraft:gold_block '
                    f'if block {c["x"]} {c["y"]} {c["z"]-1} minecraft:gold_block '
                    f'run tag @a[tag=!bingo_{si}] add bingo_{si}'
                )

            # 発火処理（1回だけ）
            m.execute(
                f'execute as @a[tag=bingo_{si},tag=!bingo_done_{si}] run '
                f'title @a title {{"text":"{player}","color":"gold","bold":true}}'
            )

            m.execute(
                f'execute as @a[tag=bingo_{si},tag=!bingo_done_{si}] run '
                f'title @a subtitle {{"text":"BINGO!!!!!!","color":"green","bold":true}}'
            )

            m.execute(
                f'execute as @a[tag=bingo_{si},tag=!bingo_done_{si}] run '
                f'playsound minecraft:ui.toast.challenge_complete master @a'
            )

            # 完了タグ付与
            m.execute(
                f'tag @a[tag=bingo_{si},tag=!bingo_done_{si}] add bingo_done_{si}'
            )

        time.sleep(0.2)

# ============================================================
# MAIN
# ============================================================

def main():
    arg = sys.argv[1] if len(sys.argv)>1 else "set"

    if arg=="set":
        build()
    elif arg=="start":
        start()

main()
