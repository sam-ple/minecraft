import minescript as m
import time

TICK_DELAY = 0.1  # tick間隔（秒）

# 矢の着弾時に置き換えるブロック
REPLACE_BLOCK = "red_concrete"
TARGET_BLOCK = "grass_block"

while True:
    # 矢がブロックに刺さったら着弾処理
    m.execute(
        f"execute as @e[type=arrow,nbt={{inGround:1b}}] at @s run fill ~-1 ~-1 ~-1 ~1 ~1 ~1 {REPLACE_BLOCK} replace {TARGET_BLOCK}"
    )
    time.sleep(TICK_DELAY)
