import minescript as m
import time

# チェック対象のバイオーム一覧
BIOMES_TO_CHECK = [
    "minecraft:plains",
    "minecraft:forest",
    "minecraft:river",
    "minecraft:desert",
    "minecraft:savanna",
    "minecraft:taiga",
]

SCORE_OBJECTIVE = "visited_biomes"
player = m.player_name()

# スコアボード作成（既にあればエラー無視される）
m.execute(f"scoreboard objectives add {SCORE_OBJECTIVE} dummy")

# サイドバーに表示
m.execute(f"scoreboard objectives setdisplay sidebar {SCORE_OBJECTIVE}")

# バイオーム名をスコアプレイヤー名として使う
for biome_id in BIOMES_TO_CHECK:
    biome_short = biome_id.split(":")[1]
    m.execute(f"scoreboard players set {biome_short} {SCORE_OBJECTIVE} 0")

def check_biomes():
    x, y, z = map(int, m.player_position())

    for biome_id in BIOMES_TO_CHECK:
        biome_short = biome_id.split(":")[1]

        # 未訪問で、現在そのバイオームにいるかチェック
        condition = (
            f"/execute if biome {x} {y} {z} {biome_id} "
            f"if score {biome_short} {SCORE_OBJECTIVE} matches 0"
        )

        # 通知
        m.execute(
            condition +
            f" run title {player} title {{\"text\":\"First Visit!\",\"color\":\"gold\"}}"
        )
        m.execute(
            condition +
            f" run title {player} subtitle {{\"text\":\"{biome_short}\",\"color\":\"yellow\"}}"
        )

        # スコアを 1 に更新（再通知防止）
        m.execute(
            condition +
            f" run scoreboard players set {biome_short} {SCORE_OBJECTIVE} 1"
        )

# メインループ（2秒ごと）
while True:
    check_biomes()
    time.sleep(2)
