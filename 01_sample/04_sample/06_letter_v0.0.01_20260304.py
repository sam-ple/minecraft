# -------------------------
# 標準ライブラリ
# -------------------------
from sys import (argv, exit)
from time import sleep
import random

# -------------------------
# 外部ライブラリ
# -------------------------
import minescript
from minescript import (execute, echo)

# -------------------------
# 引数
# -------------------------
arg1 = argv[1] if len(argv) > 1 else (echo("コマンドを指定してください。") or exit(1))
arg2 = argv[2] if len(argv) > 2 else None


if arg1 == "letter":

    x, y, z = minescript.player_position()
    x, y, z = int(x), int(y), int(z - 5)

    # 5×5ドットフォント
    letter_maps = {

        "H": [
            "█   █",
            "█   █",
            "█████",
            "█   █",
            "█   █",
        ],
        "E": [
            "█████",
            "█    ",
            "████ ",
            "█    ",
            "█████",
        ],
        "L": [
            "█    ",
            "█    ",
            "█    ",
            "█    ",
            "█████",
        ],
        "O": [
            "█████",
            "█   █",
            "█   █",
            "█   █",
            "█████",
        ],
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
        "P": [
            "████ ",
            "█   █",
            "████ ",
            "█    ",
            "█    ",
        ],
        "Y": [
            "█   █",
            " █ █ ",
            "  █  ",
            "  █  ",
            "  █  ",
        ],
        "！": [
            "  █  ",
            "  █  ",
            "  █  ",
            "     ",
            "  █  ",
        ],
        "×": [
            "█   █",
            " █ █ ",
            "  █  ",
            " █ █ ",
            "█   █",
        ],
        " ": [
            "     ",
            "     ",
            "     ",
            "     ",
            "     ",
        ],
    }

    colors = [
        "red_wool", "orange_wool", "yellow_wool",
        "lime_wool", "light_blue_wool", "blue_wool",
        "purple_wool", "magenta_wool", "pink_wool",
    ]

    word = "HELLO！ MINECRAFT × PYTHON"

    for idx, letter in enumerate(word):

        # 画面クリア
        for dy in range(5):
            for dx in range(5):
                bx = x + dx - 2
                by = y + 4 - dy
                bz = z
                execute(f"/setblock {bx} {by} {bz} minecraft:air")

        letter_map = letter_maps.get(letter)
        color = colors[idx % len(colors)]

        if letter_map:
            for dy, row in enumerate(letter_map):
                for dx, ch in enumerate(row):
                    if ch == "█":
                        bx = x + dx - 2
                        by = y + 4 - dy
                        bz = z
                        execute(f"/setblock {bx} {by} {bz} minecraft:{color}")

        echo(f"{letter} を表示！✨")
        sleep(0.2)

    echo("HELLO！MINECRAFT × PYTHON 完成！🎉")
