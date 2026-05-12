import minescript as m
import time
import math

# 最初のプレイヤーを取得
player = m.players()[0].name

# スタート地点
# sx, sy, sz = m.players(name=player)[0].position
sx, sy, sz = map(int, m.players(name=player)[0].position)

while True:
    # 現在位置
    px, py, pz = m.players(name=player)[0].position

    # XZ差分
    dx = px - sx
    dz = pz - sz

    # 距離計算
    raw_distance = math.sqrt(dx * dx + dz * dz)

    # distance = int(raw_distance)      
    # distance = round(raw_distance)      # 四捨五入
    distance = math.floor(raw_distance)   # 常に切り捨て
    # distance = math.ceil(raw_distance)  # 常に切り上げ


    # 整数化（見た目用）
    isx, isz = int(sx), int(sz)
    ipx, ipz = int(px), int(pz)

    # 表示
    m.execute(
        f'tellraw {player} '
        f'{{"text":"[DIST XZ] start(x{isx},z{isz}) -> now(x{ipx},z{ipz}) : {distance} blocks","color":"gold"}}'
    )

    time.sleep(20)
