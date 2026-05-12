import minescript as m
from minescript import EventQueue, EventType
import time, math, json, threading, random

PLAYER = m.player_name()
BOSSBAR_ID = "minecraft:direction_bar"

# --- Constants ---
MAX_AMMO = 8
ammo = MAX_AMMO
FIRE_INTERVAL = 0.5  # Fire interval in seconds

# --- Bossbar initialization ---
m.execute("gamerule sendCommandFeedback false")
m.execute("title @a clear")
m.execute(f"bossbar add {BOSSBAR_ID} Direction")
m.execute(f"bossbar set {BOSSBAR_ID} max 1")
m.execute(f"bossbar set {BOSSBAR_ID} value 1")
m.execute(f"bossbar set {BOSSBAR_ID} color white")
m.execute(f"bossbar set {BOSSBAR_ID} players {PLAYER}")

# --- Direction handling ---
degree_marks = [i for i in range(0, 360, 15)]
direction_labels = {0: "S", 90: "W", 180: "N", 270: "E"}

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
        if line != last_line:
            name_json = json.dumps({"text": line, "color": "white"})
            m.execute(f"bossbar set {BOSSBAR_ID} name {name_json}")
            last_line = line
        time.sleep(0.1)

# --- Ammo handling ---
def update_ammo_display():
    filled = "■" * ammo
    empty = "□" * (MAX_AMMO - ammo)
    m.execute(f'title {PLAYER} actionbar {json.dumps({"text": filled+empty, "color":"gold"})}')

def ammo_display_loop():
    while True:
        update_ammo_display()
        time.sleep(0.2)

def reload_ammo():
    global ammo
    ammo = MAX_AMMO
    m.execute(f"clear {PLAYER} minecraft:iron_ingot 1")
    m.echo("🔄 Reloaded!")
    update_ammo_display()

# --- Weapon check ---
def spyglass_in_mainhand():
    hands = m.player_hand_items()
    if not hands or not hands.main_hand:
        return False
    item = hands.main_hand.get("item") if isinstance(hands.main_hand, dict) else str(hands.main_hand)
    return item == "minecraft:spyglass"

def iron_ingot_in_mainhand():
    hands = m.player_hand_items()
    if not hands or not hands.main_hand:
        return False
    item = hands.main_hand.get("item") if isinstance(hands.main_hand, dict) else str(hands.main_hand)
    return item == "minecraft:iron_ingot"

# --- Player eye position ---
def eye_pos():
    x, y, z = m.player_position()
    yaw, pitch = m.player_orientation()
    y += 1.62
    return x, y, z, yaw, pitch

# --- Fire arrow with custom tag ---
def fire():
    global ammo
    if ammo <= 0:
        m.echo("❌ No ammo! Reload with iron ingot + Left Shift.")
        return
    ammo -= 1
    update_ammo_display()

    ex, ey, ez, yaw, pitch = eye_pos()
    rad_yaw = math.radians(yaw)
    rad_pitch = math.radians(pitch)

    dx = -math.sin(rad_yaw) * math.cos(rad_pitch) + random.uniform(-0.02, 0.02)
    dy = -math.sin(rad_pitch) + random.uniform(-0.02, 0.02)
    dz = math.cos(rad_yaw) * math.cos(rad_pitch) + random.uniform(-0.02, 0.02)

    # Summon arrow with tag "sniper_arrow"
    m.execute(f'summon minecraft:arrow {ex} {ey} {ez} {{Motion:[{dx:.3f},{dy:.3f},{dz:.3f}],Tags:["sniper_arrow"]}}')
    m.execute(f"playsound minecraft:entity.arrow.shoot master {PLAYER}")

# --- Distance calculation ---
def distance(pos1, pos2):
    return math.sqrt(sum((a-b)**2 for a,b in zip(pos1,pos2)))

# --- Arrow collision monitoring ---
def arrow_monitor_loop():
    checked_arrows = set()
    while True:
        arrows = m.entities(type="minecraft:arrow")
        for arrow in arrows:
            if "sniper_arrow" not in getattr(arrow, "tags", []):
                continue
            if arrow.uuid in checked_arrows:
                continue
            # Check if arrow hit something (on ground or touching entity)
            if getattr(arrow, "on_ground", False) or getattr(arrow, "passengers", []):
                # Hit effect
                ax, ay, az = arrow.position
                m.execute(f"particle minecraft:crit {ax} {ay} {az} 0 0 0 0 20 force")
                m.execute(f"playsound minecraft:entity.arrow.hit_player master @a {ax} {ay} {az} 1 1")
                # Distance to player
                px, py, pz = m.player_position()
                dist = distance((ax, ay, az), (px, py, pz))
                m.echo(f"💥 Hit detected at {dist:.1f}m")
                # Mark as processed
                checked_arrows.add(arrow.uuid)
                # Remove arrow to prevent multiple triggers
                m.execute(f"kill @e[type=arrow,limit=1,sort=nearest,nbt={{UUID:[I;{arrow.uuid[0]},{arrow.uuid[1]},{arrow.uuid[2]},{arrow.uuid[3]}]}}]")
        time.sleep(0.05)

# --- Main ---
def main():
    global ammo
    m.echo("🎯 Arrow Sniper (Spyglass): Left click to shoot / Direction shown in bossbar")
    m.echo("🔫 Ammo starts with 8 | Reload: hold iron ingot + Left Shift")
    m.echo("✨ Only your arrows count | Hit particles shown on target!")

    threading.Thread(target=update_bossbar_loop, daemon=True).start()
    threading.Thread(target=ammo_display_loop, daemon=True).start()
    threading.Thread(target=arrow_monitor_loop, daemon=True).start()

    with EventQueue() as eq:
        eq.register_mouse_listener()
        eq.register_key_listener()
        last_shot = 0.0

        while True:
            e = eq.get()
            now = time.time()

            # Left click to fire
            if e.type == EventType.MOUSE and e.button == 0 and e.action == 1:
                if not spyglass_in_mainhand():
                    continue
                if now - last_shot < FIRE_INTERVAL:
                    continue
                last_shot = now
                fire()

            # Reload when releasing Left Shift (key 340) while holding iron ingot
            if e.type == EventType.KEY and e.action == 0 and e.key == 340:
                if iron_ingot_in_mainhand():
                    reload_ammo()

main()
