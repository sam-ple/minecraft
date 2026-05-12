# Fabric 1.21.8 / Minescript 5.0b1 / Minescript Plus v0.10a
# Pull from chest (top area only) → close → open inventory → auto-equip armor & put a sword into hotbar 0 → close
import time
import minescript as m
from minescript_plus import Inventory, Keybind, Screen

_busy = False

# Predicates
ARMOR_SUFFIXES = ("_helmet", "_chestplate", "_leggings", "_boots")
SPECIAL_HELMETS = ("minecraft:turtle_helmet", "minecraft:carved_pumpkin")

def is_sword(it: str) -> bool:
    return it and it.endswith("_sword")

def is_armor(it: str) -> bool:
    return it and (it.endswith(ARMOR_SUFFIXES) or it in SPECIAL_HELMETS)

# ===== Pull from container (chest-side only) =====
def pull_all_from_chest_only_top(max_pass=10, sleep_s=0.01):
    """Pull all items from the *upper chest area only* and return count"""
    moved = 0
    try:
        total = m.container_size()  # e.g., single 27+36=63, double 54+36=90
        chest_slots = max(0, min(54, total - 36)) or 27
    except Exception:
        chest_slots = 27

    for _ in range(max_pass):
        items = m.container_get_items() or []
        # Stop if chest-side is empty
        chest_has_item = any(st.slot < chest_slots for st in items)
        if not chest_has_item:
            break

        moved_this = 0
        for s in range(chest_slots):
            if Inventory.shift_click_slot(s):  # chest → player
                moved += 1
                moved_this += 1
                time.sleep(sleep_s)
        if moved_this == 0:
            break
    return moved

# ===== Inventory organizing (in inventory view slot indices) =====
def equip_armor_and_put_sword_hotbar0():
    """Assumes the player inventory screen is open; auto-equip armor and place a sword in hotbar 0"""
    equipped = 0
    moved_sword = 0

    # 1) Armor: shift-clicking armor in view 9..44 auto-equips to empty armor slots
    for _ in range(3):  # multiple passes to handle reshuffles
        changed = False
        for st in sorted(m.container_get_items() or [], key=lambda s: s.slot):
            if 9 <= st.slot <= 44 and is_armor(st.item):
                if Inventory.shift_click_slot(st.slot):
                    equipped += 1
                    changed = True
                    time.sleep(0.01)
        if not changed:
            break

    # 2) Sword: if hotbar 0 doesn't have a sword, swap a sword from 9..44 into hotbar 0
    items = {st.slot: st for st in (m.container_get_items() or [])}
    has_sword_in_hotbar0 = (36 in items and is_sword(items[36].item))

    if not has_sword_in_hotbar0:
        sword_slot = None
        for st in (m.container_get_items() or []):
            if 9 <= st.slot <= 44 and is_sword(st.item):
                sword_slot = st.slot
                break
        if sword_slot is not None:
            if Inventory.inventory_hotbar_swap(sword_slot, 0):  # number-key style swap
                moved_sword += 1
                time.sleep(0.02)

    return equipped, moved_sword

# ===== Main (G key) =====
def pull_then_equip():
    global _busy
    if _busy:
        m.echo("⏳ Already running…")
        return
    _busy = True
    try:
        # 1) Open the chest
        if not Inventory.open_targeted_chest():
            m.echo("⚠️ Look straight at a chest/barrel/shulker and try again.")
            return

        # 2) Pull only the upper container area; when empty, close
        moved_from_chest = pull_all_from_chest_only_top()
        try:
            Screen.close_screen()
        except Exception:
            pass

        # 3) Open player inventory and organize
        opened = False
        try:
            # Use dedicated API if available; otherwise press the inventory keybind (default 'E')
            if hasattr(Screen, "open_inventory") and Screen.open_inventory():
                opened = True
            else:
                m.press_key_bind("key.inventory", True); time.sleep(0.05)
                m.press_key_bind("key.inventory", False)
                opened = Screen.wait_screen(delay=1200)
        except Exception:
            opened = False

        equipped = moved_sword = 0
        if opened:
            equipped, moved_sword = equip_armor_and_put_sword_hotbar0()
            # 4) Close inventory
            try:
                Screen.close_screen()
            except Exception:
                pass
        else:
            m.echo("⚠️ Couldn't open inventory; skipping organization.")

        m.echo(f"✅ Pulled {moved_from_chest} / Equipped {equipped} / Sword→hotbar0 {moved_sword}")
    finally:
        _busy = False

# Bind G
kb = Keybind()
kb.set_keybind(
    71,
    pull_then_equip,
    name="PullAll_ThenEquip",
    category="Minescript+",
    description="Pull chest-side slots only; close; open inventory to auto-equip armor and move a sword to hotbar 0; close."
)

m.echo("🎹 G: Pull from chest → close → open inventory → equip armor & put sword in slot 0 → close")
while True:
    time.sleep(1)
