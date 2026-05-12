import minescript as m
import time

TICK_DELAY = 0.1
ITEM = "minecraft:carrot_on_a_stick"
DIST = 3
TP_Y = -64

# ==============================
# Scoreboard
# ==============================
m.execute("scoreboard objectives add used_carrot minecraft.used:carrot_on_a_stick")
m.execute("scoreboard objectives add used_prev dummy")

# ==============================
# Main loop
# ==============================
while True:

    # ==========================
    # ① 視線で光らせる
    # ==========================
    m.execute(f'execute as @a if entity @s[nbt={{SelectedItem:{{id:"{ITEM}"}}}}] at @s anchored eyes positioned ^ ^ ^{DIST} run tag @e[type=!player,limit=1,sort=nearest,distance=..1] add target')

    m.execute("effect give @e[tag=target] glowing 1 1 true")

    # ==========================
    # ② 右クリック検知（差分）
    # ==========================
    m.execute('execute as @a if score @s used_carrot > @s used_prev run tag @s add just_clicked')

    # ==========================
    # ③ 捕獲
    # ==========================
    m.execute("execute as @a[tag=just_clicked] if entity @e[tag=target] run give @s minecraft:pig_spawn_egg 1")

    m.execute(f'execute as @a[tag=just_clicked] at @s run tp @e[tag=target,limit=1,sort=nearest] ~ {TP_Y} ~')
    m.execute("execute as @a[tag=just_clicked] run kill @e[tag=target,limit=1,sort=nearest]")

    # ==========================
    # ④ 後処理
    # ==========================
    m.execute("tag @a[tag=just_clicked] remove just_clicked")
    m.execute("tag @e[tag=target] remove target")

    # ★ここが超重要
    m.execute('execute as @a run scoreboard players operation @s used_prev = @s used_carrot')

    time.sleep(TICK_DELAY)
