# ==============================
# sample_game.py
# common.py 利用サンプル
# ==============================

import time, sys
import minescript as m
from common import (
    chat, title_main,
    countdown_start, countdown_end,
    save_start_pos, setup_bossbar,
    update_bossbar, end_game_common
)

START_POS_FILE = "sample_start_pos.json"
DURATION = 30

game_active = False
start_time = 0
end_countdown_started = False

# ==============================
# start
# ==============================
def start_game():
    global game_active, start_time, end_countdown_started

    save_start_pos(START_POS_FILE)
    setup_bossbar("sample", "Sample Game", DURATION)

    countdown_start()

    start_time = time.time()
    game_active = True
    end_countdown_started = False

    chat("🎮 Sample Game Started!", "aqua")

# ==============================
# end
# ==============================
def end_game():
    global game_active
    game_active = False
    end_game_common("sample", START_POS_FILE)
    chat("🏁 Sample Game Ended", "gold")

# ==============================
# command
# ==============================
if len(sys.argv) >= 2:
    if sys.argv[1] == "start":
        start_game()
    sys.exit(0)

# ==============================
# main loop
# ==============================
while True:
    if game_active:
        remain = update_bossbar("sample", start_time, DURATION)

        if remain == 5 and not end_countdown_started:
            end_countdown_started = True
            countdown_end(5)

        if remain <= 0:
            end_game()

    time.sleep(0.1)

# players = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Heidi"] 