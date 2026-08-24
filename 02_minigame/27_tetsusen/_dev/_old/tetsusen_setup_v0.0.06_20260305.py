import minescript as m
import math
import json
import sys
import os

# =========================================
# JSON保存ディレクトリ
# =========================================
# BASE_DIR = "minescript"
# os.makedirs(BASE_DIR, exist_ok=True)

# FILE_START_POS = f"{BASE_DIR}/tetsusen_start_pos.json"
# FILE_SHULKER = f"{BASE_DIR}/tetsusen_shulker_positions.json"
# FILE_CHUNK = f"{BASE_DIR}/tetsusen_chunk.json"

BASE_DIR = "minescript/data/tetsusen"
os.makedirs(BASE_DIR, exist_ok=True)

FILE_START_POS = f"{BASE_DIR}/start_pos.json"
FILE_SHULKER = f"{BASE_DIR}/shulker_positions.json"
FILE_CHUNK = f"{BASE_DIR}/chunk.json"

COLORS = ["red", "blue", "green", "yellow", "purple"]

# =========================================
# プレイヤー指定（任意）
# =========================================
PLAYERS = [
    "", "saaample", "crocadooo", "", ""
]

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
# def flatten_area():

#     m.execute("gamerule sendCommandFeedback false")
#     m.execute("tp @p ~ ~ ~ 0 30")

#     x_min, x_max = x-25, x+25
#     z_min, z_max = z-25, z+25

#     for xi in range(x_min, x_max+1):
#         for zi in range(z_min, z_max+1):
#             m.execute(f"setblock {xi} {y-1} {zi} minecraft:grass_block")

#     for yi in range(y, y+20):
#         for xi in range(x_min, x_max+1):
#             for zi in range(z_min, z_max+1):
#                 m.execute(f"setblock {xi} {yi} {zi} minecraft:air")

#     m.execute(f"kill @e[type=cat,x={x-25},y={y-5},z={z-25},dx=50,dy=10,dz=50]")
#     m.execute(f"kill @e[type=item,x={x-25},y={y-5},z={z-25},dx=50,dy=10,dz=50]")

#     m.execute(f"setworldspawn {x} {y} {z}")
#     m.execute(f"spawnpoint @p {x} {y} {z}")
#     m.execute(f"setblock {x} {y-1} {z} minecraft:gold_block")

#     with open(FILE_START_POS, "w") as f:
#         json.dump({"x": x, "y": y, "z": z}, f, indent=4)

#     m.echo("Flatten completed + start position saved.")

def flatten_area():

    m.execute("gamerule sendCommandFeedback false")
    m.execute("tp @p ~ ~ ~ 0 30")

    x_min, x_max = x-25, x+25
    z_min, z_max = z-25, z+25

    # 地面
    m.execute(
        f"fill {x_min} {y-1} {z_min} {x_max} {y-1} {z_max} minecraft:grass_block"
    )

    # 空気化
    # for yi in range(y, y+20):
    #     m.execute(
    #         f"fill {x_min} {yi} {z_min} {x_max} {yi} {z_max} minecraft:air"
    #     )

    # 空気化
    m.execute(f"fill {x-25} {y} {z-25} {x+25} {y+9} {z+25} minecraft:air")
    m.execute(f"fill {x-25} {y+10} {z-25} {x+25} {y+20} {z+25} minecraft:air")

    # 猫を上空に飛ばす
    m.execute(f"tp @e[tag=sitting_cat,x={x-25},y={y-5},z={z-25},dx=50,dy=10,dz=50] ~ ~20 ~")

    # 猫をkill
    # m.execute(f"kill @e[type=cat,x={x-25},y={y-5},z={z-25},dx=50,dy=10,dz=50]")
    m.execute(f"kill @e[tag=sitting_cat,x={x-25},y={y+15},z={z-25},dx=50,dy=20,dz=50]")

    # アイテムと額縁を消す
    m.execute(f"kill @e[type=item,x={x-25},y={y-5},z={z-25},dx=50,dy=30,dz=50]")
    m.execute(f"kill @e[type=item_frame,x={x-25},y={y-5},z={z-25},dx=50,dy=30,dz=50]")

    # big_player_head もkill
    m.execute('kill @e[tag=big_player_head]')

    # スポーン位置設定
    m.execute(f"setworldspawn {x} {y} {z}")
    m.execute(f"spawnpoint @p {x} {y} {z}")
    m.execute(f"setblock {x} {y-1} {z} minecraft:gold_block")

    # 開始位置保存
    with open(FILE_START_POS, "w") as f:
        json.dump({"x": x, "y": y, "z": z}, f, indent=4)

    m.echo("Flatten completed + start position saved.")

# =========================================
# ブラスト炉システム
# =========================================
def build_furnace_system(offset_x, color, shulker_list, player_name):

    base_x = x + offset_x
    base_y = y
    base_z = FRONT_Z

    shulker_list.append({
        "color": color,
        "x": base_x,
        "y": base_y,
        "z": base_z,
        "player": player_name
    })

    # for xi in range(base_x-2, base_x+3):
    #     for zi in range(base_z-1, base_z+4):
    #         m.execute(f"setblock {xi} {base_y-1} {zi} minecraft:{color}_concrete")

    m.execute(
        f"fill {base_x-2} {base_y-1} {base_z-1} {base_x+2} {base_y-1} {base_z+3} minecraft:{color}_concrete"
    )

    m.execute(f"setblock {base_x} {base_y} {base_z} minecraft:{color}_shulker_box")
    m.execute(f"setblock {base_x} {base_y} {base_z+1} minecraft:hopper[facing=north]")
    m.execute(f"setblock {base_x+1} {base_y} {base_z+1} minecraft:hopper[facing=west]")
    m.execute(f"setblock {base_x-1} {base_y} {base_z+1} minecraft:hopper[facing=east]")
    m.execute(f"setblock {base_x} {base_y} {base_z+2} minecraft:hopper[facing=north]")

    m.execute(f"setblock {base_x+1} {base_y+1} {base_z+1} minecraft:blast_furnace[facing=north]")
    m.execute(f"setblock {base_x} {base_y+1} {base_z+1} minecraft:blast_furnace[facing=north]")
    m.execute(f"setblock {base_x-1} {base_y+1} {base_z+1} minecraft:blast_furnace[facing=north]")
    m.execute(f"setblock {base_x} {base_y+1} {base_z+2} minecraft:hopper")

    m.execute(f"setblock {base_x} {base_y+2} {base_z+2} minecraft:blast_furnace[facing=north]")

    beacon_x = base_x
    beacon_z = base_z + 7

    for xi in range(beacon_x-1, beacon_x+2):
        for zi in range(beacon_z-1, beacon_z+2):
            m.execute(f"setblock {xi} {base_y-3} {zi} minecraft:iron_block")

    m.execute(f"setblock {beacon_x} {base_y-2} {beacon_z} minecraft:beacon")
    m.execute(f"setblock {beacon_x} {base_y-1} {beacon_z} minecraft:{color}_stained_glass")

# =========================================
# チェスト
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

                m.execute(f'item replace block {cx} {cy} {cz} container.{slot} with minecraft:diamond_pickaxe{ench} 1')
                m.execute(f'item replace block {cx+1} {cy} {cz} container.{slot} with minecraft:diamond_pickaxe{ench} 1')

            else:

                m.execute(f'item replace block {cx} {cy} {cz} container.{slot} with minecraft:{item_id} {count}')
                m.execute(f'item replace block {cx+1} {cy} {cz} container.{slot} with minecraft:{item_id} {count}')

        m.execute(f'summon minecraft:item_frame {cx} {cy} {cz+1} {{Facing:3,Invisible:1b,Item:{{id:"minecraft:{item_id}",Count:1b}}}}')

# =========================================
# トーチ
# =========================================
def place_torches():

    for dx in range(21, -22, -6):
        for dz in range(21, -22, -6):
            m.execute(f"setblock {x+dx} {y} {z+dz} minecraft:torch")

# =========================================
# 猫
# =========================================
def place_sitting_cats():

    for dx in range(19, -18, -6):
        for dz in range(19, -18, -6):
            # m.execute(f"summon minecraft:cat {x+dx} {y} {z+dz} {{NoAI:1b,Sitting:1b,Rotation:[180f,0f]}}")
            # タグ "sitting_cat" を付けて召喚
            m.execute(
                f'summon minecraft:cat {x+dx} {y} {z+dz} '
                f'{{NoAI:1b,Sitting:1b,Rotation:[180f,0f],Tags:["sitting_cat"]}}'
            )

# =========================================
# メイン
# =========================================
def main():

    arg = sys.argv[1] if len(sys.argv) > 1 else "set"

    if arg == "flat":
        flatten_area()
        return

    if arg == "set":

        m.execute("forceload remove all")
        m.execute(f"forceload add {x-32} {z-32} {x+32} {z+32}")

        with open(FILE_CHUNK, "w") as f:
            json.dump({
                "x1": x-32,
                "z1": z-32,
                "x2": x+32,
                "z2": z+32
            }, f, indent=4)

        furnace_offsets = [-12, -6, 0, 6, 12]
        # colors = ["red", "blue", "green", "yellow", "purple"]

        shulker_positions = []

        for i, (offset, color) in enumerate(zip(furnace_offsets, COLORS)):

            player_name = ""

            if i < len(PLAYERS):
                player_name = PLAYERS[i]

            build_furnace_system(offset, color, shulker_positions, player_name)

        place_all_chests_horizontal()
        place_torches()
        place_sitting_cats()

        with open(FILE_SHULKER, "w") as f:
            json.dump(shulker_positions, f, indent=4)

        m.echo("FULL BASE completed + JSON exported.")

    if arg == "set2":

        with open(FILE_SHULKER) as f:
            data = json.load(f)

        for entry in data:

            if entry["player"]:

                m.execute(
                    f'setblock {entry["x"]} {entry["y"]+2} {entry["z"]} '
                    f'minecraft:player_head[rotation=0]{{profile:"{entry["player"]}"}} replace'
                )

        m.echo("Player heads placed.")

    if arg == "set3":

        with open(FILE_SHULKER) as f:
            data = json.load(f)

        for entry in data:

            if not entry["player"]:
                continue

            head_x = entry["x"]
            head_y = entry["y"] + 10
            head_z = entry["z"] + 2

            m.execute(
                f'summon minecraft:item_display {head_x} {head_y} {head_z} '
                f'{{item:{{id:"minecraft:player_head",Count:1b,'
                f'components:{{"minecraft:profile":{{name:"{entry["player"]}"}}}}}},'
                f'billboard:"fixed",Tags:["big_player_head"]}}'
            )

            m.execute(
                f'data modify entity '
                f'@e[tag=big_player_head,x={head_x},y={head_y},z={head_z},distance=..1,limit=1] '
                f'transformation.scale set value [6f,6f,1f]'
            )

        m.echo("Big player heads placed.")

main()
