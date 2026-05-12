# ============================================================
# BINGO SYSTEM (FINAL COMPLETE)
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
# FLATTEN
# ============================================================

def flatten():
    m.execute(f"fill {x-25} {y-1} {z-25} {x+25} {y-1} {z+25} minecraft:grass_block")
    m.execute(f"fill {x-25} {y} {z-25} {x+25} {y+10} {z+25} minecraft:air")

    m.execute(f"kill @e[type=item_frame,x={x-25},y={y-5},z={z-25},dx=50,dy=30,dz=50]")
    m.execute(f"kill @e[type=glow_item_frame,x={x-25},y={y-5},z={z-25},dx=50,dy=30,dz=50]")
    m.execute("kill @e[type=item_display]")

    m.execute(f"setworldspawn {x} {y} {z}")
    m.execute(f"spawnpoint @a {x} {y} {z}")

# ============================================================
# BUILD（UI付き）
# ============================================================

def build():

    data = []

    for si, offset in enumerate(SET_OFFSETS):

        base_x = x + offset
        base_z = z - 7

        # 土台
        m.execute(f"fill {base_x+1} {y} {base_z} {base_x+3} {y} {base_z} {BASE_BLOCK}")
        m.execute(f"fill {base_x+1} {y+1} {base_z} {base_x+3} {y+3} {base_z} {FRAME_BLOCK}")

        set_data = []

        # 3x3
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

        # 入力
        ix = base_x
        iz = base_z

        m.execute(f"setblock {ix} {y} {iz} {INPUT_BLOCK}")
        m.execute(f"setblock {ix} {y+1} {iz} minecraft:stone")

        m.execute(
            f'summon minecraft:item_frame {ix} {y+1} {iz+1} '
            f'{{Facing:3b,Tags:["input_{si}"]}}'
        )

        # =========================
        # UI
        # =========================
        player = PLAYERS[si]
        color  = COLORS[si % len(COLORS)]

        if player:

            center = set_data[4]
            cx, cy, cz = center["x"], center["y"], center["z"]

            for dx in [-1,0,1]:
                m.execute(f"setblock {cx+dx} {cy+2} {cz-1} minecraft:{color}_concrete")

            head_y = cy + 5

            m.execute(
                f'summon minecraft:item_display {cx} {head_y} {cz-1} '
                f'{{item:{{id:"minecraft:player_head",Count:1b,'
                f'components:{{"minecraft:profile":{{name:"{player}"}}}}}},'
                f'billboard:"fixed",Tags:["big_head_{si}"]}}'
            )

            # ★ エラー防止（distance指定）
            m.execute(
                f'execute as @e[tag=big_head_{si},distance=..50] run '
                f'data modify entity @s transformation.scale set value [4f,4f,3f]'
            )

            m.execute(
                f'execute as @e[tag=big_head_{si},distance=..50] run '
                f'data merge entity @s {{Rotation:[180f,0f]}}'
            )

            m.execute(
                f'setblock {ix} {y+2} {iz} '
                f'minecraft:player_head[rotation=8]{{profile:"{player}"}}'
            )

        data.append({
            "set": si,
            "targets": set_data,
            "input_tag": f"input_{si}"
        })

    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE,"w") as f:
        json.dump(data,f,indent=4)

# ============================================================
# START（完全安定版）
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
                tag = f"target_{entry['set']}_{i}"

                cond = f'@e[type=item_frame,tag={input_tag},nbt={{Item:{{id:"{item}"}}}},tag=!done]'

                m.execute(f'execute as {cond} run setblock {target["x"]} {target["y"]} {target["z"]-1} minecraft:gold_block')

                # ★ エラー防止（distance必須）
                m.execute(f'execute as {cond} run kill @e[type=item_frame,tag={tag},distance=..1,limit=1]')

                m.execute(
                    f'execute as {cond} run summon minecraft:glow_item_frame '
                    f'{target["x"]} {target["y"]} {target["z"]} '
                    f'{{Facing:3b,Fixed:1b,Tags:["{tag}"],Item:{{id:"{item}",Count:1b}}}}'
                )

                m.execute(f'execute as {cond} run playsound minecraft:entity.player.levelup master @a')
                m.execute(f'execute as {cond} run data remove entity @s Item')
                m.execute(f'execute as {cond} run tag @s add done')

        # doneリセット
        for entry in data:
            m.execute(
                f'execute as @e[type=item_frame,tag={entry["input_tag"]},nbt=!{{Item:{{}}}},tag=done] '
                f'run tag @s remove done'
            )

        # =========================
        # ビンゴ判定（タグ方式）
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

                m.execute(
                    f'execute '
                    f'if block {a["x"]} {a["y"]} {a["z"]-1} minecraft:gold_block '
                    f'if block {b["x"]} {b["y"]} {b["z"]-1} minecraft:gold_block '
                    f'if block {c["x"]} {c["y"]} {c["z"]-1} minecraft:gold_block '
                    f'run tag @a[tag=!bingo_{si}] add bingo_{si}'
                )

            # ★ 1回だけ発火
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

            m.execute(
                f'tag @a[tag=bingo_{si},tag=!bingo_done_{si}] add bingo_done_{si}'
            )

        time.sleep(0.2)

# ============================================================
# TEST
# ============================================================

def test():
    for item in BINGO_ITEMS:
        m.execute(f'give @a {item} 10')

# ============================================================
# MAIN
# ============================================================

def main():
    arg = sys.argv[1] if len(sys.argv)>1 else "flat"

    if arg=="flat":
        flatten()
    elif arg=="set":
        build()
    elif arg=="start":
        start()
    elif arg=="test":
        test()

main()
