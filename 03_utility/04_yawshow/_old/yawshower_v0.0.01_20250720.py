import minescript as m
import time

player = m.player_name()
bossbar_id = "minecraft:direction_bar"

# Setup bossbar
m.execute("title @a clear")
m.execute(f"bossbar add {bossbar_id} Direction")
m.execute(f"bossbar set {bossbar_id} max 360")
m.execute(f"bossbar set {bossbar_id} color blue")
m.execute(f"bossbar set {bossbar_id} players {player}")

# Convert yaw angle to cardinal direction
def get_facing_label(yaw):
    yaw = (yaw + 360) % 360  # Normalize to 0–359
    if 45 <= yaw < 135:
        return "West"
    elif 135 <= yaw < 225:
        return "North"
    elif 225 <= yaw < 315:
        return "East"
    else:
        return "South"

last_yaw = None
last_direction = None

while True:
    yaw, _ = m.player_orientation()
    yaw = (yaw + 360) % 360  # Normalize

    direction = get_facing_label(yaw)

    # Update only if changed
    if int(yaw) != last_yaw or direction != last_direction:
        m.execute(f"bossbar set {bossbar_id} value {int(yaw)}")
        m.execute(f'bossbar set {bossbar_id} name {{"text":"{direction} ({int(yaw)}°)","color":"white"}}')
        last_yaw = int(yaw)
        last_direction = direction

    time.sleep(0.5)
