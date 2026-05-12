# /give @p minecraft:pale_oak_sign
# /data get block -25 71 9
# /summon armor_stand ~ ~ ~ {ShowArms:1b}
# /give @p minecraft:piglin_head
# /give @p minecraft:golden_chestplate
# /give @p minecraft:golden_leggings
# /give @p minecraft:golden_boots
# /give @p minecraft:golden_sword
# /data get entity @e[type=minecraft:armor_stand,sort=nearest,limit=1]
# /data get entity @p
# /data get entity @p equipment
# /data get entity sampleeeeeee equipment


# ===========================
from sys import argv, exit
from minescript import execute, player_position ,echo
import math
import json

arg1 = argv[1] if len(argv) > 1 else (echo("コマンドを指定してください。") or exit(1))

# ---------------------------------------------------
# 看板
# ---------------------------------------------------
if arg1 == "sign":
    # プレイヤーの現在位置
    x, y, z = map(math.floor, player_position())

    # 看板設置位置
    sign_x, sign_y, sign_z = x, y, z

    # 看板を設置（正面：プレイヤーから見える方向）
    execute(f'setblock {sign_x} {sign_y} {sign_z} minecraft:pale_oak_sign[rotation=0]')

    # JSON形式のテキストをPython辞書で定義（文字列ではない）
    sign_data = {
        "front_text": {
            "color": "black",
            "has_glowing_text": 0,
            "messages": [
                {"text": ""},
                {"text": "テスト"},
                {"text": ""},
                {"text": ""}
            ]
        }
    }

    # JSON文字列に変換（ダブルクォートのエスケープ不要）
    sign_data_str = json.dumps(sign_data, separators=(',', ':'))

    # 最後のコマンドは囲わない（文字列としてではなくJSON構造として解釈させる）
    execute(f'data merge block {sign_x} {sign_y} {sign_z} {sign_data_str}')

# ---------------------------------------------------
# アーマースタンド
# ---------------------------------------------------
elif arg1 == "armorstand":
    # プレイヤーの足元に召喚
    x, y, z = map(math.floor, player_position())

    # NBTデータをPython辞書で記述
    nbt = {
        "ShowArms": 1,
        "Invisible": 0,
        "Small": 0,
        "NoBasePlate": 0,
        "equipment": {
            "mainhand": {"id": "minecraft:golden_sword", "count": 1},
            "head": {"id": "minecraft:piglin_head", "count": 1},
            "chest": {"id": "minecraft:golden_chestplate", "count": 1},
            "legs": {"id": "minecraft:golden_leggings", "count": 1},
            "feet": {"id": "minecraft:golden_boots", "count": 1}
        }
    }

    # JSONからNBT形式へ変換（itemNBTは構造が特殊）
    nbt_str = json.dumps(nbt, separators=(',', ':'))

    # summonコマンドを実行
    execute(f'summon armor_stand {x} {y} {z} {nbt_str}')

# ---------------------------------------------------
# 未対応
# ---------------------------------------------------
else:
    echo(f"未対応のコマンドです: {arg1}")

