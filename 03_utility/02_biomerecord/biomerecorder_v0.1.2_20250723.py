import minescript as m
import time
from minescript import EventQueue, EventType

# 対象バイオーム一覧
BIOMES = [
    "minecraft:plains",
    "minecraft:forest",
    "minecraft:river",
    "minecraft:desert",
    "minecraft:savanna",
    "minecraft:taiga",
]

SCORE_OBJ = "visited_biomes"
player = m.player_name()

# スコアボード初期化（既に存在していてもOK）
m.execute(f"scoreboard objectives add {SCORE_OBJ} dummy")
m.execute(f"scoreboard objectives setdisplay sidebar {SCORE_OBJ}")
for biome_id in BIOMES:
    biome_short = biome_id.split(":")[1]
    m.execute(f"scoreboard players set {biome_short} {SCORE_OBJ} 0")

def check_biomes():
    x, y, z = map(int, m.player_position())
    for biome_id in BIOMES:
        biome_short = biome_id.split(":")[1]

        condition = (
            f"/execute if biome {x} {y} {z} {biome_id} "
            f"if score {biome_short} {SCORE_OBJ} matches 0"
        )

        # 初訪問時のみ表示とスコア記録
        m.execute(condition + f' run tellraw {player} {{"text":"🌍 First visit: {biome_short}","color":"aqua","bold":true}}')
        m.execute(condition + f" run scoreboard players set {biome_short} {SCORE_OBJ} 1")

def show_status():
    # 1行で表示するtellraw JSONの構築
    components = []

    for biome_id in BIOMES:
        biome_short = biome_id.split(":")[1]

        # 各バイオームのステータスを /execute if で個別にチェックして表示
        m.execute(
            f'/execute if score {biome_short} {SCORE_OBJ} matches 1 run '
            f'tellraw {player} ['
            f'{{"text":"| ","color":"white"}},'
            f'{{"text":"★","color":"green","bold":true}},'
            f'{{"text":" {biome_short} ","color":"white"}}]'
        )
        m.execute(
            f'/execute unless score {biome_short} {SCORE_OBJ} matches 1 run '
            f'tellraw {player} ['
            f'{{"text":"| ","color":"white"}},'
            f'{{"text":"☆","color":"gray"}},'
            f'{{"text":" {biome_short} ","color":"white"}}]'
        )

# メインループ：イベント処理と定期チェック
with EventQueue() as eq:
    eq.register_chat_listener()
    m.echo("🌿 BiomeChecker 起動中。--status で訪問状況を確認。")

    while True:
        event = eq.get()
        if event.type != EventType.CHAT:
            continue

        msg = event.message.strip()
        if msg.startswith("<") and ">" in msg:
            msg = msg.split(">", 1)[1].strip()

        if msg == "--status":
            show_status()

        # バイオーム訪問チェック（2秒ごと）
        check_biomes()
        time.sleep(2)
