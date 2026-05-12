import minescript as m
import time

# -------------------------------
# 🌍 Biome Tracker 最適版
# タグなし・全プレイヤー対応・サイドバー連動・初回通知のみ
# -------------------------------

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

SLEEP = 2  # チェック間隔（秒）

# -------------------------------
# 初期化
# -------------------------------
m.execute("gamerule sendCommandFeedback false")

# 進捗スコア（サイドバー用）
m.execute("scoreboard objectives add biome_progress dummy")
m.execute("scoreboard objectives setdisplay sidebar biome_progress")

# バイオーム個別スコア
for biome in BIOMES:
    m.execute(f"scoreboard objectives add {biome} dummy")
    m.execute(f"scoreboard players set @a {biome} 0")

m.execute('tellraw @a {"text":"🌍 Biome Tracker Started","color":"gold"}')

# -------------------------------
# メインループ
# -------------------------------
while True:
    # 初回訪問判定・通知・スコア更新
    for biome in BIOMES:
        full = f"minecraft:{biome}"

        # 未訪問プレイヤーがバイオームに入ったらスコア1に
        m.execute(
            f"execute as @a at @s if biome ~ ~ ~ {full} if score @s {biome} matches 0 run scoreboard players set @s {biome} 1"
        )

        # スコア1なら初回通知＆スコア2に変更（通知は1回のみ）
        m.execute(
            f"execute as @a if score @s {biome} matches 1 run tellraw @s "
            f'{{"text":"🌿 New biome discovered: {biome}","color":"aqua"}}'
        )
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

    # サイドバー用スコアにコピー
    m.execute("execute as @a run scoreboard players operation @s biome_progress = @s temp_counter")

    # ループ間隔
    time.sleep(SLEEP)
