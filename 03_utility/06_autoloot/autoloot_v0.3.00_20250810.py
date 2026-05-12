# Fabric 1.21.8 / Minescript 5.0b1 / Minescript Plus v0.10a
# G: Spawn weighted-loot chest (dict-based loot & hotbar map) → H: Pull & upgrade (skip weak gear) + shield + hotbar layout → J: Remove chest
import time, math, random
import minescript as m
from time import sleep
from minescript_plus import Inventory, Keybind, Screen

_busy = False
_LAST_CHEST_POS = None  # Last spawned chest position (spawn with G → remove with J)

# =========================
# Core ranking & detection logic
# =========================
ARMOR_ORDER = ["leather", "gold", "chainmail", "iron", "turtle", "diamond", "netherite"]
SWORD_ORDER = ["wood", "gold", "stone", "iron", "diamond", "netherite"]

ARMOR_SLOTS   = {"head": 5, "chest": 6, "legs": 7, "feet": 8}  # Inventory-screen view indices
ARMOR_SUFFIX  = {"head": "_helmet", "chest": "_chestplate", "legs": "_leggings", "feet": "_boots"}
SPECIAL_HELMETS = ("minecraft:turtle_helmet",)

def _mat_of(item_id: str) -> str | None:
    if not item_id: return None
    it = item_id.split(":")[-1]
    it = it.replace("golden_", "gold_").replace("wooden_", "wood_")
    if it == "turtle_helmet": return "turtle"
    for mname in ["netherite","diamond","iron","chainmail","gold","leather","stone","wood"]:
        if it.startswith(mname + "_"): return mname
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

# Filter to skip "weak gear" when pulling from chests
_WEAK_MATS = {"leather", "wood", "chainmail", "turtle", "stone", "gold"}
_ARMOR_SUFFIXES_TUP = tuple(ARMOR_SUFFIX.values())

def _is_gear(item_id: str) -> bool:
    if not item_id: return False
    if item_id.endswith("_sword"): return True
    if any(item_id.endswith(suf) for suf in _ARMOR_SUFFIXES_TUP): return True
    if item_id in SPECIAL_HELMETS or item_id.endswith("carved_pumpkin"): return True
    return False

def is_weak_gear(item_id: str) -> bool:
    if not _is_gear(item_id): return False
    if item_id.endswith("carved_pumpkin"): return True
    mat = _mat_of(item_id)
    return mat in _WEAK_MATS

# =========================
# Loot generation via dictionaries
# =========================
# Rarity weights (smaller = rarer)
WEIGHTS = {
    "COMMON":    12,
    "UNCOMMON":   5,
    "RARE":       2,
    "LEGENDARY":  1,
}

# Per-item max stack (default 1)
MAX_STACK = {
    "minecraft:snowball":     16,
    "minecraft:arrow":        64,
    "minecraft:stone":        64,
    "minecraft:golden_apple": 64,
}
def _max_stack(item_id: str) -> int:
    return MAX_STACK.get(item_id, 1)

# Category → item list (dict-based)
LOOT_CATEGORIES = {
    "COMMON": [
        # swords
        "minecraft:wooden_sword","minecraft:stone_sword",
        # leather
        "minecraft:leather_helmet","minecraft:leather_chestplate",
        "minecraft:leather_leggings","minecraft:leather_boots",
        # stacks / blocks
        "minecraft:snowball","minecraft:arrow","minecraft:stone",
    ],
    "UNCOMMON": [
        "minecraft:iron_sword","minecraft:golden_sword",
        "minecraft:chainmail_helmet","minecraft:chainmail_chestplate",
        "minecraft:chainmail_leggings","minecraft:chainmail_boots",
        "minecraft:iron_helmet","minecraft:iron_chestplate",
        "minecraft:iron_leggings","minecraft:iron_boots",
        "minecraft:golden_helmet","minecraft:golden_chestplate",
        "minecraft:golden_leggings","minecraft:golden_boots",
        # utility
        "minecraft:bow","minecraft:shield","minecraft:water_bucket",
    ],
    "RARE": [
        "minecraft:diamond_sword",
        "minecraft:diamond_helmet","minecraft:diamond_chestplate",
        "minecraft:diamond_leggings","minecraft:diamond_boots",
        "minecraft:turtle_helmet",
        "minecraft:lava_bucket","minecraft:golden_apple",
    ],
    "LEGENDARY": [
        "minecraft:netherite_sword",
        "minecraft:netherite_helmet","minecraft:netherite_chestplate",
        "minecraft:netherite_leggings","minecraft:netherite_boots",
    ],
}

# =========================
# Hotbar layout via dictionary
# =========================
# Slot 0 is "sword only"—do not touch it here
HOTBAR_MAP = {
    1: "minecraft:bow",
    2: "minecraft:arrow",
    8: "minecraft:stone",
    7: "minecraft:snowball",
    6: "minecraft:water_bucket",
    5: "minecraft:lava_bucket",
    4: "minecraft:golden_apple",
}

# -----------------------------------------
# G: Spawn a weighted-loot chest 3 blocks ahead (dict-based)
# -----------------------------------------
def spawn_weighted_loot_chest():
    global _LAST_CHEST_POS
    x, y, z = m.player_position()
    ix, iy, iz = math.floor(x) + 3, math.floor(y), math.floor(z)
    m.execute(f"/setblock {ix} {iy} {iz} chest replace")
    sleep(0.3)

    # Expand dict → weighted list
    items = []  # [(item_id, max_stack, weight)]
    for rarity, ids in LOOT_CATEGORIES.items():
        w = WEIGHTS[rarity]
        for _id in ids:
            items.append((_id, _max_stack(_id), w))

    available_slots = list(range(27))
    num_to_place = random.randint(6, 12)
    weights = [w for (_, _, w) in items]

    placed = 0
    for _ in range(num_to_place):
        if not available_slots:
            break
        slot = random.choice(available_slots); available_slots.remove(slot)
        item_id, max_stack, _w = random.choices(items, weights=weights, k=1)[0]
        count = 1 if max_stack == 1 else random.randint(1, max_stack)
        m.execute(f"/item replace block {ix} {iy} {iz} container.{slot} with {item_id} {count}")
        sleep(0.03)
        placed += 1

    _LAST_CHEST_POS = (ix, iy, iz)
    m.echo(f"✅ Spawned weighted loot chest at ({ix},{iy},{iz}) with {placed} stacks.")

# -----------------------------------------
# J: Remove the last spawned chest (do not touch contents)
# -----------------------------------------
def remove_last_chest_only():
    global _LAST_CHEST_POS
    if not _LAST_CHEST_POS:
        m.echo("ℹ️ No spawned chest recorded yet (press G first).")
        return
    x, y, z = _LAST_CHEST_POS
    m.execute(f"/setblock {x} {y} {z} air replace")
    _LAST_CHEST_POS = None
    m.echo("🗑️ Removed the spawned chest.")

# -----------------------------------------
# H: Pull (skip weak gear) → best armor & best sword → shield → hotbar layout → close
# -----------------------------------------
def pull_all_from_chest_only_top():
    moved = 0
    try:
        total = m.container_size()       # single:63 / double:90
        chest_slots = max(0, min(54, total - 36)) or 27
    except Exception:
        chest_slots = 27

    while True:
        items_by_slot = {st.slot: st for st in (m.container_get_items() or [])}
        if not any(s < chest_slots and s in items_by_slot for s in range(chest_slots)):
            break

        progress = 0
        for s in range(chest_slots):
            st = items_by_slot.get(s)
            if not st or not st.item:
                continue
            if is_weak_gear(st.item):
                continue
            if Inventory.shift_click_slot(s):
                moved += 1
                progress += 1
                time.sleep(0.01)

        if progress == 0:
            break
    return moved

def equip_best_armor_sword_shield():
    changed = 0
    shield_equipped = 0

    def refresh_items():
        return {st.slot: st for st in (m.container_get_items() or [])}

    # 1) Armor: compare current (5..8) vs candidates in 9..44; swap if better
    items = refresh_items()
    for part, suffix in ARMOR_SUFFIX.items():
        armor_slot = ARMOR_SLOTS[part]
        cur_item = items.get(armor_slot).item if armor_slot in items else None
        cur_score = _armor_score(cur_item)

        best_slot, best_score = None, -1
        for slot, st in items.items():
            if 9 <= slot <= 44 and st.item:
                it = st.item
                if it.endswith(suffix) or (part == "head" and it in SPECIAL_HELMETS):
                    sc = _armor_score(it)
                    if sc > best_score:
                        best_slot, best_score = slot, sc

        if best_score > cur_score and best_slot is not None:
            Inventory.click_slot(best_slot, right_button=False)   # pick
            time.sleep(0.01)
            Inventory.click_slot(armor_slot, right_button=False)  # place/swap
            time.sleep(0.01)
            Inventory.click_slot(best_slot, right_button=False)   # put back remainder
            time.sleep(0.01)
            changed += 1
            items = refresh_items()

    # 2) Sword → put the strongest into hotbar 0 (view 36)
    items = refresh_items()
    hotbar0_item  = items.get(36).item if 36 in items else None
    hotbar0_score = _sword_score(hotbar0_item)

    best_slot, best_score = None, -1
    for slot, st in items.items():
        if 9 <= slot <= 44 and st.item and st.item.endswith("_sword"):
            sc = _sword_score(st.item)
            if sc > best_score:
                best_slot, best_score = slot, sc

    if best_slot is not None and best_score > hotbar0_score:
        if Inventory.inventory_hotbar_swap(best_slot, 0):
            changed += 1
            time.sleep(0.02)

    # 3) Shield → offhand (view 45)
    items = refresh_items()
    if not (45 in items and items[45].item == "minecraft:shield"):
        search_order = list(range(9, 36)) + list(range(37, 45)) + [36]
        shield_slot = None
        for s in search_order:
            st = items.get(s)
            if st and st.item == "minecraft:shield":
                shield_slot = s
                break
        if shield_slot is not None:
            Inventory.click_slot(shield_slot, right_button=False)
            time.sleep(0.01)
            Inventory.click_slot(45, right_button=False)
            time.sleep(0.01)
            Inventory.click_slot(shield_slot, right_button=False)
            time.sleep(0.01)
            shield_equipped = 1
            changed += 1

    return changed, shield_equipped

# --- Hotbar layout via dict (keep sword fixed in slot 0) ---
def _place_item_to_hotbar_exact(item_id: str, hotbar_index: int) -> bool:
    """Move item_id to hotbar.{index} (view slot = 36+index). Returns True on success."""
    items = {st.slot: st for st in (m.container_get_items() or [])}
    target_view = 36 + hotbar_index
    if target_view in items and items[target_view].item == item_id:
        return False  # already placed

    # Exclude 45 (offhand). Avoid 36 (leftmost) to protect the sword; if the source itself is 36, allow it as a last resort.
    sources = [slot for slot, st in items.items() if st.item == item_id and slot not in (45,)]
    if (36 in items) and items[36].item == item_id and 36 not in sources:
        sources.append(36)

    for src in sources:
        if Inventory.inventory_hotbar_swap(src, hotbar_index):
            time.sleep(0.01)
            return True
    return False

def layout_hotbar_tools():
    changed = 0
    for idx, item_id in HOTBAR_MAP.items():
        if _place_item_to_hotbar_exact(item_id, idx):
            changed += 1
    return changed

def pull_then_upgrade():
    global _busy
    if _busy:
        m.echo("⏳ Already running…"); return
    _busy = True
    try:
        if not Inventory.open_targeted_chest():
            m.echo("⚠️ Look straight at a chest/barrel/shulker and try again."); return

        moved = pull_all_from_chest_only_top()
        try: Screen.close_screen()
        except Exception: pass

        opened = False
        try:
            m.press_key_bind("key.inventory", True); time.sleep(0.05)
            m.press_key_bind("key.inventory", False)
            opened = Screen.wait_screen(delay=1200)
        except Exception:
            opened = False

        upgraded = shielded = laid_out = 0
        if opened:
            upgraded, shielded = equip_best_armor_sword_shield()
            laid_out = layout_hotbar_tools()
            try: Screen.close_screen()
            except Exception: pass
        else:
            m.echo("⚠️ Couldn't open inventory; skipping upgrades.")

        m.echo(f"✅ Pulled (no weak gear) {moved} / Upgraded {upgraded} / Shield:{bool(shielded)} / Hotbar laid out:{laid_out}")
    finally:
        _busy = False

# ========= Keybinds (G/H swapped; J = remove) =========
kb = Keybind()
kb.set_keybind(71, spawn_weighted_loot_chest, name="SpawnLootChest",  category="Minescript+", description="Spawn a weighted-loot chest 3 blocks ahead.")  # G
kb.set_keybind(72, pull_then_upgrade,        name="PullAndUpgrade",   category="Minescript+", description="Pull chest (skip weak gear) → upgrade armor/sword → shield → layout hotbar.")  # H
kb.set_keybind(74, remove_last_chest_only,   name="RemoveLootChest",  category="Minescript+", description="Remove the last spawned chest.")  # J

m.echo("🎹 G: Spawn weighted-loot chest | H: Pull→upgrade→shield→layout | J: Remove spawned chest")
while True:
    time.sleep(1)