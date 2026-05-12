import minescript as m
import time
import json
from minescript import EventQueue, EventType

# Overworld バイオーム一覧（2025年版）
BIOMES = [
    "minecraft:the_void", "minecraft:plains", "minecraft:sunflower_plains", "minecraft:snowy_plains",
    "minecraft:ice_spikes", "minecraft:desert", "minecraft:swamp", "minecraft:mangrove_swamp",
    "minecraft:forest", "minecraft:flower_forest", "minecraft:birch_forest", "minecraft:dark_forest",
    "minecraft:old_growth_birch_forest", "minecraft:old_growth_pine_taiga", "minecraft:old_growth_spruce_taiga",
    "minecraft:taiga", "minecraft:snowy_taiga", "minecraft:savanna", "minecraft:savanna_plateau",
    "minecraft:windswept_hills", "minecraft:windswept_gravelly_hills", "minecraft:windswept_forest",
    "minecraft:windswept_savanna", "minecraft:jungle", "minecraft:sparse_jungle", "minecraft:bamboo_jungle",
    "minecraft:badlands", "minecraft:eroded_badlands", "minecraft:wooded_badlands", "minecraft:meadow",
    "minecraft:cherry_grove", "minecraft:grove", "minecraft:snowy_slopes", "minecraft:frozen_peaks",
    "minecraft:jagged_peaks", "minecraft:stony_peaks", "minecraft:river", "minecraft:frozen_river",
    "minecraft:beach", "minecraft:snowy_beach", "minecraft:stony_shore", "minecraft:warm_ocean",
    "minecraft:lukewarm_ocean", "minecraft:deep_lukewarm_ocean", "minecraft:ocean", "minecraft:deep_ocean",
    "minecraft:cold_ocean", "minecraft:deep_cold_ocean", "minecraft:frozen_ocean", "minecraft:deep_frozen_ocean",
    "minecraft:mushroom_fields", "minecraft:dripstone_caves", "minecraft:lush_caves", "minecraft:deep_dark"
]

SCORE_OBJ = "visited_biomes"
TEMP_COUNTER = "biome_counter"
player = m.player_name()

def init_scoreboard():
    try:
        m.execute(f"scoreboard objectives add {SCORE_OBJ} dummy")
    except Exception:
        pass
    try:
        m.execute(f"scoreboard objectives add {TEMP_COUNTER} dummy")
    except Exception:
        pass

    # サイドバー非表示
    m.execute("scoreboard objectives setdisplay sidebar")

    for biome_id in BIOMES:
        short = biome_id.split(":")[1]
        m.execute(f"scoreboard players set {short} {SCORE_OBJ} 0")

def check_biomes():
    x, y, z = map(int, m.player_position())
    for biome_id in BIOMES:
        short = biome_id.split(":")[1]

        # 未訪問なら 1 に更新
        m.execute(
            f"/execute if score {short} {SCORE_OBJ} matches 0 "
            f"if biome {x} {y} {z} {biome_id} "
            f"run scoreboard players set {short} {SCORE_OBJ} 1"
        )

        # 初訪問（スコアが 1）なら通知＆2 に更新（1回限り）
        m.execute(
            f"/execute if score {short} {SCORE_OBJ} matches 1 "
            f"if biome {x} {y} {z} {biome_id} "
            f"run tellraw {player} [{{\"text\":\"🌍 First visit: {short}\",\"color\":\"aqua\",\"bold\":true}}]"
        )
        m.execute(
            f"/execute if score {short} {SCORE_OBJ} matches 1 "
            f"if biome {x} {y} {z} {biome_id} "
            f"run scoreboard players set {short} {SCORE_OBJ} 2"
        )

def show_status():
    m.execute(f"scoreboard players set {TEMP_COUNTER} {SCORE_OBJ} 0")
    for biome_id in BIOMES:
        short = biome_id.split(":")[1]
        m.execute(
            f"/execute if score {short} {SCORE_OBJ} matches 2.. run "
            f"scoreboard players add {TEMP_COUNTER} {SCORE_OBJ} 1"
        )

    m.execute(
        f'tellraw {player} ["",'
        f'{{"text":"🌿 Biome Progress: ","color":"gold"}},'
        f'{{"score":{{"name":"{TEMP_COUNTER}","objective":"{SCORE_OBJ}"}}}},'
        f'{{"text":"/{len(BIOMES)}","color":"white"}}]'
    )

    for biome_id in BIOMES:
        short = biome_id.split(":")[1]
        m.execute(
            f"/execute if score {short} {SCORE_OBJ} matches 2.. run "
            f'tellraw {player} [{{"text":"★ {short}","color":"green"}}]'
        )
        m.execute(
            f"/execute unless score {short} {SCORE_OBJ} matches 2.. run "
            f'tellraw {player} [{{"text":"☆ {short}","color":"gray"}}]'
        )

def give_book():
    pages = []
    visited = []
    unvisited = []

    for biome_id in BIOMES:
        short = biome_id.split(":")[1]
        try:
            result = m.get_score(short, SCORE_OBJ)
            if result >= 2:
                visited.append(f"★ {short}")
            else:
                unvisited.append(f"☆ {short}")
        except Exception:
            unvisited.append(f"☆ {short}")

    lines = visited + unvisited
    chunks = [lines[i:i+14] for i in range(0, len(lines), 14)]
    for chunk in chunks:
        page = [[ "\n".join(chunk) ]]
        pages.append(page)

    book_nbt = {
        "pages": pages,
        "title": "Biome Progress",
        "author": player
    }
    nbt_str = f'written_book_content={json.dumps(book_nbt)}'
    m.execute(f'give {player} written_book[{nbt_str}]')
    m.echo("📘 Biome Book を配布しました")

# 起動処理
init_scoreboard()

with EventQueue() as eq:
    eq.register_chat_listener()
    m.echo("🌍 BiomeTracker 起動中。--status で進捗確認、--book で本を入手できます。")

    while True:
        event = eq.get()
        if event.type == EventType.CHAT:
            msg = event.message.strip()
            if msg.startswith("<") and ">" in msg:
                msg = msg.split(">", 1)[1].strip()

            if msg == "--status":
                show_status()
            elif msg == "--book":
                give_book()

        check_biomes()
        time.sleep(2)
