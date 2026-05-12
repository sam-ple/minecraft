import minescript as m
import time
import json
import random

player = m.player_name()
bossbar_id = "minecraft:direction_bar"

# Setup bossbar
m.execute("title @a clear")
m.execute(f"bossbar remove {bossbar_id}")
m.execute(f"bossbar add {bossbar_id} Direction")
m.execute(f"bossbar set {bossbar_id} max 1")
m.execute(f"bossbar set {bossbar_id} value 1")
m.execute(f"bossbar set {bossbar_id} color white")
m.execute(f"bossbar set {bossbar_id} players {player}")

# Degrees and direction labels
degree_marks = list(range(0, 360, 15))
direction_labels = {0: "S", 90: "W", 180: "N", 270: "E"}
cardinals = list(direction_labels.items())

def normalize_yaw(yaw):
    return (yaw + 360) % 360

def find_nearest_index(lst, val):
    return min(range(len(lst)), key=lambda i: abs(lst[i] - val))

def build_bossbar_line(yaw):
    yaw = normalize_yaw(yaw)
    idx = find_nearest_index(degree_marks, yaw)
    indices = [(idx + i) % len(degree_marks) for i in range(-2, 3)]
    parts = []
    for i in indices:
        deg = degree_marks[i]
        label = direction_labels.get(deg, str(deg))
        if i == idx:
            parts.append(f"[ {label} ]")
        else:
            parts.append(f" {label} ")
    return "|".join(parts)

# Start with random direction
current_target_deg, current_target_label = random.choice(cardinals)
last_display = ""
last_change = time.time()

# Teleport player to face target direction
def face_direction(deg):
    x, y, z = m.player_position()
    m.execute(f"tp {player} {x} {y} {z} {deg} 0")

face_direction(current_target_deg)
m.execute(f'title {player} actionbar {{"text":"🧭 Face {current_target_label}","color":"gold"}}')

while True:
    yaw, _ = m.player_orientation()
    yaw = normalize_yaw(yaw)

    # Update bossbar
    line = build_bossbar_line(yaw)
    if line != last_display:
        name_json = json.dumps({"text": line, "color": "white"})
        m.execute(f"bossbar set {bossbar_id} name {name_json}")
        last_display = line

    # Check facing direction
    diff = abs(normalize_yaw(yaw - current_target_deg))
    if diff > 30:
        m.execute(f"damage {player} 1 minecraft:generic")

    # Change direction every 30s
    if time.time() - last_change > 30:
        current_target_deg, current_target_label = random.choice(cardinals)
        face_direction(current_target_deg)
        m.execute(f'title {player} actionbar {{"text":"🧭 New direction: {current_target_label}","color":"gold"}}')
        last_change = time.time()

    time.sleep(0.5)
