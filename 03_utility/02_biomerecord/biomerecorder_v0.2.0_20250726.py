import minescript as m
import threading
from minescript import EventQueue, EventType

m.execute("gamerule sendCommandFeedback false")

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

SCORE_OBJ = "visited_biomes"
TEMP_COUNTER = "biome_counter"
player = m.player_name()

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

def show_status():
    m.execute(f"scoreboard players set {TEMP_COUNTER} {SCORE_OBJ} 0")
    for b in BIOMES:
        m.execute(
            f"/execute if score {b} {SCORE_OBJ} matches 2.. run "
            f"scoreboard players add {TEMP_COUNTER} {SCORE_OBJ} 1"
        )
    m.execute(
        f'tellraw {player} ["",'
        f'{{"text":"🌿 Biome Progress: ","color":"gold"}},'
        f'{{"score":{{"name":"{TEMP_COUNTER}","objective":"{SCORE_OBJ}"}}}},'
        f'{{"text":"/{len(BIOMES)}","color":"white"}}]'
    )
    m.execute(f'tellraw {player} [{{"text":"--- ✅ Visited ---","color":"green"}}]')
    for b in BIOMES:
        m.execute(
            f'/execute if score {b} {SCORE_OBJ} matches 2.. run '
            f'tellraw {player} [{{"text":"✔ {b}","color":"green"}}]'
        )
    m.execute(f'tellraw {player} [{{"text":"--- ❌ Not Yet ---","color":"red"}}]')
    for b in BIOMES:
        m.execute(
            f'/execute unless score {b} {SCORE_OBJ} matches 2.. run '
            f'tellraw {player} [{{"text":"• {b}","color":"red"}}]'
        )

def show_visited():
    m.echo("🗺️ Visited Biomes:")
    for b in BIOMES:
        m.execute(
            f'/execute if score {b} {SCORE_OBJ} matches 2.. run '
            f'tellraw {player} [{{"text":" - {b}","color":"green"}}]'
        )

def show_not_visited():
    m.echo("🗺️ Not Visited Biomes:")
    for b in BIOMES:
        m.execute(
            f'/execute unless score {b} {SCORE_OBJ} matches 2.. run '
            f'tellraw {player} [{{"text":" - {b}","color":"red"}}]'
        )

def periodic_check():
    check_biomes()
    threading.Timer(2.0, periodic_check).start()

# Startup
init_scoreboard()
periodic_check()

with EventQueue() as eq:
    eq.register_chat_listener()
    m.echo("🌍 BiomeTracker running. Use --status to check progress, --check1 for visited, --check2 for not visited, --reset to reset.")

    while True:
        event = eq.get()
        if event.type == EventType.CHAT:
            msg = event.message.strip()
            if msg.startswith("<") and ">" in msg:
                msg = msg.split(">", 1)[1].strip()
            if msg == "--status":
                show_status()
            elif msg == "--check1":
                show_visited()
            elif msg == "--check2":
                show_not_visited()
            elif msg == "--reset":
                reset_scoreboard()
