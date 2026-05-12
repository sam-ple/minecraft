# ============================================================
# BINGO SYSTEM (CLEAN + GAME)
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

# ============================================================
# BASE POSITION
# ============================================================

px, py, pz = m.player().position
x, y, z = map(math.floor,(px,py,pz))

DATA_FILE = "minescript/data/bingo/positions.json"

# ============================================================
# FLATTEN
# ============================================================

def flatten():
    m.execute(f"fill {x-25} {y-1} {z-25} {x+25} {y-1} {z+25} minecraft:grass_block")

    m.execute(f"fill {x-25} {y} {z-25} {x+25} {y+9} {z+25} minecraft:air")
    m.execute(f"fill {x-25} {y+10} {z-25} {x+25} {y+20} {z+25} minecraft:air")

    m.execute(f"kill @e[type=item_frame,x={x-25},y={y-5},z={z-25},dx=50,dy=30,dz=50]")
    m.execute(f"kill @e[type=glow_item_frame,x={x-25},y={y-5},z={z-25},dx=50,dy=30,dz=50]")
    m.execute("kill @e[type=item_display]")

    m.execute(f"setworldspawn {x} {y} {z}")
    m.execute(f"spawnpoint @a {x} {y} {z}")

# ============================================================
# BUILD
# ============================================================

def build():

    data = []

    for si, offset in enumerate(SET_OFFSETS):

        base_x = x + offset
        base_z = z - 7

        # =========================
        # 土台（3幅に変更）
        # =========================
        m.execute(f"fill {base_x+1} {y} {base_z} {base_x+3} {y} {base_z} {BASE_BLOCK}")

        # 壁（中央3幅）
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
        player = PLAYERS[si] if si < len(PLAYERS) else ""
        color  = COLORS[si % len(COLORS)]

        if player:

            center = set_data[4]
            cx, cy, cz = center["x"], center["y"], center["z"]

            # 色ブロック（上に1段）
            for dx in [-1,0,1]:
                m.execute(f"setblock {cx+dx} {cy+2} {cz-1} minecraft:{color}_concrete")

            # 巨大ヘッド
            head_y = cy + 5

            m.execute(
                f'summon minecraft:item_display {cx} {head_y} {cz-1} '
                f'{{item:{{id:"minecraft:player_head",Count:1b,'
                f'components:{{"minecraft:profile":{{name:"{player}"}}}}}},'
                f'billboard:"fixed",Tags:["big_head_{si}"]}}'
            )

            m.execute(
                f'data modify entity @e[tag=big_head_{si},limit=1] '
                # f'transformation.scale set value [4f,4f,0.1f]'
                f'transformation.scale set value [4f,4f,3f]'
            )

            m.execute(
                f'data merge entity @e[tag=big_head_{si},distance=..40,limit=1] '
                f'{{Rotation:[180f,0f]}}'
            )

            # 入力上ヘッド（反転）
            m.execute(
                f'setblock {ix} {y+2} {iz} '
                f'minecraft:player_head[rotation=8]{{profile:"{player}"}}'
            )

        data.append({
            "set": si,
            "targets": set_data,
            "input_tag": f"input_{si}"
        })

    with open(DATA_FILE,"w") as f:
        json.dump(data,f,indent=4)

# ============================================================
# START（ゲーム処理）
# ============================================================

def start():

    with open(DATA_FILE) as f:
        data = json.load(f)

    while True:

        for entry in data:
            input_tag = entry["input_tag"]

            for i,item in enumerate(BINGO_ITEMS):

                target_tag = f"target_{entry['set']}_{i}"
                target = entry["targets"][i]

                cond = f'@e[type=item_frame,tag={input_tag},nbt={{Item:{{id:"{item}"}}}},tag=!done]'

                # 背面ブロック
                m.execute(
                    f'execute as {cond} run setblock {target["x"]} {target["y"]} {target["z"]-1} minecraft:gold_block'
                )

                # 元の額縁削除
                m.execute(
                    f'execute as {cond} run kill @e[type=item_frame,tag={target_tag},distance=..0.1,limit=1]'
                )

                # 光る額縁
                m.execute(
                    f'execute as {cond} run summon minecraft:glow_item_frame '
                    f'{target["x"]} {target["y"]} {target["z"]} '
                    f'{{Facing:3b,Fixed:1b,Tags:["{target_tag}"],Item:{{id:"{item}",Count:1b}}}}'
                )

                # SE
                m.execute(
                    f'execute as {cond} run playsound minecraft:entity.player.levelup master @a'
                )

                # 入力削除
                m.execute(
                    f'execute as {cond} run data remove entity @s Item'
                )

                # doneタグ
                m.execute(
                    f'execute as {cond} run tag @s add done'
                )

        # doneリセット
        for entry in data:
            m.execute(
                f'execute as @e[type=item_frame,tag={entry["input_tag"]},nbt=!{{Item:{{}}}},tag=done] '
                f'run tag @s remove done'
            )

        time.sleep(0.2)

# =========================
# TEST（アイテム配布）
# =========================
def test():
    for item in BINGO_ITEMS:
        m.execute(f'give @a {item} 10')


# =========================
# MAIN
# =========================
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
