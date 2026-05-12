import minescript as m
import time

# ==============================
# Settings
# ==============================
TICK_DELAY = 0.1  # ループ間隔

# 検知対象アイテムリスト（追加するだけでOK）
TARGET_ITEMS = [
    "minecraft:carrot_on_a_stick", 
    "minecraft:diamond_sword", 
    "minecraft:apple"
]

# スニーク用スコアボード
SNEAK_SCOREBOARD = "sneak_time"

# ==============================
# ヘルパー
# ==============================
def format_name(item_id: str) -> str:
    """スコアボード名用に安全な文字列に変換"""
    return item_id.replace("minecraft:", "").replace(":", "_")

# ==============================
# スコアボード初期化
# ==============================
for item in TARGET_ITEMS:
    name = format_name(item)
    criteria_item = item.replace("minecraft:", "")  # ← 修正ポイント！

    m.execute(f'scoreboard objectives add has_{name} dummy')
    m.execute(f'scoreboard objectives add right_click_{name} dummy')
    m.execute(f'scoreboard objectives add right_click_prev_{name} dummy')
    m.execute(f'scoreboard objectives add used_{name} minecraft.used:{criteria_item}')  # 修正済み
    m.execute(f'scoreboard players set @a has_{name} 0')
    m.execute(f'scoreboard players set @a right_click_{name} 0')
    m.execute(f'scoreboard players set @a right_click_prev_{name} 0')
    m.execute(f'scoreboard players set @a used_{name} 0')

# スニーク用
m.execute('scoreboard objectives add sneak_prev dummy')
m.execute('scoreboard objectives add is_sneaking dummy')
m.execute('scoreboard objectives add sneak_state dummy')  # 0=not sneaking, 1=sneaking
m.execute('scoreboard players reset @a sneak_prev')
m.execute('scoreboard players reset @a is_sneaking')
m.execute('scoreboard players reset @a sneak_state')

m.echo("Right-Click or Sneak detection running for all target items...")

# ==============================
# メインループ
# ==============================
while True:
    # スニーク判定（共通）
    m.execute(f'execute as @a if score @s {SNEAK_SCOREBOARD} > @s sneak_prev run scoreboard players set @s is_sneaking 1')
    m.execute(f'execute as @a unless score @s {SNEAK_SCOREBOARD} > @s sneak_prev run scoreboard players set @s is_sneaking 0')

    # アイテムごとの処理
    for item in TARGET_ITEMS:
        name = format_name(item)

        # --- 持っているか判定 ---
        m.execute(f'execute as @a if entity @s[nbt={{SelectedItem:{{id:"{item}"}}}}] run scoreboard players set @s has_{name} 1')
        m.execute(f'execute as @a unless entity @s[nbt={{SelectedItem:{{id:"{item}"}}}}] run scoreboard players set @s has_{name} 0')

        # --- 右クリック判定 ---
        m.execute(f'execute as @a if score @s used_{name} matches 1.. run scoreboard players set @s right_click_{name} 1')
        m.execute(f'execute as @a unless score @s used_{name} matches 1.. run scoreboard players set @s right_click_{name} 0')

        # --- ライジングエッジ（右クリック） ---
        m.execute(f'execute as @a if score @s right_click_{name} matches 1.. unless score @s right_click_prev_{name} matches 1.. if score @s has_{name} matches 1.. run tellraw @a ["",{{"selector":"@s"}},{{"text":" right-clicked {item}!","color":"gold"}}]')
        m.execute(f'execute as @a if score @s right_click_{name} matches 1.. run scoreboard players set @s right_click_prev_{name} 1')
        m.execute(f'execute as @a unless score @s right_click_{name} matches 1.. run scoreboard players set @s right_click_prev_{name} 0')
        m.execute(f'scoreboard players set @a used_{name} 0')

        # --- スニーク開始・終了 ---
        m.execute(f'execute as @a if score @s is_sneaking matches 1 if score @s sneak_state matches 0 if score @s has_{name} matches 1 run tellraw @a ["",{{"selector":"@s"}},{{"text":" started sneaking with {item}!","color":"yellow"}}]')
        m.execute(f'execute as @a if score @s is_sneaking matches 1 run scoreboard players set @s sneak_state 1')
        m.execute(f'execute as @a if score @s is_sneaking matches 0 if score @s sneak_state matches 1 if score @s has_{name} matches 1 run tellraw @a ["",{{"selector":"@s"}},{{"text":" stopped sneaking with {item}!","color":"red"}}]')
        m.execute(f'execute as @a if score @s is_sneaking matches 0 run scoreboard players set @s sneak_state 0')

    # スニーク時間更新
    m.execute(f'execute as @a run scoreboard players operation @s sneak_prev = @s {SNEAK_SCOREBOARD}')

    time.sleep(TICK_DELAY)
