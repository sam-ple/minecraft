from time import sleep, time
import re
import threading
from minescript import echo, player_get_targeted_entity, entities

# ==================================================
# Settings
# ==================================================
CHECK_INTERVAL = 0.1
PRINT_INTERVAL = 1.0
MAX_DISTANCE = 50  # プレイヤーからの距離制限を広めに
SHORT_LEN = 500

# ==================================================
# NBT helpers
# ==================================================
VARIANT_RE = re.compile(r'variant:"?minecraft:([a-z_]+)"?')

def extract_variant(nbt):
    """NBTからvariantを抽出"""
    if not isinstance(nbt, str):
        return None, "NBT is not str"
    m = VARIANT_RE.search(nbt)
    if not m:
        return None, "variant not found"
    return m.group(1), "ok"

def short(text, max_len=SHORT_LEN):
    """長い文字列を短縮"""
    if not isinstance(text, str):
        return text
    return text if len(text) <= max_len else text[:max_len] + " ..."

def is_wolf(entity_type):
    """entity_typeにwolfを含むかで判定"""
    if not entity_type:
        return False
    return "wolf" in entity_type.lower()

# ==================================================
# Main debug loop
# ==================================================
def entity_debug_loop():
    echo("🧪 Wolf / NBT Debug started")
    echo("Look at a wolf or have wolves nearby. Data updates every 1s.")

    last_print = 0

    while True:
        now = time()
        if now - last_print < PRINT_INTERVAL:
            sleep(CHECK_INTERVAL)
            continue

        last_print = now

        # --- Targeted entity ---
        target = player_get_targeted_entity(nbt=True)

        # --- Nearest wolves ---
        wolves = entities(
            nbt=True,
            type=".*wolf",  # 正規表現で拾う
            sort="nearest",
            limit=5,
            max_distance=MAX_DISTANCE
        )

        nearest = wolves[0] if wolves else None

        # --- Output ---
        echo("──────── DEBUG SNAPSHOT ────────")

        # Targeted
        echo("[Targeted]")
        if not target:
            echo(" none")
        else:
            v, reason = extract_variant(target.nbt)
            echo(f" type    : {target.type}")
            echo(f" nbtType : {type(target.nbt).__name__}")
            echo(f" variant : {v} ({reason})")
            if not is_wolf(target.type):
                echo(" note    : target is not a wolf")
            echo(f" nbtRaw  : {short(target.nbt)}")

        # Nearest Wolves
        echo("[Nearest Wolves]")
        if not wolves:
            echo(" none")
        else:
            for w in wolves:
                v, reason = extract_variant(w.nbt)
                echo(f" uuid    : {w.uuid}")
                echo(f" type    : {w.type}")
                echo(f" nbtType : {type(w.nbt).__name__}")
                echo(f" variant : {v} ({reason})")
                echo(f" nbtRaw  : {short(w.nbt)}")
                echo(f" pos     : {w.position}")

        echo("──────────── END ────────────")
        sleep(CHECK_INTERVAL)

# ==================================================
# Start background thread
# ==================================================
threading.Thread(
    target=entity_debug_loop,
    daemon=True
).start()
