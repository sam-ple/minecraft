import minescript as m
import time

# Full Inventory Support
# Enhances the item count logic to **sum across all inventory slots**, not just the first.
# Ensures milestones and CLEAR detection work correctly even with multiple stacks.

IRON_ID = "minecraft:iron_ingot"
GOAL = 100
last_notified = 0
last_shown_count = -1  # Ensure the action bar shows at least once
cleared = False

def get_iron_count():
    # Count all iron ingots across the entire inventory
    inv = m.player_inventory()
    total = 0
    for item in inv:
        if item.item == IRON_ID:
            total += item.count
    return total

def show_actionbar(count):
    # Display the current iron count in the action bar
    m.execute(f'title @a actionbar {{"text":"Iron: {count}/{GOAL}","color":"gray"}}')

def notify_milestone(count):
    # Notify when a multiple of 10 ingots is reached
    m.execute(f'tellraw @a {{"text":"Iron Collected: {count}","color":"yellow"}}')

def notify_clear():
    # Notify when the collection goal is achieved
    m.execute('title @a title {"text":"CLEAR!","color":"green","bold":true}')
    m.execute(f'tellraw @a {{"text":"You have collected {GOAL} iron ingots!","color":"aqua"}}')

def main_loop():
    global last_notified, last_shown_count, cleared
    while True:
        count = get_iron_count()

        # Only update the action bar if the count has changed
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
