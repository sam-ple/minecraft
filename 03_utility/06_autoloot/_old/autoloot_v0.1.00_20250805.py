# Move Only Specific Items from Chest
from minescript_plus import Inventory
import time

# Items to extract
TARGET_ITEMS = [
    "minecraft:diamond",
    "minecraft:emerald",
    "minecraft:gold_ingot"
]

def move_items_from_chest():
    if not Inventory.open_targeted_chest():
        print("Failed to open chest.")
        return

    chest_slot_range = range(27)  # Single chest

    for item_id in TARGET_ITEMS:
        while True:
            slot = Inventory.find_item(item_id, container=True)
            if slot is None or slot not in chest_slot_range:
                break  # Move to next item
            if not Inventory.shift_click_slot(slot):
                print(f"Failed to move item from slot {slot}.")
                return
            print(f"Moved {item_id} from slot {slot}.")
            time.sleep(0.2)

    print("✅ Target item transfer complete.")

move_items_from_chest()
