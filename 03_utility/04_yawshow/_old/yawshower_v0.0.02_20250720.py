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
degree_marks = [0, 15, 30, 45, 60, 75, 90, 105, 120, 135,
                150, 165, 180, 195, 210, 225, 240, 255, 270, 285,
                300, 315, 330, 345]

# Cardinal directions at their correct compass positions
direction_labels = {
    0: "S",
    90: "W",
    180: "N",
    270: "E",
}

def normalize_yaw(yaw):
    return (yaw + 360) % 360

def get_facing_label(yaw):
    yaw = normalize_yaw(yaw)
    if 45 <= yaw < 135:
        return "W"
    elif 135 <= yaw < 225:
        return "N"
    elif 225 <= yaw < 315:
        return "E"
    else:
        return "S"

def find_nearest_index(lst, val):
    return min(range(len(lst)), key=lambda i: abs(lst[i] - val))

def build_bossbar_line(yaw):
    yaw = normalize_yaw(yaw)
    idx = find_nearest_index(degree_marks, yaw)

    # Show 5 items: current in center if possible
    start = max(0, idx - 2)
    end = min(len(degree_marks), start + 5)
    if end - start < 5:
        start = max(0, end - 5)

    line_marks = degree_marks[start:end]

    parts = []
    for i, deg in enumerate(line_marks):
        label = direction_labels.get(deg, str(deg))
        if i == idx - start:
            parts.append(f"| {label} |")
        else:
            parts.append(label)
    return " ".join(parts)

last_display = None

while True:
    yaw, _ = m.player_orientation()
    line = build_bossbar_line(yaw)

    if line != last_display:
        name_json = json.dumps({"text": line, "color": "white"})
        m.execute(f"bossbar set {bossbar_id} name {name_json}")
        last_display = line

    time.sleep(0.5)
