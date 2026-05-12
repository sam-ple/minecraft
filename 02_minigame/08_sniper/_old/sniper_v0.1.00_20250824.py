import minescript as m
from minescript import EventQueue, EventType
import time, math, json, threading

PLAYER = m.player_name()
BOSSBAR_ID = "minecraft:direction_bar"

# --- Bossbar initialization ---
m.execute("gamerule sendCommandFeedback false")
m.execute("title @a clear")
m.execute(f"bossbar add {BOSSBAR_ID} Direction")
m.execute(f"bossbar set {BOSSBAR_ID} max 1")
m.execute(f"bossbar set {BOSSBAR_ID} value 1")
m.execute(f"bossbar set {BOSSBAR_ID} color white")
m.execute(f"bossbar set {BOSSBAR_ID} players {PLAYER}")

# --- Direction handling ---
degree_marks = [0,15,30,45,60,75,90,105,120,135,150,165,
                180,195,210,225,240,255,270,285,300,315,330,345]
direction_labels = {0:"S",90:"W",180:"N",270:"E"}

def build_bossbar_line(yaw):
    yaw = (yaw + 360) % 360
    idx = min(range(len(degree_marks)), key=lambda i: abs(degree_marks[i] - yaw))
    total = len(degree_marks)
    indices = [(idx + i) % total for i in range(-2, 3)]
    parts = []
    for i in indices:
        deg = degree_marks[i]
        label = direction_labels.get(deg, str(deg))
        if i == idx:
            parts.append(f"▶ {label} ◀")
        else:
            parts.append(f" {label} ")
    return "|".join(parts)

def update_bossbar_loop():
    last_line = None
    while True:
        yaw, pitch = m.player_orientation()
        line = build_bossbar_line(yaw)
        if line != last_line:  # Update only if changed
            name_json = json.dumps({"text": line, "color": "white"})
            m.execute(f"bossbar set {BOSSBAR_ID} name {name_json}")
            last_line = line
        time.sleep(0.1)

# --- Weapon handling ---
def spyglass_in_mainhand():
    hands = m.player_hand_items()
    if not hands or not hands.main_hand:
        return False
    if isinstance(hands.main_hand, dict):
        item = hands.main_hand.get("item", None)
    else:
        item = str(hands.main_hand)
    return item == "minecraft:spyglass"

def eye_pos():
    x, y, z = m.player_position()
    yaw, pitch = m.player_orientation()
    y += 1.62
    return x, y, z, yaw, pitch

def fire():
    ex, ey, ez, yaw, pitch = eye_pos()
    target = m.player_get_targeted_entity(20)
    if target:
        tx, ty, tz = target.position
        # Hit particles
        m.execute(f"particle minecraft:crit {tx} {ty+1} {tz} 0 0 0 0 20 force")
        # Hit sound
        m.execute(f"playsound minecraft:entity.arrow.hit_player master @a {tx} {ty} {tz} 1 1")
        # Apply damage
        m.execute(f"damage {target.uuid} 20 minecraft:generic")
        m.echo(f"💥 Hit {target.type} for 20 damage!")
    else:
        # Miss effect
        m.execute(f"particle minecraft:poof {ex} {ey} {ez} 0 0 0 0 10 force")
        m.execute(f"playsound minecraft:entity.blaze.shoot master @a {ex} {ey} {ez} 0.5 1")
        m.echo("💨 Missed...")

# --- Main loop ---
def main():
    m.echo("🎯 Sniper (Spyglass): Left click to shoot / Direction shown in bossbar")

    # Run bossbar update loop in a separate thread
    threading.Thread(target=update_bossbar_loop, daemon=True).start()

    with EventQueue() as eq:
        eq.register_mouse_listener()
        last_shot = 0.0
        while True:
            e = eq.get()
            if e.type == EventType.MOUSE and e.button == 0 and e.action == 1:
                if not spyglass_in_mainhand():
                    continue
                now = time.time()
                if now - last_shot < 0.5:
                    continue
                last_shot = now
                fire()

main()
