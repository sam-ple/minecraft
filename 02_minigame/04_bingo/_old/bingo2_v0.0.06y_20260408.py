# ============================================================
# BINGO SYSTEM (STABLE BASE)
# ============================================================

import minescript as m
import math, sys, json, time, os

# ============================================================
# DATA
# ============================================================

BASE_DIR = "minescript/data/bingo"
os.makedirs(BASE_DIR, exist_ok=True)
FILE_POS = f"{BASE_DIR}/positions.json"

SET_OFFSETS = [-20, -10, 0, 10, 20]

BINGO_ITEMS = [
    "minecraft:apple","minecraft:bread","minecraft:carrot",
    "minecraft:potato","minecraft:cooked_beef",
    "minecraft:cooked_porkchop","minecraft:melon_slice",
    "minecraft:cookie","minecraft:beetroot_soup",
]

FRAME_BLOCK = "minecraft:quartz_block"
BASE_BLOCK = "minecraft:light_gray_concrete"
INPUT_BLOCK = "minecraft:gold_block"

COLORS = ["red","blue","green","yellow","purple"]

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
    m.execute(f"setworldspawn {x} {y} {z}")
    m.execute(f"spawnpoint @a {x} {y} {z}")

# ============================================================
# BUILD
# ============================================================

def build(players=None):
    data = []

    for si, offset in enumerate(SET_OFFSETS):
        base_x = x + offset
        base_z = z - 7

        # 土台
        m.execute(f"fill {base_x} {y} {base_z} {base_x+4} {y} {base_z} {BASE_BLOCK}")

        # 壁
        m.execute(f"fill {base_x+1} {y+1} {base_z} {base_x+3} {y+3} {base_z} {FRAME_BLOCK}")

        set_data=[]
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

            set_data.append({"index": idx,"x": fx,"y": fy,"z": fz})

        # 入力装置
        ix = base_x + 2
        iz = base_z + 5

        m.execute(f"setblock {ix} {y} {iz} {INPUT_BLOCK}")
        m.execute(f"setblock {ix} {y+1} {iz} minecraft:stone")

        m.execute(
            f'summon minecraft:item_frame {ix} {y+1} {iz+1} '
            f'{{Facing:3b,Tags:["input_{si}"]}}'
        )

        entry = {
            "set": si,
            "targets": set_data,
            "input_tag": f"input_{si}",
            "player": players[si] if players and si < len(players) else ""
        }

        data.append(entry)

    with open(FILE_POS,"w") as f:
        json.dump(data,f,indent=4)

# ============================================================
# SET2（位置完全修正版）
# ============================================================

def set2():
    with open(FILE_POS) as f:
        data = json.load(f)

    for si, entry in enumerate(data):
        player = entry.get("player","")
        if not player:
            continue

        center = entry["targets"][4]
        cx, cy, cz = center["x"], center["y"], center["z"]

        # 色ブロック（ズレ修正済）
        color = COLORS[si % len(COLORS)]
        for dx in range(-1, 2):
            m.execute(f"setblock {cx+dx} {cy+3} {cz} minecraft:{color}_concrete")

        # 巨大ヘッド
        head_y = cy + 8

        m.execute(
            f'summon minecraft:item_display {cx} {head_y} {cz} '
            f'{{item:{{id:"minecraft:player_head",Count:1b,'
            f'components:{{"minecraft:profile":{{name:"{player}"}}}}}},'
            f'billboard:"fixed",Tags:["big_head_{si}"]}}'
        )

        m.execute(
            f'data modify entity @e[tag=big_head_{si},limit=1,sort=nearest] '
            f'transformation.scale set value [6f,6f,1f]'
        )

        # 入力ヘッド（ズレ修正）
        ix = cx
        iz = cz + 4

        m.execute(
            f'setblock {ix} {y+2} {iz} minecraft:player_head[rotation=0]{{profile:"{player}"}} replace'
        )

# ============================================================
# START（安定版）
# ============================================================

def start():
    with open(FILE_POS) as f:
        data = json.load(f)

    while True:
        for entry in data:
            input_tag = entry["input_tag"]

            for i,item in enumerate(BINGO_ITEMS):
                target_tag = f"target_{entry['set']}_{i}"
                target = entry["targets"][i]

                condition = f'@e[type=item_frame,tag={input_tag},nbt={{Item:{{id:"{item}"}}}},tag=!done]'

                # 背面ブロック
                m.execute(
                    f'execute as {condition} run setblock {target["x"]} {target["y"]} {target["z"]-1} minecraft:gold_block'
                )

                # 額縁削除
                m.execute(
                    f'execute as {condition} run kill @e[type=item_frame,tag={target_tag},distance=..0.1,limit=1]'
                )

                # 光る額縁
                m.execute(
                    f'execute as {condition} run summon minecraft:glow_item_frame '
                    f'{target["x"]} {target["y"]} {target["z"]} '
                    f'{{Facing:3b,Fixed:1b,Tags:["{target_tag}","done"],Item:{{id:"{item}",Count:1b}}}}'
                )

                # SE
                m.execute(
                    f'execute as {condition} run playsound minecraft:entity.player.levelup master @a'
                )

                # 入力削除
                m.execute(
                    f'execute as {condition} run data remove entity @s Item'
                )

                # doneタグ
                m.execute(
                    f'execute as {condition} run tag @s add done'
                )

        # doneリセット
        for entry in data:
            m.execute(
                f'execute as @e[type=item_frame,tag={entry["input_tag"]},nbt=!{{Item:{{}}}},tag=done] '
                f'run tag @s remove done'
            )

        time.sleep(0.2)

# ============================================================
# MAIN
# ============================================================

def main():
    arg = sys.argv[1] if len(sys.argv)>1 else "flat"

    if arg=="flat":
        flatten()
    elif arg=="set":
        players = ["saaample","crocadooo","","",""]
        build(players)
    elif arg=="set2":
        set2()
    elif arg=="start":
        start()

main()
