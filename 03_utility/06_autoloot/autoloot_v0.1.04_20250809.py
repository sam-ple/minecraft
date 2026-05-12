# Pull from chest, then upgrade to the best armor & best sword
# Fabric 1.21.8 / Minescript 5.0b1 / Minescript Plus v0.10a
import time
import minescript as m
from minescript_plus import Inventory, Keybind, Screen

_busy = False

# ---- Ranking tables ----
ARMOR_ORDER = ["leather", "gold", "chainmail", "iron", "turtle", "diamond", "netherite"]
SWORD_ORDER = ["wood", "gold", "stone", "iron", "diamond", "netherite"]

# Inventory-screen view indices for armor slots
ARMOR_SLOTS = {
    "head": 5,
    "chest": 6,
    "legs": 7,
    "feet": 8,
}
ARMOR_SUFFIX = {
    "head": "_helmet",
    "chest": "_chestplate",
    "legs": "_leggings",
    "feet": "_boots",
}
SPECIAL_HELMETS = ("minecraft:turtle_helmet",)  # pumpkins are ignored as armor

def _mat_of(item_id: str) -> str | None:
    if not item_id:
        return None
    it = item_id.split(":")[-1]
    # normalize "golden_" -> "gold_", "wooden_" -> "wood_"
    it = it.replace("golden_", "gold_").replace("wooden_", "wood_")
    if it == "turtle_helmet":
        return "turtle"
    for mname in ["netherite","diamond","iron","chainmail","gold","leather","stone","wood"]:
        if it.startswith(mname + "_"):
            return mname
    return None

def _armor_score(item_id: str) -> int:
    if not item_id: return -1
    if item_id.endswith("carved_pumpkin"): return -1
    mat = _mat_of(item_id)
    return ARMOR_ORDER.index(mat) if mat in ARMOR_ORDER else -1

def _sword_score(item_id: str) -> int:
    if not item_id or not item_id.endswith("_sword"): return -1
    mat = _mat_of(item_id)
    return SWORD_ORDER.index(mat) if mat in SWORD_ORDER else -1

# ---- Pull chest-side only (prevents back-and-forth loops) ----
def pull_all_from_chest_only_top():
    moved = 0
    try:
        total = m.container_size()       # e.g., single 63, double 90
        chest_slots = max(0, min(54, total - 36)) or 27
    except Exception:
        chest_slots = 27

    while True:
        items = m.container_get_items() or []
        if not any(st.slot < chest_slots for st in items):
            break
        moved_this = 0
        for s in range(chest_slots):
            if Inventory.shift_click_slot(s):
                moved += 1
                moved_this += 1
                time.sleep(0.01)
        if moved_this == 0:
            break
    return moved

# ---- In inventory view, swap to the strongest gear/weapon ----
def equip_best_armor_and_best_sword():
    equipped_or_swapped = 0

    def refresh_items():
        return {st.slot: st for st in (m.container_get_items() or [])}

    # 1) Armor: for each part, compare current (5..8) vs best in 9..44; swap if better
    items = refresh_items()
    for part, suffix in ARMOR_SUFFIX.items():
        armor_slot = ARMOR_SLOTS[part]
        cur_item = items.get(armor_slot).item if armor_slot in items else None
        cur_score = _armor_score(cur_item)

        # find best candidate in 9..44
        best_slot, best_item, best_score = None, None, -1
        for slot, st in items.items():
            if 9 <= slot <= 44 and st.item:
                it = st.item
                if it.endswith(suffix) or (part == "head" and it in SPECIAL_HELMETS):
                    sc = _armor_score(it)
                    if sc > best_score:
                        best_slot, best_item, best_score = slot, it, sc

        if best_score > cur_score:
            # manual swap: pick -> click armor -> click back to original slot
            Inventory.click_slot(best_slot, right_button=False)      # pick best
            time.sleep(0.01)
            Inventory.click_slot(armor_slot, right_button=False)     # place (swap occurs)
            time.sleep(0.01)
            Inventory.click_slot(best_slot, right_button=False)      # put remainder back
            time.sleep(0.01)
            equipped_or_swapped += 1
            items = refresh_items()

    # 2) Sword: find best in 9..44; compare with hotbar0 (view 36); swap if better
    items = refresh_items()
    hotbar0_item = items.get(36).item if 36 in items else None
    hotbar0_score = _sword_score(hotbar0_item)

    best_slot, best_item, best_score = None, None, -1
    for slot, st in items.items():
        if 9 <= slot <= 44 and st.item and st.item.endswith("_sword"):
            sc = _sword_score(st.item)
            if sc > best_score:
                best_slot, best_item, best_score = slot, st.item, sc

    if best_score > hotbar0_score and best_slot is not None:
        if Inventory.inventory_hotbar_swap(best_slot, 0):  # number-key style swap
            equipped_or_swapped += 1
            time.sleep(0.02)

    return equipped_or_swapped

# ---- Main (G key) ----
def pull_then_upgrade():
    global _busy
    if _busy:
        m.echo("⏳ Already running…")
        return
    _busy = True
    try:
        if not Inventory.open_targeted_chest():
            m.echo("⚠️ Look straight at a chest/barrel/shulker and try again.")
            return
        moved = pull_all_from_chest_only_top()
        try:
            Screen.close_screen()
        except Exception:
            pass

        # Open inventory and upgrade to the best armor/sword
        opened = False
        try:
            m.press_key_bind("key.inventory", True); time.sleep(0.05)
            m.press_key_bind("key.inventory", False)
            opened = Screen.wait_screen(delay=1200)
        except Exception:
            opened = False

        upgraded = 0
        if opened:
            upgraded = equip_best_armor_and_best_sword()
            try:
                Screen.close_screen()
            except Exception:
                pass
        else:
            m.echo("⚠️ Couldn't open inventory; skipping upgrades.")

        m.echo(f"✅ Pulled {moved} / Upgraded {upgraded} (armor & sword)")
    finally:
        _busy = False

# Bind G
kb = Keybind()
kb.set_keybind(
    71,
    pull_then_upgrade,
    name="PullAndUpgrade",
    category="Minescript+",
    description="Pull chest, then auto-upgrade armor & move best sword to hotbar 0."
)

m.echo("🎹 G: Pull from chest → close → open inventory → swap to stronger armor/sword → close")
while True:
    time.sleep(1)