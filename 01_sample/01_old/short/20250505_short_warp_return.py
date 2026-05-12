import minescript
from minescript import execute

# === プレイヤー位置（初期設定）取得 ===
x, y, z = map(int, minescript.player_position())

# プレイヤーを南向きに（基準を固定）
minescript.execute(f"/tp @p {x} {y} {z} 0 0")

# プレイヤーの南側（前方）
dx, dz = 1, 3
block_x = x + dx
block_y = y + 2
block_z = z + dz

minescript.execute(f"/setblock {block_x} {block_y} {block_z} minecraft:pale_oak_wood")
minescript.execute(f"/setblock {block_x} {block_y - 1} {block_z} minecraft:pale_oak_wood")
minescript.execute(f"/setblock {block_x} {block_y - 1} {block_z - 1} minecraft:pale_oak_button[facing=north]")
minescript.execute(f"/setblock {block_x} {block_y} {block_z - 1} minecraft:pale_oak_wall_sign[facing=north]{{Text1:'{{\"text\":\"テレポート\"}}'}}")
# コマンドブロックを設置（地下）
minescript.execute(f"/setblock {block_x} {block_y - 2} {block_z} minecraft:command_block")
# 中身のコマンドを設定（テレポート）
minescript.execute(f"/data merge block {block_x} {block_y - 2} {block_z} {{Command:'/tp @p -196 65 84'}}")

# === テレポート先座標（スポーン地点や任意の座標に変更可） ===
tp_x, tp_y, tp_z = x, y, z  # 今回はプレイヤーの初期位置に設定

# === コマンドブロックを設置して雪玉検知＆ワープ ===
command = (
    f"execute as @e[type=snowball] at @s run tp @p[distance=..3] {tp_x} {tp_y} {tp_z}"
)

# コマンドブロック設置（反復・無条件・常時実行）
execute(
    f'setblock {x-1} {y} {z+3} repeating_command_block{{Command:"{command}",auto:1b,conditional:0b}} replace'
)

# 雪玉支給
execute("give @p minecraft:snowball 16")
