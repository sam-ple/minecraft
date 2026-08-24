import minescript as m
import math
import json
import sys
import time

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
def flatten_area():

    m.execute("gamerule sendCommandFeedback false")
    m.execute("tp @p ~ ~ ~ 0 30")

    x_min, x_max = x-25, x+25
    z_min, z_max = z-25, z+25

    for xi in range(x_min, x_max+1):
        for zi in range(z_min, z_max+1):
            m.execute(f"setblock {xi} {y-1} {zi} minecraft:grass_block")

    for yi in range(y, y+20):
        for xi in range(x_min, x_max+1):
            for zi in range(z_min, z_max+1):
                m.execute(f"setblock {xi} {yi} {zi} minecraft:air")

    # 猫削除（範囲限定）
    m.execute(
        f"kill @e[type=cat,"
        f"x={x-25},y={y-5},z={z-25},"
        f"dx=50,dy=10,dz=50]"
    )

    # ドロップアイテム削除（範囲限定）
    m.execute(
        f"kill @e[type=item,"
        f"x={x-25},y={y-5},z={z-25},"
        f"dx=50,dy=10,dz=50]"
    )

    # ワールドスポーン（中央固定）
    m.execute(f"setworldspawn {x} {y} {z}")
    # プレイヤースポーン固定
    m.execute(f"spawnpoint @p {x} {y} {z}")
    # 足元に金ブロック
    m.execute(f"setblock {x} {y-1} {z} minecraft:gold_block")

    m.echo("Flatten completed + dropped items cleared.")

# =========================================
# 4ブラスターシステム + 色床 + ビーコン
# =========================================
def build_furnace_system(offset_x, color, shulker_list):

    base_x = x + offset_x
    base_y = y
    base_z = FRONT_Z

    # JSON保存用
    shulker_list.append({
        "color": color,
        "x": base_x,
        "y": base_y,
        "z": base_z,
        "player": None
    })

    # -------------------------
    # 床（色コンクリ 5x5）
    # -------------------------
    for xi in range(base_x-2, base_x+3):
        for zi in range(base_z-1, base_z+4):
            m.execute(f"setblock {xi} {base_y-1} {zi} minecraft:{color}_concrete")

    # -------------------------
    # Layer 1
    # -------------------------
    m.execute(f"setblock {base_x} {base_y} {base_z} minecraft:{color}_shulker_box")
    m.execute(f"setblock {base_x} {base_y} {base_z+1} minecraft:hopper[facing=north]")
    m.execute(f"setblock {base_x+1} {base_y} {base_z+1} minecraft:hopper[facing=west]")
    m.execute(f"setblock {base_x-1} {base_y} {base_z+1} minecraft:hopper[facing=east]")
    m.execute(f"setblock {base_x} {base_y} {base_z+2} minecraft:hopper[facing=north]")

    # -------------------------
    # Layer 2
    # -------------------------
    m.execute(f"setblock {base_x+1} {base_y+1} {base_z+1} minecraft:blast_furnace[facing=north]")
    m.execute(f"setblock {base_x} {base_y+1} {base_z+1} minecraft:blast_furnace[facing=north]")
    m.execute(f"setblock {base_x-1} {base_y+1} {base_z+1} minecraft:blast_furnace[facing=north]")
    m.execute(f"setblock {base_x} {base_y+1} {base_z+2} minecraft:hopper")

    # -------------------------
    # Layer 3
    # -------------------------
    m.execute(f"setblock {base_x} {base_y+2} {base_z+2} minecraft:blast_furnace[facing=north]")

    # -------------------------
    # ビーコン
    # -------------------------
    beacon_x = base_x
    beacon_z = base_z + 7

    for xi in range(beacon_x-1, beacon_x+2):
        for zi in range(beacon_z-1, beacon_z+2):
            m.execute(f"setblock {xi} {base_y-3} {zi} minecraft:iron_block")

    m.execute(f"setblock {beacon_x} {base_y-2} {beacon_z} minecraft:beacon")
    m.execute(f"setblock {beacon_x} {base_y-1} {beacon_z} minecraft:{color}_stained_glass")


# =========================================
# ダブルチェスト6基（横一列・間1マス）
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

                m.execute(
                    f'item replace block {cx} {cy} {cz} container.{slot} '
                    f'with minecraft:diamond_pickaxe{ench} 1'
                )
                m.execute(
                    f'item replace block {cx+1} {cy} {cz} container.{slot} '
                    f'with minecraft:diamond_pickaxe{ench} 1'
                )

            else:
                m.execute(
                    f'item replace block {cx} {cy} {cz} container.{slot} '
                    f'with minecraft:{item_id} {count}'
                )
                m.execute(
                    f'item replace block {cx+1} {cy} {cz} container.{slot} '
                    f'with minecraft:{item_id} {count}'
                )

        # -------------------------
        # 額縁追加
        # -------------------------
        m.execute(
            f'summon minecraft:item_frame {cx} {cy} {cz+1} '
            f'{{Facing:3,Invisible:1b,Item:{{id:"minecraft:{item_id}",Count:1b}}}}'
        )

# -------------------------
# トーチ
# -------------------------
def place_torches():
    for dx in range(21, -13, -6):
        for dz in range(21, -22, -6):
            m.execute(f"setblock {x+dx} {y} {z+dz} minecraft:torch")

# -------------------------
# 座った猫
# -------------------------
def place_sitting_cats():
    for dx in range(19, -12, -6):
        for dz in range(19, -18, -6):
            m.execute(f"summon minecraft:cat {x+dx} {y} {z+dz} {{NoAI:1b,Sitting:1b,Rotation:[180f,0f]}}")

    # for dx in range(17, -14, -6):
    #     for dz in range(17, -20, -6):
    #         m.execute(f"summon minecraft:cat {x+dx} {y} {z+dz} {{NoAI:1b,Sitting:1b,Rotation:[180f,0f]}}")

# =========================================
# メイン
# =========================================
def main():

    arg = "set"
    if len(sys.argv) > 1:
        arg = sys.argv[1]

    if arg == "flat":
        flatten_area()
        return

    if arg == "set":

        m.execute(f"forceload add {x-32} {z-32} {x+32} {z+32}")

        furnace_offsets = [-12, -6, 0, 6, 12]
        colors = ["red", "blue", "green", "yellow", "purple"]

        shulker_positions = []

        for offset, color in zip(furnace_offsets, colors):
            build_furnace_system(offset, color, shulker_positions)

        place_all_chests_horizontal()

        place_torches()
        place_sitting_cats()

        # JSON出力
        BASE_DIR = "minescript"
        with open(f"{BASE_DIR}/shulker_positions.json", "w") as f:
            json.dump(shulker_positions, f, indent=4)

        m.echo("FULL BASE completed + JSON exported.")

    if arg == "set2":

        BASE_DIR = "minescript"

        with open(f"{BASE_DIR}/shulker_positions.json") as f:
            data = json.load(f)

        for entry in data:

            if entry["player"]:

                px = entry["x"]
                py = entry["y"]
                pz = entry["z"]

                player = entry["player"]

                # /setblock ~ ~ ~ player_head[rotation=0]{profile:"crocadooo"} replace
                # シュルカーの1ブロック上
                m.execute(
                    f'setblock {px} {py+1} {pz} '
                    f'minecraft:player_head[rotation=0]{{profile:"{player}"}} replace'
                )

        m.echo("Player heads placed.")

    if arg == "start":

        BASE_DIR = "minescript"
        SLOT_COUNT = 27

        # -------------------------
        # JSON読み込み
        # -------------------------
        with open(f"{BASE_DIR}/shulker_positions.json") as f:
            data = json.load(f)

        SHULKER_MAP = {}

        for entry in data:
            player = entry.get("player")
            if player:
                SHULKER_MAP[player] = (
                    entry["x"],
                    entry["y"],
                    entry["z"]
                )

        if not SHULKER_MAP:
            m.echo("No players defined in JSON.")
            return

        m.echo("Game Start.")

        # -------------------------
        # scoreboard準備
        # -------------------------
        m.execute("scoreboard objectives remove iron")
        m.execute("scoreboard objectives remove temp")

        m.execute("scoreboard objectives add iron dummy")
        m.execute("scoreboard objectives add temp dummy")

        m.execute(
            'scoreboard objectives modify iron displayname '
            '{"text":"Iron Ingots","color":"gold"}'
        )

        m.execute("scoreboard objectives setdisplay sidebar iron")

        # -------------------------
        # 監視ループ開始
        # -------------------------
        while True:

            for PLAYER, (X, Y, Z) in SHULKER_MAP.items():

                # 合計リセット
                m.execute(f"scoreboard players set {PLAYER} iron 0")

                for i in range(SLOT_COUNT):

                    m.execute(f"scoreboard players set {PLAYER} temp 0")

                    m.execute(
                        f'execute if data block {X} {Y} {Z} '
                        f'Items[{{Slot:{i}b,id:"minecraft:iron_ingot"}}] '
                        f'run execute store result score {PLAYER} temp run '
                        f'data get block {X} {Y} {Z} '
                        f'Items[{{Slot:{i}b,id:"minecraft:iron_ingot"}}].count'
                    )

                    m.execute(
                        f"scoreboard players operation {PLAYER} iron += {PLAYER} temp"
                    )

                # アクションバー表示（本人のみ）
                m.execute(
                    f'execute as {PLAYER} run title {PLAYER} actionbar '
                    f'{{"text":"Iron: ","color":"gold",'
                    f'"extra":[{{"score":{{"name":"{PLAYER}","objective":"iron"}}}}]}}'
                )

            time.sleep(1)

main()
