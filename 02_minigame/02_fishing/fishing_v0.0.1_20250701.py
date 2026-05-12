import minescript as m
import time
import json

m.execute('/item replace entity @p hotbar.0 with minecraft:fishing_rod')

map_enchants = [
    "minecraft:luck_of_the_sea 3",
    "minecraft:lure 3",
    "minecraft:unbreaking 3",
    "minecraft:mending 1"
]
for ench in map_enchants:
    m.execute(f"/enchant @p {ench}")
    
POINTS = {
    "minecraft:cod": 1,
    "minecraft:salmon": 2,
    "minecraft:pufferfish": 3,
    "minecraft:tropical_fish": 5,
    "minecraft:enchanted_book": 10,
    "minecraft:name_tag": 8,
    "minecraft:nautilus_shell": 6,
    "minecraft:saddle": 7,
}

def tell_score(score):
    m.execute(f'title @a actionbar {{"text":"Score: {score}","color":"green"}}')

def tell_message(msg, color="white"):
    m.execute(f'tellraw @a {{"text":"{msg}","color":"{color}"}}')

def snapshot_inventory():
    inv = m.player_inventory()
    return {item.item: item.count for item in inv if item.count > 0}

# Game starts
score = 0
duration = 180  # seconds
start_time = time.time()
end_time = start_time + duration

prev_items = snapshot_inventory()

tell_message("Fishing Game Started! You have 180 seconds.", "yellow")

while True:
    current_time = time.time()
    if current_time >= end_time:
        tell_message(f"Time's up! Final score: {score}", "gold")
        break

    current_items = snapshot_inventory()

    for item_id in current_items:
        if item_id in POINTS:
            prev_count = prev_items.get(item_id, 0)
            curr_count = current_items[item_id]
            if curr_count > prev_count:
                delta = curr_count - prev_count
                added_score = delta * POINTS[item_id]
                score += added_score
                tell_message(f"+{added_score} points for {item_id.split(':')[1]}", "aqua")
                tell_score(score)

    prev_items = current_items
    time.sleep(0.25)
