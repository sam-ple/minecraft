import minescript as m
import time
import json
import math

player = m.player_name()
bossbar_id = "minecraft:direction_bar"

# Setup bossbar (hidden progress bar)
m.execute("title @a clear")
m.execute(f"bossbar add {bossbar_id} Direction")
m.execute(f"bossbar set {bossbar_id} max 1")
m.execute(f"bossbar set {bossbar_id} value 1")
m.execute(f"bossbar set {bossbar_id} color white")
m.execute(f"bossbar set {bossbar_id} players {player}")

# Degree marks every 15°
degree_marks = [
    0, 15, 30, 45, 60, 75, 90, 105, 120, 135,
    150, 165, 180, 195, 210, 225, 240, 255, 270, 285,
    300, 315, 330, 345
]

# Cardinal directions
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
    total = len(degree_marks)
    indices = [(idx + i) % total for i in range(-2, 3)]
    parts = []
    for i in indices:
        deg = degree_marks[i]
        label = direction_labels.get(deg, str(deg))
        if i == idx:
            parts.append(f"[ {label} ]")
        else:
            parts.append(f" {label} ")
    return "|".join(parts)

last_display = None

while True:
    # --- コンパス表示 (bossbar) ---
    yaw, pitch = m.player_orientation()
    line = build_bossbar_line(yaw)
    if line != last_display:
        name_json = json.dumps({"text": line, "color": "white"})
        m.execute(f"bossbar set {bossbar_id} name {name_json}")
        last_display = line

    # --- アクションバー表示 ---
    x, y, z = m.player_position()
    pos_str = f"📍Pos: {int(x)}, {int(y)}, {int(z)} | 🎯Yaw: {int(yaw)}, Pitch: {int(pitch)}"

    entity_info = ""
    block_info = ""

    # 対象エンティティ検出
    target_entity = m.player_get_targeted_entity(20)
    if target_entity:
        ex, ey, ez = target_entity.position
        entity_type = target_entity.type
        if entity_type.startswith("entity.minecraft."):
            entity_type = entity_type[len("entity.minecraft."):]
        entity_info = f"👾 Mob: {entity_type} @ ({int(ex)}, {int(ey)}, {int(ez)})"

    # 対象ブロック検出
    target_block = m.player_get_targeted_block(20)
    if target_block:
        bx, by, bz = target_block.position
        block_type = target_block.type
        if block_type.startswith("minecraft:"):
            block_type = block_type[len("minecraft:"):]
        block_info = f"🧱 Block: {block_type} @ ({bx}, {by}, {bz})"

    # 表示合成（モブ → ブロックの順）
    extra_info = ""
    if entity_info and block_info:
        extra_info = f"{entity_info} | {block_info}"
    elif entity_info:
        extra_info = entity_info
    elif block_info:
        extra_info = block_info

    # 最終表示
    full_actionbar = f"{pos_str}"
    if extra_info:
        full_actionbar += f" | {extra_info}"

    actionbar_json = json.dumps({
        "text": full_actionbar,
        "color": "aqua"
    })
    m.execute(f"title @a actionbar {actionbar_json}")

    time.sleep(0.5)
