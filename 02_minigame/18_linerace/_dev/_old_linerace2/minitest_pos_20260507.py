import minescript as m
import time

# ============================================
# SETTINGS
# ============================================

TICK = 1

PLAYERS = [
    "crocadooo",
    "saaample",
]

# ============================================
# INIT OBJECTIVES
# ============================================

OBJECTIVES = [
    "PosX",
    "PosZ",
    "StartX",
    "StartZ",
    "Dist"
]

for obj in OBJECTIVES:
    m.execute(f"scoreboard objectives add {obj} dummy")

# sidebar表示
m.execute("scoreboard objectives setdisplay sidebar Dist")

# ============================================
# SAVE START POSITION
# ============================================

# 現在位置を保存
m.execute(
    "execute as @a "
    "store result score @s StartX "
    "run data get entity @s Pos[0] 100"
)

m.execute(
    "execute as @a "
    "store result score @s StartZ "
    "run data get entity @s Pos[2] 100"
)

# ============================================
# MAIN LOOP
# ============================================

while True:

    # ----------------------------------------
    # 現在座標更新
    # ----------------------------------------

    m.execute(
        "execute as @a "
        "store result score @s PosX "
        "run data get entity @s Pos[0] 100"
    )

    m.execute(
        "execute as @a "
        "store result score @s PosZ "
        "run data get entity @s Pos[2] 100"
    )

    # ----------------------------------------
    # 距離計算
    # Dist = PosZ - StartZ
    # ----------------------------------------

    m.execute(
        "execute as @a "
        "run scoreboard players operation @s Dist = @s PosZ"
    )

    m.execute(
        "execute as @a "
        "run scoreboard players operation @s Dist -= @s StartZ"
    )

    # ----------------------------------------
    # チャット表示
    # ----------------------------------------

    for name in PLAYERS:

        m.execute(
            f'tellraw @a ['
            f'{{"text":"{name} Distance : ","color":"yellow"}},'
            f'{{"score":{{"name":"{name}","objective":"Dist"}},"color":"green"}}'
            f']'
        )

    time.sleep(TICK)
