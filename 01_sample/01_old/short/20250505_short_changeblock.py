# import time
# import minescript
# from minescript import execute

# # === 初期設定 ===
# x, y, z = map(int, minescript.player_position())
# execute(f'/tp {x} {y} {z} 0')

# # 鉄ブロック（3×3平面）をプレイヤーの5ブロック前に設置
# for dx in [-1, 0, 1]:
#     for dy in [0, 1, 2]:
#         execute(f"setblock {int(x+dx)} {int(y+dy)} {int(z+5)} white_concrete")

# # 雪玉が白ブロックに当たったら赤ブロックに置換するコマンド
# command = (
#     "execute as @e[type=snowball] at @s "
#     "run fill ~-1 ~-1 ~-1 ~1 ~1 ~1 light_blue_concrete replace white_concrete"
# )

# # コマンドブロック（反復・無条件・常にアクティブ）を6ブロック先に1つ縦に設置
# for i in range(1):
#     cmd = (
#         f'setblock {int(x)} {int(y+i)} {int(z+6)} '
#         f'repeating_command_block{{Command:"{command}",auto:1b,conditional:0b}} replace'
#     )
#     execute(cmd)

# # プレイヤーに雪玉を16個渡す
# execute(f'give @p minecraft:snowball 16')

import minescript
from minescript import execute

# === プレイヤーの位置取得 ===
x, y, z = map(int, minescript.player_position())

# === 白コンクリート 3×3（5ブロック前に縦配置） ===
for dx in [-1, 0, 1]:
    for dy in [0, 1, 2]:
        execute(f"setblock {x+dx} {y+dy} {z+5} white_concrete")

# === コマンド（優先順） ===
commands = [
    # トライデントで水色 → 白
    "execute as @e[type=trident] at @s run fill ~-1 ~-1 ~-1 ~1 ~1 ~1 white_concrete replace light_blue_concrete",

    # トライデントで黄色 → 白
    "execute as @e[type=trident] at @s run fill ~-1 ~-1 ~-1 ~1 ~1 ~1 white_concrete replace yellow_concrete",

    # 矢で白 → 水色
    "execute as @e[type=arrow] at @s run fill ~-1 ~-1 ~-1 ~1 ~1 ~1 light_blue_concrete replace white_concrete",

    # 矢で黄色 → 水色
    "execute as @e[type=arrow] at @s run fill ~-1 ~-1 ~-1 ~1 ~1 ~1 light_blue_concrete replace yellow_concrete",

    # 雪玉で水色 → 黄色
    "execute as @e[type=snowball] at @s run fill ~-1 ~-1 ~-1 ~1 ~1 ~1 yellow_concrete replace light_blue_concrete",

    # 雪玉で白 → 黄色
    "execute as @e[type=snowball] at @s run fill ~-1 ~-1 ~-1 ~1 ~1 ~1 yellow_concrete replace white_concrete",

    # 矢とトライデントを毎tick削除（無条件）
    "kill @e[type=arrow]",
    "kill @e[type=trident]",
]

# === コマンドブロック設置（反復・無条件・常時実行） ===
for i, cmd in enumerate(commands):
    execute(
        f'setblock {x} {y+i-10} {z+6} '
        f'repeating_command_block{{Command:"{cmd}",auto:1b,conditional:0b}} replace'
    )

# === アイテム配布 ===
execute("give @p minecraft:snowball 16")
execute("give @p minecraft:bow 1")
execute("give @p minecraft:arrow 32")
execute("give @p minecraft:trident 8")
