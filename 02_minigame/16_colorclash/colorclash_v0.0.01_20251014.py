import minescript as m
import time

TICK_DELAY = 0.1  # tick間隔（秒）

# 変換ルール：元ブロック → 置換ブロック
COLOR_MAP = {
    "dirt": "yellow_concrete",
    "grass_block": "green_concrete",
    "stone": "light_blue_concrete",
    "sand": "red_concrete",
    "gravel": "orange_concrete",
}

while True:
    for block, color in COLOR_MAP.items():
        # 雪玉が当たったら指定ブロックを色付きコンクリートに置換
        m.execute(
            f"execute as @e[type=snowball] at @s run fill ~-1 ~-1 ~-1 ~1 ~1 ~1 {color} replace {block}"
        )
    time.sleep(TICK_DELAY)
