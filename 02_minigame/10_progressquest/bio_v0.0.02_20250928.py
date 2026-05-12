import minescript as m
from minescript import EventQueue, EventType
import re
import threading

player = m.player_name()
visited = set()

# ファイルから既存の訪問済みを読み込む
try:
    with open("bio_output.txt", "r", encoding="utf-8") as f:
        content = f.read().strip()
        if content:
            visited = set(content.split(","))
except FileNotFoundError:
    visited = set()

# 初訪問チャット検出用パターン
first_visit_pattern = re.compile(r"🌍 First visit: (\w+)")

# チャット監視専用スレッド
def chat_listener():
    with EventQueue() as eq:
        eq.register_chat_listener()
        m.echo("🌍 Biome First Visit Listener running...")
        while True:
            event = eq.get()
            if not event or event.type != EventType.CHAT:
                continue
            msg = event.message
            if msg.startswith("<") and ">" in msg:
                msg = msg.split(">", 1)[1].strip()
            match = first_visit_pattern.search(msg)
            if match:
                biome = match.group(1)
                if biome not in visited:
                    visited.add(biome)
                    with open("bio_output.txt", "w", encoding="utf-8") as f:
                        f.write(",".join(sorted(visited)))
                    m.echo(f"✅ Saved first visit biome: {biome}")

# チャット監視スレッド開始
threading.Thread(target=chat_listener, daemon=True).start()

# --- 以下既存のスコアボード / periodic_check はそのまま --- #
SCORE_OBJ = "visited_biomes"
TEMP_COUNTER = "biome_counter"

BIOMES = [
    "the_void", "plains", "sunflower_plains", "snowy_plains", "ice_spikes",
    "desert", "swamp", "mangrove_swamp", "forest", "flower_forest",
    "birch_forest", "dark_forest", "old_growth_birch_forest", "old_growth_pine_taiga",
    "old_growth_spruce_taiga", "taiga", "snowy_taiga", "savanna", "savanna_plateau",
    "windswept_hills", "windswept_gravelly_hills", "windswept_forest",
    "windswept_savanna", "jungle", "sparse_jungle", "bamboo_jungle",
    "badlands", "eroded_badlands", "wooded_badlands", "meadow", "cherry_grove",
    "grove", "snowy_slopes", "frozen_peaks", "jagged_peaks", "stony_peaks",
    "river", "frozen_river", "beach", "snowy_beach", "stony_shore",
    "warm_ocean", "lukewarm_ocean", "deep_lukewarm_ocean", "ocean", "deep_ocean",
    "cold_ocean", "deep_cold_ocean", "frozen_ocean", "deep_frozen_ocean",
    "mushroom_fields", "dripstone_caves", "lush_caves", "deep_dark"
]

def init_scoreboard():
    try: m.execute(f"scoreboard objectives add {SCORE_OBJ} dummy")
    except: pass
    try: m.execute(f"scoreboard objectives add {TEMP_COUNTER} dummy")
    except: pass
    m.execute("scoreboard objectives setdisplay sidebar")
    for b in BIOMES:
        try:
            m.execute(f"scoreboard players set {b} {SCORE_OBJ} 0")
        except: pass

def reset_scoreboard():
    for b in BIOMES:
        try:
            m.execute(f"scoreboard players set {b} {SCORE_OBJ} 0")
        except: pass
    m.execute(f"scoreboard players set {TEMP_COUNTER} {SCORE_OBJ} 0")
    m.echo("♻️ Biome scores have been reset")

def check_biomes():
    try:
        x, y, z = map(int, m.player_position())
        for b in BIOMES:
            full_biome = f"minecraft:{b}"
            m.execute(
                f"/execute if score {b} {SCORE_OBJ} matches 0 "
                f"if biome {x} {y} {z} {full_biome} "
                f"run scoreboard players set {b} {SCORE_OBJ} 1"
            )
            m.execute(
                f"/execute if score {b} {SCORE_OBJ} matches 1 "
                f"if biome {x} {y} {z} {full_biome} "
                f"run tellraw {player} "
                f'[{{"text":"🌍 First visit: {b}","color":"aqua","bold":true}}]'
            )
            m.execute(
                f"/execute if score {b} {SCORE_OBJ} matches 1 "
                f"if biome {x} {y} {z} {full_biome} "
                f"run scoreboard players set {b} {SCORE_OBJ} 2"
            )
    except Exception as e:
        m.echo(f"❌ check_biomes error: {e}")

def periodic_check():
    check_biomes()
    threading.Timer(2.0, periodic_check).start()

# Startup
init_scoreboard()
periodic_check()
