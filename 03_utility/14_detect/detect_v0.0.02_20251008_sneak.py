import minescript as m
import time

# --- 設定 ---
TICK_DELAY = 0.1  # ループ間隔（秒）

# --- スコアボード初期化 ---
m.execute('scoreboard objectives add sneak_time minecraft.custom:minecraft.sneak_time')
m.execute('scoreboard objectives add sneak_prev dummy')
m.execute('scoreboard objectives add is_sneaking dummy')
m.execute('scoreboard objectives add sneak_state dummy')  # 0=非スニーク, 1=スニーク中

# 初期値クリア
m.execute('scoreboard players reset @a sneak_prev')
m.execute('scoreboard players reset @a is_sneaking')
m.execute('scoreboard players reset @a sneak_state')

m.echo("🕵️‍♂️ Sneak start/stop detection running")

# --- メインループ ---
while True:
    # 現在の累積スニーク時間が前フレームより大きければスニーク中 -> is_sneaking = 1
    m.execute('execute as @a if score @s sneak_time > @s sneak_prev run scoreboard players set @s is_sneaking 1')
    m.execute('execute as @a unless score @s sneak_time > @s sneak_prev run scoreboard players set @s is_sneaking 0')

    # --- スニーク開始・終了の判定 ---
    # sneak_state = 前回の状態（0=非スニーク, 1=スニーク中）
    # is_sneaking = 今回の状態

    # スニーク開始
    m.execute('execute as @a if score @s is_sneaking matches 1 if score @s sneak_state matches 0 run tellraw @s {"text":"💨 スネーク開始！","color":"yellow"}')
    m.execute('execute as @a if score @s is_sneaking matches 1 run scoreboard players set @s sneak_state 1')

    # スニーク終了
    m.execute('execute as @a if score @s is_sneaking matches 0 if score @s sneak_state matches 1 run tellraw @s {"text":"🛑 スネーク終了！","color":"red"}')
    m.execute('execute as @a if score @s is_sneaking matches 0 run scoreboard players set @s sneak_state 0')

    # 現在の累積値を前回値にコピー
    m.execute('execute as @a run scoreboard players operation @s sneak_prev = @s sneak_time')

    time.sleep(TICK_DELAY)
