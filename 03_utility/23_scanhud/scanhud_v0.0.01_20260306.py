"""
ScanHUD
Displays nearby important blocks in a compact HUD list.

Inspired by MicroHUD + BlockScanner
"""

import threading
import math
from time import sleep

import minescript as m
from minescript import player_position
from minescript_plus import Hud


# ============================================================
# CONFIG
# ============================================================

SEARCH_RADIUS = 12
Y_RANGE = 6
MAX_PER_BLOCK = 5

TARGET_BLOCKS = {
    "diamond_ore": "Diamond",
    "deepslate_diamond_ore": "Diamond",
    "iron_ore": "Iron",
    "deepslate_iron_ore": "Iron",
    "raw_iron_block": "Iron Vein",

    "chest": "Chest",
    "spawner": "Spawner",

    "end_portal_frame": "Portal",
    "reinforced_deepslate": "AncientCity",

    "bell": "Village",

    "trial_spawner": "Trial",
}

# ============================================================
# HUD Layout (Right side)
# ============================================================

BASE_X = 290
BASE_Y = 15
LINE_HEIGHT = 10

lines = []

for i in range(20):
    lines.append(Hud.add_text("", BASE_X, BASE_Y + i * LINE_HEIGHT))

Hud.use_toggle_key(True)

print("ScanHUD started (toggle: F12)")


# ============================================================
# Scan Result
# ============================================================

scan_result = {}


# ============================================================
# Scan Thread
# ============================================================

def scan_loop():

    global scan_result

    while True:

        try:

            px, py, pz = [round(p) for p in player_position()]

            positions = []
            offsets = []

            for dx in range(-SEARCH_RADIUS, SEARCH_RADIUS + 1):
                for dy in range(-Y_RANGE, Y_RANGE + 1):
                    for dz in range(-SEARCH_RADIUS, SEARCH_RADIUS + 1):

                        x = px + dx
                        y = py + dy
                        z = pz + dz

                        positions.append([x, y, z])
                        offsets.append((dx, dy, dz))

            blocks = m.get_block_list(positions)

            found = {}

            for blk, (dx, dy, dz) in zip(blocks, offsets):

                if not blk:
                    continue

                name = blk.replace("minecraft:", "")

                if name in TARGET_BLOCKS:

                    dist = math.sqrt(dx*dx + dy*dy + dz*dz)

                    label = TARGET_BLOCKS[name]

                    pos = (px+dx, py+dy, pz+dz)

                    found.setdefault(label, []).append((dist, pos))

            # sort & limit
            result = {}

            for label, items in found.items():

                items.sort(key=lambda x: x[0])

                result[label] = items[:MAX_PER_BLOCK]

            scan_result = result

        except Exception:
            pass

        sleep(0.5)


threading.Thread(target=scan_loop, daemon=True).start()


# ============================================================
# HUD Update Loop
# ============================================================

while True:

    try:

        line_index = 0

        Hud.set_text_string(lines[line_index], "===== ScanHUD =====")
        line_index += 1

        if not scan_result:

            Hud.set_text_string(lines[line_index], "No targets nearby")
            line_index += 1

        else:

            for label, items in scan_result.items():

                Hud.set_text_string(lines[line_index], f"[{label}]")
                line_index += 1

                for dist, pos in items:

                    x, y, z = pos

                    Hud.set_text_string(
                        lines[line_index],
                        f" {dist:4.1f}m @ {x},{y},{z}"
                    )

                    line_index += 1

        # clear remaining lines
        for i in range(line_index, len(lines)):
            Hud.set_text_string(lines[i], "")

        sleep(0.2)

    except Exception as e:
        print("ScanHUD error:", e)
        sleep(1)
