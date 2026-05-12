from time import sleep
import json
import os
import re
from minescript import echo, entities, execute

# ==================================================
# Settings
# ==================================================
SAVE_FILE = "wolf_variants.json"
CHECK_INTERVAL = 0.5
MAX_DISTANCE = 50

ALL_WOLF_VARIANTS = {
    "pale","woods","ashen","black","chestnut",
    "rusty","spotted","striped","snowy","classic","big","grumpy"
}

VARIANT_RE = re.compile(r'variant:"?minecraft:([a-z_]+)"?')

# ==================================================
# Progress load / save
# ==================================================
def load_progress():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except:
            pass
    return set()

def save_progress():
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(seen_variants), f, ensure_ascii=False, indent=2)

seen_variants = load_progress()

# ==================================================
# Utility
# ==================================================
def extract_variant(nbt_str):
    """文字列NBTからvariantを抽出"""
    if not isinstance(nbt_str, str):
        return None
    m = VARIANT_RE.search(nbt_str)
    return m.group(1) if m else None

def firework():
    execute(
        'execute at @p run summon firework_rocket ~ ~1 ~ '
        '{LifeTime:30,FireworksItem:{id:"minecraft:firework_rocket",Count:1,'
        'tag:{Fireworks:{Flight:1,Explosions:[{Type:1,Colors:[I;16711680,65280,255],FadeColors:[I;16777215]}]}}}}'
    )

def show_status():
    remaining = ALL_WOLF_VARIANTS - seen_variants
    echo(f"🐺 Wolf Variants: {len(seen_variants)}/{len(ALL_WOLF_VARIANTS)} | Remaining: {', '.join(sorted(remaining)) if remaining else 'None'}")

# ==================================================
# Main loop
# ==================================================
def wolf_detector_loop():
    echo("🐺 Wolf Variant Adventure started!")
    show_status()

    while True:
        wolves = entities(type=".*wolf", sort="nearest", limit=10, max_distance=MAX_DISTANCE, nbt=True)

        if not wolves:
            echo("🐺 No wolves nearby.")
        else:
            for w in wolves:
                variant = extract_variant(w.nbt)
                if variant and variant in ALL_WOLF_VARIANTS and variant not in seen_variants:
                    seen_variants.add(variant)
                    save_progress()
                    echo(f"🆕 New Wolf Found: {variant} ({len(seen_variants)}/{len(ALL_WOLF_VARIANTS)})")
                    firework()
                    show_status()
        sleep(CHECK_INTERVAL)

# ==================================================
# Start loop
# ==================================================
wolf_detector_loop()
