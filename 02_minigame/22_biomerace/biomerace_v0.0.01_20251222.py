import minescript as m
import time

# -------------------------------
# 🌍 Biome Explorer Game
# 制限時間付きマルチプレイヤー対応
# -------------------------------

# 設定
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

GAME_TIME = 120  # 制限時間（秒）
SLEEP = 1        # チェック間隔（秒）

# -------------------------------
# 初期化
# -------------------------------
m.execute("gamerule sendCommandFeedback false")

# サイドバー
m.execute("scoreboard objectives add biome_progress dummy")
m.execute("scoreboard objectives setdisplay sidebar biome_progress")

# バイオーム個別スコア
for biome in BIOMES:
    m.execute(f"scoreboard objectives add {biome} dummy")
    m.execute(f"scoreboard players set @a {biome} 0")

# 一時カウンター（集計用）
m.execute("scoreboard objectives add temp_counter dummy")

# ボスバー
m.execute("bossbar add game_timer \"⏳ Time Remaining\"")
m.execute("bossbar set game_timer color blue")
m.execute(f"bossbar set game_timer max {GAME_TIME}")
m.execute("bossbar set game_timer visible true")
m.execute(f"bossbar set game_timer value {GAME_TIME}")

m.execute('tellraw @a {"text":"🌍 Biome Explorer Game Started!","color":"gold"}')

# -------------------------------
# メインループ
# -------------------------------
time_remaining = GAME_TIME

while time_remaining > 0:
    for biome in BIOMES:
        full = f"minecraft:{biome}"
        
        # 初回訪問判定
        m.execute(
            f"execute as @a at @s if biome ~ ~ ~ {full} if score @s {biome} matches 0 run scoreboard players set @s {biome} 1"
        )
        
        # 初回通知
        m.execute(
            f"execute as @a if score @s {biome} matches 1 run tellraw @s "
            f'{{"text":"🌿 New biome discovered: {biome}","color":"aqua"}}'
        )
        
        # 通知済みに変更
        m.execute(
            f"execute as @a if score @s {biome} matches 1 run scoreboard players set @s {biome} 2"
        )
    
    # -------------------------------
    # 進捗集計・サイドバー反映
    # -------------------------------
    m.execute("scoreboard players set @a temp_counter 0")
    for biome in BIOMES:
        m.execute(
            f"execute as @a if score @s {biome} matches 2.. run scoreboard players add @s temp_counter 1"
        )
    m.execute("execute as @a run scoreboard players operation @s biome_progress = @s temp_counter")
    
    # -------------------------------
    # ボスバー更新
    # -------------------------------
    m.execute(f"bossbar set game_timer value {time_remaining}")
    
    time.sleep(SLEEP)
    time_remaining -= SLEEP

# -------------------------------
# 終了処理
# -------------------------------
m.execute("bossbar set game_timer visible false")
m.execute('tellraw @a {"text":"⏰ Time\'s up! Check the sidebar for final scores.","color":"gold"}')

# 終了時に全プレイヤーの進捗をまとめて表示
m.execute('tellraw @a [{"text":"⏰ Time\'s up! Final biome discoveries:","color":"gold"}]')
m.execute('execute as @a run tellraw @s [{"score":{"name":"@s","objective":"biome_progress"}}]')
