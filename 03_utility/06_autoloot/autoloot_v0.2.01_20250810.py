# Fabric 1.21.8 / Minescript 5.0b1 / Minescript Plus v0.10a
# Pull from chest (skip weak gear) → auto-upgrade armor & sword → equip shield → close
import time
import minescript as m
from minescript_plus import Inventory, Keybind, Screen

_busy = False

# ---- Ranking tables ----
ARMOR_ORDER = ["leather", "gold", "chainmail", "iron", "turtle", "diamond", "netherite"]
SWORD_ORDER = ["wood", "gold", "stone", "iron", "diamond", "netherite"]

# Inventory-screen view indices for armor slots
ARMOR_SLOTS = {"head": 5, "chest": 6, "legs": 7, "feet": 8}
ARMOR_SUFFIX = {"head": "_helmet", "chest": "_chestplate", "legs": "_leggings", "feet": "_boots"}
SPECIAL_HELMETS = ("minecraft:turtle_helmet",)  # pumpkins ignored as armor

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

# ---------- weak gear filter (skip pulling from chest) ----------
_WEAK_MATS = {"leather", "wood", "chainmail", "turtle", "stone", "gold"}
_ARMOR_SUFFIXES_TUP = tuple(ARMOR_SUFFIX.values())

def _is_gear(item_id: str) -> bool:
    if not item_id:
        return False
    if item_id.endswith("_sword"):
        return True
    if any(item_id.endswith(suf) for suf in _ARMOR_SUFFIXES_TUP):
        return True
    if item_id in SPECIAL_HELMETS or item_id.endswith("carved_pumpkin"):
        return True
    return False

def is_weak_gear(item_id: str) -> bool:
    if not _is_gear(item_id):
        return False
    if item_id.endswith("carved_pumpkin"):
        return True
    mat = _mat_of(item_id)
    return mat in _WEAK_MATS
# ---------------------------------------------------------------

# ---- Pull chest-side only, skipping weak gear ----
def pull_all_from_chest_only_top():
    moved = 0
    try:
        total = m.container_size()       # e.g., single 63, double 90
        chest_slots = max(0, min(54, total - 36)) or 27
    except Exception:
        chest_slots = 27

    while True:
        items_by_slot = {st.slot: st for st in (m.container_get_items() or [])}
        # stop if chest-side empty
        if not any(s < chest_slots and s in items_by_slot for s in range(chest_slots)):
            break

        progress = 0
        for s in range(chest_slots):
            st = items_by_slot.get(s)
            if not st or not st.item:
                continue
            # skip weak gear (leather/wood/chainmail/turtle & pumpkins)
            if is_weak_gear(st.item):
                continue
            if Inventory.shift_click_slot(s):
                moved += 1
                progress += 1
                time.sleep(0.01)

        if progress == 0:
            break

    return moved

# ---- In inventory view, swap to the strongest gear/weapon + shield to offhand ----
def equip_best_armor_sword_shield():
    changed = 0
    shield_equipped = 0

    def refresh_items():
        return {st.slot: st for st in (m.container_get_items() or [])}

    # 1) Armor: for each part, compare current (5..8) vs best in 9..44; swap if better
    items = refresh_items()
    for part, suffix in ARMOR_SUFFIX.items():
        armor_slot = ARMOR_SLOTS[part]
        cur_item = items.get(armor_slot).item if armor_slot in items else None
        cur_score = _armor_score(cur_item)

        best_slot, best_item, best_score = None, None, -1
        for slot, st in items.items():
            if 9 <= slot <= 44 and st.item:
                it = st.item
                if it.endswith(suffix) or (part == "head" and it in SPECIAL_HELMETS):
                    sc = _armor_score(it)
                    if sc > best_score:
                        best_slot, best_item, best_score = slot, it, sc

        if best_score > cur_score and best_slot is not None:
            Inventory.click_slot(best_slot, right_button=False)
            time.sleep(0.01)
            Inventory.click_slot(armor_slot, right_button=False)
            time.sleep(0.01)
            Inventory.click_slot(best_slot, right_button=False)
            time.sleep(0.01)
            changed += 1
            items = refresh_items()

    # 2) Sword: best in 9..44 vs hotbar0 (view 36); swap if better
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
            changed += 1
            time.sleep(0.02)

    # 3) Shield → offhand (view 45)
    items = refresh_items()
    offhand_item = items.get(45).item if 45 in items else None
    if offhand_item != "minecraft:shield":
        # prefer 9..35 then 37..44 (avoid 36 to not disturb hotbar0 sword)
        search_order = list(range(9, 36)) + list(range(37, 45)) + [36]
        shield_slot = None
        for slot in search_order:
            st = items.get(slot)
            if st and st.item == "minecraft:shield":
                shield_slot = slot
                break
        if shield_slot is not None:
            # manual swap: pick shield → click offhand (45) → click back to original slot
            Inventory.click_slot(shield_slot, right_button=False)
            time.sleep(0.01)
            Inventory.click_slot(45, right_button=False)
            time.sleep(0.01)
            Inventory.click_slot(shield_slot, right_button=False)
            time.sleep(0.01)
            shield_equipped = 1
            changed += 1

    return changed, shield_equipped

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

        # pull everything except weak gear
        moved = pull_all_from_chest_only_top()
        try:
            Screen.close_screen()
        except Exception:
            pass

        # open inventory & upgrade
        opened = False
        try:
            m.press_key_bind("key.inventory", True); time.sleep(0.05)
            m.press_key_bind("key.inventory", False)
            opened = Screen.wait_screen(delay=1200)
        except Exception:
            opened = False

        upgraded = 0
        shielded = 0
        if opened:
            upgraded, shielded = equip_best_armor_sword_shield()
            try:
                Screen.close_screen()
            except Exception:
                pass
        else:
            m.echo("⚠️ Couldn't open inventory; skipping upgrades.")

        m.echo(f"✅ Pulled (no weak gear) {moved} / Upgraded {upgraded} (armor & sword) / Shield equipped: {bool(shielded)}")
    finally:
        _busy = False

# Bind G
kb = Keybind()
kb.set_keybind(
    71,
    pull_then_upgrade,
    name="PullAndUpgrade",
    category="Minescript+",
    description="Pull chest (skip leather/wood/chainmail/turtle gear), then auto-upgrade armor & move best sword to hotbar 0, and equip a shield to offhand."
)

m.echo("🎹 G: Pull (skip weak leather/wood/chainmail/turtle gear) → close → open inventory → swap to stronger armor/sword + equip shield → close")
while True:
    time.sleep(1)