from time import sleep, time
import json
import os
import re
from queue import Empty

import minescript as m
from minescript import EventQueue, EventType, execute, echo

# ==================================================
# Configuration
# ==================================================

# File to store collected wolf variants
SAVE_FILE = "wolf_variants.json"

# Tick interval (seconds)
CHECK_INTERVAL = 0.1

# Required gaze duration to confirm a wolf (seconds)
LOOK_REQUIRED_TIME = 1.0

# All possible wolf variants (Minecraft 1.21+)
ALL_WOLF_VARIANTS = {
    "pale", "woods", "ashen", "black", "chestnut",
    "rusty", "spotted", "striped", "snowy",
    "classic", "big", "grumpy"
}

# Chat output pattern from `/data get entity <uuid> variant`
DATA_PATTERN = re.compile(
    r'Wolf has the following entity data: "minecraft:(\w+)"'
)

# ==================================================
# Progress Load / Save
# ==================================================

def load_progress():
    """Load already collected wolf variants from JSON."""
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            pass
    return set()

def save_progress():
    """Save collected wolf variants to JSON."""
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(seen_variants), f, indent=2, ensure_ascii=False)

seen_variants = load_progress()

# ==================================================
# UI Helpers
# ==================================================

def firework():
    """Launch a celebratory firework at the player."""
    execute(
        'execute at @p run summon firework_rocket ~ ~1 ~ '
        '{LifeTime:30,FireworksItem:{id:"minecraft:firework_rocket",Count:1,'
        'tag:{Fireworks:{Flight:1,Explosions:[{Type:1,'
        'Colors:[I;16711680,65280,255],FadeColors:[I;16777215]}]}}}}'
    )

def show_status():
    """Display current collection progress."""
    remaining = ALL_WOLF_VARIANTS - seen_variants
    echo(f"🐺 {len(seen_variants)}/{len(ALL_WOLF_VARIANTS)} collected")
    if remaining:
        echo("Remaining: " + ", ".join(sorted(remaining)))

# ==================================================
# Main Loop (Chat-Capture / Spam-Proof)
# ==================================================

def wolf_detector_loop():
    """
    Detects wolves the player is looking at.
    After maintaining gaze for a fixed time:
      - Queries the wolf's variant via /data get
      - Captures the chat output
      - Saves new variants and launches fireworks
    """

    echo("🐺 Wolf Variant Adventure (stable)")
    show_status()

    # Chat event listener (required to capture /data output)
    eq = EventQueue()
    eq.register_chat_listener()

    current_uuid = None      # UUID currently being looked at
    look_start = 0.0         # When gaze started
    queried_uuid = None      # UUID already queried (spam prevention)

    while True:
        now = time()
        target = m.player_get_targeted_entity(max_distance=20)

        # ------------------------------------------
        # Not looking at a wolf
        # ------------------------------------------
        if not target or target.type != "entity.minecraft.wolf":
            current_uuid = None
            queried_uuid = None
            sleep(CHECK_INTERVAL)
            continue

        # ------------------------------------------
        # Started looking at a new wolf
        # ------------------------------------------
        if target.uuid != current_uuid:
            current_uuid = target.uuid
            look_start = now
            queried_uuid = None
            sleep(CHECK_INTERVAL)
            continue

        # ------------------------------------------
        # Gaze duration not sufficient
        # ------------------------------------------
        if now - look_start < LOOK_REQUIRED_TIME:
            sleep(CHECK_INTERVAL)
            continue

        # ------------------------------------------
        # Already queried this wolf
        # ------------------------------------------
        if queried_uuid == current_uuid:
            sleep(CHECK_INTERVAL)
            continue

        # ------------------------------------------
        # Query variant (ONLY ONCE per wolf)
        # ------------------------------------------
        queried_uuid = current_uuid
        execute(f"data get entity {current_uuid} variant")

        # ------------------------------------------
        # Wait for chat response
        # ------------------------------------------
        timeout = time() + 0.5
        while time() < timeout:
            try:
                event = eq.get(timeout=0.05)
            except Empty:
                continue

            if event.type != EventType.CHAT:
                continue

            match = DATA_PATTERN.search(event.message)
            if not match:
                continue

            variant = match.group(1)

            # Unknown variant (future-proofing)
            if variant not in ALL_WOLF_VARIANTS:
                echo(f"❓ Unknown variant: {variant}")
                break

            # Already collected
            if variant in seen_variants:
                break

            # ------------------------------------------
            # New variant discovered
            # ------------------------------------------
            seen_variants.add(variant)
            save_progress()

            echo(f"🆕 New Wolf: {variant}")
            firework()
            show_status()
            break

        sleep(CHECK_INTERVAL)

# ==================================================
# Entry Point
# ==================================================

wolf_detector_loop()
