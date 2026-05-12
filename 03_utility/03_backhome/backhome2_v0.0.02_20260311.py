import minescript as m
import time
import math

# -------------------------
# 設定
# -------------------------
ITEM = "minecraft:clock"  # TPアイテム
TICK = 0.1                 # ループ間隔（秒）
COOLDOWN = 20              # クールタイム（ティック単位）

# ホーム座標（初期値はNone）
HOME_X = HOME_Y = HOME_Z = None

# スコアボード名
SNEAK_SCORE = "sneak_time"
SNEAK_STATE = "sneak_state"
SNEAK_PREV = "sneak_prev"
SNEAK_COOLDOWN = "sneak_cd"

# -------------------------
# スコアボード作成
# -------------------------
try:
    m.execute(f"scoreboard objectives add {SNEAK_SCORE} minecraft.custom:minecraft.sneak_time")
except:
    pass

for sb in [SNEAK_STATE, SNEAK_PREV, SNEAK_COOLDOWN]:
    try:
        m.execute(f"scoreboard objectives add {sb} dummy")
    except:
        pass

m.echo("Clock Sneak TP System Started")

# -------------------------
# メインループ
# -------------------------
while True:

    # HOME座標をまだ設定していない場合は、最初のプレイヤー位置を取得
    if HOME_X is None:
        HOME_X, HOME_Y, HOME_Z = map(math.floor,m.player_position())
        m.echo(f"ホーム座標を設定: {HOME_X}, {HOME_Y}, {HOME_Z}")

    # スニーク状態判定
    m.execute(f"execute as @a if score @s {SNEAK_SCORE} > @s {SNEAK_PREV} run scoreboard players set @s {SNEAK_STATE} 1")
    m.execute(f"execute as @a unless score @s {SNEAK_SCORE} > @s {SNEAK_PREV} run scoreboard players set @s {SNEAK_STATE} 0")

    # クールタイム中は発動不可
    m.execute(f"execute as @a[scores={{sneak_cd=1..}}] run scoreboard players set @s {SNEAK_STATE} 0")

    # 時計を持ってスニーク状態のプレイヤーをTP
    m.execute(f'execute as @a[scores={{sneak_state=1}},nbt={{SelectedItem:{{id:"{ITEM}"}}}}] run tp @s {HOME_X} {HOME_Y} {HOME_Z}')
    m.execute(f'execute as @a[scores={{sneak_state=1}},nbt={{SelectedItem:{{id:"{ITEM}"}}}}] run tellraw @s {{"text":"ホームに戻りました","color":"green"}}')

    # クールタイムセット（1回TPしたらCOOLDOWNティック発動不可）
    m.execute(f"execute as @a[scores={{sneak_state=1}}] run scoreboard players set @s {SNEAK_COOLDOWN} {COOLDOWN}")

    # クールタイムカウントダウン
    m.execute(f"scoreboard players remove @a[scores={{sneak_cd=1..}}] {SNEAK_COOLDOWN} 1")

    # スニーク前状態を更新
    m.execute(f"scoreboard players operation @a {SNEAK_PREV} = @a {SNEAK_SCORE}")

    time.sleep(TICK)
