import minescript as m
import time

# ==============================
# 設定
# ==============================
TICK_DELAY = 0.1
SNEAK_SCOREBOARD = "sneak_time"

# 対象アイテム
TARGET_ITEMS = [
    "minecraft:carrot_on_a_stick",
    "minecraft:diamond_sword",
    "minecraft:apple"
]

# ==============================
# ヘルパー
# ==============================
def format_name(item_id: str) -> str:
    return item_id.replace("minecraft:", "").replace(":", "_")

# ==============================
# スコアボード初期化
# ==============================
m.execute('scoreboard objectives add sneak_prev dummy')
m.execute('scoreboard objectives add is_sneaking dummy')
m.execute('scoreboard objectives add sneak_state dummy')

for item in TARGET_ITEMS:
    name = format_name(item)
    m.execute(f'scoreboard objectives add has_{name} dummy')
    m.execute(f'scoreboard players set @a has_{name} 0')

m.execute('scoreboard players reset @a sneak_prev')
m.execute('scoreboard players reset @a is_sneaking')
m.execute('scoreboard players reset @a sneak_state')

m.echo("Sneak detection (with held items) running...")

# ==============================
# メインループ
# ==============================
while True:
    # スニーク中か判定
    m.execute(f'execute as @a if score @s {SNEAK_SCOREBOARD} > @s sneak_prev run scoreboard players set @s is_sneaking 1')
    m.execute(f'execute as @a unless score @s {SNEAK_SCOREBOARD} > @s sneak_prev run scoreboard players set @s is_sneaking 0')

    # 各アイテムごとの処理
    for item in TARGET_ITEMS:
        name = format_name(item)

        # 持っているかどうか
        m.execute(f'execute as @a if entity @s[nbt={{SelectedItem:{{id:"{item}"}}}}] run scoreboard players set @s has_{name} 1')
        m.execute(f'execute as @a unless entity @s[nbt={{SelectedItem:{{id:"{item}"}}}}] run scoreboard players set @s has_{name} 0')

        # スニーク開始
        m.execute(f'execute as @a if score @s is_sneaking matches 1 if score @s sneak_state matches 0 if score @s has_{name} matches 1 run tellraw @a ["",{{"selector":"@s"}},{{"text":" started sneaking with {item}!","color":"yellow"}}]')

        # スニーク終了
        m.execute(f'execute as @a if score @s is_sneaking matches 0 if score @s sneak_state matches 1 if score @s has_{name} matches 1 run tellraw @a ["",{{"selector":"@s"}},{{"text":" stopped sneaking with {item}!","color":"red"}}]')

    # 状態更新
    m.execute('execute as @a if score @s is_sneaking matches 1 run scoreboard players set @s sneak_state 1')
    m.execute('execute as @a if score @s is_sneaking matches 0 run scoreboard players set @s sneak_state 0')
    m.execute(f'execute as @a run scoreboard players operation @s sneak_prev = @s {SNEAK_SCOREBOARD}')

    time.sleep(TICK_DELAY)
