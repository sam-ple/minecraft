import minescript as m
import time

# 最初のプレイヤーを取得
player = m.players()[0].name

while True:
    # プレイヤー自身の座標をチャットで表示
    px, py, pz = m.players(name=player)[0].position
    m.execute(f'tellraw {player} {{"text":"[POS] X: {int(px)} Y: {int(py)} Z: {int(pz)}","color":"yellow"}}')
    time.sleep(2)
