import minescript as m
import time

TICK_DELAY = 0.5
ITEM = "minecraft:carrot_on_a_stick"
DIST = 3
TP_Y = -64

m.execute("scoreboard objectives add used minecraft.used:carrot_on_a_stick")
m.execute("scoreboard objectives add used_prev dummy")

while True:

    players = m.players()

    # ==========================
    # ① 視線検知
    # ==========================
    for p in players:
        name = p.name
        tag = f"target_{name}"

        m.execute(f"tag @e[tag={tag}] remove {tag}")

        m.execute(f'execute as @a[name={name}] if entity @s[nbt={{SelectedItem:{{id:"{ITEM}"}}}}] at @s anchored eyes positioned ^ ^ ^{DIST} run tag @e[type=!player,limit=1,sort=nearest,distance=..1] add {tag}')

        m.execute(f"effect give @e[tag={tag}] glowing 1 1 true")

    # ==========================
    # ② クリック検知（差分）
    # ==========================
    m.execute('execute as @a if score @s used > @s used_prev run tag @s add just_clicked')

    # ==========================
    # ③ 捕獲
    # ==========================
    for p in players:
        name = p.name
        tag = f"target_{name}"

        # give
        m.execute(f'execute as @a[name={name},tag=just_clicked] if entity @e[tag={tag}] run give @s minecraft:pig_spawn_egg 1')

        # tp
        m.execute(f'execute as @a[name={name},tag=just_clicked] at @s run tp @e[tag={tag},limit=1,sort=nearest] ~ {TP_Y} ~')

        # kill
        m.execute(f'execute as @a[name={name},tag=just_clicked] run kill @e[tag={tag},limit=1,sort=nearest]')

    # ==========================
    # ④ 後処理
    # ==========================
    m.execute("tag @a[tag=just_clicked] remove just_clicked")
    m.execute("execute as @a run scoreboard players operation @s used_prev = @s used")

    time.sleep(TICK_DELAY)
