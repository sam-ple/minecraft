import minescript as m
import time

# 実行者の初期位置を基準にする
base = m.players()[0].position
bx, by, bz = base

while True:

    players = m.players()

    for p in players:
        name = p.name
        x,y,z = p.position

        # 距離計算
        dx = x - bx
        dz = z - bz
        dist = int((dx*dx + dz*dz) ** 0.5)

        # ① 取得確認（座標＋距離）
        m.execute(
            f'tellraw @a {{"text":"[P] {name} ({int(x)},{int(y)},{int(z)}) d={dist}","color":"yellow"}}'
        )

        # ② コマンド到達
        m.execute(
            f'execute as @a[name={name}] run tellraw @a {{"text":"[CMD] {name}","color":"aqua"}}'
        )

        # ③ 光る
        m.execute(
            f'execute as @a[name={name}] run effect give @s glowing 1 1 true'
        )

        # ④ particle
        m.execute(
            f'execute as @a[name={name}] at @s run particle minecraft:flame ~ ~1 ~ 0 0 0 0 3'
        )

    time.sleep(1)




# import minescript as m
# import time

# while True:

#     # ① コマンドが届くか
#     m.execute('execute as saaample run tellraw @a {"text":"[CMD OK]","color":"aqua"}')

#     # ② 光るか
#     m.execute('execute as saaample run effect give @s glowing 1 1 true')

#     # ③ particle出るか
#     m.execute('execute as saaample at @s run particle minecraft:flame ~ ~1 ~ 0 0 0 0 5')

#     time.sleep(1)



# import minescript as m
# import time

# while True:

#     players = m.players(name="saaample")

#     if players:
#         x,y,z = players[0].position

#         m.execute(
#             f'tellraw @a {{"text":"saaample {int(x)},{int(y)},{int(z)}","color":"yellow"}}'
#         )
#     else:
#         m.execute(
#             'tellraw @a {"text":"saaample NOT FOUND","color":"red"}'
#         )

#     time.sleep(1)


# import minescript as m
# import time

# base = m.players(name="crocadooo")[0].position
# bx,by,bz = base

# while True:

#     players = m.players(name="saaample")

#     if players:
#         x,y,z = players[0].position

#         dx = x - bx
#         dz = z - bz
#         dist = int((dx*dx + dz*dz) ** 0.5)

#         m.execute(
#             f'tellraw @a {{"text":"saaample {int(x)},{int(y)},{int(z)} d={dist}","color":"yellow"}}'
#         )
#     else:
#         m.execute(
#             'tellraw @a {"text":"saaample NOT FOUND","color":"red"}'
#         )

#     time.sleep(1)

# import minescript as m
# import time

# PLAYERS = ["crocadooo", "saaample"]

# while True:

#     for name in PLAYERS:

#         # 存在チェック（重要）
#         m.execute(
#             f'execute if entity @a[name={name}] run tellraw @a {{"text":"[OK] {name}","color":"green"}}'
#         )

#         # 光る（距離無関係）
#         m.execute(
#             f'execute as @a[name={name}] run effect give @s glowing 1 1 true'
#         )

#         # パーティクル（距離無関係）
#         m.execute(
#             f'execute as @a[name={name}] at @s run particle minecraft:flame ~ ~1 ~ 0 0 0 0 3'
#         )

#     time.sleep(1)
