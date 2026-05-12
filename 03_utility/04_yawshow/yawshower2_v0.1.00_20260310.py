import minescript as m
import time
import json
import threading

PLAYER = m.player_name()
BOSSBAR_ID = "minecraft:direction_bar"

# ==============================
# Bossbar 初期化
# ==============================
def init_bossbar():
    m.execute(f"bossbar add {BOSSBAR_ID} Direction")
    m.execute(f"bossbar set {BOSSBAR_ID} max 1")
    m.execute(f"bossbar set {BOSSBAR_ID} value 1")
    m.execute(f"bossbar set {BOSSBAR_ID} color white")
    m.execute(f"bossbar set {BOSSBAR_ID} players {PLAYER}")

# ==============================
# 方位データ
# ==============================
degree_marks = [
    0,15,30,45,60,75,90,105,120,135,150,165,
    180,195,210,225,240,255,270,285,300,315,330,345
]

direction_labels = {
    0:"S",
    90:"W",
    180:"N",
    270:"E"
}

# ==============================
# 方位バー生成
# ==============================
def build_bossbar_line(yaw):
    yaw = (yaw + 360) % 360

    idx = min(range(len(degree_marks)), key=lambda i: abs(degree_marks[i] - yaw))
    total = len(degree_marks)

    parts = []

    for offset in range(-2, 3):
        i = (idx + offset) % total
        deg = degree_marks[i]

        label = direction_labels.get(deg, str(deg))

        if i == idx:
            parts.append(f"▶ {label} ◀")
        else:
            parts.append(f" {label} ")

    return "|".join(parts)

# ==============================
# Bossbar 更新ループ
# ==============================
def update_bossbar_loop():

    last = None

    while True:
        yaw, _ = m.player_orientation()
        line = build_bossbar_line(yaw)

        if line != last:
            m.execute(
                f"bossbar set {BOSSBAR_ID} name "
                f"{json.dumps({'text': line, 'color': 'white'})}"
            )
            last = line

        time.sleep(0.1)

# ==============================
# Main
# ==============================
def main():

    m.echo("🧭 Direction Bar Started")

    init_bossbar()

    threading.Thread(
        target=update_bossbar_loop,
        daemon=True
    ).start()

    while True:
        time.sleep(1)

main()
