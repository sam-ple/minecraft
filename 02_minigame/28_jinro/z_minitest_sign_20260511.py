import minescript as m
import time
import math

p = m.player()

x = math.floor(p.position[0])
y = math.floor(p.position[1])
z = math.floor(p.position[2])

def cmd(c):
    print(c)
    m.execute(c)

cmd('kill @e[type=interaction,tag=test]')

cmd(
    f'summon interaction '
    f'{x+0.5} {y+1} {z+2} '
    '{'
    'width:1f,'
    'height:1f,'
    'response:1b,'
    'Tags:["test"]'
    '}'
)

print("RIGHT CLICK")

while True:

    # クリック検知
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
        'data remove entity '
        '@e['
        'type=interaction,'
        'tag=test,'
        'nbt={interaction:{}},'
        'limit=1'
        '] '
        'interaction'
    )

    time.sleep(0.05)