import minescript as m
import time
import math

# ==================================================
# CLOCK SNEAK TP SYSTEM
# ==================================================

# -------------------------
# 設定
# -------------------------

TICK = 0.1
COOLDOWN = 20

ITEM_ID = "minecraft:command_block"
ITEM_NAME = '{"text":"TP Stick","color":"gold"}'

# -------------------------
# スコアボード
# -------------------------

SNEAK_SCORE = "sneak_time"
SNEAK_STATE = "sneak_state"
SNEAK_PREV = "sneak_prev"
SNEAK_CD = "sneak_cd"

# -------------------------
# HOME座標
# -------------------------

HOME_X = None
HOME_Y = None
HOME_Z = None

# ==================================================
# 初期化
# ==================================================

def init_scoreboard():

    try:
        m.execute(f"scoreboard objectives add {SNEAK_SCORE} minecraft.custom:minecraft.sneak_time")
    except:
        pass

    for sb in [SNEAK_STATE, SNEAK_PREV, SNEAK_CD]:
        try:
            m.execute(f"scoreboard objectives add {sb} dummy")
        except:
            pass


def give_tp_stick():
    """
    TP棒を持っていないプレイヤーに配布
    """
    m.execute(
        f'''
        execute as @a
        unless entity @s[nbt={{Inventory:[{{id:"{ITEM_ID}"}}]}}]
        run give @s command_block[custom_name='{ITEM_NAME}'] 1
        '''
    )


# ==================================================
# スニーク判定
# ==================================================

def update_sneak():

    # スニーク開始検知
    m.execute(
        f"execute as @a if score @s {SNEAK_SCORE} > @s {SNEAK_PREV} run scoreboard players set @s {SNEAK_STATE} 1"
    )

    m.execute(
        f"execute as @a unless score @s {SNEAK_SCORE} > @s {SNEAK_PREV} run scoreboard players set @s {SNEAK_STATE} 0"
    )

    # クール中は無効
    m.execute(
        f"execute as @a[scores={{sneak_cd=1..}}] run scoreboard players set @s {SNEAK_STATE} 0"
    )


# ==================================================
# TP処理
# ==================================================

def teleport_home():

    global HOME_X, HOME_Y, HOME_Z

    m.execute(
        f'''
        execute as @a[
            scores={{sneak_state=1}},
            nbt={{SelectedItem:{{id:"{ITEM_ID}"}}}}
        ]
        run tp @s {HOME_X} {HOME_Y} {HOME_Z}
        '''
    )

    m.execute(
        f'''
        execute as @a[
            scores={{sneak_state=1}},
            nbt={{SelectedItem:{{id:"{ITEM_ID}"}}}}
        ]
        run tellraw @s {{"text":"ホームに戻りました","color":"green"}}
        '''
    )

    # クールタイム
    m.execute(
        f'''
        execute as @a[scores={{sneak_state=1}}]
        run scoreboard players set @s {SNEAK_CD} {COOLDOWN}
        '''
    )


# ==================================================
# クールダウン
# ==================================================

def update_cooldown():

    m.execute(
        f"scoreboard players remove @a[scores={{sneak_cd=1..}}] {SNEAK_CD} 1"
    )


# ==================================================
# スニーク履歴更新
# ==================================================

def update_prev():

    m.execute(
        f"scoreboard players operation @a {SNEAK_PREV} = @a {SNEAK_SCORE}"
    )


# ==================================================
# メイン
# ==================================================

init_scoreboard()

m.echo("TP Stick System Started")

while True:

    # -------------------------
    # HOME座標取得
    # -------------------------

    if HOME_X is None:
        HOME_X, HOME_Y, HOME_Z = map(math.floor, m.player_position())
        m.echo(f"HOME SET : {HOME_X} {HOME_Y} {HOME_Z}")

    # -------------------------
    # TP棒配布
    # -------------------------

    give_tp_stick()

    # -------------------------
    # スニーク更新
    # -------------------------

    update_sneak()

    # -------------------------
    # TP処理
    # -------------------------

    teleport_home()

    # -------------------------
    # クールダウン
    # -------------------------

    update_cooldown()

    # -------------------------
    # 前回スニーク値更新
    # -------------------------

    update_prev()

    time.sleep(TICK)