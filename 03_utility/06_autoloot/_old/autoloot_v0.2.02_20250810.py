# Fabric 1.21.8 / Minescript 5.0b1 / Minescript Plus v0.10a
# H: Spawn weighted-loot chest → G: Pull & upgrade (skip weak gear) → J: Clear contents and remove chest
import time, math, random
import minescript as m
from time import sleep
from minescript_plus import Inventory, Keybind, Screen

_busy = False
_LAST_CHEST_POS = None  # H で作ったチェストの座標を記録

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
# ---------------------------------------------------------------

# ==== H: 前方3ブロックにチェスト設置＋重み付きランダム戦利品を詰める ====
def spawn_weighted_loot_chest():
    global _LAST_CHEST_POS
    # プレイヤー前方3ブロック
    x, y, z = m.player_position()
    ix, iy, iz = math.floor(x) + 3, math.floor(y), math.floor(z)
    m.execute(f'/setblock {ix} {iy} {iz} chest replace')
    sleep(0.3)

    # ---- Rarity weights (smaller number = rarer) ----
    W_COMMON     = 12
    W_UNCOMMON   = 5
    W_RARE       = 2
    W_LEGENDARY  = 1

    def add(pool, ids, weight, max_stack=1):
        for _id in ids:
            pool.append((_id, max_stack, weight))

    items = []

    # Swords
    add(items, ["minecraft:wooden_sword","minecraft:stone_sword"], W_COMMON)
    add(items, ["minecraft:iron_sword","minecraft:golden_sword"], W_UNCOMMON)
    add(items, ["minecraft:diamond_sword"], W_RARE)
    add(items, ["minecraft:netherite_sword"], W_LEGENDARY)

    # Armor
    add(items, [
        "minecraft:leather_helmet","minecraft:leather_chestplate",
        "minecraft:leather_leggings","minecraft:leather_boots",
    ], W_COMMON)
    add(items, [
        "minecraft:chainmail_helmet","minecraft:chainmail_chestplate",
        "minecraft:chainmail_leggings","minecraft:chainmail_boots",
        "minecraft:iron_helmet","minecraft:iron_chestplate",
        "minecraft:iron_leggings","minecraft:iron_boots",
        "minecraft:golden_helmet","minecraft:golden_chestplate",
        "minecraft:golden_leggings","minecraft:golden_boots",
    ], W_UNCOMMON)
    add(items, [
        "minecraft:diamond_helmet","minecraft:diamond_chestplate",
        "minecraft:diamond_leggings","minecraft:diamond_boots",
        "minecraft:turtle_helmet",
    ], W_RARE)
    add(items, [
        "minecraft:netherite_helmet","minecraft:netherite_chestplate",
        "minecraft:netherite_leggings","minecraft:netherite_boots",
    ], W_LEGENDARY)

    # Shield
    add(items, ["minecraft:shield"], W_UNCOMMON)

    # Snowballs (stackable)
    add(items, ["minecraft:snowball"], W_COMMON, max_stack=16)

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
        m.execute(f'/item replace block {ix} {iy} {iz} container.{slot} with {item_id} {count}')
        sleep(0.03)
        placed += 1

    _LAST_CHEST_POS = (ix, iy, iz)
    m.echo(f"✅ Spawned weighted loot chest at ({ix},{iy},{iz}) with {placed} stacks.")

# ==== J: Hで作ったチェストを中身クリア→破壊 ====
def clear_and_remove_last_chest():
    global _LAST_CHEST_POS
    if not _LAST_CHEST_POS:
        m.echo("ℹ️ No spawned chest recorded yet (press H first).")
        return
    x, y, z = _LAST_CHEST_POS
    # 中身クリア
    for s in range(27):
        m.execute(f'/item replace block {x} {y} {z} container.{s} with minecraft:air')
        sleep(0.005)
    # 破壊
    m.execute(f'/setblock {x} {y} {z} air replace')
    _LAST_CHEST_POS = None
    m.echo("🧹 Cleared contents and removed the spawned chest.")

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

# ---- Inventory: best armor + best sword to hotbar0 + shield to offhand ----
def equip_best_armor_sword_shield():
    changed = 0
    shield_equipped = 0

    def refresh_items():
        return {st.slot: st for st in (m.container_get_items() or [])}

    # 1) Armor upgrades
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

    # 2) Sword to hotbar0 if stronger
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
        if Inventory.inventory_hotbar_swap(best_slot, 0):
            changed += 1
            time.sleep(0.02)

    # 3) Shield to offhand (view 45)
    items = refresh_items()
    offhand_item = items.get(45).item if 45 in items else None
    if offhand_item != "minecraft:shield":
        search_order = list(range(9, 36)) + list(range(37, 45)) + [36]  # avoid 36 last
        shield_slot = None
        for slot in search_order:
            st = items.get(slot)
            if st and st.item == "minecraft:shield":
                shield_slot = slot
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

# ---- G: Pull → close → open inventory → upgrade/equip → close ----
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

# ---- Keybinds ----
kb = Keybind()
kb.set_keybind(72, spawn_weighted_loot_chest, name="SpawnLootChest", category="Minescript+", description="Spawn a weighted-loot chest 3 blocks ahead.")  # H
kb.set_keybind(71, pull_then_upgrade,        name="PullAndUpgrade",  category="Minescript+", description="Pull chest (skip weak gear) → upgrade armor/sword → equip shield.")  # G
kb.set_keybind(74, clear_and_remove_last_chest, name="RemoveLootChest", category="Minescript+", description="Clear contents and remove the last spawned chest.")  # J

m.echo("🎹 H: Spawn weighted-loot chest | G: Pull→upgrade→shield | J: Clear & remove spawned chest")
while True:
    time.sleep(1)