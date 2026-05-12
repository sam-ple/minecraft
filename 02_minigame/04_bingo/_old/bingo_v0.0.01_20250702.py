import minescript as m
import time
import json
from threading import Thread

# 3x3 Bingo items
bingo_items = [
    "minecraft:apple", "minecraft:bread", "minecraft:carrot",
    "minecraft:potato", "minecraft:cooked_beef", "minecraft:cooked_porkchop",
    "minecraft:melon_slice", "minecraft:cookie", "minecraft:beetroot_soup",
]

# Track collection status
got = {item: False for item in bingo_items}
bingo_achieved = False
start_time = 0
last_status_time = 0
STATUS_COOLDOWN = 5

def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def snapshot_inventory():
    inv = m.player_inventory()
    return {item.item: item.count for item in inv if item.count > 0}

def print_separator():
    m.execute('tellraw @a {"text":"-------------","color":"gray"}')

def title(text, color="white"):
    m.execute(f'title @a title {{"text":"{text}","color":"{color}","bold":true}}')

# Show only the bingo marks in 3x3 grid [x] or [ ]
def tellraw_bingo_marks():
    lines = []
    for i in range(3):
        row = ""
        for j in range(3):
            item = bingo_items[i * 3 + j]
            mark = "[x]" if got[item] else "[ ]"
            row += f"{mark} "
        lines.append({"text": row.strip(), "color": "white"})
        lines.append({"text": "\n"})
    lines.pop()  # remove last newline
    m.execute(f'tellraw @a {json.dumps({"text": "", "extra": lines}, ensure_ascii=False)}')

# Show detailed list per row with marks and item names (name always shown)
def tellraw_bingo_items():
    components = []
    for i in range(3):
        row_header = f"{i+1} row"
        components.append({"text": row_header, "color": "gold"})
        components.append({"text": "\n"})
        for j in range(3):
            item = bingo_items[i * 3 + j]
            mark = "[x]" if got[item] else "[ ]"
            name = item.split(":")[1].replace("_", " ").title()
            line = f"{mark} {name}"
            components.append({"text": line, "color": "white"})
            components.append({"text": "\n"})
    components.pop()
    m.execute(f'tellraw @a {json.dumps({"text": "", "extra": components}, ensure_ascii=False)}')

# Combined display for bingo status
def show_bingo_status():
    print_separator()
    tellraw_bingo_marks()
    tellraw_bingo_items()
    print_separator()

def listen_chat_commands():
    global got, bingo_achieved, last_status_time
    with m.EventQueue() as eq:
        eq.register_chat_listener()
        while True:
            event = eq.get()
            if event.type == m.EventType.CHAT:
                msg = event.message.lower()
                now = time.time()
                if "reset" in msg:
                    got = {item: False for item in bingo_items}
                    bingo_achieved = False
                    start_game()
                elif "status" in msg and now - last_status_time > STATUS_COOLDOWN:
                    last_status_time = now
                    m.execute('tellraw @a {"text":"Bingo Progress","color":"gold"}')
                    show_bingo_status()

def check_bingo():
    grid = [got[item] for item in bingo_items]
    lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6],             # diagonals
    ]
    for line in lines:
        if all(grid[i] for i in line):
            return True
    return False

def start_game():
    global start_time
    print_separator()
    for count in ["3", "2", "1"]:
        title(count, "gold")
        time.sleep(1)
    title("Start!", "green")
    time.sleep(1)
    start_time = time.time()
    m.execute(f'tellraw @a {{"text":"Start 3x3 Bingo!","color":"yellow"}}')
    show_bingo_status()
    print_separator()

def main_loop():
    global bingo_achieved
    prev_items = snapshot_inventory()
    while True:
        current_items = snapshot_inventory()
        for item in bingo_items:
            if not got[item]:
                if current_items.get(item, 0) > prev_items.get(item, 0):
                    got[item] = True
                    name = item.split(":")[1].replace("_", " ").title()
                    m.execute(f'title @a subtitle {{"text":"Collected: {name}","color":"aqua"}}')
                    show_bingo_status()
                    if not bingo_achieved and check_bingo():
                        bingo_achieved = True
                        elapsed = format_time(time.time() - start_time)
                        title("BINGO!", "green")
                        m.execute(f'tellraw @a {{"text":"Bingo achieved!","color":"gold"}}')
                        m.execute(f'tellraw @a {{"text":"Time: {elapsed}","color":"aqua"}}')
                        print_separator()
        prev_items = current_items
        time.sleep(0.3)

# Start the chat listener thread and the game
Thread(target=listen_chat_commands).start()
start_game()
main_loop()
