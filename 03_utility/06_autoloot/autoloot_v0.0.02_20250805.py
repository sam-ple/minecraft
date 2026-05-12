# Move All Items from Chest (without filtering)
# For Single Chest (slots 0–26)
from minescript_plus import Inventory
import time

def move_items_from_chest():
    if not Inventory.open_targeted_chest():
        print("Failed to open chest.")
        return

    for slot in range(27):  # Single chest slots
        if Inventory.shift_click_slot(slot):
            print(f"Moved item from slot {slot}.")
            time.sleep(0.2)  # Stability delay
        else:
            print(f"Failed to move item from slot {slot}.")
            break

move_items_from_chest()
