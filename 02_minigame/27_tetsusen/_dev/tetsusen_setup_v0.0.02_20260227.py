import minescript as m
import time

SLOT_COUNT = 27

# プレイヤーとシュルカー座標の紐付け
SHULKER_MAP = {
    "crocadooo": (88, 63, 74),
    # "Player2": (100, 64, 80),
    # "Player3": (120, 63, 90),
}

# objective準備
m.execute("scoreboard objectives remove iron")
m.execute("scoreboard objectives remove temp")
m.execute("scoreboard objectives add iron dummy")
m.execute("scoreboard objectives add temp dummy")
m.execute("scoreboard objectives modify iron displayname {\"text\":\"Iron Ingots\",\"color\":\"gold\"}")

# サイドバー表示
m.execute("scoreboard objectives setdisplay sidebar iron")

while True:

    for PLAYER, (X, Y, Z) in SHULKER_MAP.items():

        # 合計リセット
        m.execute(f"scoreboard players set {PLAYER} iron 0")

        for i in range(SLOT_COUNT):

            m.execute(f"scoreboard players set {PLAYER} temp 0")

            m.execute(
                f'execute if data block {X} {Y} {Z} '
                f'Items[{{Slot:{i}b,id:"minecraft:iron_ingot"}}] '
                f'run execute store result score {PLAYER} temp run '
                f'data get block {X} {Y} {Z} '
                f'Items[{{Slot:{i}b,id:"minecraft:iron_ingot"}}].count'
            )

            m.execute(f"scoreboard players operation {PLAYER} iron += {PLAYER} temp")

        # アクションバー表示（各プレイヤー本人にだけ表示）
        m.execute(
            f'execute as {PLAYER} run title {PLAYER} actionbar '
            f'{{"text":"Iron: ","color":"gold",'
            f'"extra":[{{"score":{{"name":"{PLAYER}","objective":"iron"}}}}]}}'
        )

    time.sleep(1)
