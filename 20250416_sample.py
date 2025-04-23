import minescript
import sys

if len(sys.argv) < 2:
    minescript.echo("コマンドを指定してください。")
    sys.exit(1)

user_input = sys.argv[1]

# ============================================================
# 時間設定
# ============================================================
time_map = {
    "sunrise": "sunrise",
    "day": "day",
    "noon": "noon",
    "sunset": "sunset",
    "night": "night",
    "midnight": "midnight",
}

# ============================================================
# 天気設定
# ============================================================
weather_map = {
    "clear": "clear",
    "rain": "rain",
    "thunder": "thunder",
}

# ============================================================
# ゲームモード
# ============================================================
gamemode_map = {
    "survival": "survival",
    "creative": "creative",
    "spectator": "spectator",
    "adventure": "adventure",
}

# ------------------------------------------------------------
# 時間
# ------------------------------------------------------------
if user_input in time_map:
    minescript.execute(f"/time set {time_map[user_input]}")
    minescript.echo(f"時間を「{user_input}」に設定しました。")

# ------------------------------------------------------------
# 天気
# ------------------------------------------------------------
elif user_input in weather_map:
    minescript.execute(f"/weather {weather_map[user_input]}")
    minescript.echo(f"天気を「{user_input}」に設定しました。")

# ------------------------------------------------------------
# ゲームモード
# ------------------------------------------------------------
elif user_input in gamemode_map:
    minescript.execute(f"/gamemode {gamemode_map[user_input]}")
    minescript.echo(f"ゲームモードを「{user_input}」に変更しました。")

# ------------------------------------------------------------
# 作業台
# ------------------------------------------------------------
elif user_input == "crafttable":
    minescript.execute('/give @p minecraft:crafting_table 1')
    minescript.echo("作業台を渡しました。")

# ------------------------------------------------------------
# ピンクの羊を召喚
# ------------------------------------------------------------
elif user_input == "pinksheep":
    minescript.execute('/summon minecraft:sheep ~ ~ ~ {Color:6}')
    minescript.echo("ピンクの羊を召喚しました。")


# ------------------------------------------------------------
# 配信用設定
# ------------------------------------------------------------
elif user_input == "mode":
    settings = {
        "keepInventory": "true",
        "doDaylightCycle": "false",
        "doMobSpawning": "false"
    }
    for rule, value in settings.items():
        minescript.execute(f"/gamerule {rule} {value}")
    minescript.execute("/time set day")  # 今の時間も昼にしておく
    minescript.execute("/weather clear")  # 天気も晴れにしておく
    minescript.echo("「配信用設定」を適用しました！（キープインベントリ＋常に昼＋モブ湧きオフ）")

# ------------------------------------------------------------
# チート装備一式
# ------------------------------------------------------------
elif user_input == "cheat":
    items = [
        'minecraft:netherite_sword', 'minecraft:netherite_pickaxe', 'minecraft:netherite_axe', 'minecraft:netherite_shovel',
        'minecraft:netherite_helmet', 'minecraft:netherite_chestplate', 'minecraft:netherite_leggings', 'minecraft:netherite_boots',
        'minecraft:golden_apple', 'minecraft:enchanted_golden_apple', 'minecraft:diamond', 'minecraft:cooked_beef'
    ]
    for item in items:
        minescript.execute(f'/give @p {item} 1')
    minescript.echo("チート装備を配布しました。")

# ------------------------------------------------------------
# 未対応
# ------------------------------------------------------------
else:
    minescript.echo(f"未対応のコマンドです: {user_input}")
