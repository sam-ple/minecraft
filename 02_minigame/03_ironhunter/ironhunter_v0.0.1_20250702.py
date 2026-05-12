import minescript as m
import time

# Basic Counter
# Tracks the number of iron ingots in the player’s inventory.
# Displays the count using the **action bar**.
# Sends a milestone message every **10 iron ingots** collected.
# Shows a **“CLEAR!” title** when the player collects **100**.

IRON_ID = "minecraft:iron_ingot"
GOAL = 100
last_notified = 0
last_shown_count = -1  # To ensure the action bar shows at least once
cleared = False

def get_iron_count():
    inv = m.player_inventory()
    for item in inv:
        if item.item == IRON_ID:
            return item.count
    return 0

def show_actionbar(count):
    m.execute(f'title @a actionbar {{"text":"Iron: {count}/{GOAL}","color":"gray"}}')

def notify_milestone(count):
    m.execute(f'tellraw @a {{"text":"Iron Collected: {count}","color":"yellow"}}')

def notify_clear():
    m.execute('title @a title {"text":"CLEAR!","color":"green","bold":true}')
    m.execute(f'tellraw @a {{"text":"You have collected {GOAL} iron ingots!","color":"aqua"}}')

def main_loop():
    global last_notified, last_shown_count, cleared
    while True:
        count = get_iron_count()

        # Only update action bar when count has changed
        if count != last_shown_count:
            show_actionbar(count)
            last_shown_count = count

        # Notify every 10 ingots collected (only once per milestone)
        if count >= last_notified + 10 and count < GOAL:
            last_notified = (count // 10) * 10
            notify_milestone(last_notified)

        # On completion
        if count >= GOAL and not cleared:
            cleared = True
            notify_clear()

        time.sleep(0.2)

main_loop()
