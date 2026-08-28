# Fabric 1.21.8 / Minescript 5.0b1 / Minescript Plus v0.10a
# Keybind: pull specific target items from a chest
import time
import minescript as m
from minescript_plus import Inventory, Keybind

# Target items
TARGET_ITEMS = [
    "minecraft:diamond",
    "minecraft:emerald",
    "minecraft:gold_ingot",
]

# Anti-spam guard
_busy = False

def move_items_from_chest():
    global _busy
    if _busy:
        m.echo("⏳ Already running…")
        return
    _busy = True
    try:
        if not Inventory.open_targeted_chest():
            m.echo("⚠️ Look straight at a chest/barrel/shulker and try again.")
            return

        chest_slot_range = range(27)  # Single chest assumed (use 54 for double chest)

        moved = 0
        for item_id in TARGET_ITEMS:
            while True:
                slot = Inventory.find_item(item_id, container=True)
                if slot is None or slot not in chest_slot_range:
                    break
                if not Inventory.shift_click_slot(slot):
                    m.echo(f"⚠️ Move failed: slot {slot}")
                    return
                moved += 1
                time.sleep(0.2)

        m.echo(f"✅ Target item transfer complete. (moved {moved})")
    finally:
        _busy = False

# Bind G (GLFW keycode 71)
kb = Keybind()
kb.set_keybind(
    71,
    move_items_from_chest,
    name="PullFromChest",
    category="Minescript+",
    description="Move target items from the targeted chest."
)

m.echo("🎹 Press 'G' to pull target items from the chest you're looking at.")

# Keep script alive (Keybind thread is daemon)
while True:
    time.sleep(1)
