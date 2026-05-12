# Move All Items from Chest (without filtering)
# For Single Chest (slots 0–26)

from minescript_plus import Inventory

if Inventory.open_targeted_chest():
    chest_slots = list(range(27))  
    Inventory.take_items(chest_slots)
