import minescript as m
import time

TICK_DELAY = 0.25

# スコアボード作成（初回のみ）
try:
    m.execute("/scoreboard objectives add arrowsHitTarget dummy")
except:
    pass

# ループ用カウンタ
i = 0

while True:
    # ループが生きているか
    m.execute(f'tellraw @a {{"text":"[DEBUG] tick {i}","color":"gray"}}')

    # ターゲットブロックに刺さった矢を数える
    m.execute(
        'execute as @e[type=arrow,nbt={inBlockState:{Name:"minecraft:target"}}] at @s run '
        'scoreboard players add @s arrowsHitTarget 1'
    )

    # カウント後に矢を消す（連打防止）
    m.execute(
        'execute as @e[type=arrow,nbt={inBlockState:{Name:"minecraft:target"}}] at @s run kill @s'
    )

    # プレイヤーに現在のカウントを表示（矢が刺さった数）
    m.execute(
        '/execute as @a run tellraw @s {"text":"Arrows hit target: ","color":"gold","extra":[{"score":{"name":"@s","objective":"arrowsHitTarget"}}]}'
    )

    i += 1
    time.sleep(TICK_DELAY)
