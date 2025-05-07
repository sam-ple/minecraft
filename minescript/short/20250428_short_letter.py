# -------------------------
# 標準ライブラリ
# -------------------------
from sys import (argv, exit)
from time import sleep
import random

# -------------------------
# 外部ライブラリ
# -------------------------
# import minescript as msc
import minescript
from minescript import (execute, echo)

# -------------------------
# 引数
# -------------------------
arg1 = argv[1] if len(argv) > 1 else (echo("コマンドを指定してください。") or exit(1))
arg2 = argv[2] if len(argv) > 2 else None  # 指定がなければ None


if arg1 == "letter":
    import random

    x, y, z = minescript.player_position()
#    execute(f"/tp @p {x} {y} {z} 180 0")  
    x, y, z = int(x), int(y), int(z - 5)

    # 5×5の文字マップ
    letter_maps = {
        "M": [
            "█   █",
            "██ ██",
            "█ █ █",
            "█   █",
            "█   █",
        ],
        "I": [
            "█████",
            "  █  ",
            "  █  ",
            "  █  ",
            "█████",
        ],
        "N": [
            "█   █",
            "██  █",
            "█ █ █",
            "█  ██",
            "█   █",
        ],
        "E": [
            "█████",
            "█    ",
            "████ ",
            "█    ",
            "█████",
        ],
        "C": [
            "█████",
            "█    ",
            "█    ",
            "█    ",
            "█████",
        ],
        "R": [
            "████ ",
            "█   █",
            "████ ",
            "█  █ ",
            "█   █",
        ],
        "A": [
            " ███ ",
            "█   █",
            "█████",
            "█   █",
            "█   █",
        ],
        "F": [
            "█████",
            "█    ",
            "████ ",
            "█    ",
            "█    ",
        ],
        "T": [
            "█████",
            "  █  ",
            "  █  ",
            "  █  ",
            "  █  ",
        ],
    }

    # 色パターン
    colors = [
        "red_wool", "orange_wool", "yellow_wool",
        "lime_wool", "light_blue_wool", "blue_wool",
        "purple_wool", "magenta_wool", "pink_wool",
    ]

    word = "MINECRAFT"

    # 最初に空気で消しておく（きれいにする）
    for dy in range(5):
        for dx in range(5):
            bx = x + dx - 2  # 中心合わせ
            by = y + 4 - dy
            bz = z
            execute(f"/setblock {bx} {by} {bz} minecraft:air")

    # 文字を一文字ずつ表示
    for idx, letter in enumerate(word):
        # 毎回きれいに空白にしてから描画
        for dy in range(5):
            for dx in range(5):
                bx = x + dx - 2
                by = y + 4 - dy
                bz = z
                execute(f"/setblock {bx} {by} {bz} minecraft:air")
        
        # 対応する文字のドットマップ
        letter_map = letter_maps.get(letter)
        color = colors[idx % len(colors)]  # 色は順番で選ぶ

        if letter_map:
            for dy, row in enumerate(letter_map):
                for dx, ch in enumerate(row):
                    if ch == "█":
                        bx = x + dx - 2
                        by = y + 4 - dy
                        bz = z
                        execute(f"/setblock {bx} {by} {bz} minecraft:{color}")

        echo(f"{letter} を表示したよ！✨")
        sleep(1.5)  # 次の文字に行く前にちょっと待つ

    echo("MINECRAFT全部出し切ったよ！🎉")
