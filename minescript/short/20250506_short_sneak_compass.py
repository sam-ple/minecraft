from minescript import execute
import minescript

x, y, z = map(int, minescript.player_position())
tp_x, tp_y, tp_z = x, y, z

# スコアボード初期化（初回のみ）
execute('scoreboard objectives add isSneaking minecraft.custom:minecraft.sneak_time')

# コマンド①：しゃがみ + コンパスでTP
tp_command = (
    'execute as @p[nbt={SelectedItem:{id:"minecraft:compass"}}] '
    f'if score @s isSneaking matches 1.. run tp @s {tp_x} {tp_y} {tp_z}'
)
tp_escaped = tp_command.replace('"', '\\"')

execute(
    f'setblock {x-1} {y-1} {z+3} repeating_command_block{{Command:"{tp_escaped}",auto:1b,conditional:0b}} replace'
)

# コマンド②：スコアリセット
reset_command = 'scoreboard players set @a isSneaking 0'
reset_escaped = reset_command.replace('"', '\\"')

execute(
    f'setblock {x-1} {y-1} {z+4} repeating_command_block{{Command:"{reset_escaped}",auto:1b,conditional:0b}} replace'
)

# コンパス支給
execute("give @p minecraft:compass 1")
