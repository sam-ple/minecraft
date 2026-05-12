# テツセンのシュルカー内の鉄インゴットの数をカウントしてアクションバーに表示するスクリプト
# daat blockの特性上、実行者がある程度の距離を離れるとシュルカーのデータが取得できなくなるため、シュルカーの近くにいる必要がある。
import minescript as m
import time

PLAYER = "crocadooo"
X, Y, Z = 88, 63, 74   # シュルカー座標
SLOT_COUNT = 27

# objective準備
m.execute("scoreboard objectives remove iron")
m.execute("scoreboard objectives add iron dummy")

while True:
    m.execute(f"scoreboard players set {PLAYER} iron 0")

    for i in range(SLOT_COUNT):
        # 各スロットのiron countを取得（存在しなければ0）
        m.execute(f"scoreboard players set {PLAYER} temp 0")
        m.execute(
            f'execute if data block {X} {Y} {Z} '
            f'Items[{{Slot:{i}b,id:"minecraft:iron_ingot"}}] '
            f'run execute store result score {PLAYER} temp run '
            f'data get block {X} {Y} {Z} Items[{{Slot:{i}b,id:"minecraft:iron_ingot"}}].count'
        )
        # 合計に加算
        m.execute(f"scoreboard players operation {PLAYER} iron += {PLAYER} temp")

    # アクションバー表示
    m.execute(
        f'title {PLAYER} actionbar '
        f'{{"text":"Iron: ","color":"gold",'
        f'"extra":[{{"score":{{"name":"{PLAYER}","objective":"iron"}}}}]}}'
    )

    time.sleep(1)
