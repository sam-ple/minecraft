import minescript as m
import time
import json

player = m.player_name()
bossbar_id = "minecraft:direction_bar"

# Setup bossbar with no progress bar (max=1, value=1 hides bar)
m.execute("title @a clear")
m.execute(f"bossbar add {bossbar_id} Direction")
m.execute(f"bossbar set {bossbar_id} max 1")
m.execute(f"bossbar set {bossbar_id} value 1")
m.execute(f"bossbar set {bossbar_id} color white")
m.execute(f"bossbar set {bossbar_id} players {player}")

# Degree marks spaced every 15°
degree_marks = [
    0, 15, 30, 45, 60, 75, 90, 105, 120, 135,
    150, 165, 180, 195, 210, 225, 240, 255, 270, 285,
    300, 315, 330, 345
]

# Cardinal directions at compass points
direction_labels = {
    0: "S",
    90: "W",
    180: "N",
    270: "E"
}

def normalize_yaw(yaw):
    return (yaw + 360) % 360

def find_nearest_index(lst, val):
    return min(range(len(lst)), key=lambda i: abs(lst[i] - val))

def build_bossbar_line(yaw):
    yaw = normalize_yaw(yaw)
    idx = find_nearest_index(degree_marks, yaw)

    # Always center current direction, with two on each side (wrap around)
    total = len(degree_marks)
    indices = [(idx + i) % total for i in range(-2, 3)]

    parts = []
    for i in indices:
        deg = degree_marks[i]
        label = direction_labels.get(deg, str(deg))
        if i == idx:
            parts.append(f"[{label}]")
        else:
            parts.append(label)

    return " | ".join(parts)

last_display = None

while True:
    yaw, _ = m.player_orientation()
    line = build_bossbar_line(yaw)

    if line != last_display:
        name_json = json.dumps({"text": line, "color": "white"})
        m.execute(f"bossbar set {bossbar_id} name {name_json}")
        last_display = line

    time.sleep(0.5)
