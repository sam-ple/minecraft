import minescript as m
import time
from minescript import EventQueue, EventType

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

# 初期化（1度だけ）
m.execute(f"scoreboard objectives add {SCORE_OBJ} dummy")
m.execute(f"scoreboard objectives setdisplay sidebar {SCORE_OBJ}")
for biome_id in BIOMES:
    biome_short = biome_id.split(":")[1]
    m.execute(f"scoreboard players set {biome_short} {SCORE_OBJ} 0")

def check_biomes():
    x, y, z = map(int, m.player_position())
    for biome_id in BIOMES:
        biome_short = biome_id.split(":")[1]

        # 「今の位置がbiomeでスコアが0（未訪問）」なら
        condition = (
            f"/execute if biome {x} {y} {z} {biome_id} "
            f"if score {biome_short} {SCORE_OBJ} matches 0"
        )

        # チャット通知とスコア更新（初訪問時のみ）
        m.execute(condition + f' run tellraw {player} {{"text":"🌍 First visit: {biome_short}","color":"aqua","bold":true}}')
        m.execute(condition + f" run scoreboard players set {biome_short} {SCORE_OBJ} 1")

def show_status():
    # 全バイオームの訪問状況をチャットに一覧表示
    for biome_id in BIOMES:
        biome_short = biome_id.split(":")[1]
        # スコアが1なら訪問済み、0なら未訪問をtellrawで表示
        m.execute(f'/execute if score {biome_short} {SCORE_OBJ} matches 1 run tellraw {player} {{"text":"✅ Visited: {biome_short}","color":"green"}}')
        m.execute(f'/execute unless score {biome_short} {SCORE_OBJ} matches 1 run tellraw {player} {{"text":"⬜ Not visited: {biome_short}","color":"gray"}}')

# チャットコマンド監視とメインループ
with EventQueue() as eq:
    eq.register_chat_listener()
    m.echo("Biome visit tracker ready. Send --status to see visit list.")
    while True:
        event = eq.get()
        if event.type != EventType.CHAT:
            continue
        msg = event.message.strip()
        if msg.startswith("<") and ">" in msg:
            msg = msg.split(">", 1)[1].strip()

        if msg == "--status":
            show_status()

        # 定期的にバイオーム判定（例：2秒毎）
        check_biomes()
        time.sleep(2)
