from time import sleep
import re
import json
import minescript as m

# ==================================================
# Settings
# ==================================================
UPDATE_INTERVAL = 2  # 2秒ごとに更新
MAX_DISTANCE = 20

# ==================================================
# NBT helpers
# ==================================================
VARIANT_RE = re.compile(r'variant:"?minecraft:([a-z_]+)"?')

def extract_variant(nbt):
    if not isinstance(nbt, str):
        return None, "NBT is not str"
    m_ = VARIANT_RE.search(nbt)
    if not m_:
        return None, "variant not found"
    return m_.group(1), "ok"

def short(text, max_len=1000):
    if not isinstance(text, str):
        return text
    return text if len(text) <= max_len else text[:max_len] + " ..."

def is_wolf(entity_type):
    if not entity_type:
        return False
    return "wolf" in entity_type.lower()

# ==================================================
# Chat helper
# ==================================================
def echo_chat(msg, color="aqua"):
    # JSONエスケープしてMinecraftに送信
    safe_msg = json.dumps(str(msg))
    m.execute(f'tellraw @a {{"text":{safe_msg},"color":"{color}"}}')

# ==================================================
# Main loop
# ==================================================
echo_chat("🧪 Wolf NBT Debug started")
echo_chat(f"Data updates every {UPDATE_INTERVAL}s. Look at a wolf.")

while True:
    # --- Targeted entity ---
    target = m.player_get_targeted_entity(max_distance=MAX_DISTANCE, nbt=True)

    # --- Nearest wolf ---
    wolves = m.entities(
        nbt=True,
        type=".*wolf",
        sort="nearest",
        limit=1,
        max_distance=MAX_DISTANCE
    )
    nearest = wolves[0] if wolves else None

    # --- Output ---
    echo_chat("──────── DEBUG SNAPSHOT ────────")

    # Targeted
    echo_chat("[Targeted]")
    if not target:
        echo_chat(" none")
    else:
        v, reason = extract_variant(target.nbt)
        echo_chat(f" type    : {target.type}")
        echo_chat(f" nbtType : {type(target.nbt).__name__}")
        echo_chat(f" variant : {v} ({reason})")
        if not is_wolf(target.type):
            echo_chat(" note    : target is not a wolf")

        # 安全にNBT出力
        nbt_safe = json.dumps(short(target.nbt))
        m.execute(f'tellraw @a {{"text":{nbt_safe},"color":"aqua"}}')

    # Nearest Wolf
    echo_chat("[Nearest Wolf]")
    if not nearest:
        echo_chat(" none")
    else:
        v, reason = extract_variant(nearest.nbt)
        echo_chat(f" uuid    : {nearest.uuid}")
        echo_chat(f" type    : {nearest.type}")
        echo_chat(f" nbtType : {type(nearest.nbt).__name__}")
        echo_chat(f" variant : {v} ({reason})")

        # 安全にNBT出力
        nbt_safe = json.dumps(short(nearest.nbt))
        m.execute(f'tellraw @a {{"text":{nbt_safe},"color":"aqua"}}')

    echo_chat("──────────── END ────────────")

    # --- 2秒待って次のループ ---
    sleep(UPDATE_INTERVAL)
