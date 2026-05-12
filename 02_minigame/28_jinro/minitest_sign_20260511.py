import minescript as m
import time
import math

p = m.player()

x = math.floor(p.position[0])
y = math.floor(p.position[1])
z = math.floor(p.position[2])

def cmd(c):
    # print(c)
    m.execute(c)

cmd('kill @e[type=interaction,tag=test]')

# cmd(
#     f'summon interaction '
#     f'{x+0.5} {y+1} {z+2} '
#     '{'
#     'width:1f,'
#     'height:1f,'
#     'response:1b,'
#     'Tags:["test"]'
#     '}'
# )

# 看板
cmd(
    f'setblock '
    f'{x} {y+1} {z+2} '
    f'oak_sign[rotation=8]'
)

# interaction
cmd(
    f'summon interaction '
    f'{x+0.5} {y+1.5} {z+1.9} '
    '{'
    'width:0.8f,'
    'height:0.8f,'
    'Tags:["test"]'
    '}'
)

print("RIGHT CLICK")

while True:

    # クリック
    cmd(
        'execute as '
        '@e['
        'type=interaction,'
        'tag=test,'
        'nbt={interaction:{}}'
        '] '
        'run say CLICK'
    )

    # リセット
    cmd(
        'execute as '
        '@e['
        'type=interaction,'
        'tag=test,'
        'nbt={interaction:{}}'
        '] '
        'run data remove entity @s interaction'
    )

    time.sleep(0.05)



# import minescript as m
# import time
# import math

# p = m.player()

# x = math.floor(p.position[0])
# y = math.floor(p.position[1])
# z = math.floor(p.position[2])

# def cmd(c):
#     m.execute(c)

# cmd('kill @e[type=interaction,tag=test]')

# # 看板
# cmd(
#     f'setblock '
#     f'{x} {y+1} {z+2} '
#     f'oak_sign[rotation=8]'
# )

# # interaction
# cmd(
#     f'summon interaction '
#     f'{x+0.5} {y+1.5} {z+1.9} '
#     '{'
#     'width:0.8f,'
#     'height:0.8f,'
#     'Tags:["test"]'
#     '}'
# )

# print("RIGHT CLICK")

# while True:

#     # クリック検知
#     cmd(
#         'execute as '
#         '@e['
#         'type=interaction,'
#         'tag=test,'
#         'nbt={interaction:{}}'
#         '] '
#         'run title @p title '
#         '{"text":"人狼","color":"red","bold":true}'
#     )

#     # サブタイトル
#     cmd(
#         'execute as '
#         '@e['
#         'type=interaction,'
#         'tag=test,'
#         'nbt={interaction:{}}'
#         '] '
#         'run title @p subtitle '
#         '{"text":"あなたは人狼です"}'
#     )

#     # 表示時間
#     cmd(
#         'execute as '
#         '@e['
#         'type=interaction,'
#         'tag=test,'
#         'nbt={interaction:{}}'
#         '] '
#         'run title @p times 0 40 10'
#     )

#     # interaction リセット
#     cmd(
#         'execute as '
#         '@e['
#         'type=interaction,'
#         'tag=test,'
#         'nbt={interaction:{}}'
#         '] '
#         'run data remove entity @s interaction'
#     )

#     time.sleep(0.05)
