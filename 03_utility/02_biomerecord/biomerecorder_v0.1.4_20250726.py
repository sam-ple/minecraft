import minescript as m
import json
import threading
from minescript import EventQueue, EventType

BIOMES = [
    "the_void", "plains", "sunflower_plains", "snowy_plains",
    "ice_spikes", "desert", "swamp", "mangrove_swamp",
    "forest", "flower_forest", "birch_forest", "dark_forest",
    "old_growth_birch_forest", "old_growth_pine_taiga", "old_growth_spruce_taiga",
    "taiga", "snowy_taiga", "savanna", "savanna_plateau",
    "windswept_hills", "windswept_gravelly_hills", "windswept_forest",
    "windswept_savanna", "jungle", "sparse_jungle", "bamboo_jungle",
    "badlands", "eroded_badlands", "wooded_badlands", "meadow",
    "cherry_grove", "grove", "snowy_slopes", "frozen_peaks",
    "jagged_peaks", "stony_peaks", "river", "frozen_river",
    "beach", "snowy_beach", "stony_shore", "warm_ocean",
    "lukewarm_ocean", "deep_lukewarm_ocean", "ocean", "deep_ocean",
    "cold_ocean", "deep_cold_ocean", "frozen_ocean", "deep_frozen_ocean",
    "mushroom_fields", "dripstone_caves", "lush_caves", "deep_dark"
]

SCORE_OBJ = "visited_biomes"
TEMP_COUNTER = "biome_counter"
player = m.player_name()

def init_scoreboard():
    try: m.execute(f"scoreboard objectives add {SCORE_OBJ} dummy")
    except: pass
    try: m.execute(f"scoreboard objectives add {TEMP_COUNTER} dummy")
    except: pass
    m.execute("scoreboard objectives setdisplay sidebar")
    for short in BIOMES:
        try:
            m.execute(f"scoreboard players set {short} {SCORE_OBJ} 0")
        except: pass

def reset_scoreboard():
    for short in BIOMES:
        try:
            m.execute(f"scoreboard players set {short} {SCORE_OBJ} 0")
        except: pass
    m.execute(f"scoreboard players set {TEMP_COUNTER} {SCORE_OBJ} 0")
    m.echo("♻️ Biome スコアをリセットしました")

def check_biomes():
    try:
        x, y, z = map(int, m.player_position())
        for short in BIOMES:
            full_biome = f"minecraft:{short}"
            m.execute(
                f"/execute if score {short} {SCORE_OBJ} matches 0 "
                f"if biome {x} {y} {z} {full_biome} "
                f"run scoreboard players set {short} {SCORE_OBJ} 1"
            )
            m.execute(
                f"/execute if score {short} {SCORE_OBJ} matches 1 "
                f"if biome {x} {y} {z} {full_biome} "
                f"run tellraw {player} "
                f'[{{"text":"🌍 First visit: {short}","color":"aqua","bold":true}}]'
            )
            m.execute(
                f"/execute if score {short} {SCORE_OBJ} matches 1 "
                f"if biome {x} {y} {z} {full_biome} "
                f"run scoreboard players set {short} {SCORE_OBJ} 2"
            )
    except Exception as e:
        m.echo(f"❌ check_biomes error: {e}")

def show_status():
    m.execute(f"scoreboard players set {TEMP_COUNTER} {SCORE_OBJ} 0")
    for short in BIOMES:
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
    for short in BIOMES:
        m.execute(
            f'/execute if score {short} {SCORE_OBJ} matches 2.. run '
            f'tellraw {player} [{{"text":"★{short}","color":"green"}}]'
        )
        m.execute(
            f'/execute unless score {short} {SCORE_OBJ} matches 2.. run '
            f'tellraw {player} [{{"text":"☆{short}","color":"gray"}}]'
        )

def periodic_check():
    check_biomes()
    threading.Timer(2.0, periodic_check).start()

# 実行開始
init_scoreboard()
periodic_check()

with EventQueue() as eq:
    eq.register_chat_listener()
    m.echo("🌍 BiomeTracker 起動中。--status で進捗確認、--book で本を入手、--reset でリセット")

    while True:
        event = eq.get()
        if event.type == EventType.CHAT:
            msg = event.message.strip()
            if msg.startswith("<") and ">" in msg:
                msg = msg.split(">", 1)[1].strip()
            if msg == "--status":
                show_status()
            elif msg == "--reset":
                reset_scoreboard()
